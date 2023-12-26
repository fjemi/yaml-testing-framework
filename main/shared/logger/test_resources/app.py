#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import sys
import typing
import types
import os

import logger.test_resources.module as module

from get_config.app import main as get_config
import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources', )

SCHEMA = os.path.dirname(os.path.dirname(MODULE)) + 'app.yaml'
CONFIG = get_config(module=PARENT_MODULE)
LOCALS = locals()


class Data:
  ...


class Test:
  ...


@dc.dataclass
class Test_Data:
  a: int = 0
  b: int = 0


def data_class_resource() -> Data:
  return Test_Data()


def function(data: None = None) -> int:
  return 1


def get_dataclass(*arg, **kwargs) -> Data:
  data = CONFIG.schema.Data()
  data.data = CONFIG.schema.Data()
  data.timestamp = 'timestamp'
  return data


def module_resource(module: str) -> types.ModuleType:
  return LOCALS[module]


def set_default_resource(object: str) -> typing.Any:
  if object == 'module':
    return module

  if object == 'function':
    return function

  if object == 'Test':
    test = Test()
    test.module = module
    test.function = function
    return test

  if object == 'Exception':
    try:
      a = sum(['0', 0])
    except Exception as e:
      return e


def task_resource(task: str) -> typing.Any:
  kind = type(task).__name__.lower()
  if kind == 'str':
    task = LOCALS[task]
    return task()
  if kind == 'nonetype':
    return task


def sync_function() -> str:
  return 'sync_output'


async def async_function() -> str:
  return 'async_output'


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()