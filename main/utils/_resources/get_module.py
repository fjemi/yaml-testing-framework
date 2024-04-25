#!.venv/bin/python3
# -*- coding: utf-8 -*-

import sys
from types import SimpleNamespace as sns

from utils import logger


THIS_MODULE_NAME = __name__
THIS_MODULE_LOCATION = __file__


def print_hello_world(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> None:
  log = sns(
    message='Hello World',
    standard_output=True,
    enabled=True, )
  logger(log=log)


def get__pool(_pool=None) -> dict:
  return {THIS_MODULE_LOCATION: sys.modules[THIS_MODULE_NAME]}
