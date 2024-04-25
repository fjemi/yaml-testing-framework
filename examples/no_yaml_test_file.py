#!.venv/bin/python3
# -*- coding: utf-8 -*-

MODULE = __file__


def main(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> str:
  return 'no yaml test file'


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
