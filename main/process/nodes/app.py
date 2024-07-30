#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns

from main.process.nodes import combine
from main.utils import get_config, independent, objects


CONFIG = get_config.main()
LOCALS = locals()


def main(
  yaml: str | None = None,
  module: str | None = None,
  module_route: str | None = None,
  setup: list = [],
) -> sns:
  data = sns(**locals())
  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return sns(tests=data.nodes)


def get_content(
  yaml: str | None = None,
  module: str | None = None,
  module_route: str | None = None,
  setup: list = [],
) -> sns:
  locals_ = sns(**locals())
  content = independent.get_yaml_content(location=yaml).content or {}
  content.update(locals_.__dict__)
  return sns(content=content)


def get_roots(content: dict | None = None) -> sns:
  roots = objects.get(parent=content, route='tests') or []
  store = {}

  for i, item in enumerate(roots):
    node = combine.main(parent=content, child=item)
    node = independent.get_model(schema=CONFIG.schema.Test, data=node)
    node.key = str(i)
    store.update({node.key: node})

  return sns(roots=store)


def expand_nodes(roots: dict | None = None) -> sns:
  keys = sns(visited={}, expanded={})
  flags = sns(exit_=False, expanded=False)

  while flags.exit_ is False:
    flags.expanded = False
    store = {}

    for key, node in roots.items():
      if key in keys.visited:
        continue

      nested = get_nested_nodes(node=node)
      store.update(nested)

      keys.visited[node.key] = 1
      if not nested:
        continue

      keys.expanded[node.key] = 1
      flags.expanded = True
      break

    flags.exit_ = not store
    roots.update(store)

  return sns(nodes=roots, expanded=keys.expanded)


def get_nested_nodes(node: sns | None = None) -> dict:
  nodes = objects.get(parent=node, route='tests') or []
  store = {}

  for i, item in enumerate(nodes):
    nested = combine.main(parent=node, child=item)
    nested = independent.get_model(schema=CONFIG.schema.Test, data=nested)
    nested.key = f'{node.key}|{i}'
    store.update({nested.key: nested})

  return store


def remove_expanded(
  nodes: dict | None = None,
  expanded: list | None = None,
) -> sns:
  store = []
  for key, value in nodes.items():
    if key not in expanded:
      store.append(value)
  return sns(nodes=store)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
