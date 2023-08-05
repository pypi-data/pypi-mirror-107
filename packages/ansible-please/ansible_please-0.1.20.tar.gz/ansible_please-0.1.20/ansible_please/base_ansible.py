from __future__ import annotations

import attr
import typing

from ansible_please.utils import merge_dicts, save_yaml_to_file
from ansible_please.ansible_dict import AnsibleDict
import tempfile


@attr.s(repr=False)
class BaseAnsible:
    input_dict: typing.Dict[str, typing.Any] = attr.ib(default={})

    def asdict(self, *args, **kwargs) -> AnsibleDict:
        d = {}
        for k, v in self.__dict__.items():
            value = v
            if value is not None:
                if isinstance(value, list):
                    value_list = [
                        self._get_value(sub_value)
                        for sub_value in value
                        if sub_value is not None
                    ]
                    d[k] = value_list
                else:
                    d[k] = self._get_value(value)
        d.pop("input_dict")
        d = merge_dicts(d, self.input_dict)
        return AnsibleDict(d)

    def _get_value(self, v) -> typing.Dict[str, typing.Any]:
        if isinstance(v, AnsibleDict):
            return v.asdict()
        if isinstance(v, BaseAnsible):
            return v.asdict().asdict()
        return v

    def save_to_file(self, delete=True) -> tempfile.NamedTemporaryFile:
        """Save yaml string into tempfile

        Returns:
            str: filename
        """
        return save_yaml_to_file(self.__str__(), delete=delete)

    def __str__(self):
        return self.asdict().__str__()
