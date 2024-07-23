#!.venv/bin/python3
# -*- coding: utf-8 -*-


import inspect
import os
import time
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable

import yaml as pyyaml

from main.utils import logger, objects, methods


CONFIG = '''
  environment:
    DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}
    DISABLE_LOGGING: ${DISABLE_LOGGING}
    YAML_LOADER: ${YAML_TESTING_FRAMEWORK_YAML_LOADER}
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
    logger.main(
      message=f'No YAML file at {location}',
      level='warning', )
    return sns(content=content)

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
  function: Callable | None = None,
  data: sns | dict = {},
) -> dict:
  arguments = {}
  parameters = get_function_parameters(function=function)
  for parameter in parameters:
    arguments[parameter] = objects.get(parent=data, route=parameter)
  return arguments


def format_output_as_dict(output: dict | sns | None = None) -> dict | None:
  if isinstance(output, dict):
    return output

  if hasattr(output, '__dict__'):
    return output.__dict__

  if isinstance(output, Exception):
    return dict(error=output)

  if output is None:
    return {}

  type_ = type(output).__name__
  message = f'Cannot convert object of type {type_} to a dictionary'
  logger.main(level='error', message=message)


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


def update_data(
  data: sns,
  output: dict,
) -> sns:
  for field, value in output.items():
    data = objects.update(
      parent=data,
      value=value,
      route=field, )
  return data


def process_operations(
  operations: list | str | None = None,
  data: dict | sns | None = None,
  functions: dict | None = None,
  debug: bool | None = None,
) -> sns | dict:
  operations = convert_string_to_list(string=operations)
  timestamps = sns(start=get_timestamp())
  errors = []

  for name in operations:
    method = objects.get(parent=functions, route=name)
    arguments = get_function_arguments(
      function=method,
      data=data, )
    result = methods.call.main(arguments=arguments, method=method)
    errors.append(result.exception)
    output = format_output_as_dict(output=result.output)
    data = update_data(data=data, output=output)

  timestamps = get_runtime_in_ms(timestamps=timestamps).__dict__

  flags = True in [
    errors.count(None) != len(errors),
    CONFIG.environment.DEBUG, ]
  logger.do_nothing() if not flags  else logger.main(
    message=dict(operations=operations),
    timestamps=timestamps, )
  return data


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

  models = sns(**models)
  if module_defined:
    return models

  return sns(models=models)


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
