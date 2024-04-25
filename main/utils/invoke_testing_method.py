#!.venv/bin/python3
# -*- coding: utf-8 -*-

import inspect
import os

# trunk-ignore(bandit/B404)
import subprocess
from types import SimpleNamespace as sns
from typing import List

import yaml
from utils import independent

from main.app import main as plugin


MODULE = __file__
LOCALS = locals()

CONFIG = '''
  default_arguments:
    resources_folder_name: _resources
    yaml_suffix: _test
    resource_suffix: _resource
    exclude_files:
    - ignore
    - _resources
    # module: null
    resource_flag: False
    root_flag: False
    # module_filename: app
    method: plugin
    # location: .
    logging_enabled: true
  main_operations:
  - set_default_values_for_arguments
  - set_location
  - run_tests_using_invocation_method
'''
CONFIG = yaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)

PYTEST_YAML_DEBUG = os.getenv('PYTEST_YAML_DEBUG')


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
  logging_enabled: bool | None = None,
) -> int:
  module = module or inspect.stack()[1].filename
  data = sns(**locals())
  data = independent.process_operations(
    data=data,
    operations=CONFIG.main_operations,
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
  logging_enabled: bool | None = None,
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
  resources_folder_name: str | None = None,  # root resources folder
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
  resources_folder_name: str | None = None,
  yaml_suffix: str | None = None,
  logging_enabled: bool | None = None,
) -> sns:
  data = sns(**locals())
  delattr(data, 'method')
  method = f'invoke_{method}'
  method = LOCALS.get(method, invoke_plugin)
  return method(**data.__dict__)


def invoke_plugin(
  location: str | None = None,
  exclude_files: str | List[str] | None = None,
  resources_folder_name: str | None = None,
  yaml_suffix: str | None = None,
  logging_enabled: bool | None = None,
) -> sns:
  result = plugin(
    exclude_files=exclude_files,
    project_directory=location,
    yaml_suffix=yaml_suffix,
    resources_folder_name=resources_folder_name,
    logging_enabled=logging_enabled, )
  independent.get_task_from_event_loop(task=result)
  return sns(result=result)


def invoke_pytest(
  location: str | None = None,
  exclude_files: str | None = None,
  resources_folder_name: str | None = None,
  yaml_suffix: str | None = None,
  logging_enabled: bool | None = None,
) -> sns:
  _ = exclude_files

  args = f'''
    pytest
    --no-cov
    -s
    -vvv
    -ra
    --tb=short
    --resources-folder-name={resources_folder_name}
    --project-directory={location}
    --yaml-suffix={yaml_suffix}
    --logging-enabled={logging_enabled}
  '''
  args = args.split('\n')
  args = [arg.strip() for arg in args if arg != '']

  process = subprocess.run(
    args=args,
    # trunk-ignore(bandit/B603)
    shell=False,
    check=True,
    capture_output=True,
    text=True, )
  return sns(process=process)


def examples() -> None:
  main(location=MODULE)


if __name__ == '__main__':
  examples()