import unittest
from unittest.mock import patch
from omegaconf import OmegaConf

from ansible_please.inventory import Inventory, get_ip  # noqa

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
    'python_path': /test_path/python3
"""
    )
)

EXPECTED_INVENTORY_DICT = {
    "all": {
        "children": {
            "master_host": {
                "hosts": {
                    "127.0.0.1": {
                        "ansible_connection": "local",
                        "host_checking": False,
                        "ansible_python_interpreter": "/test_path/python3",
                    }
                }
            },
            "worker_hosts": {
                "hosts": {
                    "127.0.0.1": {
                        "ansible_connection": "local",
                        "host_checking": False,
                        "ansible_python_interpreter": "/test_path/python3",
                    }
                }
            },
        },
        "vars": {
            "stdout_callback": "debug",
            "display_args_to_stdout": True,
            "host_key_checking": False,
            "look_for_keys": True,
        },
    }
}


class TestInventory(unittest.TestCase):
    @patch("ansible_please.inventory.get_ip", return_value="127.0.0.1")
    def test_inventory_creation(self, mock_get_ip):
        i = Inventory(TEST_INPUT_DICT)
        assert i.inventory_dict.data == EXPECTED_INVENTORY_DICT
        assert i.__str__()

    def test_get_ip(self):
        _ = get_ip()  # don't fail
        assert True

    @patch(
        "ansible_please.inventory.get_sockname", side_effect=Exception("mocked error")
    )
    def test_failed_ip(self, mock_get_sockname):
        IP = get_ip()
        assert IP == "127.0.0.1"
