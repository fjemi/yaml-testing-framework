#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Awaitable, Callable


LOCALS = locals()


def callable_function(parameter_a: Any | None = None) -> str:
  _ = parameter_a
  return 'callable_output'


async def awaitable_function(
  parameter_a: Any | None = None,
  parameter_b: Any | None = None,
) -> str:
  _ = parameter_a, parameter_b
  return 'awaitable_output'


def decorator(func: Callable) -> Callable:

  def call(*args, **kwargs) -> Any:
    return func(*args, **kwargs)

  call.__wrapped__ = func

  return call


@decorator
def decorated_callable(
  parameter_a: Any | None = None,
  parameter_b: Any | None = None,
  parameter_c: Any | None = None,
) -> str:
  _ = parameter_a, parameter_b, parameter_c
  return 'decorated_callable_output'


@decorator
async def decorated_awaitable(
  parameter_a: Any | None = None,
  parameter_b: Any | None = None,
  parameter_c: Any | None = None,
) -> str:
  _ = parameter_a, parameter_b, parameter_c
  return 'decorated_awaitable_output'


def get_task(task: str | None = None) -> Any:
  task = LOCALS.get(task, None)
  if isinstance(task, Awaitable | Callable):
    task = task()
  return task


def get_function(function: str | None = None) -> Awaitable | Callable:
  return LOCALS.get(function, None)


def add(a: int, b: int | str) -> sns | Exception:
  try:
    c = sum([a, b])
  except Exception as error:
    c = error

  return sns(c=c)


def subtract(a: int, c: int) -> dict:
  result = a - c
  return dict(a=result)


def multiply(b: int, c: int) -> dict:
  result = b * c
  return dict(a=result)




def get_locals(function: str | None = None) -> dict:
  _ = function
  return LOCALS


def get_exception_name(exception: Exception | None = None) -> str | None:
  if isinstance(exception, Exception | KeyError):
    return type(exception).__name__


def wrapped(func):

  def wrapped_inner(*args, **kwargs):
    return func(*args, **kwargs)

  wrapped_inner.__wrapped__ = func

  return wrapped_inner


def closure(func):

  def closure_inner(*args, **kwargs):
    return func(*args, **kwargs)

  return closure_inner


def callable() -> str:
  return 'callable_output'


async def awaitable() -> str:
  return 'awaitable_output'


@closure
def callable_decorated_closure() -> str:
  return 'decorated_callable_output'


@wrapped
def callable_decorated_wrapped() -> str:
  return 'decorated_callable_output'


@closure
async def awaitable_decorated_closure() -> str:
  return 'decorated_callable_output'


@wrapped
async def awaitable_decorated_wrapped() -> str:
  return 'decorated_callable_output'


def check_method(
  module: Any | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  _ = module
  return sns(
    passed=True,
    output=output,
    expected=expected, )


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    resource_flag=True,
    module_filename='app', )


if __name__ == '__main__':
  examples()
