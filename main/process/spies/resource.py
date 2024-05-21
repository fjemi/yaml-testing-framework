#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import get_module


MODULE = __file__
LOCALS = locals()


def get_module_wrapper(module: str) -> ModuleType:
  module = get_module.main(location=module, pool=False)
  if isinstance(module, ModuleType):
    module.SPIES = getattr(module, 'SPIES', None) or {}
  return module


def dict_sns_to_dict_dict(output: dict) -> dict:
  for key, value in output.items():
    output[key] = value.__dict__
  return output


def add(a: int, b: int) -> int:
  return a + b


def subtract(a: int, b: int) -> int:
  return a - b


def call_spy(output: sns) -> dict:
  module = output.module
  _ = module.add(a=1, b=1)
  return dict_sns_to_dict_dict(output=module.SPIES)


def examples() -> None:
  import os

  from main.utils import invoke_testing_method

  location = os.path.dirname(MODULE)
  invoke_testing_method.main(location=location)


if __name__ == '__main__':
  examples()
