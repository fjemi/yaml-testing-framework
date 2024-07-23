#!.venv/bin/python3
# -*- coding: utf-8 -*-


import asyncio
import inspect
from types import SimpleNamespace as sns
from typing import Any, Callable, Mapping

from main.utils import logger


def main(
  arguments: Any | None = None,
  method: Callable | None = None,
  function: Callable | None = None,
) -> sns:
  method = method or function
  handlers = get_handlers(arguments=arguments)
  return call_handlers(
    method=method,
    handlers=handlers,
    arguments=arguments, )


def is_coroutine(object: Any | None = None) -> bool:
  return True in [
    inspect.iscoroutinefunction(obj=object),
    inspect.iscoroutine(object=object),
    inspect.isawaitable(object=object),
  ]


def get_task_from_event_loop(task: Any | None = None) -> Any:
  if is_coroutine(object=task) and not isinstance(task, Callable):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
      task = loop.run_until_complete(task)
    finally:
      loop.close()
      asyncio.set_event_loop(None)

  return task


def caller_wrapper(method: Callable) -> Callable:

  def caller_wrapper_inner(*args, **kwargs) -> sns:
    output = None
    exception = None

    try:
      output = method(*args, **kwargs)
    except Exception as error:
      arguments = kwargs or list(args)
      logger.main(error=error, arguments=arguments)
      output = error

    output = get_task_from_event_loop(task=output)
    if isinstance(output, Exception):
      exception = output

    return sns(output=output, exception=exception)

  caller_wrapper_inner.__wrapped__ = method
  return caller_wrapper_inner


@caller_wrapper
def unpack_mapping(
  arguments: Any,
  method: Callable,
) -> sns:
  return method(**arguments)


@caller_wrapper
def unpack_list(
  arguments: Any,
  method: Callable,
) -> sns:
  return method(*arguments)


@caller_wrapper
def pack_any(
  arguments: Any,
  method: Callable,
) -> sns:
  return method(arguments)


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def get_handlers(arguments: Any) -> list:
  calls = []
  if isinstance(arguments, Mapping):
    calls.append(unpack_mapping)
  elif isinstance(arguments, list | tuple) or arguments is None:
    calls.append(unpack_list)
  calls.append(pack_any)
  return calls


def call_handlers(
  arguments: dict = {},
  handlers: list = [],
  method: Callable | None = None,
) -> sns:
  results = []

  for item in handlers:
    result = item(arguments=arguments, method=method)
    if result.exception is None:
      return result
    results.append(result)

  return results[0]


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.main/utils/methods')


if __name__ == '__main__':
  examples()
