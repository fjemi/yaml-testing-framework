#!.venv/bin/python3
# -*- coding: utf-8 -*-


import nest_asyncio


def allow_nested_event_loops() -> int:
  nest_asyncio.apply()
  return 1


allow_nested_event_loops()


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
