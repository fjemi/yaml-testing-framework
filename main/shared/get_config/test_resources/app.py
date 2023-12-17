#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any, Callable

import yaml


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


def function(parameter_1, parameter_2):
  return


def function_resource(*args, **kwargs) -> Callable:
  return function