#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
from typing import Any, Callable

import yaml
from error_handler.app import main as error_handler


MODULE = __file__
LOCALS = locals()

HANDLER_MAP = '''
cast_nonetype_packed_to_dataclass: instatiate_caster
cast_dict_packed_to_dataclass: pass_unpacked_dict
cast_any_packed_to_nonetype: pass_object_through
cast_dict_packed_to_nonetype: pass_object_through
cast_dict_unpacked_to_nonetype: pass_object_through
cast_list_packed_to_type: pass_packed_object
cast_any_packed_to_any: pass_packed_object
cast_dict_packed_to_any: pass_packed_object
cast_dict_packed_to_any: pass_packed_object
cast_nonetype_unpacked_to_function: pass_packed_object
cast_any_packed_to_type: pass_packed_object
cast_dict_packed_to_function: pass_packed_object
cast_dict_packed_to_type: pass_packed_object
cast_any_packed_to_function: pass_packed_object
cast_list_packed_to_function: pass_packed_object
cast_dict_unpacked_to_dataclass: pass_unpacked_dict
cast_dict_unpacked_to_function: pass_unpacked_dict
cast_dict_unpacked_to_any: pass_unpacked_dict
cast_nonetype_packed_to_function: pass_packed_object
cast_list_unpacked_to_function: pass_unpacked_list
cast_nonetype_packed_to_nonetype: do_nothing
cast_nonetype_unpacked_to_dataclass: instatiate_caster
cast_nonetype_packed_to_type: instatiate_caster
cast_dataclass_packed_to_type: pass_dataclass
cast_dataclass_unpacked_to_type: pass_dataclass
cast_dataclass_packed_to_any: pass_dataclass
cast_dataclass_unpacked_to_function: pass_dataclass
cast_dataclass_packed_to_function: pass_dataclass
cast_dataclass_packed_to_dataclass: pass_object_through
cast_nonetype_packed_to_nonetype: do_nothing
cast_any_packed_to_nonetype: pass_object_through
'''
HANDLER_MAP = yaml.safe_load(HANDLER_MAP)


@dc.dataclass
class Data_Class:
  pass


@error_handler()
async def pass_object_through(
  object: Any | None = None,
  # trunk-ignore(ruff/ARG001)
  caster: Any | None = None,
) -> Any:
  return object


@error_handler()
async def pass_packed_object(
  object: Any | None = None,
  caster: Any | None = None,
) -> Any:
  return caster(object)


@error_handler()
async def pass_unpacked_dict(
  object: Any | None = None,
  caster: Any | None = None,
) -> Any:
  return caster(**object)


@error_handler()
async def do_nothing(
  # trunk-ignore(ruff/ARG001)
  object: None = None,
  # trunk-ignore(ruff/ARG001)
  caster: None = None,
) -> None:
  pass


@error_handler()
async def instatiate_caster(
  # trunk-ignore(ruff/ARG001)
  object: None = None,
  caster: Any | None = None,
) -> Any:
  return caster()


DATACLASS_TO_DICT_NAMES = [
  'asdict',
  'dict',
]


@error_handler()
async def pass_dataclass(
  object: Data_Class | None = None,
  caster: Any | None = None,
) -> Any:
  for name in DATACLASS_TO_DICT_NAMES:
    if caster.__name__ != name:
      continue

    try:
      return dc.asdict(object)
    except Exception as e:
      _ = e
      return object.__dict__

  return caster(object)


@error_handler()
async def main(handler: str | None = None) -> Callable:
  handler = str(handler)
  handler = HANDLER_MAP.get(handler, None)
  return LOCALS.get(handler, None)


@error_handler()
def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
