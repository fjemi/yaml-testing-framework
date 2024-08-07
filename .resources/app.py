#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import get_module


def wrapper_get_module(
  module: str = '',
  location: str = '',
  parent: str = '',
  resource: str = '',
) -> ModuleType:
  module = module or location or parent or resource
  return get_module.main(location=module).module
