#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns


def paths_cast_arguments(paths: dict | None = None) -> sns:
  return sns(**paths)


def list_dict_to_list_sns(
  locations: list | None = None,
  paths: list | None = None,
) -> list | None:
  locations = locations or paths

  if not isinstance(locations, list):
    return locations

  locations = [sns(**item) for item in locations]
  return locations


def list_sns_to_list_dict(
  locations: list | None = None,
  paths: list | None = None,
) -> list | None:
  locations = locations or paths

  if not isinstance(locations, list):
    return locations

  locations = [item.__dict__ for item in locations]
  return locations


def list_nested_sns_to_list_nested_dict(
  locations: list | None = None,
  paths: list | None = None,
) -> list | None:
  locations = locations or paths or []
  store = []

  for item in locations:
    temp = item.__dict__

    for key, value in temp.items():
      flag = hasattr(value, '__dict__')
      temp[key] = value if not flag else getattr(value, '__dict__')
    
    store.append(temp)

  return store


def list_nested_dict_to_list_nested_sns(
  paths: dict | None = None
) -> sns:
  for i, item in enumerate(paths):
    for key, value in item.items():
      item[key] = sns(**value)
    paths[i] = sns(**item)
  return paths


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.main/process/locations/app.py')


if __name__ == '__main__':
  examples()
