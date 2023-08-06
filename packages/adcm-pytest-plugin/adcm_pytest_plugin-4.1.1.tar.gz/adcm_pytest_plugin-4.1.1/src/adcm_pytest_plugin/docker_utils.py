# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# pylint: disable=redefined-outer-name, C0103, E0401
import io
import os
import re
import random
import socket
from contextlib import contextmanager
from gzip import compress

import allure
import docker
import tarfile

from docker.errors import APIError, ImageNotFound
from docker import DockerClient
from adcm_client.util.wait import wait_for_url
from adcm_client.objects import ADCMClient
from adcm_client.wrappers.api import ADCMApiWrapper
from deprecated import deprecated
from coreapi.exceptions import ErrorMessage
from retry.api import retry_call

from .utils import random_string

MIN_DOCKER_PORT = 8000
MAX_DOCKER_PORT = 9000
DEFAULT_IP = "127.0.0.1"
CONTAINER_START_RETRY_COUNT = 20


class UnableToBind(Exception):
    pass


class RetryCountExceeded(Exception):
    pass


def _port_is_free(ip, port) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((ip, port)) != 0


def _find_random_port(ip) -> int:
    for _ in range(0, 20):
        port = random.randint(MIN_DOCKER_PORT, MAX_DOCKER_PORT)
        if _port_is_free(ip, port):
            return port
    raise UnableToBind("There is no free port for Docker after 20 tries.")


def is_docker() -> bool:
    """
    Look into cgroup to detect if we are in container
    """
    path = "/proc/self/cgroup"
    try:
        with open(path) as f:
            for line in f:
                if re.match(r"\d+:[\w=]+:/docker(-[ce]e)?/\w+", line):
                    return True
    except FileNotFoundError:
        pass
    return False


@contextmanager
def gather_adcm_data_from_container(adcm: "ADCM"):
    """
    Get /adcm/data/ form ADCM docker container
    :return: compressed file stream
    """
    bits, _ = adcm.container.get_archive("/adcm/data/")

    with io.BytesIO() as stream:
        for chunk in bits:
            stream.write(chunk)
        stream.seek(0)
        yield compress(stream.getvalue())


def get_file_from_container(instance, path, filename):
    """
    Get file from docker container and return file object

    Args:
        instance: ADCM instance
        path (str): path to file in container
        filename (str): filename in path

    Returns:
        (file object): The extracted file from tar archive from docker container

    """

    stream = instance.container.get_archive(path + filename)[0]
    file_obj = io.BytesIO()
    for i in stream:
        file_obj.write(i)
    file_obj.seek(0)
    with tarfile.open(mode="r", fileobj=file_obj) as tar:
        return tar.extractfile(filename)


@deprecated
def get_initialized_adcm_image(
    repo="local/adcminit",
    tag=None,
    adcm_repo=None,
    adcm_tag=None,
    pull=True,
    dc=None,
) -> dict:
    """
    Wrapper for backward capability
    """
    return ADCMInitializer(
        repo=repo,
        tag=tag,
        adcm_repo=adcm_repo,
        adcm_tag=adcm_tag,
        pull=pull,
        dc=dc,
    ).get_initialized_adcm_image()


