#!.venv/bin/python3
# -*- coding: utf-8 -*-


def hello_world(name: str | None = None) -> str:
  name = name or 'World'
  return f'Hello {name}'
