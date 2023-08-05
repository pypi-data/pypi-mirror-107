import attr

from ansible_please.ansible_task import AnsibleTask


@attr.s(repr=False)
class Command(AnsibleTask):

    task_name: str = attr.ib(default="command", init=False)

    task_description = attr.ib(default="Install something with command line")
    cmd: str = attr.ib(default="")
