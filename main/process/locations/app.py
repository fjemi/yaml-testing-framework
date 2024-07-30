#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
from types import SimpleNamespace as sns
from typing import Any, List

from main.utils import get_config, independent, logger, objects


ROOT_DIR = os.path.abspath(os.curdir)
ROOT_DIR = os.path.normpath(ROOT_DIR)

SETTINGS = get_config.main()
LOCALS = locals()


def main(
  project_path: Any | None = None,
  include_files: str | List[str] | None = None,
  exclude_files: str | List[str] | None = None,
  yaml_suffix: str | None = None,
  logging_flag: bool | None = None,
  timestamp: int | float | None = None,
  setup: list = [],
) -> sns:
  path = project_path
  data = sns(**locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=SETTINGS.operations.main,
    data=data, )
  return sns(locations=data.files)


def format_project_path(project_path: str = '') -> sns:
  path = project_path
  if not path:
    path = ROOT_DIR
  elif  path[0] == '.':
    path = os.path.join(ROOT_DIR, path[1:])
  return sns(path=path)


def set_path_metadata(path: str = '') -> sns:
  kind = {
    True: 'none',
    os.path.isdir(path): 'directory',
    os.path.isfile(path): 'file', }
  kind = kind[True]

  flag = kind != 'file'
  directory = path if flag else os.path.dirname(path)
  return sns(
    path=path,
    kind=kind,
    directory=directory, )


def format_yaml_suffix(yaml_suffix: str = '') -> sns:
  yaml_suffix = yaml_suffix or SETTINGS.yaml_suffix
  if yaml_suffix.find('_') != 0:
    yaml_suffix = '_' + yaml_suffix
  return sns(yaml_suffix=yaml_suffix)


def format_as_list(value: Any | None = None) -> list:
  if isinstance(value, list):
    return value
  if value is not None:
    return [value]
  return []


def format_inclusion_and_exclusion_patterns(
  exclude_files: str | list = [],
  include_files: str | list = [],
) -> sns:
  locals_ = sns(**locals())
  for route, value in locals_.__dict__.items():
    value = format_as_list(value=value)
    setting = objects.get(
      parent=SETTINGS,
      route=route,
      default=[], )
    value = [*setting, *value]
    locals_ = objects.update(
      parent=locals_,
      route=route,
      value=value, )
  return locals_


def handle_path(
  exclude_files: list = [],
  include_files: list = [],
  yaml_suffix: str = '',
  path: str = '',
  directory: str = '',
  kind: str = '',
  setup: list = [],
) -> sns:
  arguments = sns(**locals())
  route = f'handle_{kind}'
  method = objects.get(
    parent=LOCALS,
    route=route,
    default=handle_none, )
  del arguments.kind
  return method(**arguments.__dict__)


def post_processing(
  files: list = [],
  path: str = '',
) -> None:
  if files:
    return
  logger.main(
    message=f'No modules collect from {path}',
    level='warning', )


def handle_none(*args, **kwargs) -> sns:
  _ = args, kwargs
  return sns(files=[])


def handle_file(
  exclude_files: list = [],
  include_files: list = [],
  yaml_suffix: str = '',
  path: str = '',
  directory: str = '',
  setup: list = [],
) -> sns:
  locals_ = sns(**locals())
  base, extension = os.path.splitext(path)
  locals_.include_files.append(base)
  return handle_directory(**locals_.__dict__)


def handle_directory(
  exclude_files: list = [],
  include_files: list = [],
  yaml_suffix: str = '',
  path: str = '',
  directory: str = '',
  setup: list = [],
) -> sns:
  data = sns(**locals())
  data = independent.process_operations(
    functions=LOCALS,
    operations=SETTINGS.operations.handle_directory,
    data=data, )
  return sns(files=data.files)


def get_files(directory: str = '') -> sns:
  store = []
  for root, dirs, files in os.walk(directory):
    for file_ in files:
      path = os.path.join(root, file_)
      store.append(path)
  return sns(files=store)


def filter_files(
  files: list = [],
  yaml_suffix: str = '',
  exclude_files: list = [],
  include_files: list = [],
) -> sns:
  store = []

  for file_ in files:
    base, extension = os.path.splitext(file_)
    base = sns(yaml=base, module=base.replace(yaml_suffix, ''))
    if False not in [
      flag_yaml(
        base=base.yaml,
        extension=extension,
        yaml_suffix=yaml_suffix, ),
      flag_include(base=base.module, include_files=include_files),
      flag_exclude(base=base.module, exclude_files=exclude_files),
    ]:
      store.append(file_)

  return sns(files=store)


def flag_yaml(
  base: str = '',
  extension: str = '',
  yaml_suffix: str = '',
) -> bool:
  return False not in [
    extension in SETTINGS.yaml_extensions,
    base.find(yaml_suffix) > -1,]


def flag_include(
  include_files: list = [],
  base: str = '',
) -> bool:
  include_files = [base] if not include_files else include_files
  for pattern in include_files:
    if True in [base.find(pattern) > -1, base == pattern]:
      return True
  return False


def flag_exclude(
  exclude_files: list = [],
  base: str = '',
) -> bool:
  for pattern in exclude_files:
    if True in [base.find(pattern) > -1, base == pattern]:
      return False
  return True


def set_module_route(module: str = '') -> str:
  module = str(module)
  base, exception = os.path.splitext(module)
  route = base.replace(ROOT_DIR, '')
  route = os.path.normpath(route)
  route = route.split(os.path.sep)
  return '.'.join(route)


def set_modules(
  files: list = [],
  yaml_suffix: str = '',
  directory: str = '',
  setup: list = [],
) -> sns:
  store = []

  for file_ in files:
    base, yaml_extension = os.path.splitext(file_)
    base = base.replace(yaml_suffix, '')

    for module_extension in SETTINGS.module_extensions:
      path = f'{base}{module_extension}'
      if not os.path.isfile(path):
        continue

      extensions = sns(yaml=yaml_extension, module=module_extension)
      paths = sns(
        phase_='module',
        setup=setup,
        module=path,
        module_route=set_module_route(module=path),
        yaml=file_,
        extensions=extensions,
        directory=directory, )
      store.append(paths)
      break

  return sns(files=store)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
