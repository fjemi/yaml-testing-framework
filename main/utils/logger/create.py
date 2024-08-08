#!.venv/bin/python3
# -*- coding: utf-8 -*-


import logging
import os
import time
from types import SimpleNamespace as sns

import yaml as pyyaml

from main.utils import environment_variables


LOCALS = locals()

ROOT = os.getcwd()


CONFIG = '''
  environment:
    LOG_DIR: ${YAML_TESTING_FRAMEWORK_LOG_DIR}
    DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}

  suffix:
  - .yaml-testing-framework
  - logs
'''

CONFIG = pyyaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)
CONFIG.environment = environment_variables.evaluate(
  values=CONFIG.environment, return_='sns')


def main(
  path: str = '',
  suffix: str = '',
) -> sns:
  path = path or ROOT
  suffix = suffix or CONFIG.suffix
  directory = get_directory(path=path, suffix=suffix)
  location = get_location(directory=directory)
  return get_logger(location=location)


def get_timestamp() -> int:
  return int(time.time())


def get_directory(
  path: str = '',
  suffix: list | str = '',
) -> str:
  path = str(path)
  suffix = f'{os.path.sep}'.join(suffix) if isinstance(suffix, list) else suffix
  handlers = {
    True: ROOT,
    os.path.isfile(path): os.path.dirname(path),
    os.path.isdir(path): path, }
  directory = handlers[True]
  directory = os.path.join(directory, suffix)
  directory = CONFIG.environment.LOG_DIR or directory
  os.makedirs(name=directory, exist_ok=True)
  return directory


def get_location(directory: str = '') -> str:
  filename = f'{get_timestamp()}.log'
  return os.path.join(directory, filename)


def get_logger(location: str) -> logging.Logger:
  logger = logging.getLogger(location)
  logger.setLevel(logging.DEBUG)
  handler = logging.FileHandler(location, mode='w')
  formatter = logging.Formatter('%(message)s')
  handler.setFormatter(formatter)
  logger.addHandler(handler)
  return logger


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.main/utils/logger')


if __name__ == '__main__':
  examples()
