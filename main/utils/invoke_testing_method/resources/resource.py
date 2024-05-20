#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
from types import SimpleNamespace as sns


MODULE = __file__


def sns_to_dict(item: sns) -> dict:
  if hasattr(item, '__dict__'):
    item = item.__dict__
  return item


def list_sns_to_list_dict(result: list | None = None) -> list | None:
  if not isinstance(result, list):
    return result

  return [item.__dict__ for item in result]


def examples() -> None:
  from main.utils import invoke_testing_method

  location = os.path.dirname(MODULE)
  location = os.path.dirname(location)
  invoke_testing_method.main(location=location)


if __name__ == '__main__':
  examples()
