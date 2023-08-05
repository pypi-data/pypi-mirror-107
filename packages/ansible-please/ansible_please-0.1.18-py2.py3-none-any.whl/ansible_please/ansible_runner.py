from __future__ import annotations

import typing
import attr
from ansible_please.inventory import Inventory
from ansible_please.playbook import Playbook
from loguru import logger
import ansible_runner

# from ansible_runner.runner_config import RunnerConfig
from contextlib import contextmanager
import tempfile


class TempfileTuple:
    def __init__(self, inventory, playbook, delete=False):
        self.inventory_tempfile: tempfile.NamedTemporaryFile = inventory.save_to_file(
            delete
        )
        self.playbook_tempfile: tempfile.NamedTemporaryFile = playbook.save_to_file(
            delete
        )

    def delete(self) -> None:
        if self.delete:
            self.inventory_tempfile.close()
            self.playbook_tempfile.close()


@attr.s(repr=False)
class AnsibleRunner:

    playbooks: typing.List[Playbook] = attr.ib(default=[])
    input_path: str = attr.ib(default=None)
    inventory: Inventory = attr.ib(default=None)

    def __attrs_post_init__(self):
        if self.input_path is None and self.inventory is None:
            raise ValueError("Input path or Inventory must be provided!")
        if self.input_path is not None:
            self.inventory = Inventory.from_yaml(self.input_path)

    @contextmanager
    def _load_yamls(self, playbook: Playbook, delete_files=False) -> TempfileTuple:
        t = TempfileTuple(self.inventory, playbook, delete=delete_files)
        try:
            yield t
        finally:
            t.delete()

    def run(
        self, tags: typing.List[str] = ["up"], delete_files=True, verbosity=1
    ) -> None:
        tags = " ".join(tags)
        for playbook in self.playbooks:
            with self._load_yamls(playbook, delete_files=delete_files) as t:
                out = ansible_runner.run(
                    private_data_dir="/tmp/",
                    playbook=t.playbook_tempfile.name,
                    inventory=t.inventory_tempfile.name,
                    tags=tags,
                    verbosity=verbosity,
                )
                logger.info("{}: {}".format(out.status, out.rc))
                logger.info("Final status:")
                logger.info(out.stats)

    def up(self, delete_files=True):
        self.run(tags=["up"], delete_files=True)

    def down(self, delete_files=True):
        self.run(tags=["down"], delete_files=True)
