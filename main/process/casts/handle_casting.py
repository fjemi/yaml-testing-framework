#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Callable

from main.utils import get_config


MODULE = __file__
CONFIG = get_config.main(module=MODULE)
LOCALS = locals()


def main(
  temp_object: Any | None = None,
  method: Any | None = None,
  unpack: bool | None = None,
) -> sns:
  kind = type(temp_object).__name__
  kind = CONFIG.kind_map.get(kind, 'any')
  flag = int((unpack or False) and kind != 'any')
  unpack = 'unpacked' * flag or 'packed'
  handler = f'cast_{kind}_{unpack}'
  handler = LOCALS.get(handler, cast_do_nothing)

  data = sns(method=None)
  data.temp_object = handler(temp_object=temp_object, method=method)
  return data


def cast_do_nothing(
  temp_object: Any | None = None,
  method: Callable | None = None,
) -> sns:
  _ = method
  return temp_object


def cast_dict_unpacked(
  temp_object: dict | None = None,
  method: Callable | None = None,
) -> sns | None:
  return method(**temp_object)


def cast_dict_packed(
  temp_object: dict | None = None,
  method: Callable | None = None,
) -> sns:
  return method(temp_object)


def cast_nonetype_unpacked(
  temp_object: None = None,
  method: Callable | None = None,
) -> sns | None:
  _ = temp_object
  return method(**{})


def cast_nonetype_packed(
  temp_object: None = None,
  method: Callable | None = None,
) -> sns | None:
  _ = temp_object

  try:
    return method(None)
  except Exception as e:
    _ = e
    return method(**{})


def cast_list_packed(
  temp_object: list | tuple | None = None,
  method: Callable | None = None,
) -> sns:
  return method(temp_object)


def cast_list_unpacked(
  temp_object: list | tuple | None = None,
  method: Callable | None = None,
) -> sns:
  return method(*temp_object)


def cast_any_packed(
  temp_object: Any | None = None,
  method: Callable | None = None,
) -> sns:
  return method(temp_object)


def cast_any_unpacked(
  temp_object: Any | None = None,
  method: Callable | None = None,
) -> sns | None:
  try:
    return method(**temp_object)
  except Exception as e:
    _ = e

  try:
    return method(*temp_object)
  except Exception as e:
    _ = e


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
