#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
from types import SimpleNamespace as sns
from typing import Any, List

from main.utils import get_config, independent


YAML_TESTING_FRAMEWORK_ROOT_DIRECTORY = os.path.abspath(os.curdir)
YAML_TESTING_FRAMEWORK_ROOT_DIRECTORY = os.path.normpath(YAML_TESTING_FRAMEWORK_ROOT_DIRECTORY)

MODULE = __file__
CONFIG = get_config.main()
LOCALS = locals()


def main(
  project_directory: Any | None = None,
  include_files: str | List[str] | None = None,
  include_functions: str | List[str] | None = None,
  exclude_files: str | List[str] | None = None,
  exclude_functions: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  resources_folder_name: str | None = None,
  resources: list | str | None = None,
  logging_enabled: bool | None = None,
  timestamp: int | float | None = None,
) -> sns:
  # logger.main()
  path = project_directory
  data = sns(**locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=CONFIG.main_operations,
    data=data, )

  data.locations = data.locations or []

  n = len(data.locations)
  log = None
  if not data.locations:
    log = sns(message=f'No modules at location {path}')
    log.level = 'error'

  return sns(locations=data.locations, log=log)


def format_paths(path: str | None = None) -> sns:
  root = YAML_TESTING_FRAMEWORK_ROOT_DIRECTORY

  if not path:
    path = '.'
  if path[0] == '.':
    path = f'{root}/{path[1:]}'

  path = os.path.normpath(path)
  directory = path
  kind = ''

  if os.path.isfile(directory):
    kind = 'file'
    directory = os.path.dirname(directory)
  elif os.path.isdir(directory):
    kind = 'directory'

  paths = sns(**locals())
  return sns(paths=paths)


def format_yaml_suffix(yaml_suffix: str | None = None) -> sns:
  yaml_suffix = yaml_suffix or CONFIG.yaml_suffix
  if yaml_suffix.find('_') != 0:
    yaml_suffix = '_' + yaml_suffix
  return sns(yaml_suffix=yaml_suffix)


def format_resources_folder_name(
  resources_folder_name: str | None = None,
) -> sns:
  resources_folder_name = resources_folder_name or CONFIG.resources_folder_name
  return sns(resources_folder_name=resources_folder_name)


def format_exclude_files(exclude_files: str | list | None = None) -> sns:
  if isinstance(exclude_files, list):
    exclude_files = [*exclude_files, *CONFIG.exclude_files]
  elif isinstance(exclude_files, str):
    exclude_files = [exclude_files, *CONFIG.exclude_files]
  elif exclude_files is None:
    exclude_files = CONFIG.exclude_files

  return sns(exclude_files=exclude_files)


def format_resources(resources: list | str | None = None) -> sns:
  if resources is None:
    resources = []
  elif not isinstance(resources, list):
    resources = [str(resources)]
  return sns(resources=resources)


def flag_for_exclusion(
  root: str | None = None,
  exclude_files: list | None = None,
  resources_folder_name: str | None = None,
) -> bool:
  exclude_files = exclude_files or []
  patterns = [*exclude_files, str(resources_folder_name)]
  for pattern in patterns:
    if root.find(pattern) > -1:
      return True
  return False


def get_route_for_module(
  root: str | None = None,
  module: str | None = None,
) -> str:
  route = module.replace(root, '')
  route = route.replace(CONFIG.module_extension, '')
  route = route.split(os.path.sep)
  return '.'.join(route)


def get_module_and_yaml_location_when_path_kind_is_file(
  exclude_files: list | None = None,
  resources_folder_name: str | None = None,
  paths: sns | None = None,
  yaml_suffix: str | None = None,
) -> sns:
  _ = exclude_files, resources_folder_name

  data = sns(locations=[])

  if getattr(paths, 'kind', None) != 'file':
    return data

  location = sns(module=None, yaml=None)
  file_extension = os.path.splitext(paths.path)[-1]

  if file_extension == CONFIG.module_extension:
    location.module = paths.path

    for extension in CONFIG.yaml_extensions:
      yaml_ending = f'{yaml_suffix}{extension}'
      temp = paths.path.replace(CONFIG.module_extension, yaml_ending)
      if os.path.isfile(temp):
        location.yaml = temp
        break

  elif file_extension in CONFIG.yaml_extensions:
    location.yaml = paths.path
    yaml_extension = os.path.splitext(paths.path)[-1]
    yaml_ending = f'{yaml_suffix}{yaml_extension}'
    location.module = location.yaml.replace(
      yaml_ending,
      CONFIG.module_extension, )

  location.module_route = get_route_for_module(
    root=paths.root,
    module=location.module, )
  location.module_location = location.module
  data.locations.append(location)
  return data


def get_module_and_yaml_location_when_path_kind_is_directory(
  exclude_files: list | None = None,
  resources_folder_name: str | None = None,
  paths: sns | None = None,
  yaml_suffix: str | None = None,
) -> sns:
  if paths.kind != 'directory':
    return sns()

  store = []

  for root, dirs, files in os.walk(paths.directory):
    if flag_for_exclusion(
      root=root,
      exclude_files=exclude_files,
      resources_folder_name=resources_folder_name,
    ):
      continue

    for file in files:
      for extension in CONFIG.yaml_extensions:
        yaml_ending = f'{yaml_suffix}{extension}'
        if not file.endswith(yaml_ending):
          continue

        location = sns(
          yaml=os.path.join(root, file), )
        location.module = location.yaml.replace(
          yaml_ending,
          CONFIG.module_extension, )
        location.module_location = location.module
        location.module_route = get_route_for_module(
          root=paths.root,
          module=location.module, )
        store.append(location)

  return sns(locations=store)


def get_location_of_resources(
  locations: list | None = None,
  resources_folder_name: str | None = None,
  exclude_files: list | None = None,
) -> sns:
  for item in locations:
    resources = []
    directory = os.path.dirname(item.module)
    directory = os.path.join(directory, resources_folder_name)

    for root, dirs, files in os.walk(directory):
      if flag_for_exclusion(root=root, exclude_files=exclude_files):
        continue

      for file in files:
        if file.endswith(CONFIG.module_extension):
          location = os.path.join(root, file)
          resources.append(location)

    item.resources = resources

  return sns(locations=locations)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
