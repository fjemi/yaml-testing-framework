#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Callable

from main.utils import get_object, independent, set_object


MODULE = __file__
LOCALS = locals()

CONFIG = '''
  operations:
    main:
    - spy_on_method
'''
CONFIG = independent.format_configurations_defined_in_module(config=CONFIG)


def main(
  module: ModuleType,
  spies: list | None,
) -> sns:
  spies = spies or []
  store = getattr(module, 'SPIES', None) or {}
  setattr(module, 'SPIES', store)

  for item in spies:
    data = sns(module=module, route=item)
    data = independent.process_operations(
      operations=CONFIG.operations.main,
      data=data,
      functions=LOCALS, )
    module = data.module

  return sns(module=module, _cleanup=['spies'])


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def spy_on_method(
  module: ModuleType,
  route: str,
) -> sns:
  original = get_object.main(
    parent=module,
    route=route,
    default=do_nothing, )

  def spy(*args, **kwargs) -> Callable:
    called_with = args or kwargs
    module.SPIES[route] = sns(called=True, called_with=called_with)
    return original(*args, **kwargs)

  spy.__wrapped__ = original
  spy._method = 'spy'

  module.SPIES[route] = sns(called=False, called_with=None)
  set_object.main(parent=module, value=spy, route=route)
  return sns(module=module)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location=MODULE)


if __name__ == '__main__':
  examples()
