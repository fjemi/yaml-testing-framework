#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
import os
from types import ModuleType
from typing import Any, List

import pytest as py_test
from error_handler.app import main as error_handler
from get_config.app import main as get_config

# trunk-ignore(ruff/F401)
from utils import app as utils

from main.app import main as app


MODULE = __file__
CONFIG = get_config(module=MODULE)
CONFIG.root_paths = [
  f'.{os.sep}',
  f'{os.sep}{os.sep}',
  f'.{os.sep}',
  *CONFIG.root_paths,
]
LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


@error_handler()
def get_options(
  options: dict,
  option_names: dict,
) -> dict:
  store = {}
  for name in option_names:
    option_name = name.replace('-', '_')
    store[option_name] = options.get(option_name)
  return store


@error_handler()
def process_option_exclude_files(
  option: dict | None = None,
  # trunk-ignore(ruff/ARG001)
  config: py_test.Config | None = None,
) -> List[str]:
  if option is None:
    return []
  if isinstance(option, list) is False:
    option = [option]
  return option


@error_handler(default_value='')
def process_option_project_directory(
  option: str | None,
  config: py_test.Config,
) -> str:
  root = getattr(config, 'rootdir', '')
  root = str(root) or ''

  option = str(option)

  condition = option in CONFIG.root_paths
  if condition:
    return root

  condition = option.find('.') == 0
  if condition:
    option = os.path.join(root, option[1:])

  return option


@error_handler()
def get_pytest_parser(pytest_instance: ModuleType) -> py_test.Parser:
  if not pytest_instance:
    pytest_instance = get_pytest_instance()
  return pytest_instance.Parser


@error_handler()
async def get_pytest_instance(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> py_test:
  import pytest as instance
  return instance


@error_handler()
async def add_args_and_ini_options_to_parser(
  parser: py_test.Parser,
) -> py_test.Parser:
  for argument in CONFIG.options:
    parser.addoption(
      f"--{argument.get('args')}",
      **argument.get('options'),
    )
    ini_options = {'help': argument.get('options').get('help')}
    parser.addini(
      argument.get('args'),
      **ini_options,
    )
  return parser


@error_handler()
async def pytest_addoption(parser: py_test.Parser) -> None:
  add_args_and_ini_options_to_parser(parser=parser)


@error_handler()
async def pass_through(
  option: Any | None = None,
  # trunk-ignore(ruff/ARG001)
  config: py_test.Config | None = None,
) -> Any:
  return option


@error_handler()
async def pytest_configure(config: py_test.Config) -> None:
  data = {}

  names = [item['args'] for item in CONFIG.options]
  for name in names:
    option_name = f'--{name}'
    option = config.getoption(name=option_name)
    ini = config.getini(name)
    key = name.replace('-', '_')
    data[key] = option or ini

  py_test.yaml_tests = app(**data)
  py_test.yaml_tests = py_test.yaml_tests or []


@error_handler()
async def set_node_ids(item) -> str:
  item_callspec = getattr(item, 'callspec', None)

  condition = not item_callspec
  if condition:
    return item

  test = item.callspec.params.get('test', None)
  kind = type(test).__name__.lower()
  if kind in CONFIG.null_types:
    return item

  id_ = f"{test.module_location[-1]}.{test.function}"
  item._nodeid = id_.strip()
  return item


def pytest_itemcollected(item):
  item = set_node_ids(item=item)


def pytest_runtest_logreport(report):
  report.nodeid = format_report_nodeid(nodeid=report.nodeid)


def format_report_nodeid(nodeid: str) -> str:
  nodeid = str(nodeid)

  match = '<- test_entrypoint.py'
  index = nodeid.find(match)
  if index != -1:
    nodeid = nodeid[:index]

  match = '::test_['
  index = nodeid.find(match)
  if index != -1:
    nodeid = nodeid[index + len(match):]

  return nodeid.strip()


@error_handler()
async def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
