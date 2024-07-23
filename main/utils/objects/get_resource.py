#!.venv/bin/python3
# -*- coding: utf-8 -*-


import builtins
from types import ModuleType
from types import SimpleNamespace as sns


PARENT = 'PARENT'


def parent_to_sns(parent: dict | None = None) -> sns:
  return sns(**parent)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    module_filename='get',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
