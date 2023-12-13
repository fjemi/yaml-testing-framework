#!/usr/bin/env python

import dataclasses as dc
import os
import os as patch_os


@dc.dataclass
class Data:
  a: int = 0
  result: int = 0


def get_input(data: str | None = None) -> str:
  """Get input"""
  if data is None:
    data = ""
  return input(data)


def use_get_input(data: str | None = None) -> str:
  if data is None:
    data = ""
  return get_input(data=data)


def foo(data: None = None) -> str:
  return "foo"


def bar(data: "None" = None) -> str:
  return bar


def use_foo(data: None = None) -> str:
  return foo()


def add(a: int, b: int) -> int:
  return a + b


def use_add(data: None = None) -> int:
  a = 0
  b = 0
  return add(a, b)


def subtract(a: int, b: int) -> int:
  return b - a


def absolute_value(data: Data) -> Data:
  data.result = data.a
  if data.result < 0:
    data.result = data.result * -1
  return data


dictionary_module = {
  "add": add,
  "subtract": subtract,
  "foo": foo,
  "test2": {
    "test1": "test"
  },
}

variable_1 = 1
variable_2 = "a"
