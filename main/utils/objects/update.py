#!.venv/bin/python3
# -*- coding: utf-8 -*-


from types import SimpleNamespace as sns
from typing import Any, Iterable

from main.utils.objects.get import main as objects_get_main
from main.utils import logger


def main(
  parent: Any | None = None,
  value: Any | None = None,
  route: str | None = None,
) -> Any:
  data = get_route_values(
    route=route,
    parent=parent,
    value=value, )
  return reset_route_values(objects=data.objects)


def get_route_values(
  parent: Any | None = None,
  route: str | None = None,
  value: Any | None = None,
) -> sns:
  data = sns(route=route)
  data.objects = [sns(name='root', value=parent)]

  if data.route is None or data.route in ['', '.']:
    return data

  data.route = data.route.strip().split('.')

  for i, item in enumerate(data.route[:-1]):
    last = data.objects[-1]
    current = sns(name=data.route[i])
    current_route = '.'.join(data.route[:i + 1])
    current.value = objects_get_main(parent=last.value, route=current_route)
    if current.value is None and i != len(data.route) - 1:
      current.value = sns()
    data.objects.append(current)

  end = sns(value=value, name=data.route[-1])
  data.objects.append(end)

  return data


def get_slice_start_and_end_indices(name: str | None = None) -> sns:
  data = sns()
  name =  str(name).strip()
  name = f'{name}|' if name.find('|') == -1 else name
  indices = name.split('|')[:2]
  indices = [int(i) if str(i).isdigit() else None for i in indices]
  data.start, data.end = indices
  return data


def replace_slice_with_value(
  parent_value: Iterable | None = None,
  child_value: Any | None = None,
  indices: sns | None = None,
) -> Iterable:
  value = None

  if indices.start == indices.end and indices.start is not None:
    value = parent_value
    value[indices.start] = child_value
  elif indices.start == indices.end and indices.start is None:
    value = child_value
  elif False not in [
    indices.start != indices.end,
    indices.start is not None,
    indices.end is not None,
  ]:
    value = parent_value[:indices.start] + child_value
    value = value + parent_value[indices.end:]
  elif indices.start is None and indices.end is not None:
    value = parent_value[:indices.end] + child_value
  elif indices.start is not None and indices.end is None:
    value = child_value + parent_value[indices.start:]

  return value


def set_child_in_parent(
  parent: sns | None = None,
  child: sns | None = None,
) -> sns:
  if isinstance(parent.value, dict):
    parent.value.update({child.name: child.value})

  elif False not in [
    isinstance(parent.value, Iterable),
    not isinstance(parent.value, dict)
  ]:
    indices = get_slice_start_and_end_indices(name=child.name)
    parent.value = replace_slice_with_value(
      child_value=child.value,
      indices=indices,
      parent_value=parent.value, )

  elif parent.value is not None:
    try:
      setattr(parent.value, child.name, child.value)
    except Exception as error:
      arguments = dict(parent=parent, child=child)
      logger.main(error=error, arguments=arguments)
      parent.value = sns()
      setattr(parent.value, child.name, child.value)

  elif parent.value is None:
    object_ = sns()
    setattr(object_, child.name, child.value)
    parent.value = object_

  return parent


def reset_route_values(objects: list | None = None) -> Any:
  for i, parent in reversed(list(enumerate(objects[:-1]))):
    child = objects[i + 1]
    objects[i] = set_child_in_parent(parent=parent, child=child)
  return objects[0].value


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
