#!.venv/bin/python3
# -*- coding: utf-8 -*-


# trunk-ignore(ruff/F401)
import builtins
import dataclasses as dc
import threading
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Awaitable, Callable

# trunk-ignore(ruff/F401)
from assertions import module_resource as module


LOCALS = locals()
MODULE = __file__


def check_sns_resource(output: dict | None = None) -> sns:
  if isinstance(output, dict):
    return sns(**output)


def check_exception_resource(output: str | None = None) -> Exception | None:
  if output:
    exceptions = sns(RuntimeError=RuntimeError(), TypeError=TypeError())
    return getattr(exceptions, output, None)


def check_module_resource(output: str | None = None) -> ModuleType | None:
  return LOCALS.get(output, None)


def check_function_resource(output: str | None = None) -> Callable | None:

  def callable() -> str:
    return 'callable_output'

  async def coroutine() -> str:
    return 'coroutine_output'

  _ = callable, coroutine

  return locals().get(output, None)


def check_dataclass_resource(output: str | None = None) -> Any:

  @dc.dataclass
  class DataClass:
    a: str = 'a'
    b: str = 'b'

  dataclass = DataClass()
  return locals().get(output, None)


def check_class_resource(output: str | None = None) -> Any:

  class Class:
    pass

  class_ = Class()
  class_.a = 'a'
  class_.b = 'b'

  return locals().get(output, None)


def check_range_resource(output: dict | None = None) -> range | None:
  output = output or {}
  fields = ['start', 'stop', 'step']
  fields = [output.get(field, None) for field in fields if field in output]
  if not fields:
    return None
  return range(*fields)


def check_thread_resource(output: dict | None = None) -> threading.Thread:

  def target(data: None = None) -> str:
    _ = data
    return 'target_output'

  thread = threading.Thread(target=target, args=(None, ))
  return locals().get(output, None)


def check_function_output_resource(
  output: str | None = None,
) -> Callable | Awaitable | None:

  def hello_world(name: str | None = None) -> str:
    name = name or 'world'
    return f'Hello {name}'

  async def hello_earth(name: str | None = None) -> str:
    name = name or 'earth'
    return f'Hello {name}'

  def add(a: int, b: int) -> int:
    return a + b

  _ = hello_earth, hello_world, add

  return locals().get(output, None)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    module_filename='app',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
