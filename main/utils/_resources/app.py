# #!.venv/bin/python3
# # -*- coding: utf-8 -*-

import dataclasses as dc
from typing import Any, Callable, Iterable


LOCALS = locals()


@dc.dataclass
class DataClass:
  a: int = 0
  b: int = 0
  result: int = 0


def add(a: int, b: int) -> dict:
  result = a + b
  return {'result': result}


def subtract(a: int, b: int) -> dict:
  result = a - b
  return {'result': result}


def subtract_dict(nums: dict) -> dict:
  result = nums['a'] = nums['b']
  return {'result': result}


def multiply(a: int, b: int) -> dict:
  result = a * b
  return {'result': result}


def function_one_parameter(
  parameter_1: None = None,
) -> None:
  _ = parameter_1


def function_two_parameters(
  parameter_1: None = None,
  parameter_2: None = None,
) -> None:
  _ = parameter_1, parameter_2


def function_resource(function: str) -> Callable:
  return LOCALS[function]


def get_data_class_resource(*args, **kwargs) -> DataClass:
  _ = args, kwargs
  return DataClass


def data_resource(data: dict) -> DataClass:
  return DataClass(**data)


def functions_resource(*args, **kwargs) -> dict:
  _ = args, kwargs
  return LOCALS


def coroutine_resource(
  task: Any | None = None,
  object: Any | None = None,
) -> Callable:
  _ = task, object

  def entrypoint() -> str:
    return 'coroutine_output'

  return entrypoint()


def get_range_from_integer_resource(n: int) -> Iterable:
  return range(n)
