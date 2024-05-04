#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
from types import SimpleNamespace as sns
from typing import Any, List

from main.utils import get_config, independent


ROOT_DIR = os.path.abspath(os.curdir)
ROOT_DIR = os.path.normpath(ROOT_DIR)

MODULE = __file__
CONFIG = get_config.main()
LOCALS = locals()


def main(
  project_path: Any | None = None,
  include_files: str | List[str] | None = None,
  include_functions: str | List[str] | None = None,
  exclude_files: str | List[str] | None = None,
  exclude_functions: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  resources: list | str | None = None,
  logging_enabled: bool | None = None,
  timestamp: int | float | None = None,
) -> sns:
  # logger.main()
  path = project_path
  data = sns(**locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=CONFIG.operations.main,
    data=data, )

  data.locations = data.locations or []

  n = len(data.locations)
  log = None
  if not data.locations:
    log = sns(message=f'No modules at location {path}')
    log.level = 'error'

  return sns(locations=data.locations, log=log)


def format_paths(path: str | None = None) -> sns:
  root = ROOT_DIR

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
) -> bool:
  exclude_files = exclude_files or []
  for pattern in exclude_files:
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
  paths: sns | None = None,
  yaml_suffix: str | None = None,
) -> sns:
  _ = exclude_files

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
  paths: sns | None = None,
  yaml_suffix: str | None = None,
) -> sns:
  if paths.kind != 'directory':
    return sns()

  store = []

  for root, dirs, files in os.walk(paths.directory):
    if flag_for_exclusion(root=root, exclude_files=exclude_files):
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


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
