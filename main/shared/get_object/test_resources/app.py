#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any


@dc.dataclass
class Store:
  pass


def format_parents_resource(data: Any) -> Any:
  parent = Store()
  parent.field = 'value'
  data.update({'parent': parent})
  return data


def get_object_from_object_resource(data: dict) -> Any:
  data.update({'parent': __builtins__})
  return data
