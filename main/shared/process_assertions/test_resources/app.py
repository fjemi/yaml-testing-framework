#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any
import os
import yaml

from get_config.app import main as get_config


MODULE = __file__
PARENT_MODULE = os.path.dirname(os.path.dirname(MODULE)) + f'{os.sep}app.py'
CONFIG = get_config(module=PARENT_MODULE)


@dc.dataclass
class Store:
  pass


def set_exception(assertion: Any) -> Any:
  try:
    c = sum([1, '1'])
  except Exception as exception:
    assertion.exception = exception
  return assertion


def assertions_resource(
  case_: Any | None = None,
  assertions: list[dict] | None = None,
) -> Any:
  if assertions:
    return [CONFIG.schema.Assertion(**assertion) for assertion in assertions]


  if case_ == 'undefined_assertions':
    case_ = Store()
    case_.assertions = None
    return case_

  if case_ == 'defined_assertions':
    case_ = Store()
    case_.result = {'key': 'value'}
    case_.exception = {'name': 'name'}
    case_.assertions = '''
    - method: type
      field: key
      expected: str
    - method: contains
      expected:
        key: value
    '''
    case_.assertions = yaml.safe_load(case_.assertions)
    return case_


def main_resource(output: dict) -> dict:
  key = 'assertions'
  assertions = output.get(key, [])
  assertions = assertions or []
  n = range(len(assertions))
  
  for i in n:
    assertions[i] = dc.asdict(assertions[i])
  
  output[key] = assertions
  return output


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
