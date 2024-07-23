#!.venv/bin/python3
# -*- coding: utf-8 -*-


import inspect
import os
from types import SimpleNamespace as sns

from main.utils import independent, objects, schema as _schema, logger


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
  data = objects.get(
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

  flag = os.path.isfile(config)
  logger.do_nothing() if flag else logger.main(
    message=['No config YAML file', dict(module=module, config=config)],
    level='warning', )

  return sns(config=config)


def get_content_from_files(
  environment: str | None = None,
  schema: str | None = None,
  config: str | None = None,
  operations: str | None = None,
) -> sns:
  locals_ = locals()
  content = {}

  for name, location in locals_.items():
    content[name] = independent.get_yaml_content(location=location).content

  content = sns(**content)
  return sns(content=content)


def format_content_keys(content: sns | None = None) -> sns:
  for key in CONFIG.format_keys:
    value = {}
    content = content or sns(config={})

    temp = [
      objects.get(parent=content, route=key),
      objects.get(parent=content, route=f'config.{key}'), ]
    value = temp[0] or temp[1]

    handler = f'format_{key}_content'
    handler = LOCALS[handler]
    value = handler(value=value)
    content.config.update({key: value})

  return sns(content=content)


def format_environment_content(value: dict | None = None) -> sns:
  value = objects.get(
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
