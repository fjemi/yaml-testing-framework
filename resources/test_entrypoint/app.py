#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns

from main.utils import invoke_testing_method, schema


MODULE = __file__


def get_ids_resource(val: dict | None = None) -> sns:
  val = val or {}
  return sns(**val)


def test_resource(test: dict | None = None):
  test = test or {}
  test = schema.get_model(data=test, name='Test')
  return test


def checks_resource(checks: list | None = None) -> list:
  if not isinstance(checks, list):
    return checks

  return [sns(**check) for check in checks]


def examples() -> None:
  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
