#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

# trunk-ignore(ruff/F401)
from main.process.casts.handle_casting import main as handle_casting
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


def process_cast_arguments(
  cast_arguments: list | None = None,
  module: ModuleType | None = None,
  arguments: dict | None = None,
) -> sns:
  temp = main(
    casts=cast_arguments,
    module=module,
    object=arguments, )
  return sns(arguments=temp, _cleanup=['cast_arguments'])


def process_cast_output(
  cast_output: list | None = None,
  module: ModuleType | None = None,
  output: dict | None = None,
) -> sns:
  temp = main(
    casts=cast_output,
    module=module,
    object=output, )
  return sns(output=temp, _cleanup=['cast_output'])


def main(
  module: ModuleType | None = None,
  casts: list | None = None,
  object: Any | None = None,
) -> sns:
  data = locals()
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return get_object.main(parent=data, route='object')


def pre_processing(
  casts: list | None = None,
  module: ModuleType | str | None = None,
) -> sns:
  casts = casts or []
  module = module if not isinstance(module, str) else get_module.main(module=module)
  locals_ = locals()
  return sns(**locals_)


def process_casts(
  casts: list | None = None,
  module: ModuleType | None = None,
  object: Any | None = None,
) -> sns:
  locals_ = locals()

  for cast in casts:
    cast.update(locals_)
    data = independent.get_model(schema=CONFIG.schema.Cast, data=cast)
    data = independent.process_operations(
      operations=CONFIG.operations.process_casts,
      functions=LOCALS,
      data=data, )
    data = get_object.main(parent=data, route='object')
    locals_.update(dict(object=data))

  return sns(object=get_object.main(parent=locals_, route='object'))


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def get_cast_method(
  module: str | None = None,
  method: str | None = None,
) -> sns:
  name = str(method)
  method = get_object.main(
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
    temp = get_object.main(
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
    object_ = set_object.main(
      parent=object,
      value=temp_object,
      route=field, )
  return sns(object=object_)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.checks')


if __name__ == '__main__':
  examples()
