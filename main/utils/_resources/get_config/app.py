#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns


MODULE = __file__

LOCALS = locals()


def format_environment_content_cast_arguments(
  content: dict | None = None,
) -> sns | None:
  if isinstance(content, dict):
    return sns(**content)


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()