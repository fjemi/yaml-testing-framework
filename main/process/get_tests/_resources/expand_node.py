#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns


MODULE = __file__


def list_sns_to_list_dict(nodes: list | None = None) -> list | None:
  if not isinstance(nodes, list):
    return nodes

  nodes = [item.__dict__ for item in nodes if hasattr(item, '__dict__')]
  return nodes


def dict_sns_to_dict_dict(nodes: dict | None = None) -> dict | None:
  if not isinstance(nodes, dict):
    return

  for key, value in nodes.items():
    if not isinstance(value, sns):
      continue
    nodes[key] = value.__dict__

  return nodes


def nodes_as_dict(
  node: dict | None = None,
  nodes: dict | list | None = None,
) -> dict | list | None:
  if isinstance(node, sns):
    return node.__dict__

  if isinstance(nodes, sns):
    nodes = nodes.__dict__

  if isinstance(nodes, dict):
    for key, value in nodes.items():
      nodes[key] = value.__dict__
    return nodes

  elif isinstance(nodes, list):
    nodes = [node.__dict__ for node in nodes]
    return nodes


def nodes_as_sns(nodes: dict | None = None) -> dict:
  if isinstance(nodes, dict):
    for key, value in nodes.items():
      nodes[key] = sns(**value)
  elif isinstance(nodes, list):
    nodes = [sns(**node) for node in nodes]
  return nodes


def examples() -> None:
  from utils import invoke_testing_method

  invoke_testing_method.main(resource_flag=True)


if __name__ == '__main__':
  examples()
