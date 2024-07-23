#!.venv/bin/python3
# -*- coding: utf-8 -*-


import sys
from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import logger


THIS_MODULE_NAME = __name__
THIS_MODULE_LOCATION = __file__


def print_hello_world(*args, **kwargs) -> None:
  _ = args, kwargs
  logger.main(
    message='Hello World',
    standard_output=True,
    enabled=True, )


def get__pool(_pool=None) -> dict:
  return {THIS_MODULE_LOCATION: sys.modules[THIS_MODULE_NAME]}


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True, module_filename='app')


if __name__ == '__main__':
  examples()
