#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

import yaml

from main.process import casts
from main.utils import get_config, get_object, independent, schema, set_object


MODULE = __file__
CONFIG = get_config.main(module=MODULE)

LOCALS = locals()


def main(
  checks: List[dict] | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  id: str | None = None,
  id_short: str | None = None,
) -> sns:
  checks = checks or []

  for i, item in enumerate(checks):
    check = pre_processing(
      check=item,
      module=module,
      output=output,
      id=id,
      id_short=id_short, )
    check = independent.process_operations(
      data=check,
      functions=LOCALS,
      operations=CONFIG.operations.main, )
    checks[i] = check

  n = len(checks)
  plural = 's' if n != 1 else ''
  level = 'info' if n != 0 else 'warning'
  log = sns(
    level=level,
    message=f'Processed {n} check{plural} for {id_short}', )

  data = sns(
    checks=checks,
    _cleanup=['module', 'output'],
    log=log, )
  return data


def pre_processing(
  check: dict | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  id: str | None = None,
  id_short: str | None = None,
) -> sns:
  check = check or {}
  locals_ = locals()
  fields = list(locals_.keys())
  fields.remove('check')
  for field in fields:
    check = set_object.main(
      parent=check,
      route=field,
      value=locals_[field], )
  return independent.get_model(schema=CONFIG.schema.Check, data=check)


def pass_through(method: str | None = None) -> Callable:

  def pass_through_inner(
    module: ModuleType | None = None,
    output: Any | None = None,
    expected: Any | None = None,
  ) -> Callable:
    _ = output, expected, module

    return sns(
      passed=False,
      expected='',
      output=f"Assertion method {method} does not exist", )

  return pass_through_inner


def get_check_method(
  method: str | None = None,
  module: ModuleType | None = None,
) -> sns:
  name = str(method)
  method = get_object.main(parent=module, route=name)
  if isinstance(method, Callable):
    return sns(method=method)

  method = pass_through(method=name)
  module = module.__file__
  message = f'Assertion method {name} does not exist in module {module}'
  log = sns(level='error', message=message)
  output = log

  return sns(
    method=method,
    log=log,
    output=output, )


def reset_output_value(
  output: Any | None = None,
  field: str | None = None,
) -> sns:
  output = get_object.main(parent=output, route=field)
  log = None
  if output is None and field:
    type_ = type(output).__name__
    log = sns(
      level='warning',
      message=f'Field {field} does not exist in object of type {type_}', )
  return sns(
    output=output,
    _cleanup=['field'],
    log=log, )


def cast_output(
  output: Any | None = None,
  cast_output: list | None = None,
  module: ModuleType | None = None,
) -> sns:
  output = casts.main(
    module=module,
    casts=cast_output,
    object=output, )
  return sns(output=output, _cleanup=['cast_output'])


def get_check_result(
  module: ModuleType | None = None,
  method: Callable | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  result = method(
    module=module,
    output=output,
    expected=expected, )
  result.method = method.__name__
  result._cleanup = ['module']
  return result


def convert_to_yaml(
  object: Any | None = None,
  field: str | None = None,
) -> sns:
  data = sns(object=object)

  try:
    if isinstance(data.object, str):
      data.object = yaml.safe_load(data.object)
    data.object = yaml.dump(data.object).strip()
  except Exception as exception:
    exception = type(exception).__name__
    message = f'{exception} occurred trying to convert {field} to YAML'
    data.log = sns(message=message, level='error')

  return data


def handle_failed_check(
  passed: bool | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  data = sns()

  if passed is True:
    return data

  data.output = output
  data.expected = expected
  data.log = []

  for key in data.__dict__:
    value = getattr(data, key, None)
    value = convert_to_yaml(object=value, field=key)
    if not getattr(value, 'log', None):
      setattr(data, key, value.object)
    if getattr(value, 'log', None):
      data.log.append(value.log)

  data._cleanup = ['field']
  return data


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
