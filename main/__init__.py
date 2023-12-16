#!.venv/bin/python3
# -*- coding: utf-8 -*-


import nest_asyncio


def allow_nested_event_loops(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  nest_asyncio.apply()
  return 1


allow_nested_event_loops()
