#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

from main.utils import get_config, get_object, independent, set_object


MODULE = __file__
CONFIG = get_config.main(module=MODULE)
LOCALS = locals()

SIDE_EFFECTS = {}


def main(
  patches: List[dict | sns] | None = None,
  module: ModuleType | None = None,
) -> sns:
  patches = patches or []

  for item in patches:
    data = sns(patch=item, module=module)
    data = independent.process_operations(
      operations=CONFIG.operations.main,
      functions=LOCALS,
      data=data, )
    module = data.module

  return sns(_cleanup=['patches'], module=module)


def pre_processing(
  patch: dict | None = None,
  module: ModuleType | None = None,
) -> sns:
  patch = independent.get_model(
    schema=CONFIG.schema.Patch, data=patch, )
  patch.module = module
  patch.timestamp = independent.get_timestamp()

  patch.route = str(patch.route)
  if patch.route.find('.') == 0:
    patch.route = patch.route[1:]

  patch.original = get_object.main(parent=module, route=patch.route)
  return patch


def get_patch_method(
  method: str | None = None,
  value: Any | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  callable_route: str | None = None,
  original: Any | None = None,
) -> sns:
  handler = f'get_{method}_patch_method'
  handler = LOCALS.get(handler, None) or do_nothing
  value = handler(
    value=value,
    module=module,
    callable_route=callable_route,
    original=original,
    timestamp=timestamp, )
  log = None
  if value is None:
    log = sns(
      message=f'No patch method {method} found',
      level='error', )
  return sns(log=log, value=value)


def do_nothing(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  original: Any | None = None,
) -> Any:
  _ = value, timestamp, callable_route, module, original
  return original


def get_value_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  original: Any | None = None,
) -> Any:
  _ = timestamp, callable_route, module

  def patch() -> Any:
    return value

  return patch()


def get_callable_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  original: Any | None = None,
) -> Callable:
  _ = timestamp

  def patch(*args, **kwargs) -> Any:
    _ = args, kwargs

    return value

  temp = get_object.main(
    parent=module,
    route=callable_route,
    default=patch, )
  temp.__wrapped__ = original
  temp._method = 'callable'

  return temp


def get_side_effect_list_patch_method(
  value: list | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  original: Any | None = None,
) -> Callable:
  _ = callable_route, module

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
  patch._method = 'side_effect_list'

  return patch


def get_side_effect_dict_patch_method(
  value: Any | None = None,
  callable_route: str | None = None,
  timestamp: int | None = None,
  module: ModuleType | None = None,
  original: Any | None = None,
) -> Callable:
  _ = callable_route, timestamp, module

  def patch(**kwargs) -> Any:
    store = {}
    for key, default in kwargs.items():
      patch_value = value.get(key, default)
      store.update({key: patch_value})
    return store

  patch.__wrapped__ = original
  patch._method = 'side_effect_dict'

  return patch


def patch_module(
  module: ModuleType | None = None,
  route: str | None = None,
  value: Any | None = None,
) -> sns:
  module = set_object.main(
    parent=module,
    value=value,
    route=route, )
  return sns(module=module)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location=MODULE)


if __name__ == '__main__':
  examples()
