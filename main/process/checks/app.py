#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, Callable, List

import yaml

from main.process import casts, spies, setup as SETUP
from main.utils import (
  get_config,
  independent,
  logger,
  objects,
  schema,
  get_module, )


CONFIG = get_config.main()

LOCALS = locals()


def main(
  checks: list | None = None,
  output: Any | None = None,
  module: ModuleType | None = None,
  id: str | None = None,
  id_short: str | None = None,
  setup: list = []
) -> sns:
  checks = checks or []
  locals_ = sns(**locals())
  del locals_.checks
  store = []

  for item in checks:
    item.update(locals_.__dict__)
    data = independent.get_model(schema=CONFIG.schema.Main, data=item)
    data = independent.process_operations(
      data=data,
      functions=LOCALS,
      operations=CONFIG.operations.main, )
    store.append(data.check)

  return sns(checks=store)


def pass_through(method: str | None = None) -> Callable:

  def pass_through_inner(
    module: ModuleType | None = None,
    output: Any | None = None,
    expected: Any | None = None,
  ) -> Callable:
    _ = output, expected, module

    return sns(
      passed=False,
      expected='',
      output=f"Check method {method} does not exist", )

  return pass_through_inner


def get_check_method(
  method: str = '',
  module: ModuleType | None = None,
  resource: str | None = '',
) -> sns:
  module = resource or module
  module = get_module.main(module=module, default=module).module
  route = str(method)
  method = objects.get(
    parent=module,
    route=route,
    default=pass_through(method=route), )
  return sns(method=method)


def reset_output_value(
  output: Any | None = None,
  field: str | None = None,
  cast_output: list = [],
  module: ModuleType | str = '',
) -> sns:
  output = objects.get(parent=output, route=field) if field else output
  output = casts.main(
    module=module,
    object=output,
    casts=cast_output, ).object
  return sns(output=output)


def get_check_result(
  module: ModuleType | None = None,
  method: Callable | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  spies_ = spies.get_store().spies_
  setup_ = SETUP.get_store().setup_
  arguments = locals()
  arguments = independent.get_function_arguments(
    function=method, data=arguments)
  result = method(**arguments)
  result.method = objects.get(
    parent=method,
    route='__name__',
    default=method, )
  return result


def convert_to_yaml(
  object: Any | None = None,
  field: str | None = None,
) -> sns:
  try:
    temp = object
    if isinstance(temp, str):
      temp = yaml.safe_load(temp)
    return yaml.dump(temp).strip()
  except Exception as error:
    arguments = dict(object=object, field=field)
    logger.main(error=error, arguments=arguments)
    return str(object)

  return temp


def handle_failed_check(
  passed: bool | None = None,
  output: Any | None = None,
  expected: Any | None = None,
) -> sns:
  data = sns()

  if passed is True:
    return data

  data.output = output
  data.expected = expected

  for key in data.__dict__:
    value = objects.get(parent=data, route=key)
    value = convert_to_yaml(object=value, field=key)
    data = objects.update(
      parent=data,
      route=key,
      value=value, )

  return data


def post_processing(
  id: str | None = None,
  id_short: str | None = None,
  expected: Any | None = None,
  output: Any | None = None,
  passed: Any | None = None,
  method: Callable | str | None = None,
) -> sns:
  method = objects.get(
    parent=method,
    route='__name__',
    default=method, )
  check = sns(**locals())
  return sns(check=check)


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
