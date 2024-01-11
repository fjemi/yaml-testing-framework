#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
import types
import typing

import pytest
import utils.app as utils

# trunk-ignore(ruff/F401)
from main.test_resources.app import example_a, example_b, module


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  resources_folder_name='test_resources',
  module=MODULE,
)

LOCALS = locals()


class Store:
  pass


def get_pytest(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> types.ModuleType:
  import pytest as py_test
  return py_test


def get_pytest_parser(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> 'pytest.Parser':
  import pytest as py_test
  return py_test.Parser


def get_pytest_config(
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> 'pytest.Config':
  import pytest as py_test
  py_test.Config.rootdir = 'root_dir'

  if args[0] is not None:
    py_test.Config.rootdir = args[0]

  return py_test.Config


def function(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> str:
  return 'output'


def function_resource(function: str | None = None) -> typing.Callable:
  return LOCALS.get(function, None)


def module_resource(
  # trunk-ignore(ruff/F811)
  module: str | None = None,
) -> types.ModuleType | None:
  if isinstance(module, str):
    return LOCALS.get(module, None)


def handle_id_resource(data: dict | None = None) -> dict:
  data = data or {}

  module_ = data.get('module', '')
  module_ = module_resource(module=module_)

  function_ = data.get('function', '')
  kind = type(function_).__name__.lower()

  if kind == 'function':
    function_ = function_.__name__

  if hasattr(module_, str(function_)):
    function_ = getattr(module_, function_, None)

  data.update({
    'module': module_,
    'function': function_,
  })
  return data


def test_resource(test: Store | None = None) -> Store:
  return test


def get_function_output_resource(data: dict | None = None) -> dict:
  data = data or {}
  function_ = data.get('function', '')
  data['function'] = function_resource(function=function_)
  return data


def main_resource(tests: list) -> list | None:
  n = range(len(tests))
  for i in n:
    return dc.asdict(tests[i])


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
