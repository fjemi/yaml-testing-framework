#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from types import SimpleNamespace as sns
from typing import Any

from main.utils import objects


LOCALS = locals()
ROOT = os.path.dirname(__file__)


ENTRYPOINT_FILENAME = 'test_entrypoint.py'
ENTRYPOINT = ''


def get_resource(resource: str | None = None) -> Any:
  return LOCALS.get(resource, None)


def add(data: dict = {}) -> int:
  return sum(list(data.values()))


def multiply(a: int, b: int) -> int:
  return a * b


def list_dict_to_list_sns(data: list = []) -> list:
  if not isinstance(data, list):
    return data

  return [sns(**item) for item in data]


def list_sns_to_list_dict(output: list = []) -> list:

  def caster(item: sns) -> dict:
    if isinstance(item.output, Exception):
      item.output = type(item.output).__name__
    return item.__dict__

  return [caster(item=item) for item in output]


async def subtract(data: dict = {}) -> int:
  return data['b'] - data['a']


def remove_temp_directory(output: Any | None = None) -> Any:
  global ENTRYPOINT
  path = str(ENTRYPOINT)
  handler = {
    True: lambda path: path,
    os.path.isdir(path): shutil.rmtree,
    os.path.isfile(path): os.remove, }
  result = handler[True](path)
  ENTRYPOINT = f'{result}'
  return output


def temp_directory_with_entrypoint_wrapper(
  entrypoint: str = '',
  flags: sns | dict = {},
) -> dict:
  _ = entrypoint
  entrypoint = temp_directory_with_entrypoint(entrypoint='', root='')
  entrypoint = objects.get(parent=entrypoint, route='entrypoint')
  return dict(entrypoint=entrypoint, flags=flags)


def temp_directory_with_entrypoint(
  entrypoint: str = '',
  root: str = '',
) -> dict:
  _ = entrypoint
  directory = os.path.join(root or ROOT, '.artifacts')
  os.makedirs(name=directory, exist_ok=True)
  directory = tempfile.mkdtemp(dir=directory)
  entrypoint = os.path.join(
    directory,
    ENTRYPOINT_FILENAME, )
  with open(entrypoint, 'w') as file:
    file.write('entrypoint')
  return dict(entrypoint=entrypoint, root=directory)


def temp_directory_without_entrypoint(
  root: str = '',
  entrypoint: str = '',
) -> dict:
  _ = root, entrypoint
  directory = os.path.join(ROOT, '.artifacts')
  directory = tempfile.mkdtemp(dir=directory)
  os.makedirs(name=directory, exist_ok=True)
  entrypoint = ENTRYPOINT_FILENAME
  entrypoint = os.path.join(directory, entrypoint)
  return dict(entrypoint=entrypoint, root=directory)


def examples() -> None:
  from main.utils import invoke

  invoke.main(location='.main/app')


if __name__ == '__main__':
  examples()
