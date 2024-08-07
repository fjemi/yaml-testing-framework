#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import ModuleType
from types import SimpleNamespace as sns
from typing import Callable


LOCALS = locals()


def dict_sns_to_dict_dict(output: dict) -> dict:
  for key, value in output.items():
    output[key] = value.__dict__
  return output


def add(a: int, b: int) -> int:
  return a + b


def subtract(a: int, b: int) -> int:
  return a - b


def call_spy(
  output: ModuleType | Callable | None = None,
) -> None:
  if isinstance(output, ModuleType):
    output = output.add
  if isinstance(output, Callable):
    _ = output(a=1, b=1)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    module_filename='app',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
