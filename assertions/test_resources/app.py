#!.venv/bin/python3
# -*- coding: utf-8 -*-

MODULE = __file__


def assert_catch_resource(output: str | None = None) -> Exception | dict:
  if output == 'exception':
    return RuntimeError()
  elif output == 'dict':
    return {'name': 'RuntimeError'}


def example() -> None:
  from main.shared.invoke_pytest import app as invoke_pytest
  from main.shared.utils import app as utils

  parent_module = utils.get_parent_module(
    resources_folder_name='test_resources',
    module=MODULE,
  )
  invoke_pytest.main(project_directory=parent_module)


if __name__ == '__main__':
  example()
