#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

# trunk-ignore(ruff/F401)
from process.casts.handle_casting import main as handle_casting
from utils import get_config, get_object, independent, set_object


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
    data.module = module
    data.object = object_
    data = independent.process_operations(
      operations=CONFIG.main_operations,
      functions=LOCALS,
      data=data, )
    object_ = data.object

  return object_


def get_cast_method(
  module: str | None = None,
  method: str | None = None,
) -> sns:
  data = sns(method_name=method)
  data.method = get_object.main(parent=module, name=method)
  if not isinstance(data.method, Callable):
    module = getattr(module, '__file__', None)
    data.log = sns(
      level='error',
      message=f'Method {data.method_name} not in module located at {module}', )
  return data


def get_temp_object(
  object: Any | None = None,
  field: str | None = None
) -> sns:
  data = sns(temp_object=object)
  data.temp_object = get_object.main(parent=data.temp_object, name=field)
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
  from utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
