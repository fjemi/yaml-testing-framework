#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns


def sns_to_dict(item: sns) -> dict:
  if hasattr(item, '__dict__'):
    item = item.__dict__
  return item


def list_sns_to_list_dict(result: list | None = None) -> list | None:
  if not isinstance(result, list):
    return result

  return [item.__dict__ for item in result]


def examples() -> None:
  from main.utils import invoke

  invoke.main(
    resources_folder_name='resources',
    module_filename='app', )


if __name__ == '__main__':
  examples()
