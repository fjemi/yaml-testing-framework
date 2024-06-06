#!.venv/bin/python3
# -*- coding: utf-8 -*-


import asyncio
import inspect
import os
import time
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Awaitable, Callable, List

import yaml as pyyaml

from main.utils import get_object, logger, set_object


CONFIG = '''
  environment:
    DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}
    DISABLE_LOGGING: ${DISABLE_LOGGING}
    YAML_LOADER: ${YAML_TESTING_FRAMEWORK_YAML_LOADER}
  update_log_fields:
  - timestamps
  - operation
  default_logger_arguments:
    format: yaml
    standard_output: false
    debug: false
    level: info
  log_fields:
  - level
  - format
  - standard_output
  - debug
  data_and_field_names_and_defaults:
  - data: operation.__name__
    log: operation
  - data: operation.__module__
    log: location
  - data: timestamps.__dict__
    log: timestamps
  - data: output.exception
    log: error
  field_map:
    function.__name__: operation
    function.__module__: location
    timestamps.__dict__: timestamps
    output.exception: error
'''

FORMAT_CONFIG_FIELDS = ['environment', 'schema', 'operations']

MODULE = __file__
LOCALS = locals()

LOADER = None

PARAMETERS = {}


def convert_string_to_list(string: list | str | None = None) -> list | None:
  if isinstance(string, str):
    return pyyaml.safe_load(string)
  elif isinstance(string, list):
    return string


def get_yaml_loader() -> ModuleType:
  global LOADER

  if LOADER:
    return LOADER

  name = CONFIG.environment.YAML_LOADER
  name = f'{name}Loader'
  LOADER = getattr(pyyaml, name, None) or pyyaml.SafeLoader
  return LOADER


def get_yaml_content(location: str | None = None) -> sns:
  location = str(location)
  data = sns(content={})

  if os.path.isfile(location):
    with open(
        file=location,
        encoding='utf-8',
        mode='r',
    ) as file:
      data.content = file.read()
      data.content = os.path.expandvars(data.content)
      loader = get_yaml_loader()
      # trunk-ignore(bandit/B506)
      data.content = pyyaml.load(data.content, Loader=loader)
  else:
    data.log = f'No YAML file at {location}'

  return data


def is_coroutine(object: Any | None = None) -> bool:
  flag = False
  if True in [
    inspect.iscoroutinefunction(obj=object),
    inspect.iscoroutine(object=object),
    inspect.isawaitable(object=object),
  ]:
    flag = True
  return flag


def get_task_from_event_loop(task: Any | None = None) -> Any:
  if is_coroutine(object=task) and not isinstance(task, Callable):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
      task = loop.run_until_complete(task)
    finally:
      loop.close()
      asyncio.set_event_loop(None)

  return task


def get_decorated_function_from_closure(
  function: Callable | Awaitable,
) -> Callable | Awaitable:
  closure = getattr(function, '__closure__', None) or []
  for item in closure:
    contents = item.cell_contents
    contents_closure = getattr(contents, '__closure__', False) or False
    flags = [
      'function' * isinstance(contents, Callable),
      'closure' * contents_closure, ]
    flags = '.'.join(flags)

    if flags == 'function.':
      return contents
    if flags == 'function.closure':
      return get_decorated_function_from_closure(function=contents)

  return function


def get_decorated_function_from_wrapped(
  function: Callable | Awaitable,
) -> Callable | Awaitable:
  wrapped = getattr(function, '__wrapped__', None)
  if not wrapped:
    return function
  return get_decorated_function_from_wrapped(function=wrapped)


def get_decorated_function(
  function: Callable | Awaitable,
) -> Callable | Awaitable:
  wrapped = get_decorated_function_from_wrapped(function=function)
  if wrapped != function:
    return wrapped

  closure = get_decorated_function_from_closure(function=function)
  if closure != function:
    return closure

  return function


def get_function_parameters(function: Awaitable | Callable) -> list:
  global PARAMETERS
  function_ = get_decorated_function(function=function)

  file_ = inspect.getfile(function_)
  key = f'{file_}|{function_.__name__}'
  if key in PARAMETERS:
    return PARAMETERS[key]

  item = 'return'
  parameters = list(function_.__annotations__.keys())
  if item in parameters:
    parameters.remove(item)

  PARAMETERS[key] = parameters
  return parameters


def get_function_arguments(
  function: Callable,
  data: sns | dict,
) -> dict:
  arguments = {}
  parameters = get_function_parameters(function=function)
  for parameter in parameters:
    arguments[parameter] = get_object.main(parent=data, route=parameter)
  return arguments


def format_output(output: dict | sns | None = None) -> dict | None:
  if hasattr(output, '__dict__'):
    return output.__dict__
  elif isinstance(output, dict):
    return output
  elif output is None:
    return {}


def format_exception_and_trace(exception: Exception | None = None) -> dict:
  trace = []
  tb = exception.__traceback__

  while tb is not None:
    trace.append(
      dict(
        file=tb.tb_frame.f_code.co_filename,
        name=tb.tb_frame.f_code.co_name,
        line=tb.tb_lineno, ),
    )
    tb = tb.tb_next

  return dict(
    name=type(exception).__name__,
    description=str(exception),
    trace=trace, )


