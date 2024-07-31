#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any


LOCALS = locals()


def get_resource(resource: str | None = None) -> Any:
  return LOCALS.get(resource, None)


def add(data: dict) -> int:
  return sum(list(data.values()))


def multiply(a: int, b: int) -> int:
  return a * b


def list_dict_to_list_sns(data: list) -> list:
  if not isinstance(data, list):
    return data

  return [sns(**item) for item in data]


def list_sns_to_list_dict(output: list) -> list:

  def caster(item: sns) -> dict:
    if isinstance(item.output, Exception):
      item.output = type(item.output).__name__
    return item.__dict__

  return [caster(item=item) for item in output]


async def subtract(data: dict) -> int:
  return data['b'] - data['a']


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.main.app')


if __name__ == '__main__':
  examples()
