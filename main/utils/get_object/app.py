#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Iterable


MODULE = __file__

TWO = 2

def main(
  parent: Any | None = None,
  route: str | None = None
) -> Any:
  if parent is None or not isinstance(route, str):
    return parent

  data = sns(parent=parent, child=None)
  routes = route.strip().split('.')

  for child in routes:
    data.child = child
    data = get_child_object(**data.__dict__)

  return data.parent


def slice_iterable(
  parent: Iterable | None = None,
  child: int | str | None = None,
) -> Iterable | None:

  def inner(
    item: Any | None = None,
    i: int | None = None,
  ) -> int | None:
    if item.isdigit():
      return int(item)
    elif i == TWO and item is None:
      return 1

  parameters = str(child).split('|')
  parameters = [inner(item=item, i=i) for i, item in enumerate(parameters)]
  return parent[slice(*parameters)]


def get_child_object(
  parent: Any | None = None,
  child: str | None = None,
) -> sns:
  kinds = [
    'dict' * int(isinstance(parent, dict)),
    'none' * int(parent is None),
    'iterable' * int(isinstance(parent, Iterable)), ]

  kind = 'other'
  for item in kinds:
    if item:
      kind = item
      break

  if kind == 'other':
    child = getattr(parent, child, None)
  elif kind == 'dict':
    child = parent.get(child, None)
  elif kind == 'iterable':
    child = slice_iterable(parent=parent, child=child)
  elif kind == 'none':
    child = None

  return sns(parent=child, child=None)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