def get_timestamp(kind: str | None = None) -> float | int:
  timestamp = time.time()
  if kind == 'int':
    timestamp = int(timestamp)
  return timestamp


def get_runtime_in_ms(timestamps: sns) -> sns:
  timestamps.end = get_timestamp()
  timestamps.runtime_ms = (timestamps.end - timestamps.start)
  timestamps.runtime_ms = timestamps.runtime_ms * 1000
  return timestamps


def delete_field(
  parent: sns | dict,
  field: str,
) -> sns | dict | None:
  if isinstance(parent, sns):
    setattr(parent, field, None)
    delattr(parent, field)
    return parent

  elif isinstance(parent, dict):
    parent[field] = None
    del parent[field]
    return parent


def purge_data_and_output_fields(data: sns) -> int:
  fields = data.output.get('_cleanup', [])
  fields.append('_cleanup')
  for field in fields:
    delete_field(data.data, field)
    delete_field(data.output, field)
  return data


def get_function_output(data: sns) -> sns:
  data.timestamps = sns(start=get_timestamp())
  try:
    data.output = data.function(**data.arguments)
  except Exception as e:
    data.output = dict(exception=e)
  data.timestamps = get_runtime_in_ms(timestamps=data.timestamps)
  return data


def update_data_fields(data: sns) -> sns:
  for field, value in data.output.items():
    data.data = set_object.main(
      parent=data.data,
      value=value,
      route=field, )
  return data


def get_log(output: dict) -> sns | None:
  log = output.get('log', None)
  if isinstance(log, sns):
    return log
  if isinstance(log, dict):
    return sns(**log)
  if log and not isinstance(log, sns | dict):
    return sns(log=log)
  if log is None:
    return sns()


def get_default_logger_arguments(arguments: sns) -> sns:
  for field, default in CONFIG.default_logger_arguments.items():
    value = getattr(arguments.log, field, None)
    value = value or default
    setattr(arguments, field, value)
    setattr(arguments.log, field, None)
    delattr(arguments.log, field)
  return arguments


def get_log_fields_from_data(
  log: sns,
  data: sns,
) -> sns:
  for names in CONFIG.data_and_field_names_and_defaults:
    # trunk-ignore(ruff/PLW2901)
    names = sns(**names)
    value = getattr(data, names.data, None)
    if value:
      setattr(log, names.log, value)
  return log


def format_log(data: sns) -> int:
  arguments = sns()
  arguments.log = get_log(output=data.output)
  arguments = get_default_logger_arguments(arguments=arguments)
  arguments.debug = arguments.debug or data.debug
  store = arguments

  for data_field, log_field in CONFIG.field_map.items():
    value = get_object.main(parent=data, route=data_field)
    setattr(store.log, log_field, value)



  exception = getattr(store.log, 'error', None) or getattr(data, 'error', None)

  if store.debug or exception:
    store.log.arguments = data.arguments.get('arguments', None)
    store.log.output = data.output
    store.standard_output = True
    store.level = getattr(store.log, 'level', None) or 'info'
    store.level = store.level if store.level != 'info' else 'debug'

  if exception is not None:
    store.level = 'error'
    store.log.error = format_exception_and_trace(exception=exception)

    store.log.output = None
    store.log.message = None
    del store.log.output
    del store.log.message
  else:
    del store.log.error

  logger.main(**store.__dict__)
  return 1


def process_operations(
  operations: List[str] | None = None,
  data: dict | sns | None = None,
  functions: dict | None = None,
  debug: bool | None = None,
) -> sns | dict:
  operations = convert_string_to_list(string=operations)
  store = sns(**locals())

  for name in store.operations:
    store.function = store.functions[name]
    store.arguments = get_function_arguments(
      function=store.function,
      data=store.data, )
    store = get_function_output(data=store)
    store.output = get_task_from_event_loop(task=store.output)
    store.output = format_output(output=store.output)
    store = purge_data_and_output_fields(data=store)
    store = update_data_fields(data=store)
    format_log(data=store)

  return store.data


def exit_loop() -> None:
  raise StopIteration


def format_configurations_defined_in_module(
  config: str | dict,
  sns_fields: list | None = None,
) -> sns:
  if isinstance(config, str):
    config = os.path.expandvars(config)
    config = pyyaml.safe_load(config)

  sns_fields = sns_fields or []
  fields = [*FORMAT_CONFIG_FIELDS, *sns_fields]

  for field in fields:
    value = get_object.main(parent=config, route=field)
    if isinstance(value, dict):
      config[field] = sns(**value)
  return sns(**config)


def get_path_of_yaml_associated_with_module(
  module: str,
  extensions: sns,
) -> str | None:
  for yaml_extension in extensions.yaml:
    for module_extension in extensions.module:
      path = module.replace(module_extension, yaml_extension)
      if os.path.exists(path):
        return path


def get_model(
  schema: dict | sns | None = None,
  data: dict | sns | None = None,
) -> sns:
  temp = get_object.main(
    parent=schema,
    route='__dict__',
    default=schema, )

  store = {}

  for route, default in temp.items():
    value = get_object.main(
      default=default,
      route=route,
      parent=data, )
    store = set_object.main(
      parent=store,
      route=route,
      value=value, )

  return sns(**store)


CONFIG = format_configurations_defined_in_module(config=CONFIG)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
