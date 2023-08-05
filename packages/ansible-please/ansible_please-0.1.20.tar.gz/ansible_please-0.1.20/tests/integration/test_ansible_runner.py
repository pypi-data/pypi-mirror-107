import unittest
from omegaconf import OmegaConf
import docker
import pytest

from ansible_please.ansible_runner import AnsibleRunner
from ansible_please.inventory import Inventory
from ansible_please.playbook import Playbook
from ansible_please.task_templates.docker_container import DockerContainer
from ansible_please.task_templates.pip import Pip


client = docker.DockerClient()

TEST_INPUT_DICT = dict(
    OmegaConf.create(
        """
hosts:
    master_host:
      - 'localhost'
    worker_hosts:
      - '127.0.0.1'
host_info:
  '127.0.0.1':
    'python_path': /usr/bin/python3
"""
    )
)


class TestAnsibleRunner(unittest.TestCase):
    def test_missing_inventory_creation(self):
        pip_task = Pip(packages=["docker"])
        playbook = Playbook(
            name="test-invalid-playbook", hosts="master_host", tasks=[pip_task.up()],
        )
        with pytest.raises(ValueError):
            _ = AnsibleRunner(inventory=None, playbooks=[playbook])

    def test_read_from_yaml(self):
        pip_task = Pip(packages=["docker"])
        playbook = Playbook(
            name="test-invalid-playbook", hosts="master_host", tasks=[pip_task.up()],
        )
        _ = AnsibleRunner(
            input_path="tests/integration/test_input.yml", playbooks=[playbook]
        )
        assert True

    def test_run(self):
        inventory = Inventory(TEST_INPUT_DICT)
        pip_task = Pip(packages=["docker"])
        docker_container_task = DockerContainer(
            task_description="start-test-redis",
            name="test-redis",
            image="redis:latest",
        )
        playbook = Playbook(
            name="test-redis-playbook",
            hosts="master_host",
            tasks=[
                pip_task.up(),
                docker_container_task.up(),
                docker_container_task.down(),
            ],
        )
        runner = AnsibleRunner(inventory=inventory, playbooks=[playbook])

        runner.up()
        has_container = False
        for container in client.containers.list():
            if container.name == "test-redis":
                has_container = True
        assert has_container

        # tear down
        runner.down()
        has_container = False
        for container in client.containers.list():
            if container.name == "test-redis":
                has_container = True
        assert not has_container
