#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Callable

from main.utils import get_config, logger


CONFIG = get_config.main()
LOCALS = locals()


def main(
  object: Any | None = None,
  method: Any | None = None,
  unpack: bool | None = None,
) -> sns:
  kind = type(object).__name__
  kind = CONFIG.kind_map.get(kind, 'any')
  flag = int((unpack or False) and kind != 'any')
  unpack = 'unpacked' * flag or 'packed'
  handler = f'cast_{kind}_{unpack}'
  handler = LOCALS.get(handler, cast_do_nothing)
  object_ = handler(object=object, method=method)
  return sns(object=object_)


def cast_do_nothing(
  object: Any | None = None,
  method: Callable | None = None,
) -> sns:
  _ = method
  return object


def cast_dict_unpacked(
  object: dict | None = None,
  method: Callable | None = None,
) -> sns | None:
  return method(**object)


def cast_dict_packed(
  object: dict | None = None,
  method: Callable | None = None,
) -> sns:
  return method(object)


def cast_nonetype_unpacked(
  object: None = None,
  method: Callable | None = None,
) -> sns | None:
  _ = object
  return method(**{})


def cast_nonetype_packed(
  object: None = None,
  method: Callable | None = None,
) -> sns | None:
  _ = object

  try:
    return method()
  except Exception as error:
    arguments = dict(object=object, method=method)
    logger.main(error=error, arguments=arguments)

  try:
    return method(**{})
  except Exception as error:
    arguments = dict(object=object, method=method)
    logger.main(error=error, arguments=arguments)


def cast_list_packed(
  object: list | tuple | None = None,
  method: Callable | None = None,
) -> sns:
  return method(object)


def cast_list_unpacked(
  object: list | tuple | None = None,
  method: Callable | None = None,
) -> sns:
  return method(*object)


def cast_any_packed(
  object: Any | None = None,
  method: Callable | None = None,
) -> sns:
  return method(object)


def cast_any_unpacked(
  object: Any | None = None,
  method: Callable | None = None,
) -> sns | None:
  return method(object)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
