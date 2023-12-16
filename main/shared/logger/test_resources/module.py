#!.venv/bin/python3
# -*- coding: utf-8 -*-


import sys
import typing
import types


def function(data: None = None) -> int:
  return 1


def get_object(
  *args,
  **kwargs,
) -> types.ModuleType | typing.Callable:
  if args[0] == 'function':
    return function
  
  if args[0] == 'module':
    return sys
