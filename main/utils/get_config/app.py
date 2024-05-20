#!.venv/bin/python3
# -*- coding: utf-8 -*-


import inspect
import os
from types import SimpleNamespace as sns

from main.utils import get_object, independent, schema


MODULE = __file__

CONFIG = '''
  extensions:
    yaml:
    - .yaml
    - .yml
    module:
    - .py
  operations:
    main:
    - format_config_location
    - get_content_from_files
    - format_content_keys
  format_keys:
  - environment
  - schema
  - operations
'''
CONFIG = independent.format_configurations_defined_in_module(
  config=CONFIG, sns_fields=['extensions'])

LOCALS= locals()


def main(
  module: str | None = None,
  environment: str | None = None,
  config: str | None = None,
  schema: str | None = None,
) -> sns:
  data = sns(**locals())
  data.module = data.module or inspect.stack()[1].filename
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  data = get_object.main(parent=data, route='content.config') or {}
  return sns(**data)


def format_config_location(
  module: str | None = None,
  config: str | None = None,
) -> sns:
  module = str(module)
  extension = os.path.splitext(module)[-1]
  config = str(config)

  if False not in [
    extension in CONFIG.extensions.module,
    not os.path.isfile(config),
  ]:
    config = independent.get_path_of_yaml_associated_with_module(
      module=module,
      extensions=CONFIG.extensions, ) or ''

  log = None
  if os.path.isfile(config) is False:
    message = ['No config YAML file', dict(module=module, config=config)]
    log = sns(level='error', message=message)

  return sns(config=config, log=log)


def get_yaml_content_wrapper(location: str | None = None) -> sns:
  return independent.get_yaml_content(location=location)


def get_content_from_files(
  environment: str | None = None,
  schema: str | None = None,
  config: str | None = None,
  operations: str | None = None,
) -> sns:
  locals_ = locals()
  data = sns(content=sns())
  message = []

  for name, location in locals_.items():
    content = get_yaml_content_wrapper(location=location)
    setattr(data.content, name, content.content)
    if getattr(content, 'log', None):
      message.append({name: content.log})

  if message:
    data.log = sns(message=message, level='warning')

  return data


def format_content_keys(content: sns | None = None) -> sns:
  for key in CONFIG.format_keys:
    value = {}
    content = content or sns(config={})

    if getattr(content, key, None):
      value = getattr(content, key)
    if content.config.get(key, None):
      value = content.config.get(key)

    handler = f'format_{key}_content'
    handler = LOCALS[handler]
    value = handler(value=value)
    content.config.update({key: value})

  return sns(content=content)


def format_environment_content(value: dict | None = None) -> sns:
  value = value.__dict__ if hasattr(value, '__dict__') else value
  for name, variable in value.items():
    if str(variable).find('$') == 0:
      value[name] = None
  return sns(**value)


def format_schema_content(value: dict | None = None) -> sns:
  value = schema.get_models_from_schema(
    content=value,
    sns_models_flag=True, )
  return value.models


def format_operations_content(value: dict | None = None) -> sns:
  value = value or {}
  return sns(**value)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
