#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc


@dc.dataclass
class Example:
  pass


EXAMPLE = Example()
EXAMPLE.__builtins__ = __builtins__
