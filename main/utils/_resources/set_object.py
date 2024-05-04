#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns


MODULE = __file__


def list_sns_to_list_dict(data: list | None = None) -> list | None:
  if not isinstance(data, list):
    return data

  def convert(item: sns) -> dict:
    if hasattr(item.value, '__dict__'):
      item.value = item.value.__dict__
    return item.__dict__

  data = [convert(item=item) for item in data]
  return data


def list_dict_to_list_sns(data: list | None = None) -> list | None:
  if not isinstance(data, list):
    return data

  data = [sns(**item) for item in data]
  return data


def dict_to_sns(data: dict | None = None) -> sns | None:
  if not isinstance(data, dict):
    data = sns(**data)

  return data


def set_child_in_parent_cast_arguments(
  arguments: dict | None = None,
) -> dict:
  for key, value in arguments.items():
    if isinstance(value, dict):
      arguments[key] = sns(**value)

  return arguments


def reset_route_values_cast_arguments(
  data: list | None = None,
) -> list | None:
  if not isinstance(data, list):
    return data

  return [sns(**item) for item in data]



def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True, resources_folder_name='_resources')


if __name__ == '__main__':
  examples()
