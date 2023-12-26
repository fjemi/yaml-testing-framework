import asyncio
import dataclasses as dc
import threading
from time import ctime, time
from typing import Callable
import threading
from typing import Any
import inspect
import os

import yaml

import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources', )

LOCALS = locals()
# Global variable to store results from
# executing target functions in threads
THREAD_EXECUTION_RESULTS = []

TYPE_HANDLER = {
  "str": lambda name: f"Hello {name}",
  "NoneType": lambda name: "Hello World", }


def main_sync(name: str = None) -> str:
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


def sync_target(*args, **kwargs) -> str:
  return 'sync_output'


async def async_target(*args, **kwargs) -> str:
  return 'async_output'


def argument_example(argument) -> tuple | None:
  if argument == 'tuple':
    return ()


def sync_entrypoint(*args, **kwargs) -> str:
  return 'sync_entrypoint_output'


async def async_entrypoint(*args, **kwargs) -> str:
  return 'async_entrypoint_output'


def function_resource(function: str) -> Callable:
  return LOCALS[function]


def entrypoints_resource(entrypoints: str) -> list:
  if entrypoints == 'entrypoints':
    return [sync_target, async_target]
  
  return entrypoints


def argument_example_1(argument) -> dict:
  key = 'entrypoint'
  entrypoint = entrypoint_example(entrypoint=argument[key])
  argument[key] = entrypoint
  return argument


def threads_resource(threads: str | None) -> list:
  if threads == 'threads':
    return [
      threading.Thread(target=add_sync),
      threading.Thread(target=add_async), ]


def sync_exception_target(*args, **kwargs):
  return sum([1, '1'])


async def async_exception_target(*args, **kwargs):
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
  result = entrypoint()
  
  condition = inspect.iscoroutine(result)
  if condition:
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(result)
  
  return result


def coroutine_resource(*args, **kwargs) -> Any:
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
      'type': type(thread).__name__.lower(), }
    store.append(data)

  return store


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
