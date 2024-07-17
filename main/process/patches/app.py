#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable

from main.utils import (
  get_config,
  get_module,
  independent,
  objects,
)


CONFIG = get_config.main()
LOCALS = locals()

SIDE_EFFECTS = {}


def main(
  patches: list | None = None,
  module: ModuleType | None = None,
) -> sns:
  data = independent.get_model(schema=CONFIG.schema.Entry, data=locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return data.result


def process_patches(
  patches: list | None = None,
  module: ModuleType | None = None,
) -> sns:
  patches = patches or []

  for item in patches:
    data = independent.get_model(schema=CONFIG.schema.Patch, data=item)
    data.module = module
    data = independent.process_operations(
      operations=CONFIG.operations.process_patches,
      functions=LOCALS,
      data=data, )
    module = data.module

  result = sns(module=module)
  return sns(result=result)


def pre_processing(
  module: ModuleType | None = None,
  resource: ModuleType | None = None,
  route: str | None = None,
) -> sns:
  resource = resource or module
  resource = get_module.main(
    module=resource,
    default=module, ).module

  route = str(route)
  if route.find('.') == 0:
    route = route[1:]
  original = objects.get(
    parent=module,
    route=route,
    default=None, )

  timestamp = independent.get_timestamp()

  return sns(
    resource=resource,
    original=original,
    timestamp=timestamp,
    route=route, )


def get_patch_method(
  method: str | None = None,
  value: Any | None = None,
  timestamp: int | None = None,
  resource: ModuleType | None = None,
  callable_route: str | None = None,
  original: Any | None = None,
) -> sns:
  route = f'get_{method}_patch_method'
  method = objects.get(
    parent=LOCALS,
    route=route,
    default=do_nothing, )
  value = method(
    value=value,
    resource=resource,
    callable_route=callable_route,
    original=original,
    timestamp=timestamp, )
  return sns(value=value)


def do_nothing(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  resource: ModuleType | None = None,
  original: Any | None = None,
) -> None:
  _ = value, callable_route, timestamp, resource
  return original


def get_value_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  resource: ModuleType | None = None,
  original: Any | None = None,
) -> Any:
  _ = timestamp, callable_route, resource

  def patch() -> Any:
    return value

  return patch()


def get_callable_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  resource: ModuleType | None = None,
  original: Any | None = None,
) -> Callable:
  _ = timestamp

  def patch(*args, **kwargs) -> Any:
    _ = args, kwargs

    return value

  temp = objects.get(
    parent=resource,
    route=callable_route,
    default=patch, )
  temp.__wrapped__ = original
  temp.__method__ = 'callable'

  return temp


def get_side_effect_list_patch_method(
  value: list | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  resource: ModuleType | None = None,
  original: Any | None = None,
) -> Callable:
  _ = callable_route, resource

  global SIDE_EFFECTS

  data = sns(value=value, count=0)
  SIDE_EFFECTS[timestamp] = independent.get_model(
    data=data,
    schema=CONFIG.schema.Patch_Side_Effect_List, )

  def patch(*args, **kwargs) -> Any:
    _ = args, kwargs

    n = len(SIDE_EFFECTS[timestamp].value)
    if SIDE_EFFECTS[timestamp].count == n:
      SIDE_EFFECTS[timestamp].count = 0
    SIDE_EFFECTS[timestamp].count += 1
    return SIDE_EFFECTS[timestamp].value[SIDE_EFFECTS[timestamp].count - 1]

  patch.__wrapped__ = original
  patch.__method__ = 'side_effect_list'

  return patch


def get_side_effect_dict_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  resource: ModuleType | None = None,
  original: Any | None = None,
) -> Callable:
  _ = callable_route, timestamp, resource

  def patch(**kwargs) -> Any:
    store = {}
    for key, default in kwargs.items():
      patch_value = value.get(key, default)
      store.update({key: patch_value})
    return store

  patch.__wrapped__ = original
  patch.__method__ = 'side_effect_dict'

  return patch


def patch_module(
  module: ModuleType | None = None,
  route: str | None = None,
  value: Any | None = None,
) -> sns:
  temp = objects.update(
    parent=module,
    value=value,
    route=route, )
  return sns(module=temp)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
