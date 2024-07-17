#!.venv/bin/python3
# -*- coding: utf-8 -*-


import inspect
import os

# trunk-ignore(bandit/B404)
import subprocess
from types import SimpleNamespace as sns
from typing import List

import yaml as pyyaml

from main import app
from main.utils import independent


LOCATION = __file__
LOCALS = locals()

CONFIG = '''
  default_arguments:
    resources_folder_name: ''
    yaml_suffix: _test
    resource_suffix: _resource
    exclude_files:
    - ignore
    - resource
    # module: null
    resource_flag: False
    root_flag: False
    # module_filename: app
    method: plugin
    # location: .
    logging_flag: true
  operations:
    main:
    - set_default_values_for_arguments
    - set_location
    - run_tests_using_invocation_method
'''
CONFIG = independent.format_module_defined_config(
  config=CONFIG)


# trunk-ignore(ruff/PLR0913)
def main(
  location: str | None = None,
  module: str | None = None,
  module_filename: str | None = None,
  resource_flag: bool | None = None,
  root_flag: bool | None = None,
  exclude_files: str | None = None,
  resources_folder_name: str | None = None,
  resource_suffix: str | None = None,
  yaml_suffix: str | None = None,
  method: str | None = None,
  logging_flag: bool | None = None,
) -> int:
  module = module or inspect.stack()[1].filename
  data = sns(**locals())
  data = independent.process_operations(
    data=data,
    operations=CONFIG.operations.main,
    functions=LOCALS, )
  return getattr(data, 'result', [])


# trunk-ignore(ruff/PLR0913)
def set_default_values_for_arguments(
  location: str | None = None,
  module: str | None = None,
  module_filename: str | None = None,
  exclude_files: str | None = None,
  resources_folder_name: str | None = None,
  yaml_suffix: str | None = None,
  resource_suffix: str | None = None,
  method: str | None = None,
  resource_flag: bool | None= None,
  root_flag: bool | None= None,
  logging_flag: bool | None = None,
) -> sns:
  data = sns(**locals())
  for key, default in CONFIG.default_arguments.items():
    value = getattr(data, key, None)
    if value is None:
      setattr(data, key, default)
  return data


def get_parent_module_location(
  parent_filename: str | None = None,
  resource_module: str | None = None,
  resource_suffix: str | None = None,
  resources_folder_name: str | None = None,
) -> str:
  directory, filename = os.path.split(resource_module)

  if resource_suffix:
    filename = filename.replace(resource_suffix, '')

  if resources_folder_name:
    index = directory.rfind(resources_folder_name)
    directory = directory[:index]

  if parent_filename:
    index = resource_module.rfind('.')
    extension = resource_module[index:]
    filename = f'{parent_filename}{extension}'

  module = os.path.join(directory, filename)
  return os.path.normpath(module)


def set_location(
  location: str | None = None,
  module: str | None = None,
  module_filename: str | None = None,
  resource_flag: str | None = None,
  resource_suffix: str | None = None,
  root_flag: bool | None = None,
  resources_folder_name: str | None = None,
) -> sns:
  if resource_flag:
    location = get_parent_module_location(
      resource_module=module,
      resource_suffix=resource_suffix,
      resources_folder_name=resources_folder_name,
      parent_filename=module_filename, )

  elif root_flag:
    location = '.'

  elif not resource_flag and not root_flag and not location:
    location = module

  return sns(
    location=location,
    _cleanup=['module', 'root_flag', 'resource_flag'], )


def run_tests_using_invocation_method(
  method: str | None = None,
  location: str | None = None,
  exclude_files: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
) -> sns:
  data = sns(**locals())
  delattr(data, 'method')
  method = f'invoke_{method}'
  method = LOCALS.get(method, invoke_plugin)
  return method(**data.__dict__)


def invoke_plugin(
  location: str | None = None,
  exclude_files: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
) -> sns:
  result = app.main(
    exclude_files=exclude_files,
    project_path=location,
    yaml_suffix=yaml_suffix,
    logging_flag=logging_flag, )
  return sns(result=result)


def invoke_pytest(
  location: str | None = None,
  exclude_files: str | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
) -> sns:
  _ = exclude_files

  args = f'''
    - python3
    - -m
    - pipenv
    - run
    - python3
    - -m
    - pytest
    - --no-cov
    - --tb=short
    - --project-path={location}
    - --yaml-suffix={yaml_suffix}
    - --logging-flag={logging_flag}
    - -p no:yaml_testing_framework
  '''
  args = pyyaml.safe_load(args)
  process = subprocess.run(
    args=args,
    shell=True,
    check=True,  )
  return sns(process=process)


def examples() -> None:
  main(location=location)


if __name__ == '__main__':
  examples()
