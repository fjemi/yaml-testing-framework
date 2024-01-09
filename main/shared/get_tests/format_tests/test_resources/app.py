#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc

import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources',
)


def tests_resource(tests: list) -> list:
  n = range(len(tests))
  for i in n:
    test = tests[i].get('test', {})
    if dc.is_dataclass(test):
      tests[i]['test'] = dc.asdict(test)
  return tests


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()