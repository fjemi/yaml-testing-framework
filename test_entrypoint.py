#!/usr/bin/env python3

import os
import sys

import pytest

import app.main as pytest_yaml


def format_ids(test: pytest_yaml.Test | None) -> str:
  if not test:
    return

  module = test.module
  if not isinstance(module, str):
    module = module.__file__

  project_path = str(pytest.project_path)
  module = module.replace(project_path, '')
  module = module.replace('.py', '')
  module = module.replace(os.sep, '.')[1:]
  return f'{module}.{test.function} - {test.description}'


@pytest.mark.parametrize(
  argnames='test',
  argvalues=pytest.yml_tests,
  ids=lambda test: format_ids(test=test),
)
def test_case(test: pytest_yaml.Test) -> None:
  n = len(test.assertions)
  for i in range(n):
    if test.assertions[i] != test.result[i]:
      print(test.exception)
    assert test.assertions[i] == test.result[i]


if __name__ == '__main__':
  sys.exit(pytest.main(['-s', '-vvv'],))
