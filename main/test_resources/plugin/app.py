#!.venv/bin/python3
# -*- coding: utf-8 -*-


import typing
from typing import Any
import types
import os

import pytest
from unittest import mock


MODULE = __file__
PARENT_MODULE = os.path.dirname(MODULE)
PARENT_MODULE = os.path.dirname(PARENT_MODULE)
PARENT_MODULE = os.path.dirname(PARENT_MODULE)
PARENT_MODULE = os.path.join(PARENT_MODULE, 'plugin.py')


class Store:
  pass


def pytest_resource(
  # ruff: noqa: ARG001
  *args,
  **kwargs,
) -> types.ModuleType:
  return pytest


def get_locals(*args, **kwargs) -> dict:
  return {
    'process_option_option_0': lambda *args, **kwargs: 'processed_value_0',
    'process_option_option_1': lambda *args, **kwargs: 'processed_value_1', }


def get_pytest_config(config: dict | str | None = None):
  kind = type(config).__name__.lower()
  
  if kind == 'str':
    pytest.Config.rootdir = config
  elif kind == 'dict':
    for key, value in config.items():
      setattr(pytest.Config, key, value)

  return pytest.Config


def get_options_or_inis_resource(*args, **kwargs) -> 'unittest.mock':
  return mock


def pytest_parser_resource(parser: str | None = None) -> pytest.Parser:
  return pytest.Parser()


def pytest_configure_resource(config: str | None = None) -> pytest.Config:
  return pytest.Config


def set_node_ids_resource(item: Any) -> Any:
  test = Store()
  test.module_location = ['module_location']
  test.function = 'function'
  
  _ = item
  item = Store()
  item.callspec = Store()
  item.callspec.params = Store()
  item.callspec.params = {'test': test}
  
  return item


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
