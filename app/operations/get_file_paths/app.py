#!/usr/bin/env python3

import dataclasses as dc
import os
import pathlib
from typing import List

from app.shared.format_main_arguments import app as format_main_arguments
from app.shared.get_environment import app as get_environment

PROJECT_DIR = os.path.abspath(os.curdir)
MODULE_PATH = __file__
ENV = get_environment.main(module_path=MODULE_PATH)


@dc.dataclass
class Body:
  project_path: str | None = ENV.WORKDIR
  exclude_match: str | List[str] | None = None
  yml_suffix: str = "_test"
  yml_prefix: str | None = None
  test_resources_directory: str = "test_resources"


@dc.dataclass
class File_Paths:
  directory: str | None = None
  py_path: str | None = None
  yml_path: str | None = None
  test_resources: List[str] | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  call_method: str = "module"
  paths: List[File_Paths] | List[str] | None = None


async def set_project_path(data: Data) -> Data:
  if data.body.project_path:
    return data

  data.body.project_path = PROJECT_DIR
  return data


async def get_paths_for_python_files(data: Data) -> Data:
  if os.path.isfile(data.body.project_path):
    data.paths = [data.body.project_path]
    return data

  directory = pathlib.Path(data.body.project_path)
  paths = list(directory.rglob("*.py"))
  data.paths = paths
  return data


async def filter_python_file_paths(data: Data) -> Data:
  if not data.body.exclude_match:
    data.body.exclude_match = []

  if not isinstance(data.body.exclude_match, list):
    data.body.exclude_match = [data.body.exclude_match]
  data.body.exclude_match.append(data.body.test_resources_directory)

  paths = []
  for path in data.paths:
    exclusion_flag = False
    for exclusion in data.body.exclude_match:
      if str(path).find(exclusion) != -1:
        exclusion_flag = True
        break
    if exclusion_flag:
      continue
    path_str = str(path)
    paths.append(path_str)

  data.paths = paths
  return data


async def get_path_object(data: Data) -> Data:
  for i, py_path in enumerate(data.paths):
    directory = os.path.dirname(py_path)
    data.paths[i] = File_Paths(
      directory=directory,
      py_path=py_path,
    )
  return data


async def get_paths_for_associated_yml_files(data: Data) -> Data:
  suffix = f"{data.body.yml_suffix}.yml"
  paths = []
  for path in data.paths:
    yml_path = path.py_path.replace(".py", suffix)

    if not os.path.exists(yml_path):
      yml_path = None

    path.yml_path = yml_path
    paths.append(path)

  data.paths = paths
  return data


async def get_paths_for_test_resources(data: Data) -> Data:
  for path in data.paths:
    # directory = os.path.join(path.directory, data.test_resources_directory)
    directory = pathlib.Path(
      path.directory,
      data.body.test_resources_directory,
    )

    if not directory.exists:
      continue

    resource_paths = list(directory.rglob("*.*"))
    store = []
    for resource_path in resource_paths:
      resource_path_str = str(resource_path)
      store.append(resource_path_str)
    path.test_resources = store

  return data


# ruff: noqa: ARG001
async def main(
  project_path: str | None = None,
  exclude_match: str | List[str] | None = None,
  yml_suffix: str | List[str] | None = None,
  yml_prefix: str | None = None,
  test_resources_directory: str | None = None,
) -> Data:
  data = await format_main_arguments.main(
    _locals=locals(),
    main_data_class=Data,
    data_classes={"body": Body},
  )
  data = await set_project_path(data=data)
  data = await get_paths_for_python_files(data=data)
  data = await filter_python_file_paths(data=data)
  data = await get_path_object(data=data)
  data = await get_paths_for_associated_yml_files(data=data)
  data = await get_paths_for_test_resources(data=data)
  return data.paths


async def example() -> None:
  result = await main()
  print(result)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
