#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc


MODULE_LOCATION = __file__
LOCALS = locals()


@dc.dataclass
class Data:
  a: int = 0
  b: int = 0
  result: int | None = None


def subtract_numbers(
  a: int | None = None,
  b: int | None = None,
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  return a - b


def subtract_dataclass(
  data: Data | None = None,
  # trunk-ignore(ruff/ARG001)
  a: None = None,
  # trunk-ignore(ruff/ARG001)
  b: None = None,
) -> Data:
  data.result = data.a - data.b
  return data


def raise_runtime_error(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> None:
  raise RuntimeError('run time error')


def main(
  data: Data | dict | None = None,
  a: int | float | None = None,
  b: int | float | None = None,
) -> int | Data:
  kind = 'dataclass' if data else 'numbers'
  handler = f'subtract_{kind}'
  handler = LOCALS[handler]
  return handler(
    data=data,
    a=a,
    b=b, )


def examples() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(
    # invoke='pytest',
    project_directory=MODULE_LOCATION, )


if __name__ == '__main__':
  examples()
