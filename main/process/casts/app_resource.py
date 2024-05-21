#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable

from main.utils import get_module


MODULE = __file__

LOCALS = locals()


def pass_through(*args, **kwargs) -> str:
  _ = args, kwargs
  return 'pass_through'


def cast_as_str(
  temp_object: Any | None = None,
  unpack: bool | None = None,
) -> str:
  _ = unpack
  return str(temp_object)


def cast_as_int(
  temp_object: Any | None = None,
  unpack: bool | None = None,
) -> int:
  _ = unpack
  return int(temp_object)


def cast_as_split(
  temp_object: Any | None = None,
  unpack: bool | None = None,
) -> int:
  _ = unpack
  return temp_object.split('.')


def cast_dict_as_sns(temp_object: Any | None = None) -> sns:
  return sns(**temp_object)


def cast_list_to_string(a: str, b: str, c: str) -> str:
  return a + b + c


def get_method(method: str | None = None) -> Callable | None:
  return LOCALS.get(str(method), None)


def pack_nonetype(temp_object: None = None) -> str:
  _ = temp_object
  return 'output'


def unpack_nonetype() -> str:
  return 'output'


@dc.dataclass
class DataClass:
  pass


@dc.dataclass
class TestData:
  a: int = 0
  b: int = 0


DATA_CLASS_RESOURCE = TestData()


def inverse(a: int) -> int:
  return 1 / a


def negate(a: int) -> int:
  return a * -1


def add(a: int, b: int) -> int:
  return a + b


def add_list(values: list) -> int:
  return sum(values)


def add_sns(data: Any) -> Any:
  return data.a + data.b


def add_dict(temp_object: dict | None = None) -> int:
  return sum(list(temp_object.values()))


OBJECT_MAP = {
  'dataclass': TestData,
  'dict_dataclass': {
    'dataclass': TestData()
  },
  'add': add,
  'add_list': add_list,
  'add_dataclass': add_sns,
  'str': str,
  'int': int,
  'dict': dict,
  'float': float,
  'tuple': (),
  'dataclasses.asdict': dc.asdict,
  'None': None,
}


def function_one_parameter(parameter_1: None = None) -> None:
  _ = parameter_1


def function_two_parameters(
  parameter_1: None = None,
  parameter_2: None = None,
) -> None:
  _ = parameter_1, parameter_2


def function(data: None = None) -> None:
  _ = data


def function_resource(function: str) -> Callable:
  return get_resource(resource=function)


def caster_resource(caster: str) -> Callable:
  return get_resource(resource=caster)


def object_resource(object: Any | None = None) -> Callable:
  return get_resource(resource=object)


def casted_object_resource(object: Any | None = None) -> Callable:
  return get_resource(resource=object)


def module_resource(module: str | None = None) -> ModuleType | None:
  if isinstance(module, str):
    module = get_module.main(location=module, pool=False)
    return module


def kinds_resource(kinds: str | dict) -> Any:
  if isinstance(kinds, dict):
    data = DataClass()

    for key, value in kinds.items():
      setattr(data, key, value)
    return data

  if isinstance(kinds, str):
    return get_resource(resource=kinds)


def get_resource(resource: Any | None = None) -> Callable:
  if resource in LOCALS:
    return LOCALS[resource]
  return OBJECT_MAP[resource]


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    module_filename='app',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
