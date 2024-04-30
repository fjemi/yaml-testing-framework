#!.venv/bin/python3
# -*- coding: utf-8 -*-

# trunk-ignore(ruff/F401)
import builtins
from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import get_module


MODULE = __file__


def parent_to_sns(parent: dict | None = None) -> sns:
  return sns(**parent)


def get_module_wrapper(parent: str | None = None) -> ModuleType:
  return get_module.main(location=parent, pool=False)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
