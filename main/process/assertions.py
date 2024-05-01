#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

from main.process.casts import app as casts
import yaml
from main.utils import get_config, get_object, independent, schema, set_object


MODULE = __file__
CONFIG = get_config.main(module=MODULE)

LOCALS = locals()


def main(
  assertions: List[dict] | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  # key: str | None = None,
  id: str | None = None,
  id_short: str | None = None,
) -> sns:
  assertions = assertions or []

  for i, item in enumerate(assertions):
    assertion = pre_processing(
      assertion=item,
      module=module,
      output=output,
      id=id,
      id_short=id_short, )
    assertion = independent.process_operations(
      data=assertion,
      functions=LOCALS,
      operations=CONFIG.operations.main, )
    assertions[i] = assertion

  n = len(assertions)
  plural = 's' if n != 1 else ''
  level = 'info' if n != 0 else 'warning'
  log = sns(
    level=level,
    message=f'Processed {n} assertion{plural} for {id_short}', )

  data = sns(
    assertions=assertions,
    _cleanup=['module', 'output'],
    log=log, )
  return data


def pre_processing(
  assertion: dict | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  id: str | None = None,
  id_short: str | None = None,
) -> sns:
  assertion = assertion or {}
  locals_ = locals()
  fields = list(locals_.keys())
  fields.remove('assertion')
  for field in fields:
    assertion = set_object.main(
      parent=assertion,
      route=field,
      value=locals_[field], )
    # assertion.update({field: locals_[field]})
  return schema.get_model(name='process_assertions.Assertion', data=assertion)


def pass_through(
  output: Any | None = None,
  expected: Any | None = None,
  method_name: str | None = None,
) -> sns:
  _ = expected, output
  return sns(
    passed=False,
    expected='',
    output=f"Assertion method {method_name} does not exist", )


def get_assertion_method(
  method: str | None = None,
  module: ModuleType | None = None,
) -> sns:
  data = sns(method_name=str(method))
  data.method = get_object.main(
    parent=module,
    name=data.method_name, )

  if not isinstance(data.method, Callable):
    module = module.__file__
    message = f'Method {method} does not exist in module at location {module}'
    data.log = sns(
      level='error',
      message=message, )
    data.method = pass_through
    data.output = data.log

  return data


def reset_output_value(
  output: Any | None = None,
  field: str | None = None,
) -> sns:
  output = get_object.main(parent=output, name=field)
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


def get_assertion_result(
  method: Callable | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  result = method(
    output=output,
    expected=expected, )
  result.method = method.__name__
  result.module = None
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


def handle_failed_assertion(
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
