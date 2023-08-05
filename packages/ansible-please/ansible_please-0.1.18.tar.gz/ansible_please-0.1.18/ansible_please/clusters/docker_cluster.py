from ansible_please.ansible_runner import AnsibleRunner
from ansible_please.playbook import Playbook
from ansible_please.task_templates import Pip, DockerContainer

import redis
import attr
import docker
from docker.models.containers import Container
from urllib.error import HTTPError
from loguru import logger
import socket
import typing
import cloudpickle


def get_sockname(s: socket.socket):
    s.connect(("10.255.255.255", 1))
    return s.getsockname()[0]


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        IP = get_sockname(s)
    except Exception as e:
        logger.exception("Caught exception while trying to get ip: {}".format(e))
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


@attr.s(repr=False)
class DockerCluster:
    """
        Manages the ansible docker cluster
    """

    ansible_runner: AnsibleRunner = attr.ib(default=None)
    force_teardown: True = attr.ib(default=True)

    _cluster_info_redis_runner: AnsibleRunner = attr.ib(init=False)
    _ip: str = attr.ib(init=False, default=get_ip())
    _redis_client: redis.Redis = attr.ib(init=False, default=None)

    def __attrs_post_init__(self):
        self._redis_client = redis.Redis(host=self._ip, port="6380")
        self._set_ansible_runner_from_cluster()

    @property
    def _playbook_cluster_info(self):
        pip_task = Pip(packages=["docker"])
        cluster_info_task = DockerContainer(
            task_description="start-cluster-info",
            name="ansible_please-cluster-info",
            image="redis:latest",
            command=" --port 6380",
            env={"REDIS_PORT": "6380"},
        )
        return Playbook(
            name="set up ansible_please-cluster-info",
            hosts=self._ip,
            tasks=[pip_task.up(), cluster_info_task.up(), cluster_info_task.down()],
        )

    def _set_ansible_runner_from_cluster(self):
        _ansible_runner = self._get_ansible_runner_from_cluster()
        if self.ansible_runner is not None:
            if _ansible_runner is not None:
                if self.force_teardown:
                    logger.info("Tearing down existing cluster...")
                    _ansible_runner.down(verbosity=0)
                    _cluster_info_redis_runner = AnsibleRunner(
                        playbooks=[self._playbook_cluster_info],
                        inventory=_ansible_runner.inventory,
                    )
                    _cluster_info_redis_runner.down(verbosity=0)
                    logger.info("Existing cluster torn down!")
                else:
                    logger.warn(
                        "Existing ansible_please cluster detected but force_teardown is set as False, this could lead to issues with untracked containers"
                    )
        else:
            self.ansible_runner = _ansible_runner
        if self.ansible_runner is None:
            raise ValueError("AnsibleRunner must not be None!")
        self._cluster_info_redis_runner = AnsibleRunner(
            playbooks=[self._playbook_cluster_info],
            inventory=self.ansible_runner.inventory,
        )

    def _get_ansible_runner_from_redis(self) -> AnsibleRunner:
        return cloudpickle.loads(self._redis_client.get("ansible_please_runner"))

    def _get_ansible_runner_from_cluster(self) -> AnsibleRunner:
        try:
            client: docker.DockerClient = docker.DockerClient()
            container: Container = client.containers.get("ansible_please-cluster-info")
            if container.attrs["State"]["Running"]:
                logger.info(
                    "Found existing cluster with container id {}".format(
                        container.attrs["Id"]
                    )
                )
                return self._get_ansible_runner_from_redis()
            return None
        except HTTPError as e:
            # Need to check its an 403 meaning that the container doesn't exist
            status_code = e.response.status_code
            if status_code == 404:
                return None
        except Exception as e:
            logger.debug(
                "Caught exception when attempting to get current state: {}. This may be expected".format(
                    e
                )
            )
            return None

    def run(
        self, tags: typing.List[str] = ["up"], delete_files=True, verbosity=1
    ) -> None:
        self.ansible_runner.run(
            tags=tags, delete_files=delete_files, verbosity=verbosity
        )

    def up(self, delete_files=True, verbosity=1):
        self._setup_cluster_info()
        self.run(tags=["up"], delete_files=delete_files, verbosity=verbosity)

    def down(self, delete_files=True, verbosity=1):
        self._cluster_info_redis_runner.run(
            tags=["down"], delete_files=True, verbosity=0
        )
        self.run(tags=["down"], delete_files=delete_files, verbosity=verbosity)

    def _setup_cluster_info(self):
        self._cluster_info_redis_runner.run(tags=["up"], delete_files=True, verbosity=0)
        self._redis_client.set(
            "ansible_please_runner", cloudpickle.dumps(self.ansible_runner)
        )
