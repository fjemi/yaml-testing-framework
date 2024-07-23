#!.venv/bin/python3
# -*- coding: utf-8 -*-


from typing import Any, Awaitable, Callable

from main.utils.methods.call import pack_any, unpack_list, unpack_mapping


LOCALS = locals()


def add(a: int, b: int) -> int:
  return a + b


def sum_(values: list) -> int:
  return sum(values)


def get_method(
  method: str = '',
  function: str = '',
) -> Callable:
  method = method or function
  if isinstance(method, str):
    method = LOCALS.get(method, None)
  return method


def get_task(task: str | None = None) -> Any:
  method = LOCALS.get(task, None)
  return method()


def get_function(function: str | None = None) -> Awaitable | Callable:
  return LOCALS.get(function, None)


def callable_function(parameter_a: Any | None = None) -> str:
  _ = parameter_a
  return 'callable_output'


async def awaitable_function(
  parameter_a: Any | None = None,
  parameter_b: Any | None = None,
) -> str:
  _ = parameter_a, parameter_b
  return 'awaitable_output'


def list_methods_to_list_strings(output: list) -> list:
  for i, item in enumerate(output):
    output[i] = item.__wrapped__.__name__
  return output


def get_handlers(handlers: list) -> list:
  for i, item in enumerate(handlers):
    handlers[i] = LOCALS.get(item, None)
  return handlers


def greetings(name: str | None = None) -> str:
  name = name or 'World'
  return f'Hello {name}'


def call_output(output: Callable) -> Any:
  return output()


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.main/utils/methods')


if __name__ == '__main__':
  examples()
