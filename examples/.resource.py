#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns


def sum_patch(data: sns) -> sns:
  data.result = 0
  data.result = sum([i + 1 for i in range(data.a)])
  return data


def inverse(result: int) -> float:
  return 1 / result


def examples() -> None:
  from main.utils import invoke

  invoke.main(resource_flag=True)


if __name__ == '__main__':
  examples()
