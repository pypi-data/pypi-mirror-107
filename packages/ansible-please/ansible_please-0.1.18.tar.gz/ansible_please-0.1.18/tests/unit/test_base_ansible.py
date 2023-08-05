import unittest
from ansible_please.base_ansible import BaseAnsible
from ansible_please.ansible_dict import AnsibleDict
from unittest.mock import patch


class TestBaseAnsibleClass(BaseAnsible):
    def __init__(self, input_dict={"test_dict": {"z": "testz"}}):
        super(TestBaseAnsibleClass, self).__init__(input_dict)
        self.x = "testx"
        self.y = "testy"
        self.zlist = [1, 2]
        self.base_ansible = BaseAnsible(input_dict={"test_input": "test"})
        self.ansible_dict = AnsibleDict(data={"test_data": "test"})


EXPECTED_DICT: AnsibleDict = AnsibleDict(
    {
        "x": "testx",
        "y": "testy",
        "zlist": [1, 2],
        "base_ansible": {"test_input": "test"},
        "ansible_dict": {"test_data": "test"},
        "test_dict": {"z": "testz"},
    }
)


class TestBaseAnsible(unittest.TestCase):
    def test_as_dict(self):
        actual = TestBaseAnsibleClass().asdict()
        assert actual == EXPECTED_DICT

    def test__str__(self):
        actual = TestBaseAnsibleClass().__str__()
        print("ACTUAL", actual)
        print("-------------------")
        print("EXPECTED_DICT", EXPECTED_DICT)
        assert actual == EXPECTED_DICT.__str__()

    @patch("ansible_please.base_ansible.save_yaml_to_file", return_value=None)
    @patch("ansible_please.ansible_dict.save_yaml_to_file", return_value=None)
    def test_save_to_file(
        self, mock_save_yaml_to_file, mock_ansible_dict_save_yaml_to_file
    ):
        """should be covered in test_utils
        """
        _ = TestBaseAnsibleClass().save_to_file()
        assert True
        _ = AnsibleDict({"test": None}).save_to_file()
        assert True
