#!.venv/bin/python3
# -*- coding: utf-8 -*-


import nest_asyncio


MODULE = __file__


def allow_nested_event_loops(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  nest_asyncio.apply()
  return 1


allow_nested_event_loops()


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(module=MODULE)


if __name__ == '__main__':
  example()
