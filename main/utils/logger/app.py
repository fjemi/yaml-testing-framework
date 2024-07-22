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


CONFIG = '''
  environment:
    ROOT_DIR: ${YAML_TESTING_FRAMEWORK_ROOT_DIR}
    LOG_DIR: ${YAML_TESTING_FRAMEWORK_LOG_DIR}
    DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}
    LOGGING_DISABLED: ${YAML_TESTING_FRAMEWORK_LOGGING_DISABLED}
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
  log: dict | sns = None,
) -> int:
  if LOGGER is None or enabled is False:
    return 0

  log = format_log_as_sns(log=log)
  log.location = inspect.stack()[1].filename
  log.function = inspect.stack()[1][3]

  method = getattr(log, 'method', None)
  flag = isinstance(method, Callable)
  method = method if not flag else getattr(
    method,
    '__name__',
    None, )
  do_nothing() if not flag else setattr(log, 'method', method)

  data = locals()
  data = check_log_for_error(data=data)
  data = format_written_log(data=data)
  write_to_log(data=data)
  write_to_cli(data=data)

  return 1


def format_log_as_sns(log: dict | sns | None = None) -> sns:
  if isinstance(log, sns):
    return log
  if isinstance(log, dict):
    return sns(**log)
  return sns()


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
  return json.dumps(log, default=set_default)


def format_as_yaml(log: dict) -> str:
  return pyyaml.dump(log, default_flow_style=False)


def format_written_log(data: sns) -> str:
  formatter = f'format_as_{data.format}'
  formatter = LOCALS.get(formatter, format_as_yaml)

  field = '__dict__'
  temp = data.log if not hasattr(data.log, field) else getattr(
    data.log,
    field,
    None, )
  temp = {data.level: temp}

  try:
    data.log = formatter(log=temp)
  except Exception as e:
    _ = e
    data.log = str(temp)

  return data


def check_log_for_error(data: dict | None = None) -> sns:
  data = sns(**data)
  error = None

  if isinstance(data.log, dict):
    error = data.log.get('error', None) or data.log.get('exception', None)
  else:
    error = getattr(data.log, 'error', None) or getattr(data.log, 'exception', None)

  flags = sns(
    exception=isinstance(error, Exception),
    level=data.level in ['error', 'exception'], )

  if not flags.exception and not flags.level:
    return data

  if not flags.exception and flags.level:
    data.standard_output = True
    data.level = 'error'
    return data

  if flags.exception:
    error = format_exception_and_trace(exception=error)
    setattr(data.log, 'error', error)
    data.standard_output = True
    data.level = 'error'
    return data

  return data


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


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def format_exception_and_trace(exception: Exception | None = None) -> dict:
  trace = []
  tb = exception.__traceback__

  while tb is not None:
    store = dict(
      file=tb.tb_frame.f_code.co_filename,
      name=tb.tb_frame.f_code.co_name,
      line=tb.tb_lineno, )
    trace.append(store)
    tb = tb.tb_next

  return dict(
    name=type(exception).__name__,
    description=str(exception),
    trace=trace, )


def write_to_log(data: sns) -> int:
  method = getattr(
    LOGGER,
    str(data.level).lower(),
    LOGGER.debug if LOGGER else do_nothing, )
  method(data.log)
  return 1


def write_to_cli(data: sns) -> int:
  if not data.standard_output:
    return 0
  print(data.log)
  return 1


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
