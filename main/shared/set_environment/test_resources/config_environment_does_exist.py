#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc


@dc.dataclass
class Data_Class:
  pass


CONFIG = Data_Class()
CONFIG.environment = Data_Class()
CONFIG.environment.VARIABLE_C = 'VALUE_C'
