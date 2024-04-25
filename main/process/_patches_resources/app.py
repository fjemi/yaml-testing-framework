#!.venv/bin/python3
# -*- coding: utf-8 -*-

# trunk-ignore(ruff/I001)
import dataclasses as dc
# trunk-ignore(ruff/F401)
import os
# trunk-ignore(ruff/F401)
import os as patch_os
# trunk-ignore(ruff/F401)
import sys
from types import ModuleType, SimpleNamespace as sns
from typing import Any, Callable, List

from utils import get_module, invoke_testing_method, get_config, schema
import yaml


MODULE = __file__
PARENT_MODULE = invoke_testing_method.get_parent_module_location(
  resource_module=MODULE,
  resources_folder_name='_resources', )

CONFIG = get_config.main(module=PARENT_MODULE)
LOCALS = locals()


@dc.dataclass
class Data_Class:
  a: int = 0
  b: int = 0
  result: int = 0


@dc.dataclass
class Test_Data_Class:
  pass


@dc.dataclass
class Store:
  pass


GET_PARENT_RESOURCES = Data_Class()


def get_module_wrapper(module: str | None = None) -> ModuleType:
  return get_module.main(location=module, pool=False)


def get_input(data: str | None = None) -> str:
  if data is None:
    data = ''
  return input(data)


def use_get_input(data: str | None = None) -> str:
  if data is None:
    data = ''
  return get_input(data=data)


