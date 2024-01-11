#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
from types import ModuleType
from typing import Any, List

from error_handler.app import main as error_handler
from get_config.app import main as get_config
from get_object.app import main as get_object
from process_casts.app import process_casts_for_output
from utils import app as utils


MODULE = __file__
CONFIG = get_config(module=MODULE)

LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


@error_handler()
async def pass_through(
  output: Any | None = None,
) -> Data_Class:
  # global variable accessible by timestamp and number of elements
  # save method name there
  return {
    'passed': False,
    'output': f"assertion method {output} doesn't exist",
    'expected': '',
  }


@error_handler()
async def get_current_assertion(
  i: int | None = None,
  assertions: list | None = None,
  output: Any | None = None,
  exception: Exception | dict | None = None,
) -> dict:
  i = i or 0
  assertion = CONFIG.schema.Assertion(
    **assertions[i],
    exception=exception,
    output=output,
  )
  return {
    'i': i,
    'assertion': assertion,
  }


@error_handler()
async def get_assertion_method(
  assertion: Data_Class | None = None,
  module: ModuleType | None = None,
) -> dict:
  assertion.method_name = assertion.method
  assertion.method = get_object(
    parent=module,
    name=assertion.method,
  )
  if not assertion.method:
    assertion.method = pass_through
    assertion.output = assertion.method_name
  return {'assertion': assertion}


@error_handler()
async def verify_expected_output(
  assertion: Data_Class | None = None,
) -> dict:
  parameters = utils.get_function_parameters(function=assertion.method)
  arguments = {}

  for key in parameters:
    value = getattr(assertion, key, None)
    arguments[key] = value

  result = assertion.method(**arguments)
  assertion.method = assertion.method_name
  for key, value in result.items():
    setattr(assertion, key, value)

  return {'assertion': assertion}


@error_handler()
async def update_assertions_and_increment_i(
  i: int | None = None,
  assertion: Data_Class | None = None,
  assertions: list | None = None,
) -> dict:
  assertions[i] = assertion
  i = i + 1
  return {
    'i': i,
    'assertions': assertions,
  }


@error_handler()
async def get_assertion_output_field(
  assertion: Data_Class | None = None,
) -> dict:
  assertion.output = get_object(
    parent=assertion.output,
    name=assertion.field,
  )
  return {'assertion': assertion}


@error_handler()
async def get_casted_assertion_output(
  assertion: dict | None = None,
  module: ModuleType | None = None,
) -> dict:
  assertion.cast_output = assertion.cast_output or []

  key = 'output'
  casted_output = process_casts_for_output(
    output=assertion.output,
    cast_output=assertion.cast_output,
    module=module,
  )
  assertion.output = casted_output.get(key, assertion.output)

  return {'assertion': assertion}


@error_handler()
async def main(
  assertions: List[dict] | None = None,
  output: Any | None = None,
  exception: str | None = None,
  module: ModuleType | None = None,
) -> dict:
  assertions = assertions or []
  n = range(len(assertions))

  data = utils.process_arguments(
    locals=locals(),
    data_class=CONFIG.schema.Data,
  )
  data = utils.process_operations(
    data=data,
    functions=LOCALS,
    n=n,
    operations=CONFIG.operations,
  )

  return {'assertions': assertions}


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
