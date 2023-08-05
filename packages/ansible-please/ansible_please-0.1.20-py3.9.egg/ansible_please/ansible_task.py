from __future__ import annotations

import attr
from ansible_please.base_ansible import BaseAnsible
import typing
from ansible_please.ansible_dict import AnsibleDict
import types
import copy


def up(f, *args, **kwargs):
    def wrapped(*args, **kwargs) -> AnsibleTask:
        ansible_task_output = copy.deepcopy(f(*args, **kwargs))
        assert isinstance(ansible_task_output, AnsibleTask)
        ansible_task_output.task_state = "up"
        return ansible_task_output

    return wrapped


def down(f, *args, **kwargs):
    def wrapped(*args, **kwargs) -> AnsibleTask:
        ansible_task_output = copy.deepcopy(f(*args, **kwargs))
        assert isinstance(ansible_task_output, AnsibleTask)
        ansible_task_output.task_state = "down"
        return ansible_task_output

    return wrapped


class TaskMeta(type):
    def __new__(cls, name, bases, attr):
        task_states_map = {"up": up, "down": down}
        for name, value in attr.items():
            if name in task_states_map:
                if isinstance(value, types.FunctionType) or isinstance(
                    value, types.MethodType
                ):
                    attr[name] = task_states_map[name](value)

        return super(TaskMeta, cls).__new__(cls, name, bases, attr)


def validate_name(instance, attribute, value) -> None:
    if value == "":
        raise ValueError("Expected name to be a string of length > 0")


def validate_tags(instance, attribute, value) -> None:
    exclude_patterns = ["down", "up"]
    value = set(value)
    for pattern in exclude_patterns:
        value.discard(pattern)
    value = list(value)


@attr.s(repr=False)
class AnsibleTask(BaseAnsible, metaclass=TaskMeta):
    task_name: str = attr.ib(
        default="", validator=[attr.validators.instance_of(str), validate_name]
    )
    task_description: str = attr.ib(default="")
    task_state: str = attr.ib(default="up")
    tags: typing.List[str] = attr.ib(default=[], validator=[validate_tags])

    _exclude_patterns: typing.List[str] = attr.ib(
        init=False,
        default=[
            "task_name",
            "task_description",
            "tags",
            "task_state",
            "_exclude_patterns",
        ],
    )

    def asdict(self, additional_tags=[]) -> AnsibleDict:
        super_dict = super().asdict().data
        for pattern in self._exclude_patterns:
            super_dict.pop(pattern, None)
        return AnsibleDict(
            {
                "name": "[{}] {}".format(self.task_state, self.task_description),
                self.task_name: super_dict,
                "tags": self.tags + [self.task_state],
            }
        )

    def up(self) -> AnsibleTask:
        return self

    def down(self) -> AnsibleTask:
        return self

    def __str__(self):
        return self.asdict().__str__()
