#!.venv/bin/python3
# -*- coding: utf-8 -*-


import importlib
import importlib.util
import os
from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import get_object, independent


MODULE = __file__
ROOT_DIR = os.path.normpath(os.path.abspath(os.path.curdir))
LOCALS = locals()

CONFIG = '''
  schema:
    Data:
      description: Data processed through the functions of the module
      fields:
      - name: location
        type: str
        default: null
        description: Path to the module
      - name: name
        default: null
        type: str
        description: Name to import module as
      - name: key
        default: null
        type: str
        description: Key to store module under in pool
      - name: pool
        default: False
        type: bool
        description: Flag to store module in pool
  operations:
    main:
    - format_module_name
    - get_module_from_pool
    - get_module_from_location
    - add_module_to_pool
  module_extensions:
  - .py
'''
CONFIG = independent.format_module_defined_config(
  config=CONFIG)

POOL = {}


def main(
  location: str | None = None,
  name: str | None = None,
  key: str | None = None,
  pool: bool | None = None,
) -> ModuleType | None:
  data = independent.get_model(schema=CONFIG.schema.Data, data=locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=CONFIG.operations.main,
    data=data, )
  return get_object.main(parent=data, route='module')


def format_module_name(
  name: str | None = None,
  location: str | None = None,
) -> sns | None:
  if location:
    name = os.path.normpath(location)
    name = name.replace(ROOT_DIR, '')
    name = os.path.splitext(location)[0]
    name = name.split(os.sep)
    name = '.'.join(name)
    return sns(name=name)

  name = name or 'app'
  if os.path.isfile(name):
    name = format_module_name(location=name)

  return sns(name=name)


def get_module_from_pool(
  location: str | None = None,
  pool: bool | None = None,
) -> sns:
  module = None
  if pool:
    module = POOL.get(location, None)
  return sns(module=module)


def get_module_from_location(
  location: str | None = None,
  name: str | None = None,
) -> sns:
  location = str(location)
  if os.path.exists(location) is False:
    return sns()

  spec = importlib.util.spec_from_file_location(name=name, location=location)
  module = importlib.util.module_from_spec(spec)

  try:
    spec.loader.exec_module(module)
  except Exception as e:
    _ = e

  return sns(module=module)


def add_module_to_pool(
  module: ModuleType,
  location: str,
  pool: bool,
) -> sns:
  if pool is True:
    global POOL
    POOL[location] = module
  return sns()


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
