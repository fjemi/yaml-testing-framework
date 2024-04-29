#!.venv/bin/python3
# -*- coding: utf-8 -*-

import inspect
import os
from types import SimpleNamespace as sns

import yaml as pyyaml
from main.utils import get_object, independent, schema


MODULE = __file__

CONFIG = '''
yaml_extensions:
- .yaml
- .yml
operations:
- format_config_location
- get_content_from_files
- format_specified_content_keys
# - format_environment_content
# - format_schema_content
specified_content_keys:
- environment
- schema
YAML_TESTING_FRAMEWORK_DEBUG: ${YAML_TESTING_FRAMEWORK_DEBUG}
module_extension: .py
'''
CONFIG = os.path.expandvars(CONFIG)
CONFIG = pyyaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)

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
    operations=CONFIG.operations,
    functions=LOCALS,
    data=data, )
  data = get_object.main(parent=data, route='content.config') or {}
  return sns(**data)


def format_config_location(
  module: str | None = None,
  config: str | None = None,
) -> sns:
  module = str(module)
  config = str(config)
  data = sns(config=str(config))

  if False not in [
    module.find(CONFIG.module_extension) > -1,
    not os.path.isfile(data.config),
  ]:
    for extension in CONFIG.yaml_extensions:
      temp = module.replace(CONFIG.module_extension, extension)
      if os.path.exists(temp):
        data.config = temp
        break

  if os.path.isfile(data.config) is False:
    message = ['No config YAML file', dict(module=module, config=config)]
    data.log = sns(level='error', message=message)

  return data


def get_yaml_content_wrapper(location: str | None = None) -> sns:
  return independent.get_yaml_content(location=location)


FIELDS = ['environment', 'schema', 'config']


def get_content_from_files(
  environment: str | None = None,
  schema: str | None = None,
  config: str | None = None,
) -> sns:
  locals_ = locals()
  data = sns(content=sns())
  message = []

  for name in FIELDS:
    location = locals_[name]
    content = get_yaml_content_wrapper(location=location)
    setattr(data.content, name, content.content)
    if getattr(content, 'log', None):
      message.append({name: content.log})

  if message:
    data.log = sns(message=message, level='warning')

  return data


def format_specified_content_keys(content: sns | None = None) -> sns:
  for key in CONFIG.specified_content_keys:
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
  # if not isinstance(value, dict):
  #   return value

  for name, variable in value.items():
    if str(variable).find('$') == 0:
      value[name] = None
  return sns(**value)


def format_schema_content(value: dict | None = None) -> sns:
  value = schema.get_models_from_schema(
    content=value,
    sns_models_flag=True, )
  return value.models


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
