#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns

from main.utils import invoke_testing_method


def get_ids_resource(val: dict | None = None) -> sns:
  val = val or {}
  return sns(**val)


def examples() -> None:
  invoke_testing_method.main(
    resource_flag=True,
    resources_folder_name='resources',
    module_filename='test_entrypoint', )


if __name__ == '__main__':
  examples()
