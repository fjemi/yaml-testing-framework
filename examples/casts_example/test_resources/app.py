# /examples/casts_example/test_resources/app.py

import dataclasses as dc


@dc.dataclass
class Test_Data:
  a: int | float = 0
  b: int | float = 0
  result: int | float = 0
