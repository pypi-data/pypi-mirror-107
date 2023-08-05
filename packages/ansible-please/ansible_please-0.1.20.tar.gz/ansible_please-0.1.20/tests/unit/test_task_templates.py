import unittest

from ansible_please.task_templates import DockerContainer, Pip
from ansible_please.ansible_dict import AnsibleDict
from omegaconf import OmegaConf
import pytest

EXPECTED_DOCKER_DOWN_DICT = AnsibleDict(
    dict(
        OmegaConf.create(
            """
- name: '[down] test-container'
  docker_container:
    name: test_container
    state: absent
    user: nobody
    keep_volumes: false
    detach: true
    tty: false
    interactive: false
    network_mode: host
    container_default_behavior: compatibility
  tags:
  - down
"""
        )[0]
    )
)


EXPECTED_PIP_DICT = AnsibleDict(
    dict(
        OmegaConf.create(
            """
- name: '[up] Install package via pip'
  command:
    cmd: "{{ ansible_python_interpreter }} -m pip install test-package"
  tags:
  - up
"""
        )[0]
    )
)


class TestDockerContainer(unittest.TestCase):
    def test_down_docker_container(self):
        d = DockerContainer(
            task_description="test-container",
            name="test_container",
            image="test-image",
            ports=[],
        ).down()
        assert d.asdict()

    def test_invalid_ports(self):
        with pytest.raises(ValueError):
            _ = DockerContainer(
                task_description="test-container",
                name="test_container",
                image="test-image",
                ports=[2, 5],
            )


class TestPip(unittest.TestCase):
    def test_pip_creation(self):
        p = Pip(packages=["test-package"])
        assert p.asdict()
