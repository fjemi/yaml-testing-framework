#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
import os
from typing import Any, List

import utils.app as utils
from error_handler.app import main as error_handler
from get_config.app import main as get_config


ROOT_DIRECTORY = os.path.abspath(os.curdir)
ROOT_DIRECTORY = f'{ROOT_DIRECTORY}/'
MODULE = __file__
CONFIG = get_config(module=MODULE)
LOCALS = locals()


@dc.dataclass
class Data_Class:
  pass


ITERABLE_KINDS = [
  'list',
  'tuple',
]


@error_handler()
async def format_project_directory(
  project_directory: str | list | None = None,
) -> dict:
  kind = type(project_directory).__name__.lower()

  if kind in ITERABLE_KINDS:
    project_directory = project_directory[0]
  elif kind == 'nonetype':
    project_directory = ROOT_DIRECTORY

  condition = project_directory[0] == '.'
  if condition:
    project_directory = os.path.join(
      ROOT_DIRECTORY,
      project_directory[1:],
    )

  project_directory_type = [
    'file' * int(os.path.isfile(project_directory)),
    'directory' * int(os.path.isdir(project_directory)),
  ]
  project_directory_type = ''.join(project_directory_type)

  return {
    'project_directory_type': project_directory_type,
    'root_directory': ROOT_DIRECTORY,
    'project_directory': project_directory,
  }


@error_handler()
async def format_exclude_files(
  exclude_files: str | List[str] | None = None,
) -> dict:
  kind = type(exclude_files).__name__.lower()

  if kind == 'list':
    exclude_files = [*exclude_files, *CONFIG.exclude_files]
  elif kind == 'str':
    exclude_files = [exclude_files, *CONFIG.exclude_files]
  elif kind == 'nonetype':
    exclude_files = CONFIG.exclude_files

  return {'exclude_files': exclude_files}


@error_handler()
async def format_resources_folder_name(
  resources_folder_name: str | None = None,
) -> dict:
  if resources_folder_name in CONFIG.empty_values:
    resources_folder_name = CONFIG.resources_folder_name
  return {'resources_folder_name': resources_folder_name}


@error_handler()
async def format_yaml_suffix(
  yaml_suffix: str | None = None,
) -> dict:
  if yaml_suffix in CONFIG.empty_values:
    yaml_suffix = CONFIG.yaml_suffix
  return {'yaml_suffix': yaml_suffix}


@error_handler()
async def format_resources(
  resources: dict | None = None,
) -> dict:
  if resources in CONFIG.empty_values:
    resources = []
  elif isinstance(resources, str) is True:
    resources = [resources]
  return {'resources': resources}


@error_handler()
async def check_location_for_matching_extensions(
  location: str | None = None,
  extensions: str | List[str] | None = None,
) -> str:
  conditions = [
    not location,
    not extensions,
  ]
  if sum(conditions) != 0:
    return location

  if isinstance(extensions, list) is False:
    extensions = [extensions]

  extension = os.path.splitext(location)[1]
  if extension not in extensions:
    location = ''
  return location


@error_handler()
async def check_location_for_exclusion_patterns(
  location: str | None = None,
  patterns: str | List[str] | None = None,
) -> str:
  conditions = [
    not location,
    not patterns,
  ]
  if sum(conditions) != 0:
    return location

  for pattern in patterns:
    if location.find(str(pattern)) > -1:
      return ''

  return location


@error_handler()
async def check_location_for_matching_patterns(
  location: str | None = None,
  patterns: str | List[str] | None = None,
) -> str:
  conditions = [
    not location,
    not patterns,
  ]
  if sum(conditions) != 0:
    return location

  for pattern in patterns:
    if location.find(pattern) > -1:
      return location

  return ''


@error_handler()
async def get_file_locations(
  directory: str | None = None,
  match_patterns: str | List[str] | None = None,
  exclude_patterns: str | List[str] | None = None,
  match_extensions: str | List[str] | None = None,
  file_type: str | None = None,
) -> dict:
  locations = []

  directory = str(directory)
  if os.path.exists(directory) is False:
    return {'locations': locations}

  for path, subdirs, files in os.walk(directory):
    for name in files:
      location = os.path.join(path, name)
      location = check_location_for_matching_extensions(
        location=location,
        extensions=match_extensions,
      )
      location = check_location_for_exclusion_patterns(
        location=location,
        patterns=exclude_patterns,
      )
      location = check_location_for_matching_patterns(
        location=location,
        patterns=match_patterns,
      )

      if location in CONFIG.empty_values:
        continue

      if file_type != 'resources':
        location = {file_type: location}

      locations.append(location)

  return {'locations': locations}


