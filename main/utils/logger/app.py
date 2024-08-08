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

from main.utils.logger import create
from main.utils import environment_variables


LOCALS = locals()

ROOT_DIR = os.getcwd()


CONFIG = '''
  environment:
    LOG_DIR: ${YAML_TESTING_FRAMEWORK_LOG_DIR}
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
CONFIG = pyyaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)
CONFIG.environment = environment_variables.evaluate(
  values=CONFIG.environment, return_='sns')

LOGGER = create.main()
LOGGERS = dict(
  warning=LOGGER.warning,
  error=LOGGER.error,
  debug=LOGGER.debug,
  info=LOGGER.info, )


def main(
  format: str | None = None,
  level: str | None = None,
  debug: bool | None = None,
  enabled: bool | None = None,
  standard_output: bool = False,
  message: Any | None = None,
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
  level = str(level).lower()

  log = get_log(locals_=locals())
  log = format_log(log=log, format=format)
  handle_log(
    log=log,
    level=level,
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


def do_nothing(
  level: str = '',
  log: str = '',
  *args, **kwargs,
) -> None:
  if CONFIG.environment.DEBUG is True:
    print(locals(), CONFIG.environment.DEBUG)
  return lambda *_, **__: None


def handle_log(
    log: str = '',
    level: str = '',
    debug: bool = False,
    standard_output: bool = False,
) -> int:
  debug = debug or CONFIG.environment.DEBUG
  standard_output = True in [
    level != 'info',
    debug,
    standard_output, ]

  a = write_to_file(level=level, log=log) if log else 0
  b = write_to_cli(
    standard_output=standard_output,
    log=log, ) if log else 0
  return a + b


def write_to_file(
  level: str = '',
  log: str = '',
) -> int:
  method = LOGGERS.get(level, LOGGERS['info'])
  method(log)
  return 2


def write_to_cli(
  standard_output: bool = False,
  log: Any | None = None,
) -> int:
  if standard_output:
    print(log)
    return 1
  return 0


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


def examples() -> None:
  from main.utils import invoke

  invoke.main()


if __name__ == '__main__':
  examples()
