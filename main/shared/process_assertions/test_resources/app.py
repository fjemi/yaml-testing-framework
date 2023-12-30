#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from types import ModuleType
from typing import Any, Callable

import yaml
from get_config.app import main as get_config
from utils import app as utils

from assertions import app as assertions


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources', )

CONFIG = get_config(module=PARENT_MODULE)
LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


def set_exception(assertion: Any) -> Any:
  try:
    sum([1, '1'])
  except Exception as exception:
    assertion.exception = exception
  return assertion


def module_resource(module: str | None = None) -> ModuleType:
  return LOCALS.get(module, None)


def assertions_resource(
  case_: Any | None = None,
  assertions: list[dict] | None = None,
) -> Any:
  if assertions:
    return [CONFIG.schema.Assertion(**assertion) for assertion in assertions]

  if case_ == 'undefined_assertions':
    case_ = Data_Class()
    case_.assertions = None
    return case_

  if case_ == 'defined_assertions':
    case_ = Data_Class()
    case_.result = {'key': 'value'}
    case_.exception = {'name': 'name'}
    case_.assertions = '''
    - method: assertions.app.assert_type
      field: key
      expected: str
    - method: assertions.app.assert_substring_in_string
      expected:
        key: value
    '''
    case_.assertions = yaml.safe_load(case_.assertions)
    return case_


def assertion_resource(
  assertion: dict | None = None,
) -> CONFIG.schema.Assertion | None:
  if assertion:
    return CONFIG.schema.Assertion(**assertion)


def method_resource(
  module: ModuleType | None = None,
  method: str | None = None,
) -> None | Callable:
  method = str(method)
  return getattr(module, method, None)


def verify_expected_output_resource(assertion: dict | None = None) -> dict:
  assertion = CONFIG.schema.Assertion(**assertion)
  assertion.method = method_resource(
    module=assertions,
    method=assertion.method, )
  return assertion


def main_cast_output(assertions: list | None = None) -> list | None:
  if isinstance(assertions, list):
    n = range(len(assertions))
    for i in n:
      assertions[i] = dc.asdict(assertions[i])
    return assertions


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
