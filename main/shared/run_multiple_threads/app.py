#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
import inspect
import threading
import time
from types import ModuleType
from typing import Any, Callable, List

from error_handler.app import main as error_handler
from get_config.app import main as get_config
from utils import app as utils


MODULE = __file__
CONFIG = get_config(module=MODULE)
LOCALS = locals()

STORE = {}
LOCK = threading.Lock()


@dc.dataclass
class Data_Class:
  pass


@error_handler()
async def format_argument_as_empty_list(
  # trunk-ignore(ruff/ARG001)
  argument: None = None,
) -> list:
  return []


@error_handler()
async def format_argument_as_argument(argument: dict | tuple | list) -> dict:
  return argument


@error_handler()
async def format_argument_as_list(argument: Any) -> list:
  return [argument]


@error_handler()
async def format_argument(
  argument: Any | None = None,
  kind: str | None = None,
) -> list | dict:
  _ = kind
  kind = argument.__class__.__name__.lower()
  kind = kind if kind in CONFIG.format_kinds else 'any'
  kind = CONFIG.format_kinds_handler[kind]

  handler = f'format_argument_as_{kind}'
  handler = LOCALS[handler]
  return handler(argument=argument)


def update_store(result_key: str):

  def decorator(function):

    def entrypoint_wrapper(
      # trunk-ignore(ruff/ARG001)
      *args,
      # trunk-ignore(ruff/ARG001)
      **kwargs,
    ) -> Callable:
      global STORE

      result = function()

      condition = result_key in STORE
      if condition:
        STORE[result_key].append(result)
      elif not condition:
        STORE[result_key] = [result]

      return result

    return entrypoint_wrapper

  return decorator


@error_handler()
async def format_target_arguments(
  kwargs: list | None = None,
  args: tuple | list | None = None,
) -> dict:
  arguments = []

  for name in ['args', 'kwargs']:
    values = locals().get(name, None)
    if not values:
      continue

    kind = type(values).__name__.lower()

    conditions = [name == 'kwargs', kind == 'list']
    if sum(conditions) == len(conditions):
      for value in values:
        arguments.append({name: value})
    elif sum(conditions) != len(conditions):
      arguments.append({name: values})

  return {
    'args': None,
    'kwargs': None,
    'arguments': arguments,
  }


@error_handler()
async def call_sync_target_with_packed_argument(
  argument: Any | None = None,
  target: Callable | None = None,
  exception: Exception | None = None,
  output: Any | None = None,
) -> Any:
  if output and not exception:
    return output

  try:
    return target(argument)
  except Exception as e:
    _ = e
    return exception


@error_handler()
async def call_sync_target_with_unpacked_argument(
  argument: Any | None = None,
  target: Callable | None = None,
  kind: str | None = None,
) -> dict:
  output = None
  exception = None

  try:
    if kind == 'kwargs':
      output = target(**argument)
    elif kind == 'args':
      output = target(*argument)
  except Exception as e:
    exception = e

  return {
    'exception': exception,
    'output': output,
  }


@error_handler()
async def call_async_target_with_packed_argument(
  argument: Any | None = None,
  target: Callable | None = None,
  exception: Exception | None = None,
  output: Any | None = None,
) -> dict | None:
  if not exception:
    return output

  try:
    task = target(argument)
    return utils.get_task_from_event_loop(task=task)
  except Exception as e:
    _ = e
    return exception


@error_handler()
async def call_async_target_with_unpacked_argument(
  argument: Any | None = None,
  target: Callable | None = None,
  kind: str | None = None,
) -> dict:
  output = None
  exception = None

  try:
    if kind == 'kwargs':
      output = target(**argument)
    elif kind == 'args':
      output = target(*argument)
  except Exception as e:
    exception = e

  return {
    'exception': utils.get_task_from_event_loop(task=exception),
    'output': utils.get_task_from_event_loop(task=output),
  }


