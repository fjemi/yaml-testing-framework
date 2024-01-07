#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
import inspect
import os
from typing import Callable, List

import yaml as py_yaml


MODULE = __file__

CONFIG = '''
yaml_extensions:
- .yaml
- .yml
base_keys:
  config: whole
  schema: part
  environment: part
operations:
- get_yaml_location
- set_locations
- get_contents
- format_environment
- format_schema
- format_config
'''
CONFIG = py_yaml.safe_load(CONFIG)

LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


@dc.dataclass
class Data:
  module: str | None = None
  yaml: str | None = None
  contents: dict | None = None
  config: str | dict | Data_Class | None = None
  environment: str | dict | Data_Class | None = None
  schema: str | dict | Data_Class | None = None


@dc.dataclass
class Operations:
  names: List[str] | None = None
  fields: str | None = None
  results: str | None = None
  function: str | None = None


def process_arguments(locals_: dict) -> Data:
  data = Data()

  for key, value in locals_.items():
    conditions = [
      hasattr(data, key),
      value is not None,
    ]
    if sum(conditions) == len(conditions):
      setattr(data, key, value)
      locals_[key] = None

  return data


def get_yaml_location(
  module: str | None = None,
  yaml: str | None = None,
) -> dict:
  if yaml:
    return {'yaml': yaml}

  for extension in CONFIG.get('yaml_extensions'):
    location = module
    if os.path.isfile(location):
      location = location.replace('.py', extension)
    if os.path.exists(location) is True:
      return {'yaml': location}

  return {'yaml': ''}


def set_locations(
  yaml: str | None = None,
  config: str | None = None,
  environment: str | None = None,
  schema: str | None = None,
) -> dict:
  contents = {}
  locations = {}

  for key in CONFIG.get('base_keys'):
    location = locals().get(key, None)
    location = yaml if not location else location
    locations[key] = location
    contents[location] = {}

  locations.update({'contents': contents, 'yaml': None})
  return locations


def get_yaml_content(yaml: str | None = None) -> dict:
  conditions = [
    not yaml,
    os.path.exists(str(yaml)) is False,
  ]
  if True in conditions:
    return {}

  content = None
  with open(
      file=yaml,
      mode='r',
      encoding='utf-8',
  ) as file:
    content = file.read()

  content = os.path.expandvars(content)
  content = py_yaml.safe_load(content)
  return content if content else {}


def get_contents(
  contents: dict | None = None,
  config: str | None = None,
  environment: str | None = None,
  schema: str | None = None,
) -> dict:
  contents = contents or {}

  for location in contents:
    contents[location] = get_yaml_content(yaml=location)

  store = {}
  for key, value in CONFIG.get('base_keys').items():
    location = locals().get(key)

    if value == 'whole':
      content = contents[location]
    if value == 'part':
      content = contents[location].get(key, {})
      contents[location][key] = None
    store[key] = content

  store['contents'] = None
  return store


def format_config(config: dict) -> dict:
  config = convert_dict_to_dataclass(data=config, cls_name='Config')
  return {'config': config}


def convert_dict_to_dataclass(
  data: dict,
  cls_name: str,
  instantiate: bool = True,
) -> Data_Class:
  fields = []

  for key, value in data.items():
    kind = f'{type(value).__name__}'
    kind = kind if kind.find('None') != -1 else kind + ' | None'
    field = [
      key,
      kind,
      None,
    ]
    fields.append(field)

  data_class = dc.make_dataclass(
    cls_name=cls_name,
    fields=fields,
  )

  if instantiate is True:
    return data_class(**data)
  return data_class


def get_function_parameters(function: Callable) -> List[str]:
  return list(inspect.signature(function).parameters)


def format_environment(
  environment: dict,
  config: dict,
) -> dict:
  field = 'environment'

  for key, value in environment.items():
    environment[key] = os.getenv(key, value)

  environment = convert_dict_to_dataclass(
    data=environment,
    cls_name='Environment',
  )
  config[field] = environment

  return {
    field: None,
    'config': config,
  }


def format_schema(
  schema: dict | None = None,
  config: dict | None = None,
) -> dict:
  store = {}

  for scheme in schema:
    dict_ = {}

    fields = scheme.get('fields')
    for field in fields:
      dict_[field.get('name')] = field.get('default')

    cls_name = scheme.get('cls_name')
    scheme_dataclass = convert_dict_to_dataclass(
      data=dict_,
      cls_name=cls_name,
      instantiate=False,
    )

    store[cls_name] = scheme_dataclass

  store = convert_dict_to_dataclass(
    data=store,
    cls_name='Schema',
  )
  config['schema'] = store
  return {
    'schema': None,
    'config': config,
  }


def main(
  module: str | None = None,
  yaml: str | None = None,
  schema: str | dict | None = None,
  environment: str | dict | None = None,
  config: str | dict | None = None,
) -> Data_Class:
  data = process_arguments(locals_=locals())

  operations = Operations(names=CONFIG.get('operations'))
  for operation in operations.names:
    operations.function = LOCALS[operation]
    operations.parameters = get_function_parameters(
      function=operations.function
    )

    operations.fields = {}
    for parameter in operations.parameters:
      value = getattr(data, parameter, None)
      if value is None:
        continue
      operations.fields[parameter] = value

    operations.results = operations.function(**operations.fields)
    for key, value in operations.results.items():
      setattr(data, key, value)

  return data.config


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
