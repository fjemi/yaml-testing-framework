#! /usr/bin/env python3

import dataclasses as dc


@dc.dataclass
class Data:
  a: int = 0
  b: int = 0
  result: int | None = None


def subtract_numbers(a: int, b: int) -> int:
  return a - b


def subtract_dataclass(data: Data) -> Data:
  data.result = data.a - data.b
  return data


# ruff: noqa: ARG001
def raise_runtime_error(*args, **kwargs) -> None:
  raise RuntimeError("run time error")


MAIN = {
  "dataclass": subtract_dataclass,
  "int": subtract_numbers,
}


# ruff: noqa: ARG001
def main(
  data: Data | dict | None = None,
  a: int | float | None = None,
  b: int | float | None = None,
) -> int | Data:
  cases = "dataclass" if data else "numbers"
  switcher = MAIN[cases]
  data = switcher(data=data)
  return data


if __name__ == '__main__':
  data = Data(1, 2)
  result = main(data)
  print(result)
