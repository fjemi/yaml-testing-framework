#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any

from error_handler.app import main as error_handler
from get_config.app import main as get_config

# trunk-ignore(ruff/F401)
from get_module.app import main as get_module


MODULE = __file__
CONFIG = get_config(module=MODULE)
LOCALS = locals()

KINDS = [
  'dict',
  'object', ]


@dc.dataclass
class Data_Class:
  pass


@error_handler()
async def pass_through(
  data: dict,
  field_name: str,
) -> Any:
  return data.get(field_name)


@error_handler()
async def format_parents(
  data: dict,
  # trunk-ignore(ruff/ARG001)
  field_name: str,
) -> list[object]:
  parent = data.get('parent', None, )
  type_ = 'dict' if hasattr(parent, 'keys') else 'object'

  data_class = CONFIG.schema.Parents
  return data_class(
    names=[''],
    values=[parent],
    types=[type_], )


@error_handler()
async def format_names(
  data: dict,
  # trunk-ignore(ruff/ARG001)
  field_name: str,
) -> list[object]:
  names = data.get('name', '')
  names = str(names).strip()
  names = names.split('.')

  store = []
  for name in names:
    if len(name) == 0:
      continue
    store.append(name)

  return store


@error_handler()
async def get_data_class(data: dict) -> Data_Class:
  data_class = CONFIG.schema.Data()
  for field in dc.fields(data_class):
    handler = f'format_{field.name}'
    handler = LOCALS.get(
      handler,
      pass_through, )
    value = handler(
      data=data,
      field_name=field.name, )
    setattr(data_class, field.name, value)
  return data_class


@error_handler()
def get_object_from_dict(
  name: str,
  parent: dict,
) -> Any | None:
  return parent.get(name)


@error_handler()
async def get_object_from_object(
  name: str,
  parent: dict,
) -> Any | None:
  if hasattr(parent, name):
    return getattr(parent, name)


@error_handler()
async def get_object(data: Data_Class) -> Data_Class:
  for name in data.names:
    handler = f'get_object_from_{data.parents.types[-1]}'
    handler = LOCALS[handler]
    value = handler(
      parent=data.parents.values[-1],
      name=name, )
    type_ = 'dict' if isinstance(value, dict) else 'object'

    data.parents.values.append(value)
    data.parents.types.append(type_)
    data.parents.names.append(name)

  return data


UNDEFINED = ['', '.', 'None', None, ]


@error_handler()
async def main(
  parent: Any | None = None,
  name: str | None = None,
) -> Any:
  name = str(name).strip()
  if name in CONFIG.undefined:
    return parent

  data = get_data_class(data=locals())
  data = get_object(data=data)
  return data.parents.values[-1]


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
