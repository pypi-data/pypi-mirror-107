from __future__ import annotations

import attr
import typing
from ansible_please.task_templates.command import Command


@attr.s(repr=False)
class Pip(Command):

    cmd: str = attr.ib(
        default="{{ ansible_python_interpreter }} -m pip install", init=False
    )

    task_description: str = attr.ib(default="Install package via pip")
    packages: typing.List[str] = attr.ib(default=[])

    def __attrs_post_init__(self):
        for p in self.packages:
            self.cmd += " {}".format(p)
        self._exclude_patterns.append("packages")
