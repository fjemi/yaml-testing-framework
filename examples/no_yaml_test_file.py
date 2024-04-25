#!.venv/bin/python3
# -*- coding: utf-8 -*-

MODULE = __file__


def main(*args, **kwargs) -> str:
  _ = args, kwargs

  return 'no yaml test file'


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
