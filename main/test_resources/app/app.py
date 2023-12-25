#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import os
import types
import typing

import main.test_resources.app.example_a as example_a
import main.test_resources.app.example_b as example_b
import main.test_resources.app.module as module
import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  resources_folder_name='test_resources',
  module=MODULE, )

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
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> 'pytest.Config':
  import pytest as py_test
  py_test.Config.rootdir = 'root_dir'
  if args[0] is not None:
    py_test.Config.rootdir = args[0]
  return py_test.Config


def get_locals(_locals: typing.List[str]) -> dict:
  store = {}
  for name in _locals:
    function_ = f'process_option_{name}'
    # trunk-ignore(ruff/ARG005)
    store[function_] = lambda *args, **kwargs: function_value
  return store


def function(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> str:
  return 'output'


def function_resource(function: str | None = None) -> typing.Callable:
  return LOCALS.get(function, None)


def module_resource(module: str | None = None) -> types.ModuleType | None:
  if isinstance(module, str):
    return LOCALS.get(module, None)


def handle_id_resource(data: dict | None = None) -> dict:
  data = data or {}

  module = data.get('module', '')
  module = module_resource(module=module)

  function_ = data.get('function', '')
  kind = type(function_).__name__.lower()

  if kind == 'function':
    function_ = function_.__name__

  if hasattr(module, str(function_)):
    function_ = getattr(module, function_, None)

  data.update({
    'module': module,
    'function': function_, })
  return data


def test_resource(test: Store | None = None) -> Store:
  return test


def get_function_output_resource(data: dict | None = None) -> dict:
  data = data or {}
  function_ = data.get('function', '')
  data['function'] = function_resource(function=function_)
  return data


def main_resource(tests: list) -> list:
  n = range(len(tests))
  for i in n:
    tests[i] = dc.asdict(tests[i])
  return tests


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
