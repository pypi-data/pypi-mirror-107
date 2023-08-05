import unittest
from ansible_please.playbook import Playbook
from ansible_please.task_templates import Command
from ansible_please.ansible_dict import AnsibleDict
from .test_constants import EXPECTED_TEST_PLAYBOOK  # noqa


class TestPlaybook(unittest.TestCase):
    def test_playbook_creation(self):
        c = Command(cmd="echo test")
        p = Playbook(name="test_playbook", hosts="test_hosts", tasks=[c])
        assert p.asdict() == AnsibleDict(EXPECTED_TEST_PLAYBOOK)
