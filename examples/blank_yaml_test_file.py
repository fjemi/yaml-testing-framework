#!.venv/bin/python3
# -*- coding: utf-8 -*-

from typing import Any


def main(data: None = None) -> Any | None:
  return data


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
