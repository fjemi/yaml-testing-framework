#!.venv/bin/python3
# -*- coding: utf-8 -*-


MODULE = __file__


def add(
  a: int = 0,
  b: int = 0,
) -> int:
  return a + b


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(
    resources_folder_name='resources_folder_name',
    project_directory=MODULE, )


if __name__ == '__main__':
  example()
