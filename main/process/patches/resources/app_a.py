#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc


@dc.dataclass
class DataClassResource:
  field: str = 'value'


EXAMPLE_OBJECT = DataClassResource()


@dc.dataclass
class TestDataClass:
  pass


EXAMPLE_DICTIONARY = {'key': 'value'}