# pylint: disable=too-many-instance-attributes
class ADCMInitializer:
    """
    Class for initialized ADCM image preparation.
    """

    __slots__ = (
        "repo",
        "tag",
        "adcm_repo",
        "adcm_tag",
        "pull",
        "dc",
        "preupload_bundle_urls",
        "adcm_api_credentials",
        "_adcm",
        "_adcm_cli",
    )

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        repo="local/adcminit",
        tag=None,
        adcm_repo=None,
        adcm_tag=None,
        pull=True,
        dc=None,
        preupload_bundle_urls=None,
        adcm_api_credentials=None,
    ):
        self.repo = repo
        self.tag = tag if tag else random_string()
        self.adcm_repo = adcm_repo
        self.adcm_tag = adcm_tag
        self.pull = pull
        self.dc = dc if dc else docker.from_env(timeout=120)
        self.preupload_bundle_urls = preupload_bundle_urls
        self.adcm_api_credentials = adcm_api_credentials if adcm_api_credentials else {}
        self._adcm = None
        self._adcm_cli = None

    @allure.step("Prepare initialized ADCM image")
    def get_initialized_adcm_image(self) -> dict:
        """
        If image with given 'repo' and 'tag' then it was most likely created with staticimage run,
        so we just use it.
        If there is no image with given 'repo' and 'tag' we will create a new one
        """

        if image_exists(self.repo, self.tag, self.dc):
            return {"repo": self.repo, "tag": self.tag}
        else:
            return self.init_adcm()

    def init_adcm(self):
        dw = DockerWrapper(dc=self.dc)
        # Check if we use remote dockerd
        if self.dc and "localhost" not in self.dc.api.base_url:
            # dc.api.base_url is most likely tcp://{cmd_opts.remote_docker}
            base_url = self.dc.api.base_url
            ip_start = base_url.rfind("/") + 1
            ip_end = base_url.rfind(":")
            ip = base_url[ip_start:ip_end]
        else:
            # then dc.api.base_url is most likely http+docker://localhost
            ip = None
        self._adcm = dw.run_adcm(image=self.adcm_repo, tag=self.adcm_tag, remove=False, pull=self.pull, ip=ip)
        # Pre-upload bundles to ADCM before image initialization
        self._preupload_bundles()
        # Create a snapshot from initialized container
        self._adcm.container.stop()
        with allure.step(f"Commit initialized ADCM container to image {self.repo}:{self.tag}"):
            self._adcm.container.commit(repository=self.repo, tag=self.tag)
        self._adcm.container.remove()
        return {"repo": self.repo, "tag": self.tag}

    def _preupload_bundles(self):
        if self.preupload_bundle_urls:
            with allure.step("Pre-upload bundles into ADCM before image initialization"):
                self._adcm_cli = ADCMClient(url=self._adcm.url, **self.adcm_api_credentials)
                for url in self.preupload_bundle_urls:
                    retry_call(
                        self._upload_bundle,
                        fargs=[url],
                        tries=5,
                    )

    def _upload_bundle(self, url):
        try:
            self._adcm_cli.upload_from_url(url)
        except ErrorMessage as exception:
            # skip error only if bundle was already uploaded before
            # can occur in case of --staticimage use
            if "BUNDLE_ERROR" not in exception.error:
                raise exception


def image_exists(repo, tag, dc=None):
    if dc is None:
        dc = docker.from_env(timeout=120)
    try:
        dc.images.get(name="{}:{}".format(repo, tag))
    except ImageNotFound:
        return False
    return True


def split_tag(image_name: str):
    """
    Split docker image name

    >>> split_tag('fedora/httpd')
    ('fedora/httpd', None)
    >>> split_tag('fedora/httpd:')
    ('fedora/httpd', '')
    >>> split_tag('fedora/httpd:version1.0')
    ('fedora/httpd', 'version1.0')
    """
    image = image_name.split(":")
    if len(image) > 1:
        image_repo = image[0]
        image_tag = image[1]
    else:
        image_repo = image[0]
        image_tag = None
    return image_repo, image_tag


def _wait_for_adcm_container_init(container, container_ip, port, timeout=120):
    if not wait_for_url(f"http://{container_ip}:{port}/api/v1/", timeout):
        additional_message = ""
        try:
            container.kill()
        except APIError:
            additional_message = " \nWARNING: Failed to kill docker container. Try to remove it by hand"
        raise TimeoutError(f"ADCM API has not responded in {timeout} seconds{additional_message}")


