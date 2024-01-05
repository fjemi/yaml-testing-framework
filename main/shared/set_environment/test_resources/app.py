#!.venv/bin/python3
# -*- coding: utf-8 -*-

import types

import utils.app as utils


MODULE = __file__
PARENT_MODULE = utils.get_parent_module(
  module=MODULE,
  resources_folder_name='test_resources',
)


def module_resource(
  module: str | None = None,
) -> types.ModuleType | None:

  if module == 'config_environment_does_exist':
    from main.shared.set_environment.test_resources import (
      config_environment_does_exist,
    )

    return config_environment_does_exist

  elif module == 'config_environment_does_not_exist':
    from main.shared.set_environment.test_resources import (
      config_environment_does_not_exist,
    )

    return config_environment_does_not_exist


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(project_directory=PARENT_MODULE)


if __name__ == '__main__':
  example()
