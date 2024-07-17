#!.venv/bin/python3
# -*- coding: utf-8 -*-


import types

from main.utils import get_module


def wrapper_get_module(module: str | None = None) -> types.ModuleType:
  return get_module.main(location=module).module
