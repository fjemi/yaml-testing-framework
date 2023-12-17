#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc


@dc.dataclass
class Data:
  field: str = 'value'


def object_resource(*args, **kwargs) -> Data:
  return Data()