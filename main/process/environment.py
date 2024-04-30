#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import ModuleType
from types import SimpleNamespace as sns


MODULE = __file__


def main(
  module: ModuleType | None = None,
  environment: dict | None = None,
) -> sns:
  if not environment:
    location = module.__file__
    log = sns(
      level='warning',
      message=f'No environment set for module {location}', )
    return sns(log=log)

  if not hasattr(module, 'CONFIG'):
    config =  sns(environment=sns())
    setattr(module, 'CONFIG', config)

  if not hasattr(module.CONFIG, 'environment'):
    setattr(module.CONFIG, 'environment', sns())

  for key, value in environment.items():
    setattr(module.CONFIG.environment, key, value)

  return sns(module=module)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
