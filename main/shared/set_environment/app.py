#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from types import ModuleType

from get_config.app import main as get_config


MODULE = __file__
CONFIG = get_config(module=MODULE)

LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


def main(
  environment: dict | None = None,
  module: ModuleType | None = None,
) -> dict:
  environment = environment or {}
  conditions = [not environment, not module]
  if True in conditions:
    return {}

  condition = hasattr(module, 'CONFIG')
  if condition is False:
    setattr(module, CONFIG, Data_Class())

  config_environment = getattr(
    module.CONFIG,
    'environment',
    Data_Class(), )

  for key, value in environment.items():
    setattr(config_environment, key, value)
  setattr(module.CONFIG, 'environment', config_environment, )

  return {
    'module': module,
    'environment': None, }


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
