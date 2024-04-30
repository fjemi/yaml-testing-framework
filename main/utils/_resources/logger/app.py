#!.venv/bin/python3
# -*- coding: utf-8 -*-

import logging
from typing import Any, Callable

from main.utils import invoke_testing_method
from main.utils.logger import get_logger


MODULE = __file__


def do_nothing(*args, **kwargs) -> None:
  _ = args, kwargs


def logging_method_resource(*args, **kwargs) -> Callable:
  _ = args, kwargs
  return do_nothing


def get_logger_wrapper(logger: Any | None = None) -> logging.Logger:
  return get_logger(location=logger)


def examples() -> None:
  invoke_testing_method.main(
    resource_flag=True,
    resources_folder_name='_resources', )


if __name__ == '__main__':
  examples()
