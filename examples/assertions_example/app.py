# /examples/assertions_example/app.py

def subtract(
  a: int | float,
  b: int | float,
) -> int | float:
  return a - b


def add(
  a: int | float,
  b: int | float,
) -> dict:
  result = a + b
  return {'result': result}
