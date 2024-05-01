#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns

from main.process.get_tests.combine_fields import main as combine_fields
from main.utils import get_config, independent, schema


MODULE = __file__
LOCALS = locals()

CONFIG = get_config.main(module=MODULE)


def main(
  root_node: dict | None = None,
  configurations: dict | None = None,
) -> sns:
  data = sns(**locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return sns(nodes=data.nodes)


def add_configurations_to_root_node(
  root_node: dict | None = None,
  configurations: dict | None = None,
) -> sns:
  data = sns(root_node=root_node)
  data.root_node = schema.get_model(name='Test', data=data.root_node)

  for field, value in data.root_node.__dict__.items():
    configuration = configurations.get(field, None)
    combination = combine_fields(
      high=configuration,
      low=value,
      field=field, )
    setattr(data.root_node, field, combination.output)

  return data


TEST_FIELDS = schema.get_model(name='Test', data={})
TEST_FIELDS = list(TEST_FIELDS.__dict__.keys())


def expand_nested_nodes(
  key: str | None = None,
  node: sns | None = None,
  nested_nodes: list | None = None,
) -> dict:
  nodes = {}
  node.tests = None
  del node.tests

  for i, item  in enumerate(nested_nodes):
    nested_node = schema.get_model(name='Test', data=item)
    for field in TEST_FIELDS:
      low = getattr(nested_node, field, None)
      high = getattr(node, field, None)
      combination = combine_fields(
        high=high,
        low=low,
        field=field, )
      setattr(nested_node, field, combination.output)

      nested_node.key = f'{key}.{i}'
      nodes.update({nested_node.key: nested_node})

  return nodes


def get_expanded_nodes(root_node: dict | None = None) -> sns:
  data = sns(expanded_keys=[], nodes={'0': root_node})

  visited_keys = []
  node_expanded = True

  while node_expanded:
    node_expanded = False

    for key, node in data.nodes.items():
      if key in visited_keys:
        continue
      visited_keys.append(key)

      nested_nodes = getattr(node, 'tests', {})
      if not nested_nodes:
        continue

      nested_nodes = expand_nested_nodes(
        nested_nodes=nested_nodes,
        key=key,
        node=node, )
      data.nodes.update(nested_nodes)
      data.expanded_keys.append(key)
      node_expanded = True
      break

  return data


def remove_roots_of_expanded_nodes(
  expanded_keys: list | None = None,
  nodes: dict | None = None,
) -> sns:
  for key in expanded_keys:
    if key in nodes:
      del nodes[key]

  nodes = list(nodes.values())
  return sns(expanded_keys=None, nodes=nodes)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
