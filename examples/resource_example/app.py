# /examples/resources_example/app.py

import dataclasses as dc


@dc.dataclass
class Data_Class:
  pass


def add(data: Data_Class) -> Data_Class:
  data.result = data.a + data.b
  return data
