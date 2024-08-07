#!.venv/bin/python3
# -*- coding: utf-8 -*-


def add(
  a: int | None = None,
  b: int | None = None,
) -> int:
  return a + b


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
