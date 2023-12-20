#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import os


MODULE = __file__
PARENT_MODULE = os.path.dirname(MODULE)
PARENT_MODULE = os.path.dirname(PARENT_MODULE)
PARENT_MODULE = os.path.join(PARENT_MODULE, 'app.py')


def tests_resource(tests: list) -> list:
  tests = tests or []
  n = range(len(tests))
  for i in n:
    test = tests[i].get('test', {})
    tests[i] = dc.asdict(test)
  return tests


async def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  project_directory = PARENT_MODULE
  # project_directory = 'examples/add'
  invoke_pytest(
    # invoke='pytest',
    project_directory=project_directory, )


if __name__ == '__main__':
  example()
