#!/usr/bin/env python3

import dataclasses as dc
import os
from typing import List

import yaml
from setuptools import setup

ROOT_DIRECTORY = os.path.dirname(__file__)


@dc.dataclass
class Data:
  directory: str = dc.field(default_factory=lambda: ROOT_DIRECTORY)
  pipfile_lock: dict | None = None
  long_description: str | None = None
  setup_yml: dict | None = None


def get_file_contents(data: Data) -> Data:
  files = '''
  - name: Pipfile.lock
    dataclass_field: pipfile_lock
    type: json
  - name: setup.yml
    dataclass_field: setup_yml
    type: yml
  - name: README.md
    dataclass_field: long_description
    type: file
  '''
  files = yaml.safe_load(files)

  for file in files:
    path = os.path.join(data.directory, file.get('name'))

    if not os.path.exists(path):
      continue

    content = None
    with open(
      file=path,
      mode='r',
      encoding='utf-8',
    ) as file_content:
      content = file_content.read()

    if file.get('type') in ['json', 'yml']:
      content = yaml.safe_load(content)

    setattr(
      data,
      file.get('dataclass_field'),
      content,
    )

  return data


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


def get_python_requires(pipfile_lock: dict) -> str:
  versions = {}

  packages = pipfile_lock.get('default')
  for name, details in packages.items():
    markers = details.get('markers')
    if not markers:
      continue

    numbering = markers.replace("'", '').split(' ')
    numbering = numbering[-1].split('.')[0:2]
    major, minor = [int(x) for x in numbering]

    if major not in versions:
      versions[major] = []
    versions[major].append(minor)
    versions[major].sort()

  min_major = min(versions.keys())
  min_minor = min(versions[min_major])
  return f'>={min_major}.{min_minor}'


def add_pip_lock_fields_to_setup_yml(data: Data) -> Data:
  fields = {
    'setup_requires': get_setup_requires(pipfile_lock=data.pipfile_lock),
    'python_requires': get_python_requires(pipfile_lock=data.pipfile_lock),
    'long_description': data.long_description,
  }
  data.setup_yml.update(fields)
  data.pipfile_lock = None
  return data


def main(directory: str | None = None) -> Data:
  data = Data()
  if directory:
    data.directory = directory

  data = get_file_contents(data=data)
  data = add_pip_lock_fields_to_setup_yml(data=data)
  return data.setup_yml


if __name__ == '__main__':
  setup_data = main()
  setup(**setup_data)
