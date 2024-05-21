#!.venv/bin/python3
# -*- coding: utf-8 -*-


import logging
from typing import Any, Callable

from main.utils import invoke_testing_method
from main.utils import logger as logger_resource


MODULE = __file__


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def logging_method_resource(*args, **kwargs) -> Callable:
  _ = args, kwargs
  return do_nothing


def get_logger_wrapper(logger: Any | None = None) -> logging.Logger:
  return logger_resource.get_logger(location=logger)


def list_sns_to_list_dict(output: Any) -> Any:
  if not isinstance(output, list):
    return output

  return [item.__dict__ for item in output]


def examples() -> None:
  invoke_testing_method.main(
    resource_flag=True,
    module_filename='app',
    resources_folder_name='resources', )


if __name__ == '__main__':
  examples()
