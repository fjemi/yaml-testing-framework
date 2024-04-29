#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
from types import SimpleNamespace as sns

from main.utils import independent


PYTEST_YAML_DEBUG = os.getenv('PYTEST_YAML_DEBUG')

LOCALS = locals()
MODULE = __file__

YAML_EXTENSIONS = ['.yaml', '.yml']
MODULE_EXTENSION = '.py'

OPERATIONS = [
  'get_yaml_location',
  'get_yaml_content_wrapper',
  'get_models_from_schema',
]


def main(
  module: str | None = None,
  yaml: str | None = None,
  sns_models_flag: bool | None = None,
) -> sns:
  data = sns(**locals())
  data = independent.process_operations(
    data=data,
    functions=LOCALS,
    operations=OPERATIONS, )
  return getattr(data, 'models', {})


def get_yaml_location(
  module: str | None = None,
  yaml: str | None = None,
) -> sns:
  data = sns(location=None)

  if yaml:
    data.location = yaml
    return data

  temp = module or MODULE

  if temp.find(MODULE_EXTENSION) != -1:
    temp = os.path.splitext(temp)[0]

    for extension in YAML_EXTENSIONS:
      location = f'{temp}{extension}'
      if os.path.isfile(location):
        data.location = location
        break

  return data


def get_yaml_content_wrapper(location: str | None = None) -> sns:
  return independent.get_yaml_content(location=location)


def get_models_from_schema(
  content: dict | None = None,
  sns_models_flag: bool | None = None,
  location: str | None = None,
) -> sns:
  data = sns(models=sns())

  content = content or {}
  for name, scheme in content.items():
    model = {}

    for field in scheme.get('fields'):
      field_name = field.get('name', '')
      default = field.get('default', None)
      model[field_name] = default

    if sns_models_flag:
      model = sns(**model)

    setattr(data.models, name, model)

  if not data.models.__dict__:
    data.log = sns(
      message=f'No schema defined in YAML at location {location}',
      level='warning', )

  return data


MODELS = main()


def get_model(
  name: str | None = None,
  data: dict | sns | None = None,
  models: sns | None = None,
) -> sns:
  models = models or MODELS

  model = getattr(models, str(name), {})
  store = sns()

  data = data or {}
  if hasattr(data, '__dict__'):
    data = data.__dict__
  if hasattr(model, '__dict__'):
    model = model.__dict__

  for key, default in model.items():
    value = data.get(key, default)
    setattr(store, key, value)

  return store


if __name__ == '__main__':
  from main.utils import invoke_testing_method

  invoke_testing_method.main()
