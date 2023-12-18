# #!.venv/bin/python3
# # -*- coding: utf-8 -*-


from typing import Any
import dataclasses as dc
from typing import Callable
from types import ModuleType


LOCALS = locals()


@dc.dataclass
class Data_Class:
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


def function_one_parameter(parameter_1: None = None) -> None:
  return


def function_two_parameters(
  parameter_1: None = None,
  parameter_2: None = None,
) -> None:
  return


def function_resource(function: str) -> Callable:
  return LOCALS[function]


def data_class_resource(*args, **kwargs) -> Data_Class:
  return Data_Class


def data_resource(data: dict) -> Data_Class:
  return Data_Class(**data)


def functions_resource(*args, **kwargs) -> dict:
  return LOCALS


def coroutine_resource(task: Any | None = None) -> Any:
  async def entrypoint() -> str:
    return 'coroutine_output'

  return entrypoint()