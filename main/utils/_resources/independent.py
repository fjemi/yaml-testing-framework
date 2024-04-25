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


def decorator(func):
  def call(*args, **kwargs):
    return func(*args, **kwargs)
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
    return sns(c=c)
  except Exception as e:
    return e


def subtract(a: int, c: int) -> dict:
  result = a - c
  return dict(a=result)


def multiply(b: int, c: int) -> dict:
  result = b * c
  return dict(a=result)


def get_exception(exception: str | None = None) -> Exception | None:
  exceptions = sns(
    exception=Exception(),
    runtime_error=RuntimeError('runtime_error'),
    type_error=add(1, '1'), )
  return getattr(exceptions, str(exception), None)


def get_locals(function: str | None = None) -> dict:
  _ = function
  return LOCALS


def get_exception_name(exception: Exception | None = None) -> str | None:
  if isinstance(exception, Exception | KeyError):
    return type(exception).__name__


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
