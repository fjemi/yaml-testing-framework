#!/usr/bin/env python3

import copy
import dataclasses as dc
from typing import Any

from app.shared.format_main_arguments import app as format_main_arguments


@dc.dataclass
class Body:
  assertion: dict | None = None
  result: Any | None = None
  text: str | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  result: Any | None = None
  passed: bool = False
  call_method: str = "module"


async def assert_equals(data: Data) -> Data:
  value = data.body.assertion.get("equals")

  if data.body.result == value:
    data.passed = True

  if data.body.result != value:
    data.passed = False
  data.result = {'equals': data.body.result}

  return data


async def assert_type(data: Data) -> Data:
  result_type = type(data.body.result).__name__
  assertion_type = data.body.assertion.get("type")

  types = copy.deepcopy(assertion_type)
  if not isinstance(types, list):
    types = [types]

  if result_type in types:
    data.passed = True
    data.result = {"type": assertion_type}
  if result_type not in types:
    data.passed = False
    data.result = {"type": result_type}

  return data


async def assert_has_attributes(data: Data) -> Data:
  has_attributes = data.body.assertion.get("has_attributes")

  data.passed = []
  data.result = {}

  for key, value in has_attributes.items():
    assert_value = None
    if hasattr(data.body.result, key):
      assert_value = getattr(data.body.result, key)
    data.result[key] = assert_value

    if value == assert_value:
      data.passed.append(True)
    if value != assert_value:
      data.passed.append(False)

  data.result = {"has_attributes": data.result}
  return data


async def assert_has_keys(data: Data) -> Data:
  has_keys = data.body.assertion.get("has_keys")

  data.passed = []
  data.result = {}

  for key, value in has_keys.items():
    assert_value = data.body.result.get(key)
    data.result[key] = assert_value

    if value == assert_value:
      data.passed.append(True)
    if value != assert_value:
      data.passed.append(False)

  data.result = {"has_keys": data.result}
  return data


async def assert_length(data: Data) -> Data:
  data.result = {'length': len(data.body.result)}
  return data


ASSERTIONS = {
  "equals": assert_equals,
  "type": assert_type,
  "has_attributes": assert_has_attributes,
  "has_keys": assert_has_keys,
  'length': assert_length,
}


# ruff: noqa: ARG001
async def main(
  assertion: dict | None = None,
  result: Any | None = None,
  text: str | None = None,
) -> Any:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  cases = list(data.body.assertion.keys())[0]
  switcher = ASSERTIONS[cases]
  data = await switcher(data=data)
  return data


async def example() -> None:
  tests = [
    """
    assertion:
      equals: test
    result: test
    """,
    """
    assertion:
      type: str
    result: test
    """,
    """
    assertion:
      has_keys:
        test: test
    result:
      test: test
    """,
  ]
  for text in tests:
    result = await main(text=text)
    print(result)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
