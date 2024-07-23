#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

from main.process.casts import handle_casting
from main.utils import (
  get_config,
  get_module,
  objects,
  independent,
  logger,
)


LOCALS = locals()

CONFIG = get_config.main()


def process_cast_arguments(
  cast_arguments: list | None = None,
  module: ModuleType | None = None,
  arguments: dict | None = None,
) -> sns:
  temp = main(
    casts=cast_arguments,
    module=module,
    object=arguments, ).object
  return sns(arguments=temp)


def process_cast_output(
  cast_output: list | None = None,
  module: ModuleType | None = None,
  output: dict | None = None,
) -> sns:
  temp = main(
    casts=cast_output,
    module=module,
    object=output, ).object
  return sns(output=temp)


def main(
  casts: list | None = None,
  module: ModuleType | None = None,
  object: Any | None = None,
) -> sns:
  casts = casts or []
  locals_ = sns(module=module, object=object)
  
  for item in casts:
    item.update(locals_.__dict__)
    data = independent.get_model(schema=CONFIG.schema.Main, data=item)
    data = independent.process_operations(
      operations=CONFIG.operations.main,
      functions=LOCALS,
      data=data, )
    locals_.object = data.object

  return sns(object=locals_.object)


def method_does_not_exist(method: str) -> None:
  logger.main(level='warning', message='Method {method} does not exist')

  def method_does_not_exist_inner(*args, **kwargs) -> None:
    _ = args, kwargs

  return method_does_not_exist_inner


def get_method(
  module: ModuleType | None = None,
  resource: str = '',
  method: str = '',
) -> sns:
  module = resource or module
  module = get_module.main(module=module, default=module).module
  route = str(method)
  method = objects.get(parent=module, route=route)
  method = method if isinstance(method, Callable) else method_does_not_exist(method=route)
  return sns(method=method)


def get_object(
  object: Any | None = None,
  field: str = '',
  method: Callable | None = None,
  unpack: bool = False,
) -> sns:
  temp = object if not field else objects.get(
    parent=object,
    route=field, )
  temp = handle_casting.main(
    object=temp,
    method=method,
    unpack=unpack, ).object
  return sns(temp=temp)


def reset_object(
  temp: Any | None = None,
  object: Any | None = None,
  field: str | None = None,
) -> sns:
  object_ = temp if not field else objects.update(
    parent=object,
    value=temp,
    route=field, )
  return sns(object=object_)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main('.')


if __name__ == '__main__':
  examples()
