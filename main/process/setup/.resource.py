#!.venv/bin/python3
# -*- coding: utf-8 -*-


import time
from types import ModuleType
from typing import Callable


MODULE = __file__
LOCALS = locals()


def get_setup_object(*args, **kwargs) -> str:
  _ = args, kwargs
  return 'setup_object'


def get_method(method: str = '') -> Callable | None:
  return LOCALS.get(str(method), None)


def get_string(*args, **kwargs) -> str:
  _ = args, kwargs
  return 'value'


def get_integer(*args, **kwargs) -> int:
  _ = args, kwargs
  return 1


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def living(*args, **kwargs) -> str:
  _ = args, kwargs

  stopped = False
  while not stopped:
    time.sleep(1)
    stopped = True

  return 'timed_out'


def greetings(name: str | None = None) -> str:
  name = name or 'World'
  return f'Hello {name}'


def keep_running() -> str:
  time.sleep(3)
  return 'dead'


def get_future_result(
  future: 'Future | ProcessFuture | None' = None,
) -> str | None:
  return future.result()


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    resource_flag=True,
    module_filename='app', )


if __name__ == '__main__':
  examples()

