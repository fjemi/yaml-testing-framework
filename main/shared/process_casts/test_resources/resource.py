#!.venv/bin/python3
# -*- coding: utf-8 -*-


def pass_through(
  # trunk-ignore(ruff/ARG001)
  *args,
  # trunk-ignore(ruff/ARG001)
  **kwargs,
) -> str:
  return 'pass_through'
