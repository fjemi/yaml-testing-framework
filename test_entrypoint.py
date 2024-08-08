#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns

import pytest


def get_test_id(val) -> str:
  if hasattr(val, 'id'):
    return val.id


def get_yaml_tests(pytest: ModuleType) -> list:
  return getattr(pytest, 'yaml_tests', None) or []


@pytest.mark.parametrize(
  argnames='test',
  ids=get_test_id,
  argvalues=get_yaml_tests(pytest=pytest), )
def test_(test: sns) -> None:
  # trunk-ignore(bandit/B101)
  assert test.expected == test.output


def examples() -> None:
  from main.utils import invoke

  invoke.main()


if __name__ == '__main__':
  examples()
