#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import inspect
import json
import logging
import os
import time
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable

import yaml as pyyaml


MODULE = __file__
LOCALS = locals()

ROOT_DIR = os.path.abspath(os.curdir)


CONFIG = '''
  environment:
    ROOT_DIR: ${YAML_TESTING_FRAMEWORK_ROOT_DIR}
    LOG_DIR: ${YAML_TESTING_FRAMEWORK_LOG_DIR}
    DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}
    LOGGING_DISABLED: ${YAML_TESTING_FRAMEWORK_LOGGING_DISABLED}
  operations:
    main:
    - convert_data
    - log_data
    - write_output_to_terminal
  default_arguments:
    format: yaml
    standard_output: false
    debug: false
    level: info
  defaults:
    format: yaml
    standard_output: false
    debug: false
    level: info
  log_fields:
  - message
  - operation
  - timestamps
  - output
  - exception
  levels:
  - debug
  - info
  - error
  - warning
'''
CONFIG = os.path.expandvars(CONFIG)
CONFIG = pyyaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)
CONFIG.environment = sns(**CONFIG.environment)
CONFIG.operations = sns(**CONFIG.operations)

LOGGER = None


def main(
  format: str | None = None,
  level: str | None = None,
  debug: bool | None = None,
  enabled: bool | None = None,
  standard_output: bool = False,
  log: Any | None = None,
) -> int:
  conditions = [
    LOGGER is None,
    enabled is False,
  ]
  if True in conditions:
    return 0

  log.location = getattr(log, 'location', None, ) or inspect.stack()[1].filename
  log.operation = getattr(log, 'operation', None, ) or inspect.stack()[1][3]
  format_ = format or CONFIG.defaults.get('format')
  format_method = LOCALS.get(f'format_as_{format_}', format_as_yaml)
  log = format_method(log={level: log.__dict__})

  logging_method = getattr(LOGGER, level.lower(), LOGGER.debug)
  logging_method(log)
  if debug or standard_output:
    print(log)

  return 1


# trunk-ignore(ruff/PLR0911)
def set_default(object: Any) -> Any:
  if isinstance(object, ModuleType):
    return object.__file__

  if isinstance(object, Callable):
    return object.__name__

  if isinstance(object, Exception):
    return sns(
      exception=type(object).__name__,
      description=str(object), ).__dict__

  if type(object).__name__.lower() == 'Test':
    if isinstance(object.module, ModuleType):
      object.module = object.module.__file__

    if isinstance(object.function, Callable):
      object.function = object.function.__name__

    try:
      return dc.asdict(object)
    except Exception as e:
      _ = e
      return object.__dict__

    if dc.is_dataclass(object):
      return dc.asdict(object)

    if isinstance(object, sns):
      return object.__dict__

  print(f'Cannot serialize object of type {type(object).__name__}')
  return str(object)


def format_as_json(log: dict) -> str:
  try:
    return json.dumps(log, default=set_default)
  except Exception as e:
    _ = e
    return f'{log}\n'


def format_as_yaml(log: dict) -> str:
  try:
    return pyyaml.dump(log, default_flow_style=False)
  except Exception as e:
    _ = e
    return str(log)


def get_timestamp() -> float:
  return time.time()


def get_log_file_location(
  project_path: str,
  root_directory: str,
) -> str:
  filename = project_path.replace(root_directory, '')
  filename = os.path.splitext(filename)[0]
  filename = filename.replace(os.path.sep, '.')
  filename = f'root{filename}'
  if filename.find('.') == len(filename) - 1:
    filename = filename[:-1]

  directory = CONFIG.environment.LOG_DIR or f'{ROOT_DIR}/.logs'
  os.makedirs(name=directory, exist_ok=True)
  location = f'{directory}/{filename}.log'
  location = os.path.normpath(location)
  return location


def get_logger(location: str) -> logging.Logger:
  logger = logging.getLogger(location)
  logger.setLevel(logging.DEBUG)
  handler = logging.FileHandler(location, mode='w')
  formatter = logging.Formatter('%(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger


def create_logger(
  logging_enabled: bool,
  project_path: str,
) -> sns:
  data = sns(status=1)
  if logging_enabled:
    global LOGGER
    location = get_log_file_location(
      project_path=project_path,
      root_directory=ROOT_DIR, )
    LOGGER = get_logger(location=location)
    return data

  data.status = 0
  return data


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
