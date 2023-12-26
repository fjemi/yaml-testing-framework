#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any, Callable

import yaml


MODULE = __file__

LOCALS = locals()


@dc.dataclass
class Config:
  environment: dict | None = None
  schema: list | None = None


def get_config(data: Any) -> Any:
  data.config = Config()
  data.config.environment = {'ENV': 'ENV'}

  schema = '''
  - cls_name: Data_A
    description: null
    slots: False
    fields:
    - name: name_a
      type: None
    - name: name_b
      type: None
  - cls_name: Data_B
    description: null
    slots: False
    fields:
    - name: name_a
      type: None
    - name: name_b
      type: None
  '''
  schema = yaml.safe_load(schema)
  data.config.schema = schema
  return data


def function(
  # trunk-ignore(ruff/ARG001)
  parameter_1: None = None,
  # trunk-ignore(ruff/ARG001)
  parameter_2: None = None,
) -> None:
  return


def function_resource(
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> Callable:
  function_ = args[0]
  return LOCALS[function_]


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest
  from utils import app as utils


  parent_module = utils.get_parent_module(
    resources_folder_name='test_resources',
    module=MODULE, )
  invoke_pytest(project_directory=parent_module)


if __name__ == '__main__':
  example()
