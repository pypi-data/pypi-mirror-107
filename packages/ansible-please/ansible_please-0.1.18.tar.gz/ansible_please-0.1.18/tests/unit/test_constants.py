from omegaconf import OmegaConf

EXPECTED_HOST_INPUT_DICT = dict(
    OmegaConf.create(
        """
hosts:
    master_host:
      - '127.0.0.1'
    worker_hosts:
      - '127.0.0.1'
host_info:
  '127.0.0.1':
"""
    )
)

EXPECTED_TEST_PLAYBOOK = dict(
    OmegaConf.create(
        """
- name: test_playbook
  hosts: test_hosts
  gather_facts: true
  tasks:
  - name: '[up] Install something with command line'
    command:
      cmd: echo test
    tags:
    - up
"""
    )[0]
)
