#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
import os
from types import ModuleType
from typing import Any, Callable, List

from error_handler.app import main as error_handler
from get_config.app import main as get_config
from utils import app as utils


MODULE = __file__
CONFIG = get_config(module=MODULE)

LOCALS = locals()

TEST_FIELDS = [field.name for field in dc.fields(CONFIG.schema.Test)]


@dc.dataclass
class Data_Class:
  pass


@error_handler()
async def pass_through(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> dict:
  return {}


@error_handler()
async def format_function_refactor(
  function: str | list | None = None,
)-> dict:
  function_ = function
  kind = type(function_).__name__.lower()

  if kind == 'list':
    for item in function_:
      if not item:
        continue
      function_ = item
      break

  elif kind == 'nonetype':
    function_ = ''

  return {
    'function': function_,
    'function_name': function_, }


@error_handler()
async def format_exclude_functions_refactor(
  exclude_functions: str | list | None = None,
)-> dict:
  return format_field_as_list(
    field='exclude_functions',
    value=exclude_functions, )


@error_handler()
async def format_field_as_list(
  value: Any | None = None,
  field: str | None = None,
)-> dict | None:
  kind = type(value).__name__.lower()

  if kind in ['list', 'tuple']:
    return {field: value}

  elif kind == 'nonetype':
    return {field: []}

  elif kind not in ['list', 'tuple', 'nonetype']:
    return {field: [value]}


@error_handler()
async def format_exclude_modules_refactor(
  exclude_modules: str | list | None = None,
)-> dict:
  return format_field_as_list(
    field='exclude_modules',
    value=exclude_modules, )


@error_handler()
async def format_resources_refactor(
  resources: str | list | None = None,
) -> dict:
  return format_field_as_list(
    field='resources',
    value=resources, )


@error_handler()
async def format_description_refactor(
  description: str | list | None = None,
) -> dict:
  return format_field_as_list(
    field='description',
    value=description, )


@error_handler()
async def format_field_as_str(
  value: Any | None = None,
  field: str | None = None,
) -> dict:
  kind = type(value).__name__.lower()

  if kind == 'str':
    pass

  elif kind == 'list':
    temp = ''
    for item in value:
      if item:
        temp = item
        break
    value = temp

  elif kind == 'nonetype':
    value = ''

  else:
    value = str(value)

  return {field: value}


@error_handler()
async def format_module_refactor(
  module: str | None = None,
) -> dict:
  return format_field_as_str(
    field='module',
    value=module, )


@error_handler()
async def format_yaml_refactor(
  yaml: dict | None = None,
) -> dict:
  return format_field_as_str(
    field='yaml',
    value=yaml, )


@error_handler()
async def format_arguments_refactor(
  arguments: list | dict | None = None,
) -> dict:
  return format_field_as_dict(
    field='arguments',
    value=arguments, )


@error_handler()
async def format_cast_arguments_refactor(
  cast_arguments: list | dict | None = None,
) -> dict:
  return format_field_as_list(
    field='cast_arguments',
    value=cast_arguments, )


@error_handler()
async def format_cast_output_refactor(
  cast_output: list | dict | None,
) -> dict:
  return format_field_as_list(
    field='cast_output',
    value=cast_output, )


@error_handler()
async def format_field_as_dict(
  field: str | None = None,
  value: Any | None = None,
) -> dict:
  kind = type(value).__name__.lower()

  if kind == 'dict':
    pass

  elif kind == 'list':
    store = {}

    for item in value:
      if not isinstance(item, dict):
        continue

      for key, sub_value in item.items():
        store[key] = sub_value

    value = store

  elif kind == 'nonetype':
    value = {}

  return {field: value}

@error_handler()


async def format_environment_refactor(
  environment: Any | None = None,
) -> dict:
    return format_field_as_dict(
    field='environment',
    value=environment, )


@error_handler()
async def format_patches_refactor(
  patches: Any | None = None,
) -> dict:
  return format_field_as_list(
    field='patches',
    value=patches )


@error_handler()
async def format_assertions_refactor(
  assertions: Any | None = None,
) -> dict:
  return format_field_as_list(
    field='assertions',
    value=assertions, )


@error_handler()
async def format_id_long_refactor(
  description: str | List[str] | None = None,
  function: Callable | str | None = None,
  module: ModuleType | Callable | None = None,
  yaml: str | None = None,
) -> dict:
  id_long = {
    'function': function,
    'module': module,
    'yaml': yaml,
    'description': description, }
  return {'id_long': id_long}


def format_project_directory_refactor(
  project_directory: str | None = None,
) -> dict:
  kind = type(project_directory).__name__.lower()

  if kind == 'list':
    temp = ''

    for item in project_directory:
      if item:
        temp = item
        break

    project_directory = temp

  elif kind == 'nonetype':
    project_directory = ''

  project_directory = project_directory.split(os.sep)
  project_directory = '.'.join(project_directory)

  return {'project_directory': project_directory}


@error_handler()
async def format_id_short_refactor(
  module_location: str | None = None,
  function: str | None = None,
  description: str | List[str] | None = None,
) -> dict:
  locals_ = locals()

  kind = type(description).__name__.lower()
  if kind == 'list':
    temp = ''

    for item in reversed(description):
      if item:
        temp = item
        break

    description = temp
  elif kind == 'nonetype':
    description = ''

  kind = type(module_location).__name__.lower()
  if kind == 'list':
    temp = ''

    for item in reversed(module_location):
      if item:
        temp = item
        break

    module_location = temp
  elif kind == 'nonetype':
    module_location = ''

  function_ = function
  kind = type(function_).__name__.lower()
  if kind == 'list':
    temp = ''
    for item in reversed(function_):
      if item:
        temp = item
        break
    function_ = temp
  elif kind == 'nonetype':
    function_ = ''

  id_short = f' {module_location}.{function_} - {description} '
  return {'id_short': id_short}


@error_handler()
async def main(
  tests: List[dict] | None = None,
) -> dict:
  tests = [] if not tests else tests
  n = reversed(range(len(tests)))

  for i in n:
    tests[i] = utils.process_operations(
    operations=CONFIG.main_operations,
    functions=LOCALS,
    data=tests[i], )
    test = utils.process_arguments(
      locals=tests[i],
      data_class=CONFIG.schema.Test, )
    tests[i] = {'test': test}

  return {'tests': tests}


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
