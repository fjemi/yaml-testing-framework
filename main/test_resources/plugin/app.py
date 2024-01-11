#!.venv/bin/python3
# -*- coding: utf-8 -*-

import types
from typing import Any
from unittest import mock

import pytest
import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources',
)


class Store:
  pass


def pytest_resource(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> types.ModuleType:
  return pytest


def get_locals(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> dict:
  return {
    'process_option_option_0':
    # trunk-ignore(ruff/ARG005)
    lambda *args,
    # trunk-ignore(ruff/ARG005)
    **kwargs: 'processed_value_0',
    'process_option_option_1':
    # trunk-ignore(ruff/ARG005)
    lambda *args,
    # trunk-ignore(ruff/ARG005)
    **kwargs: 'processed_value_1',
  }


def project_directory_option_resource(option: str | None) -> str:
  conditions = [
    option is None,
    option == '.',
  ]

  if True in conditions:
    option = 'root_dir'

  return option


def process_option_project_directory_resource(
  arguments: dict | None = None,
) -> pytest.Config:
  arguments = arguments or {}

  option = arguments.get('option', None)
  option = project_directory_option_resource(option=option)

  config = pytest.Config
  setattr(config, 'rootdir', option)

  arguments.update({
    'option': option,
    'config': config,
  })

  return arguments


def get_options_or_inis_resource(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> mock:
  return mock


def pytest_parser_resource(
  # trunk-ignore(ruff/ARG001)
  parser: str | None = None,
) -> pytest.Parser:
  return pytest.Parser()


def pytest_configure_resource(
  # trunk-ignore(ruff/ARG001)
  config: str | None = None,
) -> pytest.Config:
  return pytest.Config


def set_node_ids_resource(item: Any) -> Store:
  test = Store()
  test.module_route = ['module_route']
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
