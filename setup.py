#!/usr/bin/env python3
# encoding: utf-8

import dataclasses as dc
import os
from typing import List

import yaml
from setuptools import find_packages, setup

ROOT_DIRECTORY = os.path.dirname(__file__)


@dc.dataclass
class Data:
  directory: str = dc.field(default_factory=lambda: ROOT_DIRECTORY)
  pipfile_lock: dict | None = None
  setup_yml: dict | None = None


def get_file_contents(data: Data) -> Data:
  files = {
    "Pipfile.lock": "pipfile_lock",
    "setup.yml": "setup_yml",
  }
  for filename, attribute_name in files.items():
    path = os.path.join(data.directory, filename)

    if not os.path.exists(path):
      continue

    content = None
    with open(
      file=path,
      mode="r",
      encoding="utf-8",
    ) as file:
      content = file.read()
      content = yaml.safe_load(content)
      setattr(
        data,
        attribute_name,
        content,
      )
  return data


def get_install_requires(pipfile_lock: dict) -> List[str]:
  default = pipfile_lock.get("default")
  exclude_keys = [
    "coverage",
    "iniconfig",
    "packaging",
    "pluggy",
  ]
  packages = []

  for key, value in default.items():
    if key in exclude_keys:
      continue
    version = value.get("version")
    requirement = f"{key}{version}"
    packages.append(requirement)

  return packages


def get_python_requires(pipfile_lock: dict) -> str:
  versions = {}

  packages = pipfile_lock.get('default')
  for name, details in packages.items():
    markers = details.get('markers')
    if not markers:
      continue

    numbering = markers.replace("'", '').split(" ")
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
    "install_requires": get_install_requires(pipfile_lock=data.pipfile_lock),
    "python_requires": get_python_requires(pipfile_lock=data.pipfile_lock),
  }
  data.setup_yml.update(fields)
  data.pipfile_lock = None
  return data


def main(directory: str | None) -> Data:
  data = Data()
  if directory:
    data.directory = directory

  data = get_file_contents(data=data)
  data = add_pip_lock_fields_to_setup_yml(data=data)
  data.setup_yml["packages"] = find_packages(**data.setup_yml["packages"])
  return data.setup_yml


if __name__ == '__main__':
  setup_data = main()
  setup(**setup_data)
