#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any


def sns_to_dict(data: sns | list | None = None) -> dict | list | None:
  if hasattr(data, '__dict__'):
    return data.__dict__

  if isinstance(data, list):
    data = [item.__dict__ for item in data]
    return data

  if isinstance(data, dict):
    for key, value in data.items():
      data[key] = value.__dict__
    return data


def dict_dict_to_dict_sns(data: Any | None = None) -> Any:
  for key, value in data.items():
    data[key] = sns(**value)
  return data


def examples() -> None:
  from main.utils import invoke

  invoke.main(
    resources_folder_name='resources',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
