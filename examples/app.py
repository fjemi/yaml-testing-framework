#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any


LOCALS = locals()

CONSTANT = 0


def main(
  a: int | float | None = None,
  b: int | float | None = None,
  n: int | None = None,
  method: str | None = None,
) -> sns:
  _locals = locals()
  data = sns()
  for key, value in _locals.items():
    if value is None:
      continue
    setattr(data, key, value)
  method = LOCALS.get(method, do_nothing)
  return method(data=data)


def do_nothing(data: Any | None = None) -> sns:
  if isinstance(data, sns):
    data.result = 'Method does not exist'
  return data


def add(data: sns | None = None) -> sns:
  data.result = data.a + data.b
  return data


def subtract(data: sns | None = None) -> sns:
  data.result = data.a - data.b
  return data


def multiply(data: sns) -> sns:
  data.result = 0
  for i in range(data.a):
    temp = sns(a=data.result, b=data.b)
    data.result = add(temp).result
  return data


def constant(data: sns | None = None) -> sns:
  data.result = CONSTANT
  return data


def factorial(data: sns | None = None) -> sns:
  data.result = 1
  if data.a == 0:
    return data

  for i in range(data.a):
    data.result = data.result * (i + 1)

  return data


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
