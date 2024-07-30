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


LOCALS = locals()

ROOT_DIR = os.path.abspath(os.curdir)
ROOT_DIR = os.path.normpath(ROOT_DIR)


CONFIG = '''
  environment:
    ROOT_DIR: ${YAML_TESTING_FRAMEWORK_ROOT_DIR}
    LOG_DIR: ${YAML_TESTING_FRAMEWORK_ROOT_DIR}
    DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}
    LOGGING_DISABLED: ${YAML_TESTING_FRAMEWORK_LOGGING_DISABLED}
  
  log_fields:
  - message
  - arguments
  - error
  - output
  - timestamps
  - location

  levels:
  - warning
  - error
  - info
  - debug

  formats:
  - yaml
  - json

  defaults:
    format: yaml
    level: debug
    debug: False
    standard_output: False
    enabled: True
'''
CONFIG = os.path.expandvars(CONFIG)
CONFIG = pyyaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)
CONFIG.environment = sns(**CONFIG.environment)

LOGGER = None


def main(
  format: str | None = None,
  level: str | None = None,
  debug: bool | None = None,
  enabled: bool | None = None,
  standard_output: bool = False,
  message: str | None = None,
  arguments: Any | None = None,
  output: Any | None = None,
  timestamps: dict | None = None,
  error: Exception | None = None,
) -> int:
  if LOGGER is None or enabled is False:
    return 0

  method = inspect.stack()[1][3]
  location = inspect.stack()[1].filename
  location = get_location_route(location=location, method=method)

  error = format_error(error=error)
  level = 'error' if error else level
  level = level if level in CONFIG.levels else 'debug'
  standard_output = False if not standard_output else standard_output

  log = get_log(locals_=locals())
  log = format_log(log=log, format=format)
  handle_log(
    log=log,
    level=level,
    error=error,
    debug=debug,
    standard_output=standard_output, )
  return 1


def get_location_route(
  location: str = '',
  method: str = '',
) -> str:
  location = os.path.normpath(location)
  location = location.replace(ROOT_DIR, '')
  location = os.path.splitext(location)[0]
  location = location.split(os.path.sep)
  location.append(method)
  return '.'.join(location)


def format_error(error: Exception | None = None) -> dict | None:
  if not isinstance(error, Exception):
    return error

  name = type(error).__name__
  description = str(error)
  trace = []

  tb = error.__traceback__

  while tb is not None:
    store = dict(
      file=tb.tb_frame.f_code.co_filename,
      name=tb.tb_frame.f_code.co_name,
      line=tb.tb_lineno, )
    trace.append(store)
    tb = tb.tb_next

  return dict(
    name=name,
    description=description,
    trace=trace, )


def get_log(locals_: dict = {}) -> sns:
  store = {}

  for field in CONFIG.log_fields:
    value = locals_.get(field, None)
    if value is None:
      continue
    store.update({field: value})

  level = locals_.get('level', 'info')
  return {level: store}


def format_as_json(log: dict) -> str:
  return json.dumps(log, default=set_default)


def format_as_yaml(log: dict) -> str:
  return pyyaml.dump(log, default_flow_style=False)


def format_log(
  format: str = '',
  log: Any | None = None,
) -> str:
  format_ = str(format).lower()
  format_ = format_ if format_ in CONFIG.formats else 'yaml'
  formatter = f'format_as_{format_}'
  formatter = LOCALS[formatter]

  try:
    log = formatter(log=log)
  except Exception as error:
    _ = error
    log = str(log)

  return log


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def handle_log(
    log: dict = {},
    level: str = '',
    error: Exception | None = None,
    debug: bool = False,
    standard_output: bool = False,
) -> int:
  flags = True in [
    isinstance(error,Exception),
    level == 'error', ]

  debug = debug or CONFIG.environment.DEBUG

  flags = True in [flags, debug, standard_output, ]
  standard_output = True if flags else standard_output

  a = write_to_log(level=level, log=log)
  b = write_to_cli(
    debug=debug,
    standard_output=standard_output,
    log=log, )
  return a + b


def write_to_log(
  level: str = '',
  log: Any | None = None,
) -> int:
  method = getattr(
    LOGGER,
    str(level).lower(),
    LOGGER.debug if LOGGER else do_nothing, )
  method(f'{log}\n')
  return 1


def write_to_cli(
  standard_output: bool = False,
  debug: bool = False,
  error: dict | None = None,
  level: str = '',
  log: Any | None = None,
) -> int:
  flags = sum([
    standard_output is True,
    debug is True,
    error is not None,
    level in ['error', 'exception'],
  ]) > 0
  status = 0
  if flags:
    status = 1
    print(log)
  return status




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
    except Exception as error:
      print(error)
      return object.__dict__

    if dc.is_dataclass(object):
      return dc.asdict(object)

    if hasattr(object, '__dict__'):
      return object.__dict__

  print(f'Cannot serialize object of type {type(object).__name__}')
  return str(object)


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
  logging_flag: bool,
  project_path: str,
) -> sns:
  data = sns(status=1)
  if logging_flag:
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

  invoke_testing_method.main('.')


if __name__ == '__main__':
  examples()
