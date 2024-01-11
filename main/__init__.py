#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

import nest_asyncio


MODULE = __file__
DIRECTORIES = {
  'main': '',
  'shared': 'shared',
}


def allow_nested_event_loops(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  nest_asyncio.apply()
  return 1


def add_directories_to_pythonpath(
  # trunk-ignore(ruff/ARG001)
  directories: None = None,
) -> int:
  directories = directories or DIRECTORIES
  root = os.path.dirname(__file__)

  for key, value in directories.items():
    branch = os.path.join(root, value)
    if branch not in sys.path:
      sys.path.append(branch)

  return 1


allow_nested_event_loops()
add_directories_to_pythonpath()


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(module=MODULE)


if __name__ == '__main__':
  example()
