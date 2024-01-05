#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
from typing import Any, Callable

from get_config.app import main as get_config
from utils import app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources',
)

CONFIG = get_config(module=PARENT_MODULE)
LOCALS = locals()


class Data:
  pass


def add(a: int, b: int) -> int:
  return a + b


def get_dataclass(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> Any:
  data = Data()
  data.function = add
  data.kwargs = {'a': 1, 'b': 1}
  return data


def exception_resource(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> Any:
  try:
    sum([1, '1'])
  except Exception as e:
    return e


async def awaitable_function(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'awaitable_output'


def callable_function(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'callable_output'


def function_exception(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> None:
  raise RuntimeError()


def function_resource(
  data: Any | None = None,
  function: str | None = None,
) -> Any:
  function_ = function
  key = 'function'

  if isinstance(function_, str):
    return LOCALS[function_]

  if dc.is_dataclass(data):
    function_ = getattr(data, key)
    data.function = LOCALS.get(function_, None)
    return data

  if isinstance(data, dict):
    function_ = data.get(key, '')
    function_ = LOCALS.get(function_, None)
    data.update({key: function_})
    return data


def log_function_output_resource(
  data: dict | None = None,
) -> dict:
  key = 'function'
  function_ = data.get(key, '')
  function_ = str(function_)
  data[key] = LOCALS.get(function_, '')
  return data


def get_function_parameters_resource(
  data: dict | None = None,
) -> dict:
  key = 'function'
  function_ = data.get(key, None)
  function_ = str(function_)
  data[key] = LOCALS.get(function_, None)
  return data


def set_coroutine_flag_resource(
  data: dict | None = None,
) -> dict:
  key = 'function'
  function_ = data.get(key, None)
  function_ = str(function_)
  data[key] = LOCALS.get(function_, None)
  return data


def hello_world(result: str) -> str:
  return f'Hello {result}'


def call_back_resource(data: Any) -> Any:
  if data.call_back is None:
    return data

  data.call_back = {
    'method': hello_world,
    'data': {},
  }
  return data


def sync_function() -> str:
  return 'sync_output'


async def async_function() -> str:
  return 'async_output'


def sync_exception() -> str:
  return 'string'.value


async def async_exception() -> str:
  return 'string'.value


def main_resource(
  error_handler_: Callable,
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> Any:
  return dict(
    sync_function=error_handler_(function=sync_function)(),
    async_function=error_handler_(function=async_function)(),
    sync_exception=error_handler_(function=sync_exception)(),
    async_exception=error_handler_(function=async_exception)(),
  )


def task_resource(
  # trunk-ignore(ruff/ARG001)
  task: Any | None = None,
) -> str:
  return 'async_task'


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
