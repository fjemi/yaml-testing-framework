#! /usr/bin/env python3

import dataclasses as dc
import sys
from types import ModuleType
from typing import Any

from app.shared.format_main_arguments import app as format_main_arguments


@dc.dataclass
class Body:
  value: Any | None = None
  cast_as: str | None = None
  unpack: bool = False
  module: ModuleType | None = None
  # If source code convert to module
  source_code: str | None = None
  text: str | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  caster: Any | None = None
  result: Any | None = None


async def get_module_from_source_code(data: Data) -> Data:
  if data.body.module:
    return data

  module = ModuleType("module")
  sys.modules["module"] = module
  exec(data.body.source_code, module.__dict__)

  import module

  data.module = module
  return data


async def get_caster_from_module(data: Data) -> Data:
  paths = data.body.cast_as.split(".")

  caster = None

  if hasattr(data.body.module, paths[0]):
    caster = getattr(data.body.module, paths[0])

  if paths[0] in data.body.module.__builtins__:
    caster = data.body.module.__builtins__[paths[0]]

  for path in paths[1:]:
    caster = getattr(caster, path)
  data.caster = caster
  return data


CAST_VALUE = {}


async def cast_value(data: Data) -> Data:
  value_type = type(data.body.value).__name__
  if value_type not in ["list", "tuple", "dict"]:
    value_type = "*"

  value_type = type(data.body.value).__name__
  if dc.is_dataclass(data.body.value):
    value_type = "dataclass"

  if value_type == "dataclass" and data.body.cast_as == "dict":
    data.result = dc.asdict(data.body.value)
    return data

  if value_type not in ["list", "tuple", "dict"]:
    data.result = data.caster(data.body.value)
    return data

  if data.body.unpack and value_type == "dict":
    data.result = data.caster(**data.body.value)
    return data

  if not data.body.unpack and value_type == "dict":
    data.result = data.caster(data.body.value)
    return data

  if data.body.unpack and value_type in ["list", "tuple"]:
    data.result = data.caster(*data.body.value)
    return data

  if not data.body.unpack and value_type in ["list", "tuple"]:
    data.result = data.caster(data.body.value)
    return data

  message = f"Cannot cast {value_type} as {data.body.cast_as}"
  raise RuntimeError(message)


async def get_response(data: Data) -> Any:
  return data.result


# ruff: noqa: ARG001
async def main(
  text: str | None = None,
  value: Any | None = None,
  cast_as: str | None = None,
  unpack: bool | None = None,
  module: ModuleType | None = None,
  source_code: str | None = None,
) -> Any:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  data = await get_module_from_source_code(data=data)
  data = await get_caster_from_module(data=data)
  data = await cast_value(data=data)
  data = await get_response(data=data)
  return data


async def example() -> None:
  text = """
    value: 1
    cast_as: Data
    source_code: |
      import dataclasses as dc
      from typing import Any


      @dc.dataclass
      class Data:
        value: Any | None = None

      def to_str(value):
        return str(value)
  """
  result = await main(text=text)
  print(result)

  text = """
    value: [1, 2, 3]
    unpack: true
    cast_as: to_str
    source_code: |
      import dataclasses as dc
      from typing import Any

      def to_str(x1, x2, x3):
        return f'{x1} {x2} {x3}'
  """
  result = await main(text=text)
  print(result, type(result).__name__)

  text = """
    value: 1
    cast_as: str
    source_code: |
      # no code
  """
  result = await main(text=text)
  print(result, type(result).__name__)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
