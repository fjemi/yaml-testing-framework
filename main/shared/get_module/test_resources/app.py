#!.venv/bin/python3
# -*- coding: utf-8 -*-

import asyncio
import sys

from logger.app import main as logger


THIS_MODULE_NAME = __name__
THIS_MODULE_LOCATION = __file__


def print_hello_world(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  data = "Hello World"
  asyncio.run(logger(
    data_=data,
    standard_output=True,
  ))


def get__pool(_pool=None) -> dict:
  return {THIS_MODULE_LOCATION: sys.modules[THIS_MODULE_NAME]}
