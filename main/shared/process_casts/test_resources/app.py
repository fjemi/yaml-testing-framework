# #!.venv/bin/python3
# # -*- coding: utf-8 -*-

import dataclasses as dc
from types import ModuleType
from typing import Any, Callable

# trunk-ignore(ruff/F401)
from process_casts.test_resources import resource as module


MODULE = __file__

LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


@dc.dataclass
class Test_Data:
  a: int = 0
  b: int = 0


DATA_CLASS_RESOURCE = Test_Data()


def add(a: int, b: int) -> int:
  return a + b


def add_list(values: list) -> int:
  return values[0] + values[1]


def add_dataclass(data: Any) -> Any:
  return data.a + data.b


OBJECT_MAP = {
  'dataclass': Test_Data,
  'dict_dataclass': {
    'dataclass': Test_Data()
  },
  'add': add,
  'add_list': add_list,
  'add_dataclass': add_dataclass,
  'str': str,
  'int': int,
  'dict': dict,
  'float': float,
  'tuple': (),
  'dataclasses.asdict': dc.asdict,
  'None': None,
}


def function_one_parameter(
  # trunk-ignore(ruff/ARG001)
  parameter_1: None = None,
) -> None:
  return


def function_two_parameters(
  # trunk-ignore(ruff/ARG001)
  parameter_1: None = None,
  # trunk-ignore(ruff/ARG001)
  parameter_2: None = None,
) -> None:
  return


def function(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> None:
  return


def function_resource(function: str) -> Callable:
  return get_resource(resource=function)


def caster_resource(caster: str) -> Callable:
  return get_resource(resource=caster)


def object_resource(object: Any | None = None) -> Callable:
  return get_resource(resource=object)


def casted_object_resource(object: Any | None = None) -> Callable:
  return get_resource(resource=object)


def module_resource(
  # trunk-ignore(ruff/F811)
  module: str | None = None,
) -> ModuleType | None:
  return get_resource(resource=module)


def kinds_resource(kinds: str | dict) -> Any:
  if isinstance(kinds, dict):
    data = Data_Class()
    for key, value in kinds.items():
      setattr(data, key, value)
    return data

  if isinstance(kinds, str):
    return get_resource(resource=kinds)


def get_resource(resource: Any | None = None) -> Callable:
  if resource in LOCALS:
    return LOCALS[resource]
  return OBJECT_MAP[resource]


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest
  from utils import app as utils

  parent_module = utils.get_parent_module(
    resources_folder_name='test_resources',
    module=MODULE,
  )
  invoke_pytest(project_directory=parent_module)


if __name__ == '__main__':
  example()