@error_handler()
async def get_entrypoint_for_sync_target(
  target: Callable | None = None,
  argument: dict | None = None,
  result_key: str | None = None,
  kind: str | None = None,
) -> Callable:

  @update_store(result_key=result_key)
  def entrypoint() -> None:
    data = call_sync_target_with_unpacked_argument(
      target=target,
      argument=argument,
      kind=kind,
    )
    return call_sync_target_with_packed_argument(
      target=target,
      exception=data.get('exception'),
      output=data.get('output'),
      argument=argument,
    )

  return entrypoint


@error_handler()
async def get_entrypoint_for_async_target(
  target: Callable | None = None,
  argument: dict | None = None,
  result_key: str | None = None,
  kind: str | None = None,
) -> Callable:

  @update_store(result_key=result_key)
  def entrypoint() -> dict:
    data = call_async_target_with_unpacked_argument(
      target=target,
      argument=argument,
      kind=kind,
    )
    return call_async_target_with_packed_argument(
      target=target,
      exception=data.get('exception'),
      output=data.get('output'),
      argument=argument,
    )

  return entrypoint


@error_handler()
async def get_entrypoint_handler(
  target: Callable,
  argument: dict | tuple | list | None = None,
  result_key: str | None = None,
) -> Callable:
  kind = 'args'

  key = 'kwargs'
  if key in argument:
    kind = 'kwargs'
  argument = argument[kind]

  coroutine = 'async' if utils.is_coroutine(object=target) else 'sync'
  handler = f'get_entrypoint_for_{coroutine}_target'
  handler = LOCALS[handler]
  return handler(
    target=target,
    argument=argument,
    result_key=result_key,
    kind=kind,
  )


@error_handler()
async def set_target_entrypoints_for_threads(
  target: Callable | None = None,
  arguments: list | None = None,
  result_key: str | None = None,
  module: ModuleType | None = None,
) -> dict:
  entrypoints = []

  for argument in arguments:
    entrypoint = get_entrypoint_handler(
      target=target,
      result_key=result_key,
      argument=argument,
    )
    entrypoints.append(entrypoint)

  kind = type(module).__name__.lower()
  if kind == 'module':
    module = inspect.getmodule(target)
  elif kind == 'list':
    module = module[0]
  elif kind == 'nonetype':
    module = ''

  return {
    'module': module,
    'entrypoints': entrypoints,
    'arguments': None,
  }


@error_handler()
async def create_single_thread(
  target: Callable | None = None,
  daemon: bool | None = True,
) -> threading.Thread:
  return threading.Thread(target=target, daemon=daemon)


@error_handler()
async def get_threads(entrypoints: list | None = None) -> dict:
  threads = []

  for entrypoint in entrypoints:
    thread = create_single_thread(target=entrypoint)
    # Lock to prevent duplicate threads from being created
    with LOCK:
      time.sleep(0.1)
    threads.append(thread)

  return {
    'entrypoints': None,
    'threads': threads,
  }


@error_handler()
async def run_threads_in_parallel(
  threads: threading.Thread | None = None,
) -> dict:
  threads = [] if not threads else threads
  n = range(len(threads))

  for i in n:
    threads[i].start()
  for i in n:
    threads[i].join()

  return {'threads': None}


@error_handler()
async def run_threads_in_sequence(
  threads: threading.Thread | None = None,
) -> dict:
  threads = [] if not threads else threads
  n = range(len(threads))

  for i in n:
    threads[i].start()
    threads[i].join()

  return {'threads': None}


@error_handler()
async def main(
  target: List[Callable] | Callable | None = None,
  kwargs: List[dict] | dict | None = None,
  args: List[Any] | None = None,
  timestamp: int | None = None,
) -> List[Any]:
  args = () if not args else args
  kwargs = {} if not kwargs else kwargs
  timestamp = int(time.time()) if not timestamp else timestamp
  result_key = f'{target.__name__}.{timestamp}'

  data = utils.process_arguments(
    data_class=CONFIG.schema.Data,
    locals=locals(),
  )
  data = utils.process_operations(
    operations=CONFIG.operations,
    functions=LOCALS,
    data=data,
  )

  return STORE.get(result_key, None)


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  parent_module = utils.get_parent_module(
    module=MODULE,
    resources_folder_name='test_resources', )
  invoke_pytest(project_directory=parent_module)


if __name__ == '__main__':
  example()
