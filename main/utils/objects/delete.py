#!.venv/bin/python3
# -*- coding: utf-8 -*-


from typing import Any


def main(
  parent: Any | None = None,
  route: str | None = None,
) -> Any | None:
  if parent is None:
    return parent

  route = str(route)

  if isinstance(parent, dict):
    parent[route] = None
    del parent[route]
    return parent

  setattr(parent, route, None)
  delattr(parent, route)
  return parent


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
