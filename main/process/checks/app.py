#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

import yaml

from main.process.casts import process_cast_output
from main.utils import get_config, independent, objects, schema, get_module


MODULE = __file__
CONFIG = get_config.main(module=MODULE)

LOCALS = locals()


def main(
  checks: list | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  id: str | None = None,
  id_short: str | None = None,
  __spies__: dict | None = None,
) -> sns:
  data = independent.get_model(schema=CONFIG.schema.Entry, data=locals())
  data = independent.process_operations(
    data=data,
    functions=LOCALS,
    operations=CONFIG.operations.main, )
  return data.result


def process_checks(
  checks: list | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  id: str | None = None,
  id_short: str | None = None,
  __spies__: dict | None = None,
) -> sns:
  checks = checks or []
  locals_ = locals()

  for i, item in enumerate(checks):
    data = sns(locals_=locals_, item=item)
    data = independent.process_operations(
      data=data,
      functions=LOCALS,
      operations=CONFIG.operations.process_checks, )
    checks[i] = data.check

  checks = sns(checks=checks)
  return sns(result=checks)


def pre_processing(
  locals_: dict | None = None,
  item: dict | None = None,
) -> sns:
  store = {}

  for field in CONFIG.preferred_fields:
    values = sns()
    for route, parent in locals().items():
      value = objects.get(parent=parent, route=field)
      values = objects.update(
        route=route,
        parent=values,
        value=value, )
    store[field] = values.item or values.locals_

  item.update(locals_)
  item.update(store)
  return independent.get_model(schema=CONFIG.schema.Check, data=item)


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
      output=f"Check method {method} does not exist", )

  return pass_through_inner


def get_check_method(
  method: str | None = None,
  module: ModuleType | None = None,
) -> sns:
  name = str(method)
  method = objects.get(parent=module, route=name)
  if isinstance(method, Callable):
    return sns(method=method)

  method = pass_through(method=name)
  module = module.__file__
  message = f'Check method {name} does not exist in module {module}'
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
  output = objects.get(parent=output, route=field)
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


def get_check_result(
  module: ModuleType | None = None,
  method: Callable | None = None,
  output: Any | None = None,
  expected: Any | None = None,
  __spies__: dict | None = None,
) -> sns:
  arguments = locals()
  arguments = independent.get_function_arguments(
    function=method, data=arguments)
  result = method(**arguments)
  result.method = objects.get(
    parent=method,
    route='__name__',
    default=method, )
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

  return data


def post_processing(
  id: str | None = None,
  id_short: str | None = None,
  expected: Any | None = None,
  output: Any | None = None,
  passed: Any | None = None,
  method: Callable | str | None = None,
) -> sns:
  method = objects.get(
    parent=method,
    route='__name__',
    default=method, )
  check = sns(**locals())
  return sns(check=check)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
