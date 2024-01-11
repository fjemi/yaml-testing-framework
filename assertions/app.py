#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
from typing import Any


MODULE = __file__


@dc.dataclass
class Data_Class:
  pass


def assert_exception(
  expected: str | None = None,
  exception: str | None = None,
) -> dict:
  exception = exception or {}

  if isinstance(exception, Exception):
    exception = exception.__class__.__name__
  elif isinstance(exception, dict):
    exception = exception.get('name', None)

  passed = expected == exception
  return {
    'passed': passed,
    'expected': expected,
    'output': exception,
  }


def assert_equals(
  output: Any | None = None,
  expected: Any | None = None,
) -> dict:
  passed = output == expected
  return {
    'passed': passed,
    'expected': expected,
    'output': output,
  }


def assert_length(
  output: Any | None = None,
  expected: Any | None = None,
) -> dict:
  output = len(output)
  passed = output == expected
  return {
    'passed': passed,
    'output': output,
    'expected': expected,
  }


def assert_type(
  output: Any | None = None,
  expected: Any | None = None,
) -> dict:
  passed = False

  if not isinstance(expected, list):
    expected = [expected]
  output_types = [
    type(output).__name__,
    str(output.__class__),
  ]
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

  return {
    'passed': passed,
    'output': output,
    'expected': expected,
  }


def assert_substring_in_string(
  output: str | None = None,
  expected: list | str | None = None,
) -> dict:
  store = []
  passed = True
  output = str(output)

  if not isinstance(expected, list):
    expected = [expected]

  for item in expected:
    string = str(item)
    index = output.find(string)

    if index != -1:
      store.append(string)

  output = store
  passed = expected == output
  return {
    'passed': passed,
    'output': store,
    'expected': expected,
  }


def assert_list_contains_item(
  output: Any | None = None,
  expected: list | None = None,
) -> dict:
  store = []

  if not isinstance(output, list):
    output = [output]

  for item in output:
    if item in expected:
      store.append(item)

  expected = store
  passed = expected == output
  return {
    'passed': passed,
    'expected': expected,
    'output': output,
  }


def assert_item_in_list(
  output: list | tuple | None = None,
  expected: Any | None = None,
) -> dict:
  store = []
  passed = True
  output = output or []

  if not isinstance(expected, list):
    expected = [expected]

  for item in expected:
    if item in output:
      store.append(item)

  output = store
  passed = output == expected
  return {
    'passed': passed,
    'expected': expected,
    'output': output,
  }


def assert_key_in_dict(
  output: dict | None = None,
  expected: list | str | None = None,
) -> dict:
  expected = expected or []

  if not isinstance(expected, list):
    expected = [expected]

  store = []

  for key in expected:
    if key in output:
      store.append(key)

  output = store
  passed = output == expected
  return {
    'passed': passed,
    'output': output,
    'expected': expected,
  }


def assert_key_value_in_dict(
  output: dict | None = None,
  expected: dict | None = None,
) -> dict:
  store = {}

  for key, value in expected.items():
    output_value = output.get(key, None)

    if value == output_value:
      store.update({key: value})

  output = store
  passed = output == expected
  return {
    'passed': passed,
    'output': output,
    'expected': expected,
  }


def example() -> None:
  from main.shared.invoke_pytest import app as invoke_pytest

  invoke_pytest.main(project_directory=MODULE)


if __name__ == '__main__':
  example()
