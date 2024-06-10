#!.venv/bin/python3
# -*- coding: utf-8 -*-


import inspect
import os
from types import SimpleNamespace as sns

from main.utils import get_object, independent
from main.utils import schema as _schema


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
CONFIG = independent.format_module_defined_config(
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
  data = get_object.main(
    parent=data,
    route='content.config',
    default={}, )
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

    temp = [
      get_object.main(parent=content, route=key),
      get_object.main(parent=content, route=f'config.{key}'), ]
    value = temp[0] or temp[1]

    handler = f'format_{key}_content'
    handler = LOCALS[handler]
    value = handler(value=value)
    content.config.update({key: value})

  return sns(content=content)


def format_environment_content(value: dict | None = None) -> sns:
  value = get_object.main(
    parent=value,
    route='__dict__',
    default=value, ) or {}
  for name, variable in value.items():
    value[name] = None if str(variable).find('$') == 0 else variable
  return sns(**value)


def format_schema_content(value: dict | None = None) -> sns:
  temp = independent.format_config_schema(content=value)
  temp = temp.models.__dict__
  temp.update(_schema.MODELS.__dict__)
  return sns(**temp)


def format_operations_content(value: dict | None = None) -> sns:
  value = value or {}
  return sns(**value)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
