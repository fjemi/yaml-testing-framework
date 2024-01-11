#!.venv/bin/python3
# -*- coding: utf-8 -*-

import asyncio
import threading
from typing import Any, Callable

from utils import app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources',
)

LOCALS = locals()
# Global variable to store results from
# executing target functions in threads
THREAD_EXECUTION_RESULTS = []

TYPE_HANDLER = {
  "str": lambda name: f"Hello {name}",
  # trunk-ignore(ruff/ARG005)
  "NoneType": lambda name: "Hello World",
}


def main_sync(name: str | None = None) -> str:
  kind = type(name).__name__.lower()
  if kind not in TYPE_HANDLER:
    kind = 'NoneType'
  handler = TYPE_HANDLER[kind]
  result = handler(name=name)
  return result


async def main_async(name: str | None = None) -> str:
  kind = type(name).__name__.lower()
  if kind not in TYPE_HANDLER:
    kind = 'NoneType'
  handler = TYPE_HANDLER[kind]
  result = handler(name=name)
  return result


def add_sync(
  a: int = 0,
  b: int = 0,
) -> int:
  return a + b


async def add_async(
  a: int = 0,
  b: int = 0,
) -> int:
  return a + b


def sync_target(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'sync_output'


async def async_target(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'async_output'


def argument_example(argument) -> tuple | None:
  if argument == 'tuple':
    return ()


def sync_entrypoint(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'sync_entrypoint_output'


async def async_entrypoint(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'async_entrypoint_output'


def function_resource(function: str) -> Callable:
  return LOCALS[function]


def entrypoints_resource(entrypoints: str) -> list:
  if entrypoints == 'entrypoints':
    return [sync_target, async_target]

  return entrypoints


def threads_resource(threads: str | None) -> list:
  if threads == 'threads':
    return [
      threading.Thread(target=add_sync),
      threading.Thread(target=add_async),
    ]


def sync_exception_target(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> None:
  return sum([1, '1'])


async def async_exception_target(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> None:
  return sum([1, '1'])


def target_resource(target: str | dict) -> Callable:
  kind = target.__class__.__name__.lower()

  if kind == 'dict':
    target = target.get('target')

  if kind == 'function':
    return target

  if isinstance(target, str):
    return LOCALS.get(target, None)

  return target


def get_threads_resource(threads: list | None = None) -> list:
  threads = [] if not threads else threads
  store = []
  for thread in threads:
    kind = type(thread).__name__.lower()
    store.append(kind)
  return store


def call_entrypoint(entrypoint: Callable) -> Any:
  task = entrypoint()

  if utils.is_coroutine(object=task):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
      task = loop.run_until_complete(task)
    finally:
      loop.close()
      asyncio.set_event_loop(None)

  return task


def coroutine_resource(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> Callable:

  async def async_function():
    return 'async_output'

  return async_function()


def set_target_entrypoints_for_threads_resource(entrypoints: list) -> list:
  store = []
  for entrypoint in entrypoints:
    store.append(entrypoint.__name__)
  return store


def output_threads_resource(threads: list | None) -> list:
  threads = threads or []

  store = []
  for thread in threads:
    data = {
      'target': thread._target.__name__,
      'type': type(thread).__name__.lower(),
    }
    store.append(data)

  return store


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
