#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc


@dc.dataclass
class DataClassResource:
  field: str = 'value'


EXAMPLE_OBJECT = DataClassResource()


@dc.dataclass
class Object_Parent:
  object_name_a: str = 'object_name_a'
  object_name_b: str = 'object_name_b'


@dc.dataclass
class TestDataClass:
  pass


EXAMPLE_DICTIONARY = {'key': 'value'}
