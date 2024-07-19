#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import functools
import inspect
import os
from types import FunctionType, ModuleType
from types import SimpleNamespace as sns
from typing import (
  Any,
  Callable,
  Iterable,
  Protocol,
  Type,
  runtime_checkable,
)

from main.process import casts
from main.utils import independent, objects, methods, get_module


CONFIG = '''
  schema:
    CallMethod:
      description:
      fields:
      - name: method
        description: The method to call
        default: null
        type: Callable
      - name: output
        default: []
        description: Expected output from calling method with arguments
        type: list
      - name: arguments
        default: []
        description: Arguments to pass to the method
        type: list
      - name: cast_output
        default: null
        description: List of casts to perform on output
        type: list
      - name: cast_arguments
        default: null
        description: List of casts to perform on arguments
        type: list
      - name: module
        default: ''
        description: Location of a module
        type: str

  union_types:
  - _UnionGenericAlias
  - UnionType
'''
CONFIG = independent.format_module_defined_config(config=CONFIG)


@runtime_checkable
@dc.dataclass
class DataClass(Protocol):
  pass


def get_type_hints(
  method: Callable | None = None,
  filter_out: list | None = None,
):
  store = {}

  if isinstance(method, Callable):
    store = inspect.getfullargspec(method).annotations

  if not isinstance(filter_out, list):
    filter_out = [filter_out]

  for item in filter_out:
    name = str(item)
    store[name] = None
    del store[name]

  return store


def type_checks_inner(
  output: Any | None = None,
  expected: Any | None = None,
  module: ModuleType | None = None,
  method: Callable | None = None,
  spies_: dict | None = None,
  __setup__: dict | None = None,
) -> sns:
  arguments = locals()
  arguments = independent.get_function_arguments(function=method, data=arguments)

  hints = sns()
  values = sns()
  hints.method = get_type_hints(method=method, filter_out=['return'])
  passed = []
  failed = []

  for parameter, argument in arguments.items():
    kind = type(argument).__name__.lower()

    hints.parameter = objects.get(
      parent=hints.method,
      route=parameter, )
    if type(hints.parameter).__name__ in CONFIG.union_types:
      hints.parameter = list(hints.parameter.__args__)
    else:
      hints.parameter = [hints.parameter]

    for i, item in enumerate(hints.parameter):
      if item == Any:
        passed.append(parameter)
        break

      item_kind = item.__name__.lower()
      if True in [
        kind == item_kind,
        isinstance(argument, item),
      ]:
        passed.append(parameter)
        break

      hints.parameter[i] = item_kind

    if parameter not in passed:
      failed.append(dict(
        name=parameter,
        hints=hints.parameter,
        kind=kind, ))

  if not failed:
    return method(**arguments)

  method = objects.get(
    parent=method,
    route='__name__',
    default=method, )
  parameters = dict(failed=failed, passed=passed)
  temp = dict(method=method, parameters=parameters)
  return sns(
    expected=temp,
    output=None,
    passed=False, )


def type_checks(method: Callable) -> Callable:

  @functools.wraps(method)
  def inner(
    output: Any | None = None,
    expected: Any | None = None,
    module: ModuleType | None = None,
    spies_: dict | None = None,
    __setup__: dict | None = None,
  ) -> sns:
    arguments = locals()
    arguments = independent.get_function_arguments(
      function=method, data=arguments)
    arguments.update(dict(method=method))
    return type_checks_inner(**arguments)

  return inner


@type_checks
def check_sns(
  expected: dict,
  output: sns,
) -> sns:
  store = {}
  for key, value in expected.items():
    if key in expected:
      store[key] = None
      if hasattr(output, key):
        store[key] = getattr(output, key)

  passed = store == expected
  return sns(
    passed=passed,
    expected=expected,
    output=store, )


@type_checks
def check_exception(
  expected: str,
  output: Exception,
) -> sns:
  output = type(output).__name__
  passed = expected == output
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


@type_checks
def check_module(
  output: ModuleType,
  expected: dict,
) -> sns:
  output = sns(
    location=getattr(output, '__file__', None), )
  output = output.__dict__
  passed = output == expected
  return sns(
    passed=passed,
    output=output,
    expected=expected, )


@type_checks
def check_equals(
  output: Any,
  expected: Any,
) -> sns:
  passed = output == expected
  return sns(
    expected=expected,
    output=output,
    passed=passed, )


@type_checks
def check_function(
  output: Callable | FunctionType,
  expected: dict,
) -> sns:
  temp = independent.get_decorated_function(function=output)
  if isinstance(temp, Callable):
    output = temp

  location = inspect.getfile(output)
  output = dict(name=output.__name__, location=location)
  passed = output == expected

  return sns(
    passed=passed,
    output=output,
    expected=expected, )


