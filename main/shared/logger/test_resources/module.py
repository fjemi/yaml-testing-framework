#!.venv/bin/python3
# -*- coding: utf-8 -*-

import sys
import types
import typing


def function(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  return 1


def get_object(
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> types.ModuleType | typing.Callable:
  if args[0] == 'function':
    return function
  if args[0] == 'module':
    return sys
