#!.venv/bin/python3
# -*- coding: utf-8 -*-


import threading
import time
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, Iterable

from pebble import concurrent

from main.utils import (
  logger,
  get_config,
  objects,
  independent,
  methods,
  get_module, )


MODULE = __file__
LOCALS = locals()

CONFIG = get_config.main()

STORE = {}

WAIT = 15


def process_setup(
  module: ModuleType | str | None = None,
  setup: list | None = None,
  phase_: str | None = None,
) -> sns:
  action = 'setup'
  locals_ = sns(**locals())
  return main(**locals_.__dict__) if setup else sns()


def process_teardown(
  module: ModuleType | str | None = None,
  setup: list | None = None,
  phase_: str | None = None,
) -> sns:
  action = 'teardown'
  locals_ = sns(**locals())
  return main(**locals_.__dict__) if setup else sns()


def main(
  action: str | None = None,
  phase_: str | None = None,
  setup: list | None = None,
  module: ModuleType | str | None = None,
  timeout: int | None = None,
) -> sns:
  setup = setup or []
  locals_ = sns(**locals())
  del locals_.setup

  for item in setup:
    item.update(**locals_.__dict__)
    data = independent.get_model(schema=CONFIG.schema.Main, data=item)
    data = independent.process_operations(
      data=data,
      operations=CONFIG.operations.main,
      functions=LOCALS, )

  return sns()


def get_store() -> sns:
  return sns(setup_=STORE)


def get_flags(
  phase_: str | None = None,
  phase: str | None = None,
  action: str | None = None,
) -> sns:
  phase = str(phase).lower()
  phase = objects.get(parent=CONFIG.phases, route=phase)
  flags = [
    action in CONFIG.actions,
    phase == phase_, ]
  flags = sum(flags) == len(flags)
  return sns(flags=flags)


def perform_action(
  action: str | None = None,
  method: Callable | None = None,
  arguments: Any | None = None,
  name: str | None = None,
  timeout: int | None = None,
  flags: bool | None = None,
) -> sns:
  locals_ = locals()
  handler = f'{action}_object'
  handler = objects.get(parent=LOCALS, route=handler)
  temp = independent.get_function_arguments(data=locals(), function=handler)
  return handler(**temp) if flags else do_nothing


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def get_method(
  method: str = '',
  resource: str = '',
  module: ModuleType | None = None,
) -> sns:
  resource = resource or module
  resource = get_module.main(module=resource).module
  method = objects.get(
    parent=resource,
    route=method,
    default=do_nothing, )
  return sns(method=method)


@concurrent.process
def get_future(
  method: Callable | None = None,
  arguments: dict | None = None,
) -> Any:
  arguments = arguments or {}
  task = None

  try:
    task = method(**arguments)
  except Exception as error:
    arguments = dict(arguments=arguments, method=method)
    logger.main(arguments=arguments, error=error)
    task = error

  return methods.call.get_task_from_event_loop(task=task)


def run_process_in_separate_thread(
  method: Callable | None = None,
  arguments: Any | None = None,
  timeout: int = 0,
) -> 'Any | Future | ProcessFuture':
  future = get_future(method=method, arguments=arguments)

  if timeout == -1:
    return future

  if future.done() is True or timeout == 0:
    return future.result()

  if isinstance(timeout, int):
    seconds = 0
    while not future.done():
      seconds += 3
      time.sleep(3)
      if seconds > timeout:
        break
  
  return future.result()


def setup_object(
  method: Callable | None = None,
  arguments: Any | None = None,
  timeout: int = 0,
) -> sns:
  value = run_process_in_separate_thread(
    timeout=timeout,
    method=method,
    arguments=arguments, )
  return sns(value=value)


def teardown_object(
  name: str | None = None,
  method: Callable | None = None,
) -> sns:
  value = objects.get(parent=STORE, route=name)
  kind = type(value).__name__

  if kind in ['Future', 'ProcessFuture']:
    value.cancel()

  return sns(value=None)


def update_store(
  name: str | None = None,
  value: Any | None = None,
  flags: bool | None = None,
) -> dict:
  if flags:
    return {}

  global STORE
  STORE[name] = value
  return {}


def teardown_all() -> dict:
  for name, value in STORE.items():
    value_ = teardown_object(name=name).value
    update_store(name=name, value=value_)
  return STORE


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
