#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable

from main.utils import get_config, get_module, invoke_testing_method, schema


MODULE = __file__
PARENT_MODULE = invoke_testing_method.get_parent_module_location(
  resource_suffix='_resource',
  resource_module=MODULE, )

CONFIG = get_config.main(module=PARENT_MODULE)
LOCALS = locals()


def set_exception(check: Any) -> Any:
  try:
    sum([1, '1'])
  except Exception as exception:
    check.exception = exception
  return check


def check_equals(
  module: ModuleType,
  output: Any,
  expected: Any,
) -> sns:
  _ = module
  passed = output == expected
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


def check_method_a() -> None:
  return


def wrapper_get_module(module: str | None = None) -> ModuleType:
  return get_module.main(location=module, pool=False)


def check_resource(
  check: dict | None = None,
) -> sns:
  check = check or {}
  check = sns(**check)
  return check


def method_resource(method: str | None = None) -> None | Callable:
  method = str(method)
  return LOCALS.get(method, None)


def reset_output_value_cast_arguments(
  output: dict | None = None,
) -> sns:
  return sns(**output)


def convert_to_yaml_cast_arguments(field: Any) -> Any:
  return field


def main_cast_arguments(output: dict | None = None) -> sns:
  output = output or {}
  output = sns(**output)

  module = getattr(output, 'module', None)
  output.module = get_module.main(location=module, pool=False)

  output.checks = getattr(output, 'checks', [])

  return output.__dict__


def list_sns_to_list_dict(checks: list) -> list:
  if not isinstance(checks, list):
    return checks

  def inner(item: sns) -> dict:
    return item.__dict__

  return [inner(item=item) for item in checks]


def main_cast_output(checks: list | None = None) -> list | None:
  if not isinstance(checks, list):
    return checks

  def inner(check: sns) -> dict:
    if isinstance(check.method, Callable):
      check.method = check.method.__name__
    return check.__dict__

  return [inner(check=item) for item in checks]


def convert_expected_and_output_to_yaml_cast_arguments(
  check: dict | None = None,
) -> sns:
  check = check or {}
  return sns(**check)


def compare_expected_and_output_cast_arguments(
  check: dict | None = None,
) -> sns:
  check = check or {}
  check = sns(**check)

  check.method = check_equals
  check.module = get_module.main(location=MODULE, pool=False)
  return check


def sns_to_dict(output: sns) -> dict:
  return output.__dict__


def examples() -> None:
  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
