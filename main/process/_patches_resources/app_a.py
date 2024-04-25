#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc


@dc.dataclass
class Data_Class_Resource:
  field: str = 'value'


EXAMPLE_OBJECT = Data_Class_Resource()


@dc.dataclass
class Object_Parent:
  object_name_a: str = 'object_name_a'
  object_name_b: str = 'object_name_b'


@dc.dataclass
class Test_Data_Class:
  pass


EXAMPLE_DICTIONARY = {'key': 'value'}
