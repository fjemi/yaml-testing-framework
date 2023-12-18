#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
import types


MODULE = __file__
PARENT_MODULE = os.path.dirname(MODULE)
PARENT_MODULE = os.path.dirname(PARENT_MODULE)
PARENT_MODULE = os.path.join(PARENT_MODULE, 'app.py')


def module_resource(
  module: str | None = None,
) -> types.ModuleType | None:
  if module == 'config_environment_does_exist':
    from main.shared.set_environment.test_resources import config_environment_does_exist
    return config_environment_does_exist
  elif module == 'config_environment_does_not_exist':
    from main.shared.set_environment.test_resources import config_environment_does_not_exist
    return config_environment_does_not_exist


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  project_directory = PARENT_MODULE
  # project_directory = 'main/examples/subtract'
  invoke_pytest(
    # invoke='pytest',
    project_directory=project_directory, )


if __name__ == '__main__':
  example()