@type_checks
def check_class(
  output: Type | object,
  expected: dict,
) -> sns:
  fields = {}
  expected_fields = expected.get('fields', {})
  for name in expected_fields:
    if hasattr(output, name):
      fields[name] = objects.get(
        parent=output,
        route=name, )

  output = sns(name=output.__class__.__name__, fields=fields).__dict__
  passed = output == expected
  return sns(output=output, expected=expected, passed=passed)


@type_checks
def check_length(
  output: Iterable,
  expected: int | float,
) -> sns:
  passed = len(output) == expected
  return sns(
    passed=passed,
    output=len(output),
    expected=expected, )


@type_checks
def check_type(
  output: Any,
  expected: str | list,
) -> sns:
  passed = False

  if isinstance(expected, list) is False:
    expected = [expected]
  output_types = [
    type(output).__name__,
    str(output.__class__), ]
  output = output_types

  for expected_type in expected:
    for output_type in output_types:
      index = output_type.find(expected_type)

      if index == -1:
        continue

      output = expected_type
      expected = expected_type
      passed = True
      break

  return sns(
    passed=passed,
    output=output,
    expected=expected, )


@type_checks
def check_substring_in_string(
  output: str,
  expected: list | str,
) -> sns:
  if not isinstance(expected, list):
    expected = [expected]

  output = str(output)
  output = [str(item) for item in expected if output.find(item) != -1]
  passed = expected == output

  return sns(
    output=output,
    expected=expected,
    passed=passed, )


@type_checks
def check_item_in_list(
  output: list | tuple,
  expected: Any | list,
) -> sns:
  if not isinstance(expected, list):
    expected = [expected]

  output = output or []
  output = [item for item in expected if item in output]
  passed = output == expected
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


@type_checks
def check_list_contains_item(
  output: Any,
  expected: list,
) -> sns:
  if not isinstance(output, list):
    output = [output]
  if not isinstance(expected, list):
    expected = [expected]

  expected = [item for item in output if item in expected]
  passed = expected == output
  return sns(
    expected=expected,
    output=output,
    passed=passed, )


@type_checks
def check_key_in_dict(
  output: dict,
  expected: list | str,
) -> sns:
  if not isinstance(expected, list):
    expected = [expected]

  output = [item for item in expected if item in output]
  passed = output == expected
  return sns(
    output=output,
    expected=expected,
    passed=passed, )


@type_checks
def check_range(
  output: range,
  expected: dict,
) -> sns:
  store = {}
  for key in expected:
    store[key] = getattr(output, key, 'key/value does not exist')

  passed = store == expected
  return sns(passed=passed, output=store, expected=expected)


@type_checks
def check_key_value_in_dict(
  output: dict,
  expected: dict,
) -> sns:
  fields = {}
  for key in expected:
    fields[key] = output.get(key, None)

  passed = expected == fields
  return sns(passed=passed, output=fields, expected=expected)


def call_function(
  arguments: list = [],
  output: list = [],
  method: Callable | None = None,
  cast_arguments: list = [],
  cast_output: list = [],
  module: ModuleType | str = '',
) -> Any:
  store = []
  module = get_module.main(module=module, default=module).module
  passed = True

  for i, item in enumerate(arguments):
    data = casts.main(
      module=module,
      casts=cast_arguments,
      object=item, ).object
    data = methods.call.main(arguments=data, method=method).output
    data = casts.main(
      module=module,
      casts=cast_output,
      object=data, ).object
    store.append(data)
    if data != output[i]:
      passed = False

  return sns(
    expected=output,
    output=store,
    passed=passed, )


@type_checks
def check_function_output(
  output: Callable,
  expected: Any | None,
) -> sns:
  data = independent.get_model(schema=CONFIG.schema.CallMethod, data=expected)
  data.method = output
  return call_function(**data.__dict__)


@type_checks
def check_file_exists(
  output: str,
  expected: str,
) -> sns:
  data = sns(**locals())
  data.passed = False
  if os.path.isfile(data.expected) and data.expected == data.output:
    data.passed = True
  return data


@type_checks
def check_spies(
  expected: dict,
  spies_: dict | sns,
) -> sns:
  store = {}

  for method, spy in expected.items():
    spy_store = {}

    for field, value in spy.items():
      route = f'{method}.{field}'
      spy_store[field] = objects.get(parent=spies_, route=route)

    store[method] = spy_store

  passed = store == expected
  return sns(
    output=store,
    expected=expected,
    passed=passed, )


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main('.examples')


if __name__ == '__main__':
  examples()
