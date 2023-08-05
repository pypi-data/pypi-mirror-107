import unittest
from ansible_please.utils import save_yaml_to_file, merge_dicts


class TestUtils(unittest.TestCase):
    def test_save_yaml_to_file(self):
        s = "-test_string"
        tempf = save_yaml_to_file(s, delete=True)
        with open(tempf.name, "r"):
            actual = tempf.read()
        tempf.close()
        assert actual.decode("utf-8") == s

    def test_merge_dicts(self):
        expected_dict = {"test": 1, "test2": {2: 3}}
        dict2 = {"test": 1, "test2": {2: 4}}
        dict1 = {"test2": {2: 3}}
        actual = merge_dicts(dict1, dict2)
        assert actual == expected_dict
