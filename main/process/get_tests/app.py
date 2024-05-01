#!.venv/bin/python3
# -*- coding: utf-8 -*-

from types import SimpleNamespace as sns

from main.process.get_tests import expand_node
from main.process.get_tests.combine_fields import main as combine_fields
from main.utils import get_config, independent


MODULE = __file__
CONFIG = get_config.main(module=MODULE)
LOCALS = locals()


def main(
  yaml: str | None = None,
  module: str | None = None,
  module_location: str | None = None,
  module_route: str | None = None,
  resources: str | None = None,
) -> sns:
  data = sns(**locals())
  del yaml, module, module_location, module_route, resources

  data = independent.process_operations(
    operations=CONFIG.operations.main,
    functions=LOCALS,
    data=data, )
  return data


def get_configurations_and_tests(yaml: str | None = None) -> sns:
  content = independent.get_yaml_content(location=yaml).content or {}
  data = sns()
  for key, default in CONFIG.content_keys_and_defaults.items():
    value = content.get(key, None) or default
    setattr(data, key, value)
  return data


def format_locations(
  yaml: str | None = None,
  module: str | None = None,
  module_location: str | None = None,
  module_route: str | None = None,
  resources: str | None = None,
) -> sns:
  locations = sns(**locals())
  data = sns(locations=locations)
  for key in locations.__dict__:
    setattr(data, key, None)
  return data


def add_locations_to_configurations(
  locations: sns | None = None,
  configurations: dict | None = None,
) -> sns:
  configurations = configurations or {}
  data = sns(configurations=configurations, locations=None)

  for field, location in locations.__dict__.items():
    configuration = data.configurations.get(field, None)
    combination = combine_fields(
      high=location,
      low=configuration,
      field=field, )
    data.configurations[field] = combination.output

  return data


def get_expanded_nodes(
  tests: list | None = None,
  configurations: dict | None = None,
) -> sns:
  data = sns(tests=[])
  for root_node in tests:
    expanded_nodes = expand_node.main(
      root_node=root_node,
      configurations=configurations, )
    data.tests.extend(expanded_nodes.nodes)
  return data


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
