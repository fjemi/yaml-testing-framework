#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Iterable


LOCALS = locals()

TWO = 2


def main(
  parent: Any | None = None,
  route: str | None = None,
  default: Any | None = None,
) -> Any:
  if parent is None or not isinstance(route, str):
    return default or parent

  routes = str(route).strip().split('.')

  for route in routes:
    parent = get_child(
      default=default,
      parent=parent,
      route=route, )

  return parent


def get_child_from_iterable(
  parent: Iterable | None = None,
  route: int | str | None = None,
  default: Any | None = None,
) -> Iterable | None:

  def get_index(
    item: Any | None = None,
    i: int | None = None,
  ) -> int | None:
    _ = i
    if item.isdigit():
      return int(item)

  parameters = str(route).split('|')
  parameters = [get_index(item=item, i=i) for i, item in enumerate(parameters)]
  temp = slice(*parameters)
  return parent[temp] or default


def get_parent_kind(parent: Any | None = None) -> str:
  kinds = [
    'dict' * int(isinstance(parent, dict)),
    'none' * int(parent is None),
    'iterable' * int(isinstance(parent, Iterable)), ]

  kind = 'any'
  for item in kinds:
    if item:
      kind = item
      break

  return kind


def get_child_from_any(
  parent: Any | None = None,
  route: str | None = None,
  default: Any | None = None,
) -> Any:
  return getattr(parent, route, default)


def get_child_from_dict(
  parent: dict | None = None,
  route: str | None = None,
  default: Any | None = None,
) -> Any:
  return parent.get(route, default)


def get_child_from_none(
  parent: None = None,
  route: str | None = None,
  default: Any | None = None,
) -> Any:
  _ = parent, route
  return default


def get_child(
  parent: Any | None = None,
  route: str | None = None,
  default: Any | None = None,
) -> sns:
  kind = get_parent_kind(parent=parent)
  handler = f'get_child_from_{kind}'
  handler = LOCALS[handler]
  return handler(
    parent=parent,
    route=route,
    default=default, )


def examples() -> None:
  from main.utils import invoke

  invoke.main()


if __name__ == '__main__':
  examples()