def foo(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> str:
  return 'foo'


def bar(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> str:
  return bar


def use_foo(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> str:
  return foo()


def add(a: int, b: int) -> int:
  return a + b


def use_add(
  # trunk-ignore(ruff/ARG001)
  data: None = None,
) -> int:
  a = 0
  b = 0
  return add(a, b)


def subtract(a: int, b: int) -> int:
  return b - a


def absolute_value(data: Data_Class) -> Data_Class:
  data.result = data.a
  if data.result < 0:
    data.result = data.result * -1
  return data


dictionary_module = {
  'add': add,
  'subtract': subtract,
  'foo': foo,
  'test2': {
    'test1': 'test'
  },
}

variable_1 = 1
variable_2 = 'a'


def setup_get_locals(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> dict:
  return {'add': add}


def do_nothing():
  return


def return_example(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> Test_Data_Class:
  data = Test_Data_Class()
  data.method = 'return'
  data.value = 'return_patch'
  return data


def side_effect_list_example(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> Test_Data_Class:
  data = Test_Data_Class()
  data.method = 'side_effect_list'
  data.value = [0, 1, 2, 3]
  data.timestamp = 0
  return data


def side_effect_dict_example(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> Test_Data_Class:
  data = Test_Data_Class()
  data.method = 'side_effect_dict'
  data.value = {0: 0, 1: 1, 2: 2, 3: 3}
  data.timestamp = 0
  return data


def setup_001(object_parent: str) -> dict:
  from process_patches._resources import app_a

  if object_parent == 'resources.app':
    object_parent = app_a
  return object_parent


def setup_get_parent_from_object(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> ModuleType:
  from process_patches._resources import app_a

  return app_a


def setup_0(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> ModuleType:
  from process_patches._resources import app_a

  return app_a


def setup_1(
  # trunk-ignore(ruff/ARG001)
  module: None = None,
) -> dict:
  text = '''
    add: add
    subtract: subtract
    level_0:
      level_1: ground
  '''
  text = yaml.safe_load(text)
  return yaml.dump(text)


def parent_example(
  # trunk-ignore(ruff/ARG001)
  *args,
  **kwargs,
) -> Store:
  parent = kwargs.get('parent', None)
  if not parent:
    store = Store()
    return store
  if parent == 'parent_0':
    store = Store()
    store.builtins = 'builtins'
    return store
  if parent == 'parent_1':
    store = Store()
    store.name_a = 'name_a'
    store.name_b = 'name_b'
    return store
  if parent == 'parent_2':
    store = {'key_a': 'value_a', 'key_b': 0}
    return store


def builtins_example(
  # trunk-ignore(ruff/ARG001)
  builtins: str | None = None,
) -> Store:
  store = Store()
  store.__class__ = 'module'
  return store


def get_builtins(
  # trunk-ignore(ruff/ARG001)
  *args,
  **kwargs,
) -> None | dict | Store:
  if kwargs.get('builtins') == 'dict':
    return {}
  if kwargs.get('builtins') == 'module':
    return Store()


def setup_module(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> ModuleType:
  from process_patches._resources import app_a

  return app_a


def setup_get_parent_from_builtins(
  # trunk-ignore(ruff/ARG001)
  *args,
  **kwargs,
) -> None | dict | Store:
  if kwargs.get('builtins') == 'dict':
    return {}
  if kwargs.get('builtins') == 'module':
    return Store()


def patch_object_in_dict_resource(
  # trunk-ignore(ruff/ARG001)
  patch: None = None,
) -> ModuleType:
  from process_patches._resources import app_a

  return app_a


def pass_through(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> str:
  return 'pass_through'


def setup_patch_object_in_object(
  data: Any,
) -> Store:
  from process_patches._resources import app_a

  _ = data
  data = Store()
  data.parents = Store()
  data.parents.values = [app_a, app_a.EXAMPLE_OBJECT, None]
  data.parents.types = ['object', 'object', 'object']
  data.parents.names = ['root', 'EXAMPLE_OBJECT', 'builtins']
  data.patch = 'patch'
  return data


def main_resources(
  # trunk-ignore(ruff/ARG001)
  *args, **kwargs,
) -> Any:
  from process_patches._resources import app_a

  return app_a


def patch_object_in_object_resource(arguments: dict | None = None) -> dict:
  arguments = arguments or {}
  store = {}

  for key, value in arguments.items():
    function_ = f'{key}_resource'
    function_ = LOCALS.get(function_, None)
    store[key] = function_(value)

  return store


def get_parent_cast_output(output: list | None) -> list:
  if not isinstance(output, list):
    return output

  def inner(value: Any) -> str:
    if isinstance(value, ModuleType):
      value = value.__file__
    if hasattr(value, '__dict__'):
      value = value.__dict__
    return value

  return [inner(value=value) for value in output]


def patch_resource(patch: str | None = None) -> None | str:
  if patch == 'value':
    return 'patched_value'


def parents_resource(parents: dict | str | None = None) -> Any:
  if isinstance(parents, dict):
    return schema.get_model(data=parents, name='process_patches.Data')
  from process_patches._resources import app_a

  data = sns(
    values=[
      app_a,
      app_a.EXAMPLE_OBJECT,
      'value',  ],
    types=[
      'object',
      'object',
      'object', ],
    names=[
      '',
      'EXAMPLE_OBJECT',
      'field', ],
  )
  if parents == 'parents_length_three':
    return schema.get_model(data=data, name='process_patches.Data')

  if parents == 'parents_length_one':
    from process_patches._resources import app_a
    return data(
      values=[app_a],
      types=['object'],
      names=[''],
    )


def get_patch_for_callable_cast_output(
  patch: Callable | None = None,
) -> None:
  patch = patch or do_nothing
  return patch()


def get_patch_for_side_effect_list_cast_output(
  patch: Callable | None = None,
) -> List[Any]:
  patch = patch or do_nothing()
  store = []

  no_values_repeated = True
  while no_values_repeated:
    value = patch()
    store.append(value)
    count = store.count(value)
    if count > 1:
      no_values_repeated = False

  return store


# def value_resource(value: str | None = None) -> Any:
#   if value == 'callable':
#     return callable_resource


def get_patch_for_side_effect_dict_cast_output(
  patch: Callable | None = None,
) -> dict:
  patch = patch or do_nothing()
  store = {}
  keys = ['key_0', 'key_1', 'key_2',]

  for key in keys:
    value = patch(key)
    store[key] = value

  return store


def examples() -> None:
  invoke_testing_method.main(
    resources_folder_name='_patches_resources',
    module_filename='patches',
    resource_flag=True)


if __name__ == '__main__':
  examples()
