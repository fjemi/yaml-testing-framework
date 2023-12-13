#!/usr/bin/env python3

# from importlib.machinery import SourceFileLoader
import dataclasses as dc
import importlib
import inspect
import os
from types import ModuleType

from app.shared.format_main_arguments import app as format_main_arguments

MODULE_PATH = __file__


@dc.dataclass
class Body:
  path: str | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  module: ModuleType | None = None
  call_method: str = "module"


async def raise_exception(data: Data) -> None:
  message = f"No module exists at {data.body.path}"
  raise RuntimeError(message)


async def load_module_from_path(data: Data) -> Data:
  """Returns a python module at a given file path"""
  module_name = os.path.basename(data.body.path)
  spec = importlib.util.spec_from_file_location(
    name=module_name,
    location=data.body.path,
  )
  data.module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(data.module)
  return data


GET_MODULE = {
  True: load_module_from_path,
  False: raise_exception,
}


async def get_module(data: Data) -> Data:
  cases = os.path.exists(data.body.path)
  switcher = GET_MODULE[cases]
  data = await switcher(data=data)
  return data


async def get_response(data: Data) -> Data:
  if data.call_method == "module":
    return data.module
  if data.call_method == "api":
    source = inspect.getsource(data.module)
    return source


# ruff: noqa: ARG001
async def main(path: str | None = None) -> ModuleType:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  data = await get_module(data=data)
  data = await get_response(data=data)
  return data


async def example() -> None:
  directory = os.path.dirname(MODULE_PATH)
  path = os.path.join(directory, "test_resources", "app.py")
  module = await main(path=path)
  print(module)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
