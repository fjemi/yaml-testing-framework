#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Iterable, Mapping


LOCALS = locals()


def main(
  object: Any | None = None,
  route: str | None = None,
) -> Any | None:
  object_ = object
  type_ = get_type(object_=object_)
  handler = f'delete_from_{type_}'
  handler = LOCALS[handler]
  return handler(object_=object_, route=route)


def get_type(object_: Any | None = None) -> str:
  types = dict(
    none=object_ is None,
    mapping=isinstance(object_, Mapping),
    iterable=isinstance(object_, Iterable),
    any=True, )
  for type_, value in types.items():
    if value:
      return type_


def delete_from_none(
  object_: None = None,
  route: str | None = None,
) -> dict:
  _ = object_, route


def delete_from_mapping(
  object_: dict | None = None,
  route: str | None = None,
) -> dict:
  object_.update({route: None})
  del object_[route]
  return object_


def delete_from_any(
  object_: Any | None = None,
  route: str | None = None,
) -> Any:
  setattr(object_, route, None)
  delattr(object_, route)
  return object_


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