@error_handler()
async def format_module_locations(
  root_directory: str | None = None,
  locations: List[dict] | None = None,
) -> dict:
  locations = locations or []
  n = range(len(locations))

  for i in n:
    module = locations[i].get('module', '')
    condition = module not in CONFIG.empty_values

    if condition:
      module_location = module.replace(CONFIG.module_extension, '')
      module_location = module_location.replace(root_directory, '')
      module_location = module_location.split(os.sep)
      module_location = '.'.join(module_location)

    elif not condition:
      module_location = ''

    locations[i]['module_location'] = module_location

  return {'locations': locations}


@error_handler()
async def get_modules(
  locations: List[dict] | None = None,
  yaml_suffix: str | None = None,
  # trunk-ignore(ruff/ARG001)
  project_directory: str | None = None,
  project_directory_type: str | None = None,
) -> dict:
  conditions = [
    project_directory_type == '',
    project_directory_type == 'file',
  ]
  if True in conditions:
    return {'locations': locations}

  n = range(len(locations))

  for i in n:
    location = locations[i].get('yaml', '')

    extension = os.path.splitext(location)[1]
    match = f'{yaml_suffix}{extension}'
    index = location.rfind(match)

    if index != -1:
      module = location[:index] + CONFIG.module_extension
    elif index == -1:
      module = ''

    locations[i]['module'] = module

  return {'locations': locations}


@error_handler()
async def get_yamls(
  exclude_files,
  resources_folder_name,
  project_directory,
  project_directory_type,
  yaml_suffix,
) -> dict:
  condition = resources_folder_name not in exclude_files
  if condition:
    exclude_files.append(resources_folder_name)

  if project_directory_type == 'directory':
    return get_file_locations(
      directory=project_directory,
      exclude_patterns=exclude_files,
      match_extensions=CONFIG.yaml_extensions,
      file_type='yaml',
    )
  elif project_directory_type == 'file':
    module = None
    yaml = None

    extension = os.path.splitext(project_directory)[1]
    condition = extension == CONFIG.module_extension

    if condition:
      module = project_directory
      for yaml_extension in CONFIG.yaml_extensions:
        location = project_directory.replace(
          CONFIG.module_extension,
          f'{yaml_suffix}{yaml_extension}'
        )
        if os.path.exists(location):
          yaml = location
          break
    elif not condition:
      yaml = project_directory
      key = f'{yaml_suffix}{extension}'
      module = yaml.replace(
        key,
        CONFIG.module_extension,
      )

    locations = [{
      'module': module,
      'yaml': yaml,
    }]
    return {'locations': locations}


@error_handler()
async def get_resources(
  resources_folder_name: str | None = None,
  exclude_files: List[str] | None = None,
  resources: List[str] | None = None,
  locations: List[dict] | None = None,
) -> dict:
  if resources_folder_name in exclude_files:
    exclude_files.remove(resources_folder_name)

  if not resources:
    resources = []

  n = reversed(range(len(locations)))

  for i in n:
    module = locations[i].get('module', '')

    condition = module in CONFIG.empty_values
    if condition:
      del locations[i]
      continue

    directory = os.path.dirname(module)
    directory = os.path.join(
      directory,
      resources_folder_name,
    )

    store = get_file_locations(
      directory=directory,
      exclude_patterns=exclude_files,
      match_extensions=CONFIG.module_extension,
      file_type='resources',
    )
    store = store.get('locations', [])
    locations[i]['resources'] = [*resources, *store]

  return {'locations': locations}


@error_handler()
async def main(
  project_directory: Any | None = None,
  include_files: str | List[str] | None = None,
  include_functions: str | List[str] | None = None,
  exclude_files: str | List[str] | None = None,
  exclude_functions: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  resources_folder_name: str | None = None,
) -> dict:
  data = utils.process_arguments(
    locals=locals(),
    data_class=CONFIG.schema.Locations,
  )
  data = utils.process_operations(
    functions=LOCALS,
    data=data,
    operations=CONFIG.operations,
  )
  return {'locations': data.locations}


@error_handler()
async def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
