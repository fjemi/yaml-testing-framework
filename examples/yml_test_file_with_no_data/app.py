#!.venv/bin/python3
# -*- coding: utf-8 -*-

MODULE_LOCATION = __file__


# ruff: noqa: ARG001
def main(*args, **kwargs) -> str:
  return 'yaml test file with no data'


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest

  invoke_pytest(
    invoke='pytest',
    project_directory=MODULE_LOCATION,
  )


if __name__ == '__main__':
  example()
