#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns


def paths_cast_arguments(paths: dict | None = None) -> sns:
  return sns(**paths)


def list_dict_to_list_sns(locations: list | None = None) -> list | None:
  if not isinstance(locations, list):
    return locations

  locations = [sns(**item) for item in locations]
  return locations


def list_sns_to_list_dict(locations: list | None = None) -> list | None:

  def cast(item: sns) -> dict:
    item = item.__dict__
    key = 'extensions'
    if key in item:
      item[key] = item[key].__dict__
    return item

  return [cast(item=item) for item in locations]


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
