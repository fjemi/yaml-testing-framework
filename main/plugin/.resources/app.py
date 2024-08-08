#!.venv/bin/python3
# -*- coding: utf-8 -*-


import types
from types import SimpleNamespace as sns
from unittest import mock

import pytest

from main.utils import configs, invoke


MODULE = __file__
PARENT_MODULE = invoke.get_parent_module_location(
  resource_module=MODULE,
  resources_folder_name='_resources', )

CONFIG = configs.main(module=PARENT_MODULE)


def pytest_resource(*args, **kwargs) -> types.ModuleType:
  _ = args, kwargs
  return pytest


def get_locals(*args, **kwargs) -> dict:
  _ = args, kwargs

  return {
    'process_option_option_0':
    # trunk-ignore(ruff/ARG005)
    lambda *args,
    # trunk-ignore(ruff/ARG005)
    **kwargs: 'processed_value_0',
    'process_option_option_1':
    # trunk-ignore(ruff/ARG005)
    lambda *args,
    # trunk-ignore(ruff/ARG005)
    **kwargs: 'processed_value_1',
  }


def project_path_option_resource(option: str | None) -> str:
  if True in [
    option is None,
    option == '.',
  ]:
    option = 'YAML_TESTING_FRAMEWORK_ROOT_DIR'
  return option


def process_option_project_path_resource(
  arguments: dict | None = None,
) -> pytest.Config:
  arguments = arguments or {}

  option = arguments.get('option', None)
  option = project_path_option_resource(option=option)

  config = pytest.Config
  setattr(config, 'rootdir', option)

  arguments.update({
    'option': option,
    'config': config, })
  return arguments


def get_options_or_inis_resource(*args, **kwargs) -> mock:
  _ = args, kwargs
  return mock


def pytest_parser_resource(parser: str | None = None) -> pytest.Parser:
  _ = parser
  return pytest.Parser()


def pytest_configure_resource(
  config: str | None = None,
) -> pytest.Config | None:
  import pytest as instance
  if config:
    pluginmanager = mock.Mock()
    config = instance.Config(pluginmanager=pluginmanager)

    ini_cache = sns(yaml_suffix='_test', project_path=PARENT_MODULE).__dict__
    opt_2_dest = {}
    for key, value in ini_cache.items():
      opt_key = f'--{key}'.replace('_', '-')
      opt_2_dest[opt_key] = value

    config._opt2dest = opt_2_dest
    config._inicache = ini_cache
    return config


def set_node_ids_resource(item: str | None = None) -> sns:
  if not item:
    return {}
  test = sns(id_short=item)
  params = {'test': test}
  callspec = sns(params=params)
  item = sns(callspec=callspec)
  return item


def examples() -> None:
  from main.utils import invoke

  invoke.main(project_path=PARENT_MODULE)


if __name__ == '__main__':
  examples()
