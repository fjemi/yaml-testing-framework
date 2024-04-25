#!.venv/bin/python3
# -*- coding: utf-8 -*-

from main.__init__ import sys


def get_sys_path(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> dict:
  return sys.path
