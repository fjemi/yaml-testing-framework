#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any

from main.utils import get_config


CONFIG = get_config.main()

LOCALS = locals()


def main(
  high: Any | None = None,
  low: Any | None = None,
  field: str | None = None,
) -> sns:
  levels = sns(low=low, high=high)
  kind = CONFIG.combine_fields_as.get(field, 'low_or_high')
  handler = f'combine_levels_as_{kind}'
  handler = LOCALS.get(handler, None)
  return handler(levels=levels)


def combine_levels_as_list(levels: sns | None = None) -> sns:
  store = []

  for level in CONFIG.levels:
    value = getattr(levels, level, None)
    if value in CONFIG.empty_values:
      continue
    if not isinstance(value, list):
      value = [value]
    store.extend(value)

  return sns(output=store)


def combine_levels_as_dict(levels: sns | None = None) -> sns:
  output = {}

  for level in CONFIG.levels:
    value = getattr(levels, level, {})
    if isinstance(value, dict):
      output.update(value)

  return sns(output=output)


def combine_levels_as_low_or_high(levels: sns | None = None) -> sns:
  output = levels.high
  if levels.low not in CONFIG.empty_values:
    output = levels.low
  return sns(output=output)


def combine_levels_as_high_or_low(levels: sns | None = None) -> sns:
  output = levels.low
  if levels.high not in CONFIG.empty_values:
    output = levels.high
  return sns(output=output)


def combine_levels_as_high(levels: sns | None = None) -> sns:
  return sns(output=levels.high)


def combine_levels_as_low(levels: sns | None = None) -> sns:
  return sns(output=levels.low)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
