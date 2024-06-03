#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

from main.process.casts import handle_casting
from main.utils import (
  get_config,
  get_module,
  get_object,
  independent,
  set_object,
)


MODULE = __file__
LOCALS = locals()

CONFIG = get_config.main(module=MODULE)


def main(
  module: ModuleType | None = None,
  casts: List[dict | sns] | None = None,
  object: Any | None = None,
) -> sns:
  object_ = object
  casts = casts or []

  for cast in casts:
    data = sns(**cast)
    data.module = get_module_wrapper(module=module)
    data.object = object_
    data = independent.process_operations(
      operations=CONFIG.operations.main,
      functions=LOCALS,
      data=data, )
    object_ = data.object

  return object_


def handle_casting_wrapper(
  temp_object: Any,
  method: Any,
  unpack: bool,
) -> sns:
  return handle_casting.main(
    temp_object=temp_object,
    method=method,
    unpack=unpack, )


def get_module_wrapper(module: ModuleType | str) -> ModuleType | None:
  if isinstance(module, ModuleType):
    return module
  if isinstance(module, str):
    return get_module.main(location=module, pool=False)


def get_cast_method(
  module: str | None = None,
  method: str | None = None,
) -> sns:
  name = str(method)
  method = get_object.main(parent=module, route=name)
  if isinstance(method, Callable):
    return sns(method=method)

  method = get_object.main(parent=module, route='pass_through')
  module = getattr(module, '__file__', None)
  log = sns(
    level='error',
    message=f'Cast method {name} not in module {module}', )

  return sns(method=method, log=log)


def get_temp_object(
  object: Any | None = None,
  field: str | None = None
) -> sns:
  data = sns(temp_object=object)
  data.temp_object = get_object.main(parent=data.temp_object, route=field)
  if data.temp_object is None:
    data.log = f'Field {field} not in object of type {type(object).__name__}'
  return data


def reset_object(
  temp_object: Any | None = None,
  object: Any | None = None,
  field: str | None = None,
) -> sns:
  if not field:
    object_ = temp_object
  elif field:
    object_ = set_object.main(
      parent=object,
      value=temp_object,
      route=field, )
  return sns(object=object_, temp_object=None)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
