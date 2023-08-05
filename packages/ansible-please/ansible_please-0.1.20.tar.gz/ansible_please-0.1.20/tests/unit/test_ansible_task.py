import unittest
from ansible_please.ansible_task import AnsibleTask
from ansible_please.ansible_dict import AnsibleDict
import copy
import pytest

EXPECTED_UP_DICT = AnsibleDict(
    {
        "name": "[up] test description",
        "test_task_name": {"test": 2},
        "tags": ["test-tag", "up"],
    }
)

test_ansible_task = AnsibleTask(
    input_dict={"test": 2},
    task_name="test_task_name",
    task_description="test description",
    tags=["test-tag"],
)


class TestAnsibleTask(unittest.TestCase):
    def test_invalid_name(self):
        with pytest.raises(ValueError):
            _ = AnsibleTask(task_name="")

    def test__str__(self):
        assert test_ansible_task.__str__() == EXPECTED_UP_DICT.__str__()

    def test_asdict(self):
        actual = test_ansible_task.asdict()
        assert actual == EXPECTED_UP_DICT

    def test_up(self):
        actual = test_ansible_task.up().asdict()
        assert actual == EXPECTED_UP_DICT

    def test_down(self):
        actual = test_ansible_task.down().asdict()
        expected = copy.deepcopy(EXPECTED_UP_DICT.data)
        expected["name"] = "[down] test description"
        expected["tags"] = ["test-tag", "down"]
        assert actual == AnsibleDict(expected)
