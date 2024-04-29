#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable

import yaml
from main.utils import (
  get_config,
  get_module,
  invoke_testing_method,
  schema,
)


MODULE = __file__
PARENT_MODULE = invoke_testing_method.get_parent_module_location(
  resource_suffix='_resource',
  resource_module=MODULE, )

CONFIG = get_config.main(module=PARENT_MODULE)
LOCALS = locals()


def set_exception(assertion: Any) -> Any:
  try:
    sum([1, '1'])
  except Exception as exception:
    assertion.exception = exception
  return assertion


def check_equals(
  output: Any,
  expected: Any,
) -> sns:
  passed = output == expected
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


def check_method_a() -> None:
  return


def get_module_wrapper(module: str | None = None) -> ModuleType:
  return get_module.main(location=module, pool=False)


def assertions_resource(
  case_: Any | None = None,
  assertions: list[dict] | None = None,
) -> Any:
  if assertions:
    return [
      schema.get_model(
        name='process_assertion.Assertion',
        data=assertion,
      ) for assertion in assertions
    ]

  if case_ == 'undefined_assertions':
    return sns(assertions=None)

  if case_ == 'defined_assertions':
    case_ = sns()
    case_.result = {'key': 'value'}
    case_.exception = {'name': 'name'}
    case_.assertions = '''
    - method: assertions.app.check_type
      field: key
      expected: str
    - method: assertions.app.check_substring_in_string
      expected:
        key: value
    '''
    case_.assertions = yaml.safe_load(case_.assertions)
    return case_


def assertion_resource(
  assertion: dict | None = None,
) -> sns:
  assertion = assertion or {}
  assertion = sns(**assertion)
  return assertion


def method_resource(method: str | None = None) -> None | Callable:
  method = str(method)
  return LOCALS.get(method, None)


def reset_output_value_cast_arguments(
  output: dict | None = None,
) -> sns:
  return sns(**output)


def convert_to_yaml_cast_arguments(field: Any) -> Any:
  # values = sns('None'=None, list=['a'])
  return field


def main_cast_arguments(output: dict | None = None) -> sns:
  output = output or {}
  output = sns(**output)

  module = getattr(output, 'module', None)
  output.module = get_module.main(location=module, pool=False)

  output.assertions = getattr(output, 'assertions', [])

  return output.__dict__


def list_sns_to_list_dict(assertions: list) -> list:
  if not isinstance(assertions, list):
    return assertions

  def inner(item: sns) -> dict:
    return item.__dict__

  return [inner(item=item) for item in assertions]


def main_cast_output(assertions: list | None = None) -> list | None:
  if not isinstance(assertions, list):
    return assertions

  def inner(assertion: sns) -> dict:
    if isinstance(assertion.method, Callable):
      assertion.method = assertion.method.__name__
    return assertion.__dict__

  return [inner(assertion=item) for item in assertions]


def convert_expected_and_output_to_yaml_cast_arguments(
  assertion: dict | None = None,
) -> sns:
  assertion = assertion or {}
  return sns(**assertion)


def compare_expected_and_output_cast_arguments(
  assertion: dict | None = None,
) -> sns:
  assertion = assertion or {}
  assertion = sns(**assertion)

  assertion.method = check_equals
  assertion.module = get_module.main(location=MODULE, pool=False)
  return assertion


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
