#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
import dataclasses as dc

from typing import Any, Callable

from get_config.app import main as get_config


MODULE = __file__
PARENT_MODULE = os.path.dirname(MODULE)
PARENT_MODULE = os.path.dirname(PARENT_MODULE)
PARENT_MODULE = os.path.join(PARENT_MODULE, 'app.py')
CONFIG = get_config(module=PARENT_MODULE)
LOCALS = locals()


class Data:
  pass


def add(a: int, b: int) -> int:
  return a + b


def get_dataclass(*args, **kwargs) -> Any:
  data = Data()
  data.function = add
  data.kwargs = {'a': 1, 'b': 1}
  return data


def exception_resource(*args, **kwargs) -> Any:
  try:
    c = 1 + '1'
  except Exception as e:
    return e


async def awaitable_function(*args, **kwargs) -> str:
  return 'awaitable_output'


def callable_function(*args, **kwargs) -> str:
  return 'callable_output'


def function_exception(*args, **kwargs) -> None:
  raise RuntimeException()
  

def function_resource(
  data: Any | None = None,
  function: str | None = None,
) -> Any:
  if function:
    return LOCALS[function]
  
  if dc.is_dataclass(data):
    function = getattr(data, 'function')
    data.function = LOCALS.get(function, None)
    return data

  
  if isinstance(data, dict):
    function = data.get('function', '')
    function = LOCALS.get(function, None)
    data.update({'function': function})
    return data


def log_function_output_resource(
  data: dict | None = None,
) -> dict:
  function = data.get('function', '')
  function = str(function)
  data['function'] = LOCALS.get(function, '')
  return data


def get_function_parameters_resource(
  data: dict | None = None,
) -> dict:
  function = data.get('function', None)
  function = str(function)
  data['function'] = LOCALS.get(function, None)
  return data


def set_coroutine_flag_resource(
  data: dict | None = None,
) -> dict:
  function = data.get('function', None)
  function = str(function)
  data['function'] = LOCALS.get(function, None)
  return data


def hello_world(result: str) -> str:
  return f'Hello {result}'


def call_back_resource(data: Any) -> Any:
  if data.call_back is None:
    return data

  method = data.call_back = {
    'method': hello_world,
    'data': {}, }
  return data


def sync_function() -> str:
  return 'sync_output'


async def async_function() -> str:
  return 'async_output'


def sync_function_exception() -> str:
  return 'string'.value


async def async_function_exception() -> str:
  return 'string'.value


def main_resource(error_handler_: dict, *args, **kwargs, ) -> Any:
  return dict(
    sync_function=error_handler_(function=sync_function)(),
    async_function=error_handler_(function=async_function)(),
    sync_function_exception=error_handler_(function=sync_function_exception)(),
    async_function_exception=error_handler_(function=async_function_exception)(), )


def task_resource(task: Any) -> str:
  return 'async_task'

  
def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  project_directory = PARENT_MODULE
  # project_directory = 'main'
  invoke_pytest(project_directory=project_directory)


if __name__ == '__main__':
  example()