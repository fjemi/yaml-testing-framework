#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import modules


def wrapper_modules(
  module: str = '',
  location: str = '',
  parent: str = '',
  resource: str = '',
) -> ModuleType:
  module = module or location or parent or resource
  return modules.main(location=module).module
