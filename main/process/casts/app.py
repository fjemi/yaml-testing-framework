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
    object=arguments, )
  return sns(arguments=temp)


def process_cast_output(
  cast_output: list | None = None,
  module: ModuleType | None = None,
  output: dict | None = None,
) -> sns:
  temp = main(
    casts=cast_output,
    module=module,
    object=output, )
  return sns(output=temp)


def main(
  module: ModuleType | None = None,
  casts: list | None = None,
  object: Any | None = None,
) -> sns:
  data = independent.get_model(schema=CONFIG.schema.Main, data=locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return data.result


def process_casts(
  casts: list | None = None,
  module: ModuleType | None = None,
  object: Any | None = None,
) -> sns:
  casts = casts or []
  data = sns(module=module, object=object)
  
  for item in casts:
    data = format_data(
      object=object,
      item=item,
      module=module, )
    data = independent.process_operations(
      operations=CONFIG.operations.process_casts,
      functions=LOCALS,
      data=data, )

  return sns(result=data.object)


def format_data(
  module: ModuleType | str | None = None,
  object: Any | None = None,
  item: dict | None = None,
) -> sns:
  cast = independent.get_model(schema=CONFIG.schema.Cast, data=item)
  cast.object = object
  cast.module = cast.module or module
  cast.module = get_module.main(module=cast.module, default=cast.module).module
  return cast


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def get_cast_method(
  module: str | None = None,
  method: str | None = None,
) -> sns:
  name = str(method)
  method = objects.get(
    parent=module,
    route=name,
    default=do_nothing, )
  return sns(method=method)


def get_temp_object(
  object: Any | None = None,
  field: str | None = None
) -> sns:
  temp = object
  if field:
    temp = objects.get(
      parent=temp,
      route=field,
      default=temp, )
  return sns(temp_object=temp)


def reset_object(
  temp_object: Any | None = None,
  object: Any | None = None,
  field: str | None = None,
) -> sns:
  object_ = temp_object
  if field:
    object_ = objects.update(
      parent=object,
      value=temp_object,
      route=field, )
  return sns(object=object_)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
