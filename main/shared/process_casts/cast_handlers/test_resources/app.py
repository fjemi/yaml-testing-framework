#!.venv/bin/python3
# -*- coding: utf-8 -*-


import dataclasses as dc
from typing import Any


@dc.dataclass
class Test_Data:
  a: int = 0
  b: int = 0


def get_resources(
  caster: Any | None = None,
  object: Any | None = None,
) -> Any:
  if 'str' in [caster, object]:
    return str
  if 'int' in [caster, object]:
    return int
  if 'dataclass' in [caster, object]:
    return Test_Data

