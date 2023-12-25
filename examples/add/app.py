#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc


MODULE = __file__
LOCALS = locals()


@dc.dataclass
class Data:
  a: int = 0
  b: int = 0
  result: int = 0


def add_numbers(
  a: int | None = None,
  b: int | None = None,
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  return a + b


def add_dataclass(
  data: Data | None = None,
  # trunk-ignore(ruff/ARG001)
  a: None = None,
  # trunk-ignore(ruff/ARG001)
  b: None = None,
) -> Data:
  data.result = data.a + data.b
  return data


def main(  # ruff: noqa: ARG001
  data: Data | None = None,
  a: int | float | None = None,
  b: int | float | None = None,
) -> int | Data:
  kind = 'dataclass' if data else 'numbers'
  handler = f'add_{kind}'
  handler = LOCALS[handler]
  return handler(
    data=data,
    a=a,
    b=b, )


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
