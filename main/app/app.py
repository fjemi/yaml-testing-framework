#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Callable, List

from main.process import (
  spies,
  casts,
  checks,
  patches,
  environment,
  locations,
  nodes,
)
from main.utils import (
  get_config,
  get_module,
  independent,
  logger,
  objects,
  methods,
)

MODULE = __file__
CONFIG = get_config.main()
LOCALS = locals()

MODULE_EXTENSION = '.py'
LOGGING_ENABLED = True
TEST_IDS = {}


def main(
  project_path: str | None = None,
  exclude_files: str | list | None = None,
  include_files: str | list | None = None,
  exclude_methods: str | list | None = None,
  include_methods: str | list | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
) -> list:
  logger.create_logger(
    logging_flag=logging_flag,
    project_path=project_path, )
  data = independent.get_model(schema=CONFIG.schema.App, data=locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return getattr(data, 'tests', None) or []


def handle_id(
  module_route: str | None = None,
  function: str | None = None,
  description: str | List[str] | None = None,
  key: str | None = None,
) -> sns:
  id_short = f'{module_route}.{function}'
  id_ = f' {id_short} - {key} '

  description = description or []
  if isinstance(description, list) and len(description) > 0:
    description = description[-1]
  if len(description) > 0:
    description = f'- {description} '
    id_ = id_ + description

  log = f'Generated test id for {id_short}'
  return sns(
    id=id_,
    id_short=id_short,
    log=log, )


def get_resource_route(
  resource: str,
  module: str,
) -> str:
  routes = sns(resource=resource, module=module)
  for key, value in routes.__dict__.items():
    value_ = os.path.normpath(str(value))
    value_ = value_.split(os.sep)
    setattr(routes, key, value_)

  start = 0
  for i, item in enumerate(routes.resource):
    if item != routes.module[i]:
      start = i
      break

  routes = routes.resource[start:]
  routes[-1] = routes[-1].replace(MODULE_EXTENSION, '')
  return '.'.join(routes)


def get_function(
  function: str | None = None,
  module: ModuleType | None = None,
) -> sns:
  function_ = objects.get(parent=module, route=function)
  if isinstance(function_, Callable):
    return sns(function=function_, function_name=function)

  message = 'Could not retrieve {} from {}'.format(function, module.__file__)
  log = sns(exception=RuntimeError(message), level='error', )

  return sns(log=log)


def run_test_for_function(test: sns | None = None) -> sns:
  test = independent.process_operations(
    operations=CONFIG.operations.run_test_for_functions,
    functions=LOCALS,
    data=test, )
  return test.checks


def run_test_handler(tests: list | None = None) -> sns:
  tests = tests or []
  results = []

  for test in reversed(tests):
    target = ''
    for test_kind in CONFIG.test_kinds:
      if test_kind in test.__dict__:
        target = f'run_test_for_{test_kind}'
        break
    target = LOCALS.get(target)
    result = target(test)
    results.extend(result)

  return sns(tests=results)


def run_tests(locations: List[sns] | None = None) -> sns:
  tests = []

  for i, item in enumerate(locations):
    result = independent.process_operations(
      operations=CONFIG.operations.run_tests,
      functions=LOCALS,
      data=item, )
    tests.extend(result.tests)

  log = None
  if not tests:
    log = sns(
      message='No tests collected',
      level='warning',
      standard_output=True, )

  return sns(tests=tests, log=log)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(location=MODULE)


if __name__ == '__main__':
  examples()
