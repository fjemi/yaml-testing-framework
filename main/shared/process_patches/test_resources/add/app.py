#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses


LOCALS = locals()


@dataclasses.dataclass
class Data:
  a: int = 0
  b: int = 0


def add_numbers(_locals: dict) -> int:
  return _locals['a'] + _locals['b']


def add_dataclass(_locals: dict) -> int:
  data = _locals['data']
  return data.a + data.b


MAIN = {
  'dataclass': add_dataclass,
  'int': add_numbers,
}


def main(
  data: Data | dict | None = None,
  a: int | float | None = None,
  b: int | float | None = None,
) -> int:
  cases = 'dataclass' if data else 'numbers'
  switcher = MAIN[cases]
  data = switcher(_locals=locals())
  return data


def example() -> None:
  import asyncio

  from logger.app import main as logger


  data = Data(1, 2)
  data = main(data)
  asyncio.run(logger(
    data=data,
    standard_output=True, ))


if __name__ == '__main__':
  example()
