#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc


@dc.dataclass
class Test_Data_Class:
  a: int | None = None
  b: int | None = None


TEST_VARIABLE = "test"


def test_function() -> None:
  return
