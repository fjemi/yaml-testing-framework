#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

from utils import get_config, get_object, independent, schema, set_object


MODULE = __file__
CONFIG = get_config.main(module=MODULE)
LOCALS = locals()

SIDE_EFFECTS = {}


def main(
  patches: List[dict | sns] | None = None,
  module: ModuleType | None = None,
) -> sns:
  patches = patches or []

  for patch in patches:
    data = pre_processing(patch=patch, module=module)
    data = independent.process_operations(
      operations=CONFIG.main_operations,
      functions=LOCALS,
      data=data, )
    module = data.module

  return sns(_cleanup=['patches'], module=module)


def pre_processing(
  patch: dict | None = None,
  module: ModuleType | None = None,
) -> sns:
  patch = schema.get_model(name='Patch', data=patch)
  patch.module = module
  patch.timestamp = independent.get_timestamp()
  return patch


def get_patch_method(
  method: str | None = None,
  value: Any | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  callable_route: str | None = None,
) -> sns:
  handler = f'get_{method}_patch_method'
  handler = LOCALS.get(handler, do_nothing)

  data = sns(do_nothing=False)
  data.value = handler(
    value=value,
    module=module,
    callable_route=callable_route,
    timestamp=timestamp, )
  if data.value is None:
    data.do_nothing = True
    data.log = sns(
      message=f'No patch method {method} found',
      level='error', )
  return data


def do_nothing(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
) -> None:
  _ = value, timestamp, callable_route, module


def get_value_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
) -> Any:
  _ = timestamp, callable_route, module

  def patch(
    patch_value: Any | None = None,
  ) -> Any:
    return patch_value

  return patch(patch_value=value)


def get_callable_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
) -> Callable:
  _ = timestamp

  if callable_route:
    return get_object.main(parent=module, route=callable_route)

  def callable_patch(*args, **kwargs) -> Any:
    # callable patch
    _ = args, kwargs
    return value

  return callable_patch


def get_side_effect_list_patch_method(
  value: list | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
) -> Callable:
  _ = callable_route, module

  global SIDE_EFFECTS

  data = sns(value=value, count=0)
  SIDE_EFFECTS[timestamp] = schema.get_model(
    data=data,
    name='Patch_Side_Effect_List', )
  
  def side_effect_list_patch(*args, **kwargs) -> Any:
    _ = args, kwargs

    n = len(SIDE_EFFECTS[timestamp].value)
    if SIDE_EFFECTS[timestamp].count == n:
      SIDE_EFFECTS[timestamp].count = 0
    SIDE_EFFECTS[timestamp].count += 1
    return SIDE_EFFECTS[timestamp].value[SIDE_EFFECTS[timestamp].count - 1]

  return side_effect_list_patch


def get_side_effect_dict_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
) -> Callable:
  _ = callable_route, timestamp, module

  def side_effect_dict_patch(**kwargs) -> Any:
    store = {}
    for key, default in kwargs.items():
      patch_value = value.get(key, default)
      store.update({key: patch_value})
    return store

  return side_effect_dict_patch


def patch_module(
  module: ModuleType | None = None,
  route: str | None = None,
  name: str | None = None,
  value: Any | None = None,
  do_nothing: bool | None = None,
) -> sns:
  if not do_nothing:
    route = route or name
    module = set_object.main(
      parent=module,
      value=value,
      route=route, )
  return sns(module=module)


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
