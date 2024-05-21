#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import inspect
import os
import threading
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Awaitable, Callable

from main.process import casts
from main.utils import get_object, independent


@dc.dataclass
class DataClass:
  pass


def check_sns(
  module: ModuleType | None = None,
  expected: dict | None = None,
  output: sns | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, sns),
    expected=expected,
    expected_check=isinstance(expected, dict), )
  if type_checks != 'passed':
    return type_checks

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


def check_exception(
  module: ModuleType | None = None,
  expected: str | None = None,
  output: Exception | dict | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, Exception),
    expected=expected,
    expected_check=isinstance(expected, str), )
  if type_checks != 'passed':
    return type_checks

  output = type(output).__name__
  passed = expected == output
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


def check_module(
  module: ModuleType | None = None,
  output: ModuleType | None = None,
  expected: dict | None = None,
) -> sns:
  _ = module

  if not isinstance(output, ModuleType):
    return sns(
      passed=False,
      output=f'Output is a {type(output).__name__} not a module',
      expected=expected, )

  if not isinstance(expected, dict):
    return sns(
      passed=False,
      output=f'Expected is a {type(expected).__name__} not a dict',
      expected=expected, )

  output = sns(
    location=getattr(output, '__file__', None), )
  output = output.__dict__
  passed = output == expected
  return sns(
    passed=passed,
    output=output,
    expected=expected, )


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


def check_function(
  module: ModuleType | None = None,
  output: Callable | None = None,
  expected: dict | None = None,
) -> sns:
  _ = module

  if not isinstance(output, Callable):
    return failed_type_check(
      output=output,
      output_wanted='Callable', )

  if not isinstance(expected, dict):
    return failed_type_check(
      expected=expected,
      expected_wanted='dict', )

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


def perform_type_checks(
  output: Any | None = None,
  output_check: bool | None = None,
  expected: Any | None = None,
  expected_check: bool | None = None,
) -> sns | str:
  if expected_check and output_check:
    return 'passed'

  output = [
    f'Output is of type {type(output).__name__}',
    f'Expected is of type {type(expected).__name__}', ]
  return sns(
    passed=False,
    output=output,
    expected=expected, )


def check_dataclass(
  module: ModuleType | None = None,
  output: DataClass | None = None,
  expected: dict | None = None,
) -> sns:
  _ = module

  output_check = dc.is_dataclass(output)
  expected_check = isinstance(expected, dict)
  type_checks = perform_type_checks(
    output=output,
    output_check=output_check,
    expected=expected,
    expected_check=expected_check, )
  if type_checks != 'passed':
    return type_checks

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


def check_class(
  module: ModuleType | None = None,
  output: object | None = None,
  expected: dict | None = None,
) -> sns:
  _ = module

  output_check = inspect.isclass(output) or hasattr(object, '__bases__')
  type_checks = perform_type_checks(
    output=output,
    output_check=output_check,
    expected=expected,
    expected_check=isinstance(expected, dict), )
  if type_checks != 'passed':
    return type_checks

  fields = {}
  expected_fields = expected.get('fields', {})
  for name in expected_fields:
    if hasattr(output, name):
      fields[name] = get_object.main(
        parent=output,
        name=name, )

  output = sns(name=output.__class__.__name__, fields=fields).__dict__
  passed = output == expected
  return sns(output=output, expected=expected, passed=passed)


def check_length(
  module: ModuleType | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  _ = module

  output_check = hasattr(output, '__len__')
  expected_check = isinstance(expected, int)
  type_checks = perform_type_checks(
    output=output,
    output_check=output_check,
    expected=expected,
    expected_check=expected_check, )
  if type_checks != 'passed':
    return type_checks

  passed = len(output) == expected
  return sns(
    passed=passed,
    output=len(output),
    expected=expected, )


def check_type(
  module: ModuleType | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  _ = module

  expected_check = isinstance(expected, str | list)
  type_checks = perform_type_checks(
    output=output,
    output_check=True,
    expected=expected,
    expected_check=expected_check, )
  if type_checks != 'passed':
    return type_checks

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


def check_substring_in_string(
  module: ModuleType | None = None,
  output: str | None = None,
  expected: list | str | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, str | list),
    expected=expected,
    expected_check=isinstance(expected, str | list), )
  if type_checks != 'passed':
    return type_checks

  if not isinstance(expected, list):
    expected = [expected]

  output = str(output)
  output = [str(item) for item in expected if output.find(item) != -1]
  passed = expected == output

  return sns(
    output=output,
    expected=expected,
    passed=passed, )


def check_item_in_list(
  module: ModuleType | None = None,
  output: list | tuple | None = None,
  expected: Any | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, list | tuple),
    expected=expected,
    expected_check=True, )
  if type_checks != 'passed':
    return type_checks

  if not isinstance(expected, list):
    expected = [expected]

  output = output or []
  output = [item for item in expected if item in output]
  passed = output == expected
  return sns(
    passed=passed,
    expected=expected,
    output=output, )


def check_list_contains_item(
  module: ModuleType | None = None,
  output: Any | None = None,
  expected: list | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=True,
    expected=expected,
    expected_check=isinstance(expected, list | tuple), )
  if type_checks != 'passed':
    return type_checks

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


def check_key_in_dict(
  module: ModuleType | None = None,
  output: dict | None = None,
  expected: list | str | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, dict),
    expected=expected,
    expected_check=True, )
  if type_checks != 'passed':
    return type_checks

  if not isinstance(expected, list):
    expected = [expected]

  output = [item for item in expected if item in output]
  passed = output == expected
  return sns(
    output=output,
    expected=expected,
    passed=passed, )


def check_range(
  module: ModuleType | None = None,
  output: dict | None = None,
  expected: dict | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, range),
    expected=expected,
    expected_check=isinstance(expected, dict), )
  if type_checks != 'passed':
    return type_checks

  store = {}
  for key in expected:
    store[key] = getattr(output, key, 'key/value does not exist')

  passed = store == expected
  return sns(passed=passed, output=store, expected=expected)


def check_key_value_in_dict(
  module: ModuleType | None = None,
  output: dict | None = None,
  expected: dict | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, dict),
    expected=expected,
    expected_check=isinstance(expected, dict), )
  if type_checks != 'passed':
    return type_checks

  fields = {}
  for key in expected:
    fields[key] = output.get(key, None)

  passed = expected == fields
  return sns(passed=passed, output=fields, expected=expected)


def check_thread(
  module: ModuleType | None = None,
  output: list| threading.Thread | None = None,
  expected: list | dict | None = None,
) -> sns:
  _ = module

  data = sns(**locals())

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, list | threading.Thread),
    expected=expected,
    expected_check=isinstance(expected, dict | list), )
  if type_checks != 'passed':
    return type_checks

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


def check_function_output(
  module: ModuleType | None = None,
  output: Callable | Awaitable | None = None,
  expected: Any | None = None,
) -> sns:
  _ = module

  type_checks = perform_type_checks(
    output=output,
    output_check=isinstance(output, Callable | Awaitable),
    expected=expected,
    expected_check=isinstance(expected, dict), )
  if type_checks != 'passed':
    return type_checks

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


def check_spies(
  module: ModuleType | None = None,
  output: str | None = None,
  expected: str | None = None,
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

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
