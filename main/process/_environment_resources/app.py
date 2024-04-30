#!.venv/bin/python3
# -*- coding: utf-8 -*-

import types

from main.utils import get_module


MODULE = __file__


def get_module_wrapper(module: str | None = None) -> types.ModuleType:
  return get_module.main(location=module, pool=False)
