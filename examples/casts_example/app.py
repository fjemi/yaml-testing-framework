# /examples/casts_example/app.py

import dataclasses as dc


@dc.dataclass
class Data:
  a: int | float
  b: int | float
  result: int | float | None = None


def add(data: Data) -> Data:
  data.result = data.a + data.b
  return data
