#!.venv/bin/python3
# -*- coding: utf-8 -*-


import nest_asyncio


def allow_nested_event_loops() -> int:
  nest_asyncio.apply()
  return 1


allow_nested_event_loops()


def examples() -> None:
  from main.utils import invoke

  invoke.main()


if __name__ == '__main__':
  examples()
