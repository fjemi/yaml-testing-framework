#!.venv/bin/python3
# -*- coding: utf-8 -*-


def list_sns_to_list_dict(result: list | None) -> list:
  result = result or []
  for i, item in enumerate(result):
    result[i] = item.__dict__
  return result


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main(
    resources_folder_name='resources',
    resource_flag=True, )


if __name__ == '__main__':
  examples()
