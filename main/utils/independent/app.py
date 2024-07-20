#!.venv/bin/python3
# -*- coding: utf-8 -*-


import inspect
import os
import time
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

import yaml as pyyaml

from main.utils import logger, objects


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


def get_yaml_content(
  location: str | None = None,
  content: dict | None = None,
) -> sns:
  if content:
    return sns()

  content = {}
  location = str(location)
  if not os.path.isfile(location):
    log = sns(message=f'No YAML file at {location}', level='warning')
    return sns(log=log, content=content)

  with open(
      file=location,
      encoding='utf-8',
      mode='r',
  ) as file:
    content = file.read()

  content = os.path.expandvars(content)
  loader = get_yaml_loader()
  # trunk-ignore(bandit/B506)
  content = pyyaml.load(content, Loader=loader)
  return sns(content=content)


def get_decorated_function_from_closure(
  function: Callable | None = None,
) -> Callable:
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
  function: Callable | None = None,
) -> Callable:
  wrapped = getattr(function, '__wrapped__', None)
  if not wrapped:
    return function
  return get_decorated_function_from_wrapped(function=wrapped)


def get_decorated_function(
  function: Callable | None = None,
) -> Callable:
  wrapped = get_decorated_function_from_wrapped(function=function)
  if wrapped != function:
    return wrapped

  closure = get_decorated_function_from_closure(function=function)
  if closure != function:
    return closure

  return function


def get_function_parameters(
  function: Callable | None = None,
) -> list:
  global PARAMETERS
  method = get_decorated_function(function=function)

  file_ = '' if not isinstance(method, Callable) else inspect.getfile(method)
  key = f'{file_}|{method.__name__}'
  if key in PARAMETERS:
    return PARAMETERS[key]

  item = 'return'
  parameters = list(method.__annotations__.keys())
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
    arguments[parameter] = objects.get(parent=data, route=parameter)
  return arguments


def format_output(output: dict | sns | None = None) -> dict | None:
  output = objects.get(
    parent=output,
    route='__dict__',
    default=output, )
  if output is None:
    output = {}
  return output


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


def get_runtime_in_ms(timestamps: sns | None = None,) -> sns:
  timestamps.end = get_timestamp()
  timestamps.runtime_ms = (timestamps.end - timestamps.start)
  timestamps.runtime_ms = timestamps.runtime_ms * 1000
  return timestamps


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
    data.data = objects.update(
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
    value = objects.get(parent=data, route=data_field)
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
    store.function = objects.get(parent=store.functions, route=name)
    store.arguments = get_function_arguments(
      function=store.function,
      data=store.data, )
    store = get_function_output(data=store)
    store.output = format_output(output=store.output)
    store = update_data_fields(data=store)
    format_log(data=store)

  return store.data


def exit_loop() -> None:
  raise StopIteration


def format_module_defined_config(
  config: str | dict,
  sns_fields: list | None = None,
  location: str | None = None,
) -> sns:
  if isinstance(config, str):
    config = os.path.expandvars(config)
    config = pyyaml.safe_load(config)

  sns_fields = sns_fields or []
  fields = [*FORMAT_CONFIG_FIELDS, *sns_fields]

  for field in fields:
    value = objects.get(parent=config, route=field)
    handler = f'format_config_{field}'
    handler = LOCALS.get(handler, pass_through)
    value = handler(
      location=location,
      content=value,
      module_defined=True, )
    config[field] = value if not isinstance(value, dict) else sns(**value)
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
  temp = objects.get(
    parent=schema,
    route='__dict__',
    default=schema, )

  store = {}

  for route, default in temp.items():
    value = objects.get(
      default=default,
      route=route,
      parent=data, )
    store = objects.update(
      parent=store,
      route=route,
      value=value, )

  return sns(**store)


def get_model_from_scheme(scheme: dict | None = None) -> sns:
  store = {}
  fields = objects.get(parent=scheme, route='fields')

  for item in fields:
    name = objects.get(parent=item, route='name')
    default = objects.get(parent=item, route='default')
    store.update({name: default})

  return sns(**store)


def format_config_schema(
  content: dict | None = None,
  location: str | None = None,
  module_defined: bool | None = None,
) -> sns:
  models = {}

  content = content or {}
  for name, scheme in content.items():
    model = get_model_from_scheme(scheme=scheme)
    models[name] = model

  log = None
  if not models:
    log = sns(
      message=f'No schema defined in YAML at location {location}',
      level='warning', )

  models = sns(**models)
  if module_defined:
    return models

  return sns(log=log, models=models)


def pass_through(
  location: str | None = None,
  content: Any | None = None,
  module_defined: bool | None = None,
) -> Any:
  _ = location, module_defined
  return content


CONFIG = format_module_defined_config(config=CONFIG)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
