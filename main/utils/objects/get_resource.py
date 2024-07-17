#!.venv/bin/python3
# -*- coding: utf-8 -*-


import builtins
from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import get_module


RESOURCE_PATH = __file__


def parent_to_sns(parent: dict | None = None) -> sns:
  return sns(**parent)


def wrapper_get_module(parent: str | None = None) -> ModuleType:
  return get_module.main(location=parent).module


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    module_filename='app',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
