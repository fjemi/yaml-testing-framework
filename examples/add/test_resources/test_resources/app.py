#!/usr/bin/env python3

import dataclasses as dc


@dc.dataclass
class Test_Dataclass:
  a: int | None = None
  b: int | None = None


TEST_VARIABLE = "test"


def test_function() -> None:
  return
