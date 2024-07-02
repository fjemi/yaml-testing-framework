#!.venv/bin/python3
# -*- coding: utf-8 -*-


import importlib
import importlib.util
import os
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any

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
      - name: module
        type: str
        default: null
        description: Path to the module
      - name: name
        default: null
        type: str
        description: Name to import module as
      - name: module_route
        default: null
        type: str
        description: Name to import module as
      - name: flag
        default: False
        type: bool
        description: >
          True if either the `location` or `module` argument passed into the
          main function is a module, otherwise false
      - name: default
        default: null
        type: Any
        description: Value to return if module does not exist

  operations:
    main:
    - pre_processing
    - format_module_name
    - get_module_from_location
    - post_processing

  module_extensions:
  - .py
'''
CONFIG = independent.format_module_defined_config(
  config=CONFIG)


def main(
  module: ModuleType | str | None = None,
  location: str | None = None,
  name: str | None = None,
  default: Any | None = None,
) -> sns:
  data = independent.get_model(schema=CONFIG.schema.Data, data=locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=CONFIG.operations.main,
    data=data, )
  return data.result


def pre_processing(
  location: str | ModuleType | None = None,
  module: str | ModuleType | None = None,
) -> sns:
  location = location or module

  if True not in [
    isinstance(location, str),
    location is None,
  ]:
    flag = True
    return sns(
      location=location.__file__,
      module=location,
      flag=True, )

  return sns(location=location, flag=False)


def format_module_name(
  name: str | None = None,
  location: str | None = None,
  flag: bool | None = None,
) -> sns | None:
  if flag:
    return sns(name=location.__name__)

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


def get_module_from_location(
  location: str | None = None,
  name: str | None = None,
  flag: bool | None = None,
  default: Any | None = None,
) -> sns:
  if flag:
    return sns()

  location = str(location)
  if not os.path.exists(location):
    return sns()

  spec = importlib.util.spec_from_file_location(name=name, location=location)
  module = importlib.util.module_from_spec(spec)

  try:
    spec.loader.exec_module(module)
  except Exception as e:
    _ = e
    module = default

  return sns(module=module)


def post_processing(
  module: ModuleType | None = None,
  default: Any | None = None,
) -> sns:
  module = default if not isinstance(module, ModuleType) else module
  result = sns(module=module)
  return sns(result=result)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
