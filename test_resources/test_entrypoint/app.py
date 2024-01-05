#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc

import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  parent_filename='test_entrypoint.py',
  resources_folder_name='test_resources',
  module=MODULE,
)


@dc.dataclass
class Store:
  pass


def test_resource(test: dict | None = None):
  test = test or {}
  store = Store()

  for key, value in test.items():
    setattr(store, key, value)

  return store


def assertions_resource(assertions: list | None = None) -> list:
  assertions = assertions or []
  n = range(len(assertions))

  for i in n:
    store = Store()
    for key, value in assertions[i].items():
      setattr(store, key, value)
    assertions[i] = store

  return assertions


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
