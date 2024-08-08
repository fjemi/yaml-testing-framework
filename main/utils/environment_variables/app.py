#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
import string
from types import SimpleNamespace as sns
from typing import Any


TRUTH = ['1', 'true', 't']


def evaluate(
  value: Any | None = None,
  values: dict | sns | None = None,
  return_: str = '',
) -> Any:
  handler = {
    True: lambda *_, **__: {},
    len(value or '') > 0: handle_value,
    len(values or '') > 0: handle_values, }
  handler = handler[True]
  return handler(
    values=values,
    value=value,
    return_=return_, )


def handle_values(
  values: sns | dict | None = None,
  value: Any | None = None,
  return_: str = '',
) -> dict | sns:
  _ = value
  values = values or {}
  values = getattr(values, '__dict__', values)
  for key, value_ in values.items():
    values[key] = handle_value(value=value_)
  return sns(**values) if return_ == 'sns' else values


def handle_value(
  values: sns | dict | None = None,
  value: Any | None = None,
  return_: str = '',
) -> Any:
  _ = values, return_

  try:
    temp = str(value)
    value = string.Template(temp).substitute(os.environ)
  except Exception as error:
    _ = error

  temp = str(value)
  value = None if temp.find('$') == 0 else value

  temp = str(value).lower()
  return True if temp in TRUTH else value

