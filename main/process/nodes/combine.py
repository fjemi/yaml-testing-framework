#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any

from main.utils import get_config, independent, objects


CONFIG = get_config.main()

LOCALS = locals()
TEST_FIELDS = list(CONFIG.schema.Test.__dict__.keys())
TEST_FIELDS.append('tests')


def main(
  parent:  dict | None = None,
  child: dict | None = None,
) -> sns:
  child = objects.get(child, '__dict__', child)
  parent = objects.get(parent, '__dict__', parent)
  fields = get_settings_fields(parent=parent, child=child)

  for field in fields:
    if field not in TEST_FIELDS:
      continue
  
    low = objects.get(parent=child, route=field)
    high = objects.get(parent=parent, route=field)
    value = combination_handler(
      low=low,
      high=high,
      field=field, )
    child = objects.update(
      parent=child,
      value=value,
      route=field, )
  
  return sns(**child)


def get_settings_fields(
  parent: dict | None = None,
  child: dict | None = None,
) -> list:
  locals_ = locals()
  store = []

  for key, value in locals_.items():
    keys = list(value.keys())
    for item in keys:
      if item not in store:
        store.append(item)

  return store


def combination_handler(
  low: Any | None = None,
  high: Any | None = None,
  field: str = '',
) -> Any:
  map_ = CONFIG.combination_map.get(field, 'low_or_high')
  handler = f'combine_{map_}'
  handler = LOCALS[handler]
  return handler(low=low, high=high)


def format_as_list(value: Any) -> list:
  if isinstance(value, list):
    return value
  if value is not None:
    return [value]
  return []


def combine_list(
  low: Any | None = None,
  high: Any | None = None,
) -> list:
  low = format_as_list(value=low)
  high = format_as_list(value=high)
  store = []

  for item in [*low, *high]:
    if item not in store:
      store.append(item)

  return store


def combine_dict(
  low: Any | None = None,
  high: Any | None = None,
) -> dict:
  store = {}
  flag = sns(
    high=isinstance(high, dict),
    low=isinstance(low, dict), )
  store.update(low if flag.low else {})
  store.update(high if flag.high else {})
  return store


def combine_low_or_high(
  low: Any | None = None,
  high: Any | None = None,
) -> Any:
  return low or high


def combine_high_or_low(
  low: Any | None = None,
  high: Any | None = None,
) -> Any:
  return high or low


def combine_high(
  low: Any | None = None,
  high: Any | None = None,
) -> Any:
  _ = low
  return high


def combine_low(
  low: Any | None = None,
  high: Any | None = None,
) -> Any:
  _ = high
  return low


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
