#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns


MODULE = __file__


def sns_to_dict(data: sns | list | None = None) -> dict | list | None:
  if isinstance(data, sns):
    return data.__dict__

  if isinstance(data, list):
    data = [item.__dict__ for item in data]
    return data

  if isinstance(data, dict):
    for key, value in data.items():
      data[key] = value.__dict__
    return data


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
