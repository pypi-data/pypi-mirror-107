from __future__ import annotations

import attr
import typing
from typing import Optional

from ansible_please.ansible_task import AnsibleTask


@attr.s(repr=False)
class DockerContainer(AnsibleTask):

    task_name: str = attr.ib(default="community.docker.docker_container", init=False)

    name: Optional[str] = attr.ib(
        default="", validator=attr.validators.instance_of(str)
    )
    image: Optional[str] = attr.ib(
        default=None,
        converter=attr.converters.optional(str),
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    command: Optional[str] = attr.ib(
        default=None,
        converter=attr.converters.optional(str),
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    ports: Optional[typing.List[str]] = attr.ib(
        default=None,
        validator=attr.validators.optional(attr.validators.instance_of(list)),
    )
    state: Optional[str] = attr.ib(
        default=None,
        converter=attr.converters.optional(str),
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    user: Optional[str] = attr.ib(
        default="nobody",
        converter=attr.converters.optional(str),
        validator=attr.validators.optional(attr.validators.instance_of(str)),
    )
    keep_volumes: bool = attr.ib(
        default=False,
        converter=attr.converters.optional(bool),
        validator=attr.validators.optional(attr.validators.instance_of(bool)),
    )
    detach: bool = attr.ib(default=True, validator=attr.validators.instance_of(bool))
    tty: bool = attr.ib(default=False, validator=attr.validators.instance_of(bool))
    interactive: bool = attr.ib(
        default=False, validator=attr.validators.instance_of(bool)
    )
    network_mode: str = attr.ib(
        default="host", validator=attr.validators.instance_of(str)
    )
    env: Optional[typing.Dict[typing.Any, typing.Any]] = attr.ib(default=None)
    entrypoint: Optional[typing.List[str]] = attr.ib(default=None)
    container_default_behavior: Optional[str] = attr.ib(default="compatibility")

    @ports.validator
    def ports_validator(self, attribute, value) -> None:
        if isinstance(self.ports, list):
            if len(self.ports) == 0:
                self.ports = None
                return

            for v in self.ports:
                if not isinstance(v, str):
                    raise ValueError(
                        "expected string but got {} of type {}".format(v, type(v))
                    )

    def down(self) -> DockerContainer:
        return DockerContainer(
            task_description=self.task_description,
            name=self.name,
            user=self.user,
            keep_volumes=self.keep_volumes,
            state="absent",
        )
