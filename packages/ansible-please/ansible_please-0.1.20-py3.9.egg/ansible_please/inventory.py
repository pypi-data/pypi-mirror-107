from __future__ import annotations

import typing
from omegaconf import OmegaConf
import socket
from ansible_please.utils import save_yaml_to_file
import tempfile
from loguru import logger
from ansible_please.ansible_dict import AnsibleDict


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


class Inventory:
    BASE_INVENTORY = """
    all:
      children:
      vars:
        stdout_callback: debug
        display_args_to_stdout: True
        host_key_checking: False
        look_for_keys: True
    """
    input_to_ansible_conversion = {"python_path": "ansible_python_interpreter"}
    required_attributes = set(["python_path"])
    required_keys = ["master_host", "worker_hosts"]

    def __init__(self, inventory_dict):
        self._local_ip = self._get_local_ip()
        self.inventory_dict: AnsibleDict = AnsibleDict(
            self.process_dict(inventory_dict)
        )

    @classmethod
    def from_yaml(cls, yaml_path):
        d = dict(OmegaConf.load(yaml_path))
        return cls(d)

    def _get_local_ip(self) -> str:
        return get_ip()

    def process_dict(self, inventory_dict):
        base_dict = OmegaConf.create(Inventory.BASE_INVENTORY)
        host_info = inventory_dict.setdefault("host_info", {})
        base_dict["all"]["children"] = {}
        self.process_host_info(inventory_dict)
        hosts = inventory_dict["hosts"]
        for host_section in hosts:
            base_dict["all"]["children"][host_section] = {}
            base_dict["all"]["children"][host_section]["hosts"] = {}
            for host in hosts[host_section]:
                base_dict["all"]["children"][host_section]["hosts"][host] = host_info[
                    host
                ]
        return base_dict

    def process_host_info(self, inventory_dict):
        hosts = inventory_dict["hosts"]
        host_info = inventory_dict.get("host_info", {})
        for host_section in hosts:
            for i, host in enumerate(hosts[host_section]):
                processed_hostname = host
                ansible_connection = "paramiko"

                if host == "localhost":
                    processed_hostname = "127.0.0.1"

                if processed_hostname == "127.0.0.1":
                    processed_hostname = self._local_ip

                if processed_hostname == self._local_ip:
                    ansible_connection = "local"

                if host in host_info:
                    self.convert_input_attributes(host_info.get(host, {}))
                    attributes = host_info.pop(host, {})
                elif processed_hostname in host_info:
                    self.convert_input_attributes(host_info[processed_hostname])
                    attributes = host_info.pop(processed_hostname, {})
                else:
                    host_info[processed_hostname] = {}
                    attributes = host_info.pop(processed_hostname)
                attributes["ansible_connection"] = ansible_connection
                attributes["host_checking"] = False
                attributes.setdefault("ansible_python_interpreter", "/usr/bin/python3")
                host_info[processed_hostname] = attributes
                hosts[host_section][i] = processed_hostname

    def convert_input_attributes(self, attributes: typing.Dict[str, str]) -> None:
        keys = list(attributes.keys())
        for key in keys:
            if key in self.input_to_ansible_conversion:
                value = attributes.pop(key)
                new_key = self.input_to_ansible_conversion[key]
                attributes[new_key] = value

    def save_to_file(self, delete=True) -> tempfile.NamedTemporaryFile:
        """Save yaml string into tempfile

        Returns:
            str: filename
        """
        return save_yaml_to_file(self.__str__(), delete=delete)

    def __str__(self) -> str:
        return self.inventory_dict.pretty(use_list=False)
