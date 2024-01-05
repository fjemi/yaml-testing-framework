#!.venv/bin/python3
# -*- coding: utf-8 -*-

# trunk-ignore(ruff/F401)
import assertions


MODULE = __file__


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest
  from utils import app as utils

  parent_module = utils.get_parent_module(
    module=MODULE,
    resources_folder_name='resources_folder_name',
  )
  invoke_pytest(
    project_directory=parent_module,
    resources_folder_name='resources_folder_name',
  )


if __name__ == '__main__':
  example()
