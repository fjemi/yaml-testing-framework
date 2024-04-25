#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns

import pytest


def get_test_id(val) -> str:
  if hasattr(val, 'id'):
    return val.id


@pytest.mark.parametrize(
  argnames='test',
  ids=get_test_id,
  argvalues=pytest.yaml_tests, )
def test_(test: sns) -> None:
  # trunk-ignore(bandit/B101)
  assert test.expected == test.output


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
