import typing

from ansible_please.ansible_task import BaseAnsible


class Playbook(BaseAnsible):
    def __init__(
        self,
        name: str = None,
        hosts: str = None,
        gather_facts: bool = True,
        tasks: typing.List[BaseAnsible] = None,
        input_dict: typing.Dict[str, typing.Any] = {},
    ):
        super(Playbook, self).__init__(input_dict)
        self.name = name
        self.hosts = hosts
        self.gather_facts = gather_facts
        self.tasks = tasks
