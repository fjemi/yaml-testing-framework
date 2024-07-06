#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True, module_filename='app')


if __name__ == '__main__':
  examples()
