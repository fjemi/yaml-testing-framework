#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, Iterable, List

from main.process import assertions as _assertions
from main.process import casts, locations
from main.process import environment as _environment
from main.process import get_tests as _get_tests
from main.process import patches as _patches
from main.utils import (
  get_config,
  get_module,
  get_object,
  independent,
  logger,
  schema,
  set_object,
)


MODULE = __file__
CONFIG = get_config.main()
LOCALS = locals()

MODULE_EXTENSION = '.py'
LOGGING_ENABLED = True
TEST_IDS = {}


def main(
  project_path: str | None = None,
  exclude_files: str | List[str] | None = None,
  include_files: str | List[str] | None = None,
  exclude_functions: str | List[str] | None = None,
  include_functions: str | List[str] | None = None,
  resources: str | list | None = None,
  yaml_suffix: str | None = None,
  logging_enabled: bool | None = None,
) -> list:
  logger.create_logger(
    logging_enabled=logging_enabled,
    project_path=project_path, )
  data = schema.get_model(name='main.app.Data', data=locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return getattr(data, 'tests', None) or []


def process_patches(
  patches: list | None,
  module: ModuleType,
) -> ModuleType:
  arguments = locals()
  return _patches.main(**arguments)


def get_locations(
  project_path: Any | None = None,
  include_files: str | List[str] | None = None,
  include_functions: str | List[str] | None = None,
  exclude_files: str | List[str] | None = None,
  exclude_functions: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  resources: list | str | None = None,
  logging_enabled: bool | None = None,
  timestamp: int | float | None = None,
) -> sns:
  arguments = locals()
  return locations.main(**arguments)


def set_environment(
  environment: dict | None,
  module: ModuleType,
) -> ModuleType:
  arguments = locals()
  return _environment.main(**arguments)


def process_assertions(
  assertions: list | None,
  module: ModuleType,
  output: Any,
  id: str,
  id_short: str,
) -> ModuleType:
  arguments = locals()
  return _assertions.main(**arguments)


def get_tests(
  yaml: str | None = None,
  module: str | None = None,
  module_route: str | None = None,
  resources: str | None = None,
) -> sns:
  arguments = locals()
  return _get_tests.main(**arguments)


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


def handle_module(
  module: str | None = None,
  module_route: List[str] | str | None = None,
  key: str | None = None,
) -> sns:
  temp = get_module.main(
    location=module,
    name=module_route,
    key=key,
    pool=False, )
  if isinstance(temp, ModuleType):
    return sns(module=temp)

  log = sns(
    message=f'No module at location {module}',
    level='warning', )
  return sns(log=log)


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


def handle_resources(
  module: ModuleType | None = None,
  resources: List[str] | str | None = None,
) -> sns:
  resources = resources or []
  visited = []
  ignored = []

  for location in resources:
    if location in visited:
      continue
    visited.append(location)

    extension = os.path.splitext(location)[1]
    if False in [
      os.path.exists(location),
      extension in CONFIG.module_extensions,
    ]:
      ignored.append(location)
      continue

    resource = get_module.main(
      location=location,
      pool=False, )
    if not isinstance(resource, ModuleType):
      ignored.append(location)
      continue
    route = get_resource_route(
      module=module.__file__,
      resource=resource.__file__, )
    module = set_object.main(
      parent=module,
      value=resource,
      route=route, )

  log = None
  if ignored:
    log = sns(
      resources_ignored=ignored,
      level='warning',
      standard_output=True, )

  return sns(module=module, _cleanup=['resources'], log=log)


def get_function(
  function: str | None = None,
  module: ModuleType | None = None,
) -> sns:
  if isinstance(function, Callable):
    return sns()

  function_ = get_object.main(parent=module, name=function)
  if isinstance(function_, Callable):
    return sns(function=function_, function_name=function)

  location = getattr(module, '__file__', None)
  message = f'Could not retrieve {function} from {location}'
  log = sns(
    message=message,
    error=RuntimeError(message),
    level='error', )
  return sns(log=log)


def handle_casting_arguments(
  cast_arguments: list | None = None,
  module: ModuleType | None = None,
  arguments: dict | None = None,
) -> sns:
  arguments = casts.main(
    casts=cast_arguments,
    module=module,
    object=arguments, )
  return sns(arguments=arguments, _cleanup=['cast_arguments'])


def get_function_output(
  arguments: sns | dict | None = None,
  function: Callable | None = None,
) -> sns:
  if isinstance(arguments, sns):
    arguments = arguments.__dict__

  kind = type(arguments).__name__.lower()
  handler = 'unpack'
  if kind not in CONFIG.unpack_kinds:
    handler = 'pack'
  handler = f'get_function_output_{handler}_arguments'
  handler = LOCALS[handler]
  return handler(function=function, arguments=arguments)


def get_function_output_unpack_arguments(
  function: Callable | None = None,
  arguments: dict | Iterable | None = None,
) -> sns:
  output = None

  try:
    if isinstance(arguments, dict):
      output = function(**arguments)
    elif isinstance(arguments, list | tuple):
      output = function(*arguments)
    else:
      output = function(arguments)
  except Exception as e:
    output = e
  finally:
    output = independent.get_task_from_event_loop(task=output)

  log = None
  exception = None
  if isinstance(output, Exception):
    log = sns(error=output, level='error')
    exception = output

  return sns(
    output=output,
    log=log,
    exception=exception, )


def get_function_output_pack_arguments(
  function: Callable | None = None,
  arguments: Any | None = None,
  exception: Exception | None = None,
  output: Any | None = None,
) -> sns:
  data = sns(output=output)

  if not exception:
    return data

  try:
    data.output = function(arguments)
  except Exception as e:
    print(e)
    data.output = e
  finally:
    data.output = independent.get_task_from_event_loop(task=data.output)

  if isinstance(data.output, Exception):
    data.exception = data.output
    message = f'{type(data.exception).__name__} occurred calling the function'
    data.log = sns(level='warning', message=message)
  return data


def handle_casting_output(
  cast_output: list | None = None,
  module: ModuleType | None = None,
  output: dict | None = None,
) -> sns:
  output = casts.main(
    casts=cast_output,
    module=module,
    object=output, )
  return sns(output=output, _cleanup=['cast_output'])


def run_test_for_function(test: sns | None = None) -> sns:
  test = independent.process_operations(
    operations=CONFIG.operations.run_test_for_functions,
    functions=LOCALS,
    data=test, )
  return test.assertions


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