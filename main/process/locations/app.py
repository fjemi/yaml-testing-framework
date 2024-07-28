#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
from types import SimpleNamespace as sns
from typing import Any, List

from main.utils import get_config, independent, logger, objects


ROOT_DIR = os.path.abspath(os.curdir)
ROOT_DIR = os.path.normpath(ROOT_DIR)

CONFIG = get_config.main()
LOCALS = locals()


def main(
  project_path: Any | None = None,
  include_files: list| None = None,
  exclude_files: list | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
  timestamp: int | float | None = None,
) -> sns:
  data = sns(**locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=CONFIG.operations.main,
    data=data, )
  locations = objects.get(
    parent=data,
    route='paths',
    default=[], )
  return sns(locations=locations)


def format_path(project_path: str = '') -> sns:
  path = str(project_path)
  add_root = {
    True: path,
    path in CONFIG.roots: ROOT_DIR,
    path[0] == '.': os.path.join(ROOT_DIR, path[1:]), }
  path = add_root[True]
  return sns(path=path)


def format_yaml_suffix(yaml_suffix: str | None = None) -> sns:
  yaml_suffix = yaml_suffix or CONFIG.yaml_suffix
  if yaml_suffix.find('_') != 0:
    yaml_suffix = '_' + yaml_suffix
  return sns(yaml_suffix=yaml_suffix)


def convert_to_list(object_: str | list | None = None) -> list | None:
  if isinstance(object_, list):
    return object_
  if isinstance(object_, str):
    return [object_]
  if object_ is None:
    return []


def format_inclusion_and_exclusion_patterns(
  exclude_files: str | list | None = None,
  include_files: str | list | None = None,
) -> sns:
  locals_ = sns(**locals())

  for route, patterns in locals_.__dict__.items():
    settings = objects.get(parent=CONFIG, route=route) or []
    settings = convert_to_list(object_=settings)
    patterns = convert_to_list(object_=patterns)
    patterns = [*patterns, *settings]
    locals_ = objects.update(parent=locals_, route=route, value=patterns, )

  return sns(
    exclude_files=locals_.exclude_files,
    include_files=locals_.include_files, )


def get_paths(
  path: str = '',
  yaml_suffix: str = '',
  exclude_files: list | None = None,
  include_files: list | None = None,
) -> sns:
  locals_ = sns(**locals())
  handlers = {
    True: 'handle_none',
    os.path.isfile(path): 'handle_file',
    os.path.isdir(path): 'handle_directory', }
  handler = handlers[True]
  handler = LOCALS[handler]
  return handler(**locals_.__dict__)


def handle_file(
  path: str | None = None,
  yaml_suffix: str = '',
  exclude_files: list = [],
  include_files: list | None = None,
) -> sns:
  directory = os.path.dirname(path)
  base, extension = os.path.splitext(path)
  include_files = include_files or []
  locals_ = sns(**locals())

  module_base = base.replace(yaml_suffix, '')
  include_files.extend([
    path,
    base,
    module_base, ])
  return handle_directory(**locals_.__dict__)


def handle_directory(
  path: str | None = None,
  directory: str | None = None,
  base: str | None = None,
  extension: str | None = None,
  yaml_suffix: str = '',
  exclude_files: list = [],
  include_files: list = [],
) -> sns:
  directory = directory or path
  data = sns(**locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=CONFIG.operations.handle_directory,
    data=data, )
  if not data.paths:
    logger.main(
      message=f'No modules at location {path}',
      arguments=data.__dict__,
      level='warning', )
  return sns(paths=data.paths)


def set_exclusion_flag(
  path: str | None = None,
  base: str | None = None,
  exclude_files: list | None = None,
) -> bool:
  if not exclude_files:
    return False

  for pattern in exclude_files:
    for item in [base, path]:
      if True in [
        item == pattern,
        item.find(pattern) > -1,
        pattern.find(item) > -1,
      ]:
        return True

  return False


def set_inclusion_flag(
  path: str | None = None,
  base: str | None = None,
  include_files: list | None = None,
) -> bool:
  return True if not include_files else set_exclusion_flag(
    path=path,
    base=base,
    exclude_files=include_files, )


def set_module_route(path: str | None = None) -> str:
  route = path.replace(ROOT_DIR, '')
  route = os.path.splitext(route)[0]
  route = os.path.normpath(route)
  route = route.split(os.path.sep)
  return '.'.join(route)


def get_yaml_paths(
  directory: str | None = None,
  yaml_suffix: str | None = None,
  include_files: list | None = None,
  exclude_files: list | None = None,
) -> sns:
  paths = []
  temp = sns()

  for root, dirs, files in os.walk(directory):
    for item in files:
      temp.path = os.path.join(root, item)
      base, extension = os.path.splitext(temp.path)
      ending = f'{yaml_suffix}{extension}'

      if False in [
        extension in CONFIG.yaml_extensions,
        base.find(yaml_suffix) != -1,
        not set_exclusion_flag(
          base=base,
          path=temp.path,
          exclude_files=exclude_files, ),
        set_inclusion_flag(
          base=base,
          path=temp.path,
          include_files=include_files, ),
      ]:
        continue

      temp.path = os.path.normpath(temp.path)
      temp.directory = os.path.dirname(temp.path)
      yaml = sns(
        directory=temp.directory,
        path=temp.path,
        base=base,
        extension=extension, )
      yaml = sns(yaml=yaml)
      paths.append(yaml)

  return sns(paths=paths)


def get_module_paths(
  paths: list | None = None,
  yaml_suffix: str | None = None,
) -> sns:

  for i, item in enumerate(paths):
    path = ''
    extension = ''
    base = item.yaml.base.replace(yaml_suffix, '')

    for temp_extension in CONFIG.module_extensions:
      temp_path = f'{base}{temp_extension}'
      if not os.path.isfile(temp_path):
        continue

      path = temp_path
      extension = temp_extension
      break

    route = set_module_route(path=path)
    item.module = sns(
      extension=extension,
      base=base,
      path=path,
      route=route,
      directory=item.yaml.directory, )
    paths[i] = item
  
  return sns(paths=paths)


def post_processing(paths: list | None = None) -> sns:
  store = []

  for item in paths:
    location = sns(
      phase_='module',
      module=item.module.path,
      module_route=item.module.route,
      yaml=item.yaml.path,
      directory=item.module.directory, )
    store.append(location)

  return sns(paths=store)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
