#!.venv/bin/python3
# -*- coding: utf-8 -*-


import asyncio
import dataclasses as dc
import functools
import inspect
import time
import traceback
from types import ModuleType
from typing import Any, Callable, Dict, List, ParamSpec, TypeVar

from get_config.app import main as get_config
from get_value.app import main as get_value
from logger.app import main as logger


MODULE = __file__

CONFIG = get_config(module=MODULE)
LOCALS = locals()


P = ParamSpec("P")
T = TypeVar("T")


@dc.dataclass
class Data:
  data: Any | None = None
  function: str | Callable | None = None
  module: str | ModuleType | None = None
  args: List[Any] = dc.field(default_factory=lambda: [])
  kwargs: Dict[str, Any] = dc.field(default_factory=lambda: {})
  result: Any | None = None
  exception: Exception | dict | None = None
  raise_exception: bool = False
  default_value: Any | None = None
  log_enabled: bool = False
  log_level: str = 'debug'
  call_back: Callable | dict | None = None
  standard_output: bool | None = CONFIG.environment.DEBUG
  timestamp: int | None = None


@dc.dataclass
class Data_Class:
  pass


def process_arguments(locals_: dict | None = None) -> Data:
  data = Data()

  locals_ = {} if not locals_ else locals_

  for key, value in locals_.items():
    conditions = [
      hasattr(data, key) is False,
      value is None, ]
    if True not in conditions:
      setattr(data, key, value)

  return data


def process_exception(exception: Exception) -> dict:
  traceback_ = []

  condition = isinstance(exception, Exception)
  if condition:
    traceback_ = traceback.format_exception(
      None,
      exception,
      exception.__traceback__, )

  store = []
  for item in traceback_:
    lines = item.split('\n')
    for line in lines:
      conditions = [len(line.strip()) == 0,]
      if True in conditions:
        continue
      store.append(line)
  traceback_ = store

  return {
    # 'description': exception.args[0],
    'description': str(exception),
    'name': type(exception).__name__,
    'traceback_': traceback_, }


def get_task_from_event_loop(
  task: Any | None = None
) -> Any:
  condition = inspect.iscoroutine(task)
  if condition:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
      task = loop.run_until_complete(task)
    finally:
      loop.close()
      asyncio.set_event_loop(None)

  return task


def get_awaitable_output(data: Data_Class) -> Any:
  try:
    task = data.function(*data.args, **data.kwargs)
  except Exception as e:
    task = e

  return get_task_from_event_loop(task=task)


def get_callable_output(data: Data_Class) -> Any:
  try:
    return data.function(
    *data.args,
    **data.kwargs, )
  except Exception as e:
    return e


def get_function_output(data: Data_Class) -> Data_Class:
  condition = asyncio.iscoroutinefunction(data.function)
  kind = 'awaitable' if condition else 'callable'
  handler = f'get_{kind}_output'
  handler = LOCALS.get(handler)

  try:
    data.result = handler(data=data)
  except Exception as exception:
    data.exception = process_exception(exception=exception)

    if data.default_value is not None:
      data.result = data.default_value
    elif data.raise_exception is True:
      raise exception

  return data


def process_function_output(data: Data_Class) -> Data_Class:
  if not data.call_back:
    return data

  function_ = get_value(data.call_back, 'method', )
  arguments = get_value(data.call_back, 'data', )
  arguments = {} if not arguments else arguments
  arguments.update({'result': data.result})
  data.result = function_(**arguments)
  return data


EMPTY_VALUES = [False, None, ]


def log_function_output(
  data: Data_Class | None = None,
  function: Callable | None = None,
  log_enabled: bool | None = None,
  standard_output: bool | None = None,
  args: tuple | list | None = None,
  kwargs: dict | None = None,
  exception: Any | None = None,
  log_level: str | None = None,
  result: Any | None = None
) -> bool:
  if log_enabled in EMPTY_VALUES:
    return False

  log = {
    'function': function.__name__,
    'module': function.__module__, }

  LOG_FIELDS = ['args', 'kwargs', 'result', 'exception']
  for field in LOG_FIELDS:
    log[field] = get_value(locals(), field)

  log_level = 'exception' if exception else log_level

  task = logger(
    level=log_level,
    standard_output=standard_output,
    data=log, )
  get_task_from_event_loop(task=task)

  return True


def get_function_parameters(
  function: str | None = None,
) -> List[str]:
  parameters = list(inspect.signature(function).parameters)
  return [] or parameters


def main(
  raise_exception: bool | None = None,
  default_value: Any | None = None,
  # trunk-ignore(ruff/ARG001)
  log_enabled: bool | None = None,
  # trunk-ignore(ruff/ARG001)
  log_level: str | None = None,
  # trunk-ignore(ruff/ARG001)
  call_back: Callable | dict | None = None,
  timestamp: int | None = None,
  # trunk-ignore(ruff/ARG001)
  standard_output: bool | None = None,
) -> Any:
  timestamp = int(time.time()) if not timestamp else timestamp

  def error_handler(function: Callable[P, T]) -> Callable[P, T]:
    @functools.wraps(function)
    def wrapper(
      *args: P.args,
      **kwargs: P.kwargs,
    ) -> T:
      data = process_arguments(locals_=locals())

      data.function = function
      # data.args = args
      # data.kwargs = kwargs
      data.raise_exception = raise_exception
      data.default_value = default_value
      data.timestamp = timestamp
      # data.call_back = call_back
      # data.standard_output = standard_output

      data = get_function_output(data=data)
      data = process_function_output(data=data)

      log_function_output(
        data=data,
        kwargs=data.kwargs,
        args=data.args,
        result=data.result,
        exception=data.exception,
        log_level=data.log_level,
        standard_output=data.standard_output,
        log_enabled=data.log_enabled, )

      return data.result
    return wrapper
  return error_handler


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
