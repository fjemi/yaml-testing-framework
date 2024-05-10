#!.venv/bin/python3
# -*- coding: utf-8 -*-


import os
from types import SimpleNamespace as sns
from typing import Any, List

import setuptools
import yaml as pyyaml


ROOT_DIR = os.path.abspath(os.curdir)
ROOT_DIR = os.path.normpath(ROOT_DIR)

CONFIG = '''
  schema:
  - description:
    fields:
    - name: directory
    - name: pipfile_lock
    - name: long_description
    - name: setup_yaml
  files:
  - name: Pipfile.lock
    field: pipfile_lock
    type: json
  - name: setup.yaml
    field: setup_yaml
    type: yaml
  - name: README.md
    field: long_description
    type: file
  content_file_types:
  - json
  - yaml
  - yml
  exclude_packages:
  - coverage
  - iniconfig
  - packaging
  - pluggy
'''
CONFIG = pyyaml.safe_load(CONFIG)
CONFIG = sns(**CONFIG)


def get_content_from_file(location: str | None = None) -> Any:
  location = str(location)
  content = None

  if os.path.isfile(location):
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

  if directory:
    for file in CONFIG.files:
      filename = file.get('name', '')
      location = os.path.join(directory, filename)
      location = os.path.normpath(location)

      content = get_content_from_file(location=location)

      condition = file.get('type', '') in CONFIG.content_file_types
      if condition and content:
        content = pyyaml.safe_load(content)

      store[file.get('field')] = content

  return store


def get_setup_requires(
  pipfile_lock: dict | None = None,
) -> List[str]:
  pipfile_lock = pipfile_lock or {}
  default = pipfile_lock.get('default', {})

  packages = []
  for key, value in default.items():
    if key not in CONFIG.exclude_packages:
      version = value.get('version')
      requirement = f'{key}{version}'
      packages.append(requirement)

  return packages


def get_python_requires(pipfile_lock: dict | None = None) -> str:
  packages = pipfile_lock.get('default')
  for name, details in packages.items():
    markers = details.get('markers', None)
    if markers:
      numbers = markers.replace('python_version', '').strip()
      numbers = numbers.replace("'", '')
      numbers = numbers.split(' ')
      return ''.join(numbers)


def merge_pip_lock_and_setup_yaml(
  long_description: str | None = None,
  setup_yaml: dict | None = None,
  pipfile_lock: dict | None = None,
  directory: str | None = None,
) -> dict:
  _ = directory
  fields = dict(
    setup_requires=get_setup_requires(pipfile_lock=pipfile_lock),
    python_requires=get_python_requires(pipfile_lock=pipfile_lock),
    long_description=long_description, )
  setup_yaml = setup_yaml or {}
  setup_yaml.update(fields)
  pipfile_lock = None
  return setup_yaml


def main(directory: str | None = None) -> sns:
  directory = directory or ROOT_DIR
  data = get_contents(directory=directory)
  data = merge_pip_lock_and_setup_yaml(**data)
  return data


if __name__ == '__main__':
  data = main()
  setuptools.setup(**data)
