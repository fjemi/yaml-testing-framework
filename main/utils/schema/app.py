#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns

from main.utils import objects, independent
from main.utils.independent import format_config_schema, get_yaml_content


LOCALS = locals()
MODULE = __file__

CONFIG = '''
  environment:
    DEBUG: YAML_TESTING_FRAMEWORK_DEBUG
  operations:
    main:
    - get_yaml_location
    - get_yaml_content
    - format_config_schema
  extensions:
    module:
    - .py
    yaml:
    - .yaml
    - .yml
'''
CONFIG = independent.format_module_defined_config(
  config=CONFIG, sns_fields=['extensions'])


def main(
  content: dict | None = None,
  module: str | None = None,
  yaml: str | None = None,
) -> sns:
  data = independent.process_operations(
    data=locals(),
    functions=LOCALS,
    operations=CONFIG.operations.main, )
  return objects.get(
    parent=data,
    route='models',
    default={}, )


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


MODELS = main()


if __name__ == '__main__':
  from main.utils import invoke_testing_method

  invoke_testing_method.main()
