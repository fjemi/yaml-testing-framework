#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns

from main.utils import get_object, independent


LOCALS = locals()
MODULE = __file__

CONFIG = '''
  environment:
    DEBUG: YAML_TESTING_FRAMEWORK_DEBUG
  operations:
    main:
    - get_yaml_location
    - get_yaml_content_wrapper
    - wrapper_format_schema_defined_in_config
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
  content: dict | None = None,
  module: str | None = None,
  yaml: str | None = None,
  dot_notation: bool | None = None,
) -> sns:
  data = independent.process_operations(
    data=locals(),
    functions=LOCALS,
    operations=CONFIG.operations.main, )
  return get_object.main(
    parent=data,
    route='models',
    default={}, )


def wrapper_format_schema_defined_in_config(
  content: dict | None = None,
  dot_notation: bool | None = None,
  location: str | None = None,
) -> sns:
  arguments = locals()
  return independent.format_schema_defined_in_config(**arguments)


def get_yaml_location(
  module: str | None = None,
  yaml: str | None = None,
  content: dict | None = None,
) -> sns:
  if content:
    return sns()

  if yaml:
    return sns(location=yaml)

  module = module or MODULE
  location = independent.get_path_of_yaml_associated_with_module(
    module=module,
    extensions=CONFIG.extensions, )

  return sns(location=location)


def get_yaml_content_wrapper(
  content: dict | None = None,
  location: str | None = None,
) -> sns:
  if content:
    return sns()

  return independent.get_yaml_content(location=location)


MODELS = main()


if __name__ == '__main__':
  from main.utils import invoke_testing_method

  invoke_testing_method.main()
