#!.venv/bin/python3
# -*- coding: utf-8 -*-


def main(*args, **kwargs) -> str:
  _ = args, kwargs

  return 'no yaml test file'


def examples() -> None:
  from main.utils import invoke

  invoke.main()


if __name__ == '__main__':
  examples()
