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
  unpack: bool | None = None,
) -> sns:
  method = method or function
  handler = get_handler(arguments=arguments, unpack=unpack)
  return handler(method=method, arguments=arguments)


def is_coroutine(object: Any | None = None) -> bool:
  return True in [
    inspect.iscoroutinefunction(obj=object),
    inspect.iscoroutine(object=object),
    inspect.isawaitable(object=object), ]


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
    flags = sns(error=False)

    try:
      output = method(*args, **kwargs)
    except Exception as error:
      arguments = kwargs or list(args)
      output = error
      flags.error = True
      logger.main(error=error, arguments=arguments)

    output = get_task_from_event_loop(task=output)
    return sns(output=output, flags=flags)

  caller_wrapper_inner.__wrapped__ = method
  return caller_wrapper_inner


@caller_wrapper
def unpack_mapping(
  arguments: Any | None = None,
  method: Callable | None = None,
) -> sns:
  return method(**arguments)


@caller_wrapper
def unpack_list(
  arguments: Any | None = None,
  method: Callable | None = None,
) -> sns:
  return method(*arguments)


@caller_wrapper
def pack_any(
  arguments: Any | None = None,
  method: Callable | None = None,
) -> sns:
  return method(arguments)


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def get_handler(
  arguments: Any | None = None,
  unpack: bool | None = None,
) -> Callable:
  if isinstance(arguments, Mapping) and unpack:
    return unpack_mapping if unpack else pack_any
  if isinstance(arguments, list | tuple) and unpack:
    return unpack_list if unpack else pack_any
  return pack_any


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.main/utils/methods')


if __name__ == '__main__':
  examples()
