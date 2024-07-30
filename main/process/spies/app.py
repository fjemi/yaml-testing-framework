#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Callable

from main.utils import independent, objects


LOCALS = locals()

CONFIG = '''
  operations:
    main:
    - spy_on_method
'''
CONFIG = independent.format_module_defined_config(config=CONFIG)

STORE = {}


def main(
  module: ModuleType | None = None,
  spies: list | None = None,
) -> sns:
  spies = spies or []
  data = sns(module=module)

  for route in spies:
    data.route = route
    data = independent.process_operations(
      operations=CONFIG.operations.main,
      data=data,
      functions=LOCALS, )

  return sns(module=data.module)


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def spy_on_method(
  module: ModuleType | None = None,
  route: str | None = None,
) -> sns:
  global STORE
  STORE[route] = sns(called=False, called_with=None)

  original = objects.get(
    parent=module,
    route=route,
    default=do_nothing, )

  def spy(*args, **kwargs) -> Callable:
    called_with = kwargs or list(args)
    global STORE
    STORE[route] = sns(called=True, called_with=called_with)
    return original(*args, **kwargs)

  spy.__wrapped__ = original
  spy.__method__ = 'spy'

  module = objects.update(
    parent=module,
    value=spy,
    route=route, )
  return sns(module=module)


def get_store() -> sns:
  return sns(spies_=STORE)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
