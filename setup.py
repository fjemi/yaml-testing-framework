#!.venv/bin/python3
# -*- coding: utf-8 -*-

import dataclasses as dc
import os
from typing import Any, List

from setuptools import setup
import yaml as py_yaml


ROOT_DIRECTORY = os.path.dirname(__file__)

FILES = '''
- name: Pipfile.lock
  field: pipfile_lock
  type: json
- name: setup.yaml
  field: setup_yaml
  type: yaml
- name: README.md
  field: long_description
  type: file
'''
FILES = py_yaml.safe_load(FILES)


@dc.dataclass
class Data:
  directory: str | None = None
  pipfile_lock: dict | None = None
  long_description: str | None = None
  setup_yaml: dict | None = None


def get_content_from_file(location: str | None = None) -> Any:
  location = str(location)

  condition = os.path.isfile(location)
  if condition is False:
    return None

  with open(
    file=location,
    mode='r',
    encoding='utf-8',
  ) as file:
    content = file.read()

  return content


def get_contents(
  directory: str | None = None,
) -> dict:
  store = {'directory': directory}

  if not directory:
    return store

  for file in FILES:
    location = f"{directory}{os.sep}{file.get('name')}"
    content = get_content_from_file(location=location)

    condition = file.get('type', '') in ['json', 'yaml']
    if condition and content:
      content = py_yaml.safe_load(content)

    store[file.get('field')] = content

  return store


def get_setup_requires(pipfile_lock: dict) -> List[str]:
  default = pipfile_lock.get('default')
  exclude_keys = [
    'coverage',
    'iniconfig',
    'packaging',
    'pluggy',
  ]
  packages = []

  for key, value in default.items():
    if key in exclude_keys:
      continue
    version = value.get('version')
    requirement = f'{key}{version}'
    packages.append(requirement)

  return packages


def get_python_requires(pipfile_lock: dict | None = None) -> str:
  packages = pipfile_lock.get('default')
  for name, details in packages.items():
    markers = details.get('markers', None)
    if not markers:
      continue

    numbers = markers.replace('python_version', '').strip()
    numbers = numbers.replace("'", '')
    numbers = numbers.split(' ')
    return ''.join(numbers)


EMPTY_VALUES = [
  None,
  {},
  [],
  '',
]


def merge_pip_lock_and_setup_yaml(
  long_description: str | None = None,
  setup_yaml: dict | None = None,
  pipfile_lock: dict | None = None,
  # trunk-ignore(ruff/ARG001)
  directory: str | None = None,
) -> dict:
  fields = dict(
    setup_requires=get_setup_requires(pipfile_lock=pipfile_lock),
    python_requires=get_python_requires(pipfile_lock=pipfile_lock),
    long_description=long_description,
  )
  setup_yaml = setup_yaml or {}
  setup_yaml.update(fields)
  pipfile_lock = None
  return setup_yaml


def main(directory: str | None = None) -> Data:
  directory = ROOT_DIRECTORY if not directory else directory
  data = get_contents(directory=directory)
  data = merge_pip_lock_and_setup_yaml(**data)
  return data


if __name__ == '__main__':
  data = main()
  setup(**data)
