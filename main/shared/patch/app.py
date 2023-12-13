#!/usr/bin/env python3

import dataclasses as dc
import time
from types import ModuleType
from typing import Any, Callable, Dict, List

from app.shared.format_main_arguments import app as format_main_arguments
from app.shared.get_module import app as get_module_at_path

MODULE_PATH = __file__

SIDE_EFFECTS = {}


@dc.dataclass
class Body:
  module: str | None = None
  object: str | List[str] | None = None
  return_value: Any | None = None
  value: Any | None = None
  side_effect_list: List | None = None
  side_effect_dict: Dict | None = None
  text: str | None = None


@dc.dataclass
class Object:
  parent: Any | None = None
  name: str | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  patch: Any | None = None
  object: Object | object | None = None
  module: str | ModuleType | None = None
  call_method: str = "module"


@dc.dataclass
class List_Side_Effect:
  values: List[Any] | None = None
  count: int | None = None


class Store:
  pass


async def get_module(data: Data) -> Data:
  # data.module = runpy.run_path(path_name=data.body.module)
  module_type = type(data.body.module).__name__
  if module_type in ["module", "ModuleType"]:
    data.module = data.body.module
    return data

  if module_type == "str":
    data.module = await get_module_at_path.main(path=data.body.module)
    return data


async def get_patch_for_value(data: Data) -> Any:

  def patch(value: Any) -> Any:
    return value

  return patch(value=data.body.value)


async def get_patch_for_return_value(data: Data) -> Callable:
  # ruff: noqa: ARG001
  def patch(*args, **kwargs) -> Any:
    return data.body.return_value

  return patch


async def get_patch_for_side_effect_list(data: Data) -> Callable:
  timestamp = int(time.time())

  global SIDE_EFFECTS
  SIDE_EFFECTS[timestamp] = List_Side_Effect(
    values=data.body.side_effect_list, count=0)

  # ruff: noqa: ARG001
  def patch(*args, **kwargs) -> Any:
    n = len(SIDE_EFFECTS[timestamp].values)
    if SIDE_EFFECTS[timestamp].count == n:
      SIDE_EFFECTS[timestamp].count = 0
    SIDE_EFFECTS[timestamp].count += 1
    return SIDE_EFFECTS[timestamp].values[SIDE_EFFECTS[timestamp].count - 1]

  return patch


async def get_patch_for_side_effect_dict(data: Data) -> Callable:

  def patch(key) -> Any:
    return data.body.side_effect_dict[key]

  return patch


CREATE_PATCH = {
  "value": get_patch_for_value,
  "return_value": get_patch_for_return_value,
  "side_effect_list": get_patch_for_side_effect_list,
  "side_effect_dict": get_patch_for_side_effect_dict,
}


async def create_patch(data: Data) -> Data:
  cases = [
    "value" if data.body.value else "",
    "return_value" if data.body.return_value else "",
    "side_effect_list" if data.body.side_effect_list else "",
    "side_effect_dict" if data.body.side_effect_dict else "",
  ]
  cases = "".join(cases)
  switcher = CREATE_PATCH[cases]
  data.patch = await switcher(data=data)
  return data


async def get_object_from_module(parent, child) -> Any:
  cases = [
    "module" if hasattr(parent, child) else "",
    "builtins" if hasattr(parent.__builtins__, child) else "",
  ]
  cases = "".join(cases)

  if hasattr(parent, child):
    child = getattr(parent, child)
    return child

  if hasattr(parent.__builtins__, child):
    child = getattr(parent.__builtins__, child)
    return child

  if not hasattr(parent, child):
    setattr(parent, child, Store())
    child = getattr(parent, child)
    return child


async def get_object_from_dictionary(parent, child) -> Any:
  if child in parent:
    return parent[child]
  if child not in parent:
    parent[child] = Store()
    return parent[child]


async def get_object_from_other(parent, child) -> Any:
  message = f"{type(parent).__name__} has no object {child}"
  raise RuntimeError(message)


GET_OBJECT = {
  "module": get_object_from_module,
  "Store": get_object_from_module,
  "dict": get_object_from_dictionary,
  "*": get_object_from_other,
}


async def get_object(data: Data) -> Data:
  paths = data.body.object.split(".")
  n = len(paths)

  parent = data.module

  if n == 1:
    data.object = Object(parent=parent, name=paths[0])
    return data

  for path in paths[:-1]:
    parent_type = type(parent).__name__
    if parent_type not in GET_OBJECT:
      parent_type = "*"

    switcher = GET_OBJECT[parent_type]
    parent = await switcher(
      parent=parent,
      child=path,
    )

  data.object = Object(parent=parent, name=paths[-1])
  return data


async def patch_object(data: Data) -> Data:
  parent_type = type(data.object.parent).__name__

  if parent_type == "dict":
    data.object.parent[data.object.name] = data.patch
    return data

  if parent_type in ["module", "Store"]:
    setattr(
      data.object.parent,
      data.object.name,
      data.patch,
    )
    return data


async def patch_module(data: Data) -> Data:
  object_name = data.body.object.split(".")[0]
  setattr(data.module, object_name, data.object)
  return data


async def get_response(data: Data) -> Data:
  if data.call_method == "module":
    return data.module

  if data.call_method == "api":
    source_code = None
    return source_code


# ruff: noqa: ARG001
async def main(
  module: str | ModuleType | None = None,
  object: str | object | None = None,
  return_value: Any | None = None,
  value: Any | None = None,
  side_effect: List | Dict | None = None,
  text: str | None = None,
) -> dict:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  data = await get_module(data=data)
  data = await create_patch(data=data)
  data = await get_object(data=data)
  data = await patch_object(data=data)
  data = await get_response(data=data)
  return data


async def example() -> None:
  import os

  text = f"""
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: add
    return_value: add_patched
    value:
    side_effect:
  """
  module = await main(text=text)
  print(module.add(1, 2))
  print(module.use_add())

  text = f"""
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: patch_os
    value: patch_os_patched
  """
  module = await main(text=text)
  print(module.patch_os)

  text = f"""
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: os.patch_os
    value: os.patch_os_patched
  """
  module = await main(text=text)
  print(module.os.patch_os)

  text = f"""
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: dictionary_module.add
    value: dictionary_module.add_patched
  """
  module = await main(text=text)
  print(module.dictionary_module["add"])

  text = f"""
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: test2.test1
    value: test2.test1_patched
  """
  module = await main(text=text)
  print(module.dictionary_module["test2"]["test1"])

  text = f"""
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: side_effect_list
    side_effect_list: [side_effect_1, side_effect_2]
  """
  module = await main(text=text)
  print(
    module.side_effect_list(),
    module.side_effect_list(),
    module.side_effect_list(),
  )


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
