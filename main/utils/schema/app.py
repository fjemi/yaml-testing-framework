#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns

from main.utils import independent


LOCALS = locals()
MODULE = __file__

CONFIG = '''
  environment:
    DEBUG: YAML_TESTING_FRAMEWORK_DEBUG
  operations:
    main:
    - get_yaml_location
    - get_yaml_content_wrapper
    - get_models_from_schema
  extensions:
    module:
    - .py
    yaml:
    - .yaml
    - .yml
'''
CONFIG = independent.format_configurations_defined_in_module(
  config=CONFIG, sns_fields=['extensions'])


def main(
  module: str | None = None,
  yaml: str | None = None,
  dot_notation: bool | None = None,
) -> sns:
  data = independent.process_operations(
    data=data,
    functions=LOCALS,
    operations=CONFIG.operations.main, )
  return getattr(data, 'models', None) or {}


def get_yaml_location(
  module: str | None = None,
  yaml: str | None = None,
) -> sns:
  if yaml:
    return sns(location=yaml)

  module = module or MODULE
  location = independent.get_path_of_yaml_associated_with_module(
    module=module,
    extensions=CONFIG.extensions, )
  return sns(location=location)


def get_yaml_content_wrapper(location: str | None = None) -> sns:
  return independent.get_yaml_content(location=location)


def get_models_from_schema(
  content: dict | None = None,
  dot_notation: bool | None = None,
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

    if dot_notation:
      model = sns(**model)

    setattr(data.models, name, model)

  if not data.models.__dict__:
    data.log = sns(
      message=f'No schema defined in YAML at location {location}',
      level='warning',
      debug=CONFIG.environment.DEBUG, )

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
