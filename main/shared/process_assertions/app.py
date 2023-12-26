#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any, List

from error_handler.app import main as error_handler
from get_config.app import main as get_config
from get_object.app import main as get_object
from utils import app as utils


MODULE = __file__
CONFIG = get_config(module=MODULE)

LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


@error_handler()
async def assert_equals(assertion: Data_Class) -> Data_Class:
  assertion.passed = assertion.actual == assertion.expected
  return assertion


@error_handler()
async def assert_str_contains(assertion: Data_Class) -> Data_Class:
  index = str(assertion.actual).find(str(assertion.expected))
  return {
    'string': assertion.actual,
    'substring': assertion.expected,
    'index': index, }


@error_handler()
async def assert_list_contains(assertion: Data_Class) -> Data_Class:
  index = -1
  if assertion.expected in assertion.actual:
      index = assertion.actual.index(assertion.expected)
  return {
    'list': assertion.actual,
    'element': assertion.expected,
    'index': index, }


@error_handler()
async def assert_dict_contains(assertion: Data_Class) -> Data_Class:
  index = 0

  for key, value in assertion.expected.items():
    if key not in assertion.actual:
      index = -1
      break

    actual_value = assertion.actual.get(key)
    if actual_value != value:
      index = -1
      break

  return {
    'dict': assertion.actual,
    'key_value': assertion.expected,
    'index': index, }


# @error_handler()
async def assert_any_contains(assertion: Data_Class) -> Data_Class:
  raise RuntimeError(f'{assertion.actual} has not element {assertion.expected}')


CONTAINS_KINDS = ['list', 'dict', 'tuple', 'str', ]


@error_handler()
async def assert_contains(assertion: Data_Class) -> Data_Class:
  kind = type(assertion.actual).__name__.lower()
  kind = 'list' if kind == 'tuple' else kind
  kind = kind if kind in CONTAINS_KINDS else 'any'
  handler = f'assert_{kind}_contains'
  handler = LOCALS[handler]
  assertion.expected = handler(assertion=assertion)

  assertion.actual = None
  if assertion.expected.get('index', -1) != -1:
    assertion.actual = assertion.expected

  assertion.passed = assertion.actual == assertion.expected
  return assertion


@error_handler()
async def assert_type(assertion: Data_Class) -> Data_Class:
  if isinstance(assertion.expected, list) is False:
    assertion.expected = [assertion.expected]

  assertion.actual = [
    str(assertion.actual.__class__),
    assertion.actual.__class__.__name__, ]

  for value in assertion.expected:
    for type_ in assertion.actual:
      assertion.passed = type_.find(value) > -1
      if assertion.passed is True:
        assertion.expected = type_
        assertion.actual = type_
        return assertion

  assertion.passed = False
  return assertion


@error_handler()
async def assert_length(assertion: Data_Class) -> Data_Class:
  if assertion.actual is None:
    assertion.actual = []

  assertion.actual = len(assertion.actual)
  assertion.passed = assertion.actual == assertion.expected
  return assertion


@error_handler()
async def assert_catch(assertion: Data_Class) -> Data_Class | None:
  if isinstance(assertion.exception, Exception):
    assertion.exception = {'name': assertion.exception.__class__.__name__}

  assertion.actual = assertion.exception.get('name')
  assertion.passed = assertion.actual.find(assertion.expected) > -1
  return assertion


@error_handler()
async def pass_through(assertion: Data_Class) -> Data_Class:
  if assertion in CONFIG.empty_values:
    return CONFIG.schema.Assertion(
      actual=True,
      expected=False,
      passed=False, )
  assertion.passed = False
  assertion.actual = not assertion.expected
  return assertion


@error_handler()
async def main(
  assertions: List[dict | Data_Class] | None = None,
  output: Any | None = None,
  exception: Any | None = None,
) -> dict:
  assertions = assertions or []
  n = range(len(assertions))

  data = utils.process_arguments(
    locals=locals(),
    data_class=CONFIG.schema.Data, )
  data = utils.process_operations(
    data=data,
    functions=LOCALS,
    n=n,
    operations=CONFIG.operations, )
  # operations = CONFIG.schema.Operations

  # for i in n:
  # for operation in CONFIG.operations:
  #   operations.function = LOCALS[operation]
  # from utils import app as utils
  #   operations.parameters = utils.get_function_parameters(
  #     function=operations.function)

  # for i in data.n:
  for i in n:
    if isinstance(assertions[i], dict) is True:
      data_class = CONFIG.schema.Assertion
      assertions[i] = data_class(
        **assertions[i],
        actual=output,
        exception=exception, )
    assertions[i].actual = get_object(
      parent=assertions[i].actual,
      name=assertions[i].field, )
    # for assertion in assertion.casts:
    #   assertion.actual = cast_value(
    #     object=assertion.actual,
    #     unpack=assertion.cast['unpack'],
    #     caster_name=assertion.cast['caster_name'], )
    handler = f'assert_{assertions[i].method}'
    handler = LOCALS.get(
      handler,
      pass_through, )
    assertions[i] = handler(assertion=assertions[i])

  return {
    'output': None,
    'exception': None,
    'assertions': assertions, }


@error_handler()
async def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
