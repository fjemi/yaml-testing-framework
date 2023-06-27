#!/usr/bin/env python3

import ast
import dataclasses as dc
from typing import Any, Callable, Dict, List, Tuple

from app.shared.format_main_arguments import app as format_main_arguments

MODULE_PATH = __file__

FUNCTION_DEFINITION_ATTRIBUTES_MAP = {
  "name": "name",
  "args": "args",
  "body": "body",
  "decorator_list": "decorators",
  "returns": "return_type",
  "type_comment": "type_comment",
}


@dc.dataclass
class Body:
  module_path: str | None = None
  output_attributes: str | List[str] | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  function_definitions: List[Tuple[str, Callable] |
    List[str]] = dc.field(default_factory=lambda: [])
  result: List[Tuple[str, Callable] | List[str]] | None = None
  call_method: bool = "module"


async def get_abstract_syntax_tree(module_path: str) -> List[Any]:
  """Returns the abstract syntax (ast) tree for a
    module given the module's path"""
  with open(
    file=module_path,
    mode="r",
    encoding="utf-8",
  ) as file:
    source = file.read()
    return ast.parse(source).body


# ruff: noqa: ARG001
async def get_function_definitions(
  abstract_syntax_tree: str,
  module_path: str,
) -> List[ast.FunctionDef]:
  """Returns a list a the user defined functions from a modules ast"""

  store = []
  for member in abstract_syntax_tree:
    if isinstance(member, ast.FunctionDef):
      store.append(member)
  return store


async def get_function_definition_returns(
  function_definition: ast.FunctionDef,) -> str:
  """Returns the return type (str, list, dict, ect)
    from a function definition"""
  return function_definition.returns.id


async def get_function_definition_name(
  function_definition: ast.FunctionDef,) -> str:
  """Returns the name from a function definition"""
  return function_definition.name


async def get_function_definition_type_comment(
  function_definition: ast.FunctionDef,) -> str:
  """Returns comments from a function definition"""
  return function_definition.type_comment


async def get_function_definition_decorator_list(
  function_definition: ast.FunctionDef,) -> str:
  """Format and return a list of decorators from a function definition"""
  n = len(function_definition.decorator_list)
  for i in range(n):
    decorator_name = function_definition.decorator_list[i].value.id
    decorator_attribute = function_definition.decorator_list[i].attr
    function_definition.decorator_list[i] = {
      "decorator_name": decorator_name,
      "decorator_attribute": decorator_attribute,
    }
  return function_definition.decorator_list


async def get_function_definition_args(
  function_definition: ast.FunctionDef,) -> List[Dict]:
  """Format and return argument data (name, type, default value)
    from a function definition."""
  function_definition_args = function_definition.args
  args = function_definition_args.args
  defaults = function_definition_args.defaults

  store = []
  # Set argument data
  for arg in args:
    # Get the argument type hint
    argument_type = None
    if hasattr(arg.annotation, "id"):
      argument_type = getattr(arg.annotation, "id")

    # Store argument data as a dictionary
    argument_data = {
      "argument": arg.arg,
      "type": argument_type,
      "default_value": None,
    }
    store.append(argument_data)

  # Set any arguments with default values
  n = len(defaults)
  for i in range(n):
    store[i]["default_value"] = defaults[i].value

  return store


async def get_function_definition_body(
  function_definition: ast.FunctionDef,) -> str:
  """Return the body form a function definition"""
  return function_definition.body


async def get_function_definition_attribute(
  attributes: str,
  function_definitions: List[ast.FunctionDef],
  _locals: Dict = locals(),
) -> Dict[str, List[Any]]:
  """Returns a list"""
  store = {}
  for attribute in attributes:
    values = []
    # attribute = FUNCTION_DEFINITION_ATTRIBUTES_MAP[attribute]
    # Setup switcher
    function_name = f"get_function_definition_{attribute}"
    function = _locals[function_name]
    # Get function definition attributes
    for function_definition in function_definitions:
      value = await function(function_definition=function_definition)
      values.append(value)
    store[attribute] = values
  return store


FORMAT_OUTPUT_SWITCHER = {
  # ruff: noqa: ARG005
  "NoneType": lambda output_attributes: [],
  "list": lambda output_attributes: output_attributes,
  "str": lambda output_attributes: [output_attributes],
}


async def parse_function_definitions(data: Data) -> Data:
  data_type = type(data.body.output_attributes).__name__
  switcher = FORMAT_OUTPUT_SWITCHER[data_type]
  data.body.output_attributes = switcher(
    output_attributes=data.body.output_attributes)

  if data.body.output_attributes == []:
    data.body.output_attributes = list(
      FUNCTION_DEFINITION_ATTRIBUTES_MAP.keys())

  if "name" not in data.body.output_attributes:
    data.body.output_attributes = ["name", *data.body.output_attributes]

  data.result = await get_function_definition_attribute(
    attributes=data.body.output_attributes,
    function_definitions=data.result,
  )
  return data


async def get_response(data: Data) -> Data:
  if data.call_method == "api":
    return data.result

  # Response is a dataclass when call method is `module`
  fields = []
  for key, value in data.result.items():
    value_type = type(value).__name__
    field = [key, f"{value_type} | None", dc.field(default=None)]
    fields.append(field)
  dataclass = dc.make_dataclass(cls_name="Data", fields=fields)
  dataclass = dataclass()
  # Add values after creating the dataclass to prevent
  #  field values from being overwritten when using `default_factory``
  for field in dc.fields(dataclass):
    value = data.result[field.name]
    setattr(dataclass, field.name, value)

  return dataclass


# ruff: noqa: ARG001
async def main(
  module_path: str | None = None,
  output_attributes: List[str] | None = None,
) -> Dict[str, List[Any]]:
  """An orchestration function used to execute the functions within this module
    and return information about a module's functions"""
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  abstract_syntax_tree = await get_abstract_syntax_tree(
    module_path=data.body.module_path)
  data.result = await get_function_definitions(
    abstract_syntax_tree=abstract_syntax_tree,
    module_path=data.body.module_path,
  )

  data = await parse_function_definitions(data=data)
  data = await get_response(data=data)
  return data


async def example() -> None:
  import os

  module_path = os.path.join(
    os.path.dirname(MODULE_PATH),
    "test_resources",
    "add",
    "app.py",
  )
  data = await main(
    module_path=module_path,
    output_attributes=[],
  )
  print(data)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
