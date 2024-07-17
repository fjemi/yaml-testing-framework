#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns

from main.utils import objects


def main(
  module: ModuleType | None = None,
  environment: dict | None = None,
) -> sns:
  environment = environment or {}
  store = objects.get(
    route='CONFIG.environment',
    default=sns(),
    parent=module, )

  for key, value in environment.items():
    store = objects.update(
      parent=store,
      value=value,
      route=key, )

  config = objects.get(
    parent=module,
    route='CONFIG',
    default=sns(), )
  config = objects.update(
    route='environment',
    value=store,
    parent=config, )
  module = objects.update(
    parent=module,
    value=config,
    route='CONFIG', )

  return sns(module=module)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location='.')


if __name__ == '__main__':
  examples()
