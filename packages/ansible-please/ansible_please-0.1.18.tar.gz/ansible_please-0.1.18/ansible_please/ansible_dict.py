import typing
from typing import NamedTuple
from omegaconf import OmegaConf
from ansible_please.utils import save_yaml_to_file


class AnsibleDict(NamedTuple):
    data: typing.Dict[str, typing.Any]

    def asdict(self):
        return self._asdict()["data"]

    def pretty(self, use_list=True):
        d = self.asdict()
        if use_list:
            d = [d]
        return OmegaConf.to_yaml(OmegaConf.create(d))

    def save_to_file(self) -> str:
        """saves yaml to tempfile

        Returns:
            str: returns tempfile name
        """
        return save_yaml_to_file(self.__str__())

    def __str__(self):
        return self.pretty()
