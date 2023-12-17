#!.venv/bin/python3
# -*- coding: utf-8 -*-


from typing import Any


MODULE = __file__
LOCALS = locals()
KINDS = ['nonetype', 'dict', ]


def get_value_from_object(
  object: Any | None = None,
  field: str | None = None,
  default_value: Any | None = None,
) -> Any:
  return getattr(
    object,
    field,
    default_value, )


def get_value_from_dict(
  object: Any | None = None,
  field: str | None = None,
  default_value: Any | None = None,
) -> Any:
  return object.get(
    field,
    default_value, )


def get_value_from_nonetype(
  # trunk-ignore(ruff/ARG001)
  object: Any | None = None,
  # trunk-ignore(ruff/ARG001)
  field: str | None = None,
  default_value: Any | None = None,
) -> None:
  return default_value


def main(
  object: Any | None = None,
  field: str | None = None,
  default_value: Any | None = None,
) -> Any:
  locals_ = locals()
  kind = type(object).__name__.lower()
  kind = kind if kind in KINDS else 'object'
  handler = f'get_value_from_{kind}'
  handler = LOCALS[handler]
  return handler(
    object=object,
    field=field,
    default_value=default_value, )


def example() -> None:
  from invoke_pytest.app import main as invoke_pytest


  invoke_pytest(project_directory=MODULE)


if __name__ == '__main__':
  example()
