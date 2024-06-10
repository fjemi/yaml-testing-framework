#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import functools
import inspect
import os
import threading
from types import FunctionType, ModuleType
from types import SimpleNamespace as sns
from typing import (
  Any,
  Awaitable,
  Callable,
  Iterable,
  Protocol,
  Type,
  runtime_checkable,
)

from main.process import casts
from main.utils import get_object, independent


MODULE = __file__

CONFIG = '''
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
  method: Callable | None,
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
) -> sns:
  values = sns(output=output, expected=expected)
  type_hints = get_type_hints(method=method, filter_out=['return'])
  passed = []

  for key, value in values.__dict__.items():
    kind = type(value).__name__.lower()
    hints = get_object.main(
      parent=type_hints,
      route=key, )
    if type(hints).__name__ in CONFIG.union_types:
      hints = list(hints.__args__)
    hints = hints if isinstance(hints, list) else [hints]

    for i, item in enumerate(hints):
      hints[i] = item.__name__.lower()

      if item == Any:
        passed.append(key)
        continue
      if True in [
        isinstance(value, item),
        kind in [hints[i]],
      ]:
        passed.append(key)

    store = dict(
      kind=kind,
      valid_kinds=hints,
      method=method.__name__, )
    setattr(values, key, store)

  if False in [
    'expected' in passed,
    'output' in passed,
  ]:
    return sns(
      passed=False,
      output=values.output,
      expected=values.expected, )

  return method(
    module=module,
    output=output,
    expected=expected, )


def type_checks(method: Callable) -> Callable:

  @functools.wraps(method)
  def inner(
    output: Any | None = None,
    expected: Any | None = None,
    module: ModuleType | None = None,
  ) -> sns:
    return type_checks_inner(
      expected=expected,
      module=module,
      method=method,
      output=output, )

  return inner


@type_checks
def check_sns(
  module: ModuleType | None = None,
  expected: dict | None = None,
  output: sns | None = None,
) -> sns:
  _ = module

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


# make this a decorator
def failed_type_check(
  output: Any | None = None,
  output_wanted: str | None = None,
  expected: Any | None = None,
  expected_wanted: str | None = None,
) -> sns:
  wanted = output_wanted
  actual = type(output).__name__
  field = 'Output'

  if expected_wanted is not None:
    wanted = expected_wanted
    actual = type(expected).__name__
    field = 'Expected'

  output = f'{field} is of type {actual} not {wanted}'
  return sns(
    output=output,
    passed=False,
    expected=expected, )


@type_checks
def check_exception(
  expected: str,
  output: Exception,
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  _ = module

  passed = output == expected
  return sns(
    expected=expected,
    output=output,
    passed=passed, )


@type_checks
def check_function(
  output: Callable | FunctionType,
  expected: dict,
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
def check_dataclass(
  output: DataClass,
  expected: dict,
  module: ModuleType | None = None,
) -> sns:
  _ = module

  name = type(output).__name__
  output = dc.asdict(output)
  fields = {}
  for key in expected.get('fields', {}):
    if key in output:
      fields[key] = output.get(key, None)

  output = sns(fields=fields, name=name).__dict__
  passed = output == expected
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


@type_checks
def check_class(
  output: Type | object,
  expected: dict,
  module: ModuleType | None = None,
) -> sns:
  _ = module

  fields = {}
  expected_fields = expected.get('fields', {})
  for name in expected_fields:
    if hasattr(output, name):
      fields[name] = get_object.main(
        parent=output,
        route=name, )

  output = sns(name=output.__class__.__name__, fields=fields).__dict__
  passed = output == expected
  return sns(output=output, expected=expected, passed=passed)


@type_checks
def check_length(
  output: Iterable,
  expected: int | float,
  module: ModuleType | None = None,
) -> sns:
  _ = module

  passed = len(output) == expected
  return sns(
    passed=passed,
    output=len(output),
    expected=expected, )


@type_checks
def check_type(
  output: Any,
  expected: str | list,
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
  output: Any | None = None,
  expected: list | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
) -> sns:
  _ = module

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
  module: ModuleType | None = None,
) -> sns:
  _ = module

  store = {}
  for key in expected:
    store[key] = getattr(output, key, 'key/value does not exist')

  passed = store == expected
  return sns(passed=passed, output=store, expected=expected)


@type_checks
def check_key_value_in_dict(
  output: dict,
  expected: dict,
  module: ModuleType | None = None,
) -> sns:
  _ = module

  fields = {}
  for key in expected:
    fields[key] = output.get(key, None)

  passed = expected == fields
  return sns(passed=passed, output=fields, expected=expected)


@type_checks
def check_thread(
  output: list| threading.Thread,
  expected: list | dict,
  module: ModuleType | None = None,
) -> sns:
  _ = module

  data = sns(**locals())

  if not isinstance(output, list):
    output = [output]
  if not isinstance(expected, list):
    expected = [expected]

  results = []
  for item in output:
    start = item.name.find('(') + 1
    target_name = item.name[start:-1]
    result = dict(target_name=target_name)
    results.append(result)

  passed = results == expected
  return sns(
    output=results,
    expected=expected,
    passed=passed, )


def call_function(
  arguments: dict | list | tuple,
  function: Callable | Awaitable,
  cast_output: list | None = None,
  module: ModuleType | str | None = None,
) -> Any:
  result = None
  exception = None

  try:
    if isinstance(arguments, dict):
      result = function(**arguments)
    elif isinstance(arguments, list | tuple):
      result = function(*arguments)
    else:
      result = function(arguments)
  except Exception as e:
    result = e

  result = independent.get_task_from_event_loop(task=result)

  if isinstance(result, Exception):
    exception = result

    try:
      result = function(arguments)
    except Exception as e:
      exception = e

    result = independent.get_task_from_event_loop(task=result)

    if isinstance(result, Exception):
      result = exception

  result = casts.main(
    module=module,
    casts=cast_output,
    object=result, )

  return result


@type_checks
def check_function_output(
  output: Callable | FunctionType,
  expected: Any | None,
  module: ModuleType | None = None,
) -> sns:
  _ = module

  expected = sns(**expected)
  output = [call_function(
    function=output,
    arguments=arguments,
    cast_output=getattr(expected, 'cast_output', []),
    module=getattr(expected, 'module', []),
    ) for arguments in expected.arguments
  ]

  passed = output == expected.output
  return sns(
    output=output,
    expected=expected.output,
    passed=passed, )


@type_checks
def check_file_exists(
  module: ModuleType | None = None,
  output: str | None = None,
  expected: str | None = None,
) -> sns:
  _ = module

  data = sns(**locals())
  data.passed = False
  if os.path.isfile(data.expected) and data.expected == data.output:
    data.passed = True
  return data


@type_checks
def check_spies(
  output: Any,
  expected: dict,
  module: ModuleType | None = None,
) -> sns:
  _ = output

  store = {}
  passed = True

  for key, values in expected.items():
    spy_store = {}

    for field, value in values.items():
      route = f'SPIES.{key}.{field}'
      spy_store[field] = get_object.main(parent=module, route=route)

    store[key] = spy_store

  passed = store == expected
  return sns(
    output=store,
    expected=expected,
    passed=passed, )


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location=MODULE)


if __name__ == '__main__':
  examples()