class ADCM:
    """
    Class that wraps ADCM Api operation over self.api (ADCMApiWrapper)
    and wraps docker over self.container (see docker module for info)
    """

    __slots__ = ("container", "ip", "port", "url", "api")

    def __init__(self, container, ip, port):
        self.container = container
        self.ip = ip
        self.port = port
        self.url = "http://{}:{}".format(self.ip, self.port)
        self.api = ADCMApiWrapper(self.url)

    def stop(self):
        """Stops container"""
        self.container.stop()


class DockerWrapper:
    """Class for connection to local docker daemon and spawn ADCM instances."""

    __slots__ = ("client",)

    def __init__(self, base_url="unix://var/run/docker.sock", dc=None):
        self.client = dc if dc else docker.DockerClient(base_url=base_url, timeout=120)

    # pylint: disable=R0913
    def run_adcm(
        self,
        image=None,
        labels=None,
        remove=True,
        pull=True,
        name=None,
        tag=None,
        ip=None,
        volumes=None,
    ):
        """
        Run ADCM in docker image.
        Return ADCM instance.

        Example:
        adcm = docker.run(image='arenadata/adcm', tag=None, ip='127.0.0.1')

        If tag is None or is not present than a tag 'latest' will be used
        """
        if not image:
            image = "hub.arenadata.io/adcm/adcm"
        if not tag:
            tag = "latest"
        if pull:
            self.client.images.pull(image, tag)
        if os.environ.get("BUILD_TAG"):
            if not labels:
                labels = {}
            labels.update({"jenkins-job": os.environ["BUILD_TAG"]})
        if not ip:
            ip = DEFAULT_IP

        container, port = self.adcm_container(
            image=image,
            labels=labels,
            remove=remove,
            name=name,
            tag=tag,
            ip=ip,
            volumes=volumes,
        )

        # If test runner is running in docker then 127.0.0.1
        # will be local container loop interface instead of host loop interface,
        # so we need to establish ADCM API connection using internal docker network
        if ip == DEFAULT_IP and is_docker():
            container_ip = self.client.api.inspect_container(container.id)["NetworkSettings"]["IPAddress"]
            port = "8000"
        else:
            container_ip = ip
        _wait_for_adcm_container_init(container, container_ip, port)
        return ADCM(container, container_ip, port)

    # pylint: disable=R0913
    @allure.step("Run ADCM container from the image {image}:{tag}")
    def adcm_container(
        self,
        image=None,
        labels=None,
        remove=True,
        name=None,
        tag=None,
        ip=None,
        volumes=None,
    ):
        """
        Run ADCM in docker image.
        Return ADCM container and bind port.
        """
        for _ in range(0, CONTAINER_START_RETRY_COUNT):
            port = _find_random_port(ip)
            try:
                container = self.client.containers.run(
                    "{}:{}".format(image, tag),
                    ports={"8000": (ip, port)},
                    volumes=volumes,
                    remove=remove,
                    detach=True,
                    labels=labels,
                    name=name,
                )
                break
            except APIError as err:
                if (
                    "failed: port is already allocated" in err.explanation
                    or "bind: address already in use" in err.explanation  # noqa: W503
                ):
                    # such error excepting leaves created container and there is
                    # no way to clean it other than from docker library
                    pass
                else:
                    raise err
        else:
            raise RetryCountExceeded(f"Unable to start container after {CONTAINER_START_RETRY_COUNT} retries")
        with allure.step(f"ADCM API started on {ip}:{port}/api/v1"):
            return container, port


def remove_docker_image(repo: str, tag: str, dc: DockerClient):
    """Remove docker image"""
    image_name = f"{repo}:{tag}"
    for container in dc.containers.list(filters=dict(ancestor=image_name)):
        try:
            container.wait(condition="removed", timeout=30)
        except ConnectionError:
            # https://github.com/docker/docker-py/issues/1966 workaround
            pass
    retry_call(
        dc.images.remove,
        fargs=[image_name],
        fkwargs={"force": True},
        tries=5,
    )
