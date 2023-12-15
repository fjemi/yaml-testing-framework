<!-- markdownlint-disable MD024 -->
# YAML Testing Framework

A testing framework and `pytest` plugin that collects and executes tests and configurations defined in YAML files. The framework aims provide a zero to low code solution for simplifying testing in Python.

Supports:

- YAML/Data driven testing
- Functional programming
- Patching objects
- Casting function arguments and output
- Multithreaded test executions

## Setup

### Install

#### From GitHub using

`pipenv`

```console
pipenv install git+https://github.com/fjemi/pytest-yaml#egg=pytest-yaml
```

`pip`

```console
pip install git+https://github.com/fjemi/pytest-yaml
```

<!-- #### From PyPi
```bash
pip install pytest-yaml
``` -->

### Add Entrypoint for Tests

Create the file `test_entrypoint.py` with the content below and place it in the project's root directory. It is used to collect and execute tests defined in YAML files.

This file is needed to:

- invoke `pytest`
- allow the plugin to collect and execute tests defined in YAML files
- pass collected tests as arguments to a parameterized test function within `test_entrypoint.py`.

```python
# test_entrypoint.py


import asyncio
import sys
import time
from typing import Any

import pytest
import yaml
from error_handler.app import main as error_handler
from get_value.app import main as get_value
from logger.app import main as logger


COUNT = 0


class Store:
  pass


@error_handler()
async def get_ids(test: Any | None) -> str:
  if isinstance(test, list):
    test = test[0]

  id_ = get_value(
    test,
    'id_short',
    id_callaback(),)

  if isinstance(id_, list):
    for item in id_:
      if item:
        return item

  return id_


@error_handler()
async def id_callaback(
  data: None = None,
) -> str:
  global COUNT

  COUNT += 1
  return f'test_{COUNT}'


asyncio.run(logger(
  data='\n\n',
  standard_output=True, ))
time.sleep(.01)


@pytest.mark.parametrize(
  argnames='test',
  ids=lambda test: get_ids(test=test),
  argvalues=pytest.yaml_tests, )
def test_(test: Any) -> None:
  if isinstance(test, list):
    test = test[0]
  if test is None:
    return

  for assertion in test.assertions:
    data = {
      'module': test.module,
      'function': test.function,
      'yaml': test.yaml, }
    if assertion.exception:
      data.update({'exception': assertion.exception,})
    asyncio.run(logger(
      data=data,
      standard_output=False, ))

    actual = assertion.actual
    expected = assertion.expected

    try:
      actual = yaml.dump(actual)
      expected = yaml.dump(expected)
    except Exception as e:  # noqa: F841
      pass

    assert expected == actual


if __name__ == '__main__':
  args = [
    '-s',
    '-vvv',
    '--project-directory=.main', ],
  sys.exit(pytest.main(args))

```

### Configure Plugin

The plugin can be configured within the pytest settings of a configuration file, such as a `pytest.ini`, or in the console when invoking pytest. The configurations are

- `project-directory` - Absolute path of a module or a directory containing modules to tests.
- `exclude-files` - A list of patterns. Modules that have loations that match one of the patterns are excluded from testsing.
- `resources` - A list containing the location of modules to use or import during tests.

#### Configure in pytest.ini

```ini
; pytest.ini

[pytest]
project-directory = project_folder
exclude_files =
  matching
  patterns
  to
  exclude
resournces =
  resource_location_a
  resource_location_b
```

#### Configure in Console

```shell
pytest --project-directory=project_folder/ --exclude_files matching patterns to exclude  --resources resource_location_a resource_location_b
```

## A Quick Example

In this example we create two files:

- `add.py` - Contains a simple function to add two numbers. This is the function we will test.
- `add_test.yml` - Contains the data for two tests, **Add two integers** and **Add two floats**, that we will use to test the function. For both tests we define arguments, `a` and `b`, to pass to the `add` function; and assert that the result from the function equals an expected value and is of an expected type

```python
# add.py

def add(a, b):
  return a + b
```

```yaml
# add_test.yml

tests:
- function: add
  description: Returns the result of adding two numbers
  tests:
  - description: Add two integers
    arguments:
      a: 1
      b: 2
    assertions:
    - method: equals
      expected: 3
    - method: type
      expected:
        - int
  - description: Add two floats
    arguments:
      a: 1.5
      b: 2.5
    assertions:
    - method: equals
      expected: 4
    - method: type
      expected:
        - float
```

Then execute the following command in the console to collect and run the tests:

```console
pytest --project-directory=./add.py -s -vvv
```

Here we see the results of the tests. Two tests were collected, **Add two integers** and **Add two floats**, and both passed.

![Alt text](./static/example_result.png?raw=true "Title")

## Creating Test Files

### Schema

```yaml
globals: ...

tests:
- function:
    type: string
    description: The name of the function
    example: add
  description:
    type: string
    description: A description of the function
    example: add two numbers
    nullable: True
  patch:
    type: array[Patch]
    description: A list of objects and values to patch
    nullable: True
  cast_arguments:
    description: >
      Cast keyword arguments before passing
      them to the function
    type: object
    examples:
      "Cast argument `a` to an integer":
        value:
          a: int
      "Cast argument `a` to an float":
        value:
          b: float
    nullable: True
  cast_output:
  - caster: string
    field: string
    unpack: bool
  assertions: Array[Assertion]
  tests: array[Test]
```

```yaml
tests:
- function: string
  environment: object
  description: string
  patches: array[object]
  cast_arguments: array[object]
  cast_output: array[object]
  assertions: array[object]
  tests: array[object]
```

### Test Resources

We can create a `test_resources` folder in the same directory as the module to test, and add any files needed to run the tests to the folder. Modules placed in the `test_resources` will automatically be imported into the module to test, and the objects with module resources can be accessed in the YAML test file as `test_resources.[module_name].[object_name]`.

#### Example

In this example we create module `app.py` as a test resource, and use the dataclass in the module to cast arguments we will pass to the function when testing.

```python
# ./test_resources/app.py

import dataclasses as dc


@dc.dataclass
class Data_Class
  a: int
  b: int
```

```yaml
# ./app_test.yml

tests:
- ...
  arguments:
    data:
      a: 0
      b: 0
  cast_arguments:
  - caster: test_resources.app.Data_Class
    field: Data
    unpack: true
```

This casts the `data` key of the `arguments` as the dataclass defined in resources module `test_resources.app`

### Patches

We can patch objects within a function's module prior to running tests. Patches can be defined for all of the tests associated with a function or an individual tests, and we can have different patches of the same object for individual tests with interference

There are four types of patches:

- **value** - A value to return when the patched object is used.
- **return_value** - A value to return when the patched object is called as function.
- **side_effect_list** - A list of values to call based off of the number of times the object is called. Returns the item at index `n - 1` of the list for the `nth` call of the object. Reverts to index 0 when number of calls exceeds the length of the list.
- **side_effect_dict** - A dictionary of key, values for to patch an object with. When the patched object is called with a key, the key's associated value is returned

#### Example

In this example we will patch Python's built in `os` module within the module we want to test, `app.py`.

```python
# app.py

import os
```

```yaml
# app_test.yml

function:
  ...
  patch:
  - object: os.value
    value: function_level_value
  - object: os.return_value
    return_value: return_value
  - object: os.side_effect_list
    side_effect_list:
    - side_effect_1
    - side_effect_2
  - object: os.side_effect_dict
    side_effect_dict:
      key_1: side_effect_1
      key_2: side_effect_2
  tests:
  - description: override function level patch
    patch:
      object: os.value
      value: overrides_function_level_patch
    ...
  - description: use function level patches
    ...
```

When these two tests are run, if the patched objects are used the result will be

```python
# test: override function level patch

value = os.value
print(value)
# prints `overrides_function_level_patch`

value = os.return_value()
print(value)
# prints `return value`

values = [
  os.side_effect_list(),
  os.side_effect_list(),
  os.side_effect_list(), ]
print(values)
# prints `[side_effect_1, side_effect_2, side_effect_1]`


# test: use function level patches

value = os.value
print(value)
# prints `function_level_value`

values =
  [os.side_effect_dict('key_1'),
  os.side_effect_dict('key_2'), ]
print(values)
prints `[side_effect_2, side_effect_1]`
```

### Casting

We can cast arguments before passing them to a function or cast the result of executing the function. Similar to patching, casting can be set at the function and individual test levels.


#### Example

```python
# ./example/add.py

def add(a, b):
  return a + b
```

```yaml
# ./example/add_test.py

tests:
- function: add
  cast_arguments:
  - field: a
    caster: __builtins__.str
  - field: b
    caster: __builtins__.str
  cast_output:
  - caster: __builtins__.int
  tests:
  - description: override function level casting
    cast_arguments:
    - field: a
      caster: __builtins__.int
    - field: b
      caster: __builtins__.int
    arguments:
      a: 0
      b: 1
    cast_output:
    - caster: __builtins__.str
    assertions:
    - method: equals
      expected: "01"
  - description: use function level casting
    arguments:
      a: 1
      b: 2
    assertions:
    - method: equals
      expected: 12
```

### Assertions

For each test we can define one or more "pseudo" assertions. Each pseudo assertion is a dictionary with the key being a function and the value being the expected result from the test function: `{assertion_name: expected_value}`. The pseudo assertion function processes the actual result from the test function, and returns a dictionary that is added to a list of results. The actual "assertion" that is picked up by pytest is carried out in the `test_entrypoint.py` file, where we assert that the the test assertions are equal to the tests results (results from pseudo assertions).

Assertions:
- equals - Checks that the expected result equals the actual result. This can include the test function resulting in an error.
- type - Check that the expected result's type equals the actual result's type
- has_attributes: Check that the actual resulting object has defined attributes and values
- has_keys: Check that the actual resulting dictionary has defined keys and values

#### Example

In this example we define two functions: one for adding two numbers and the other for adding two numbers in a dataclass. We use all of the assertions listed above in one or more of the tests.

```python
# ./add.py

import dataclasses as dc


@dc.dataclass
class Data_Class:
  a: int | None = None
  b: int | None = None
  result: int | None = None


def add_numbers(a, b):
  return a + b


def add_numbers_in_dataclass(data):
  data.result = data.a + data.b
  return data
```

```yaml
# ./add_test.yml

tests:
- function: add_numbers
  description: Returns the result of adding two numbers
  tests:
  - description: Result of adding two numbers
    arguments:
      a: 1
      b: 2
    assertions:
    - method: equals
      expected: 3
    - method: type
      expected:
        - int
  - description: Result should be an type error
    arguments:
      a: 1
      b: string
    assertions:
    - method: equals
      expected: TypeError
- function: add_numbers_in_dataclass
  description: Returns a dataclass with the result of adding two numbers
  tests:
  - description: Result should have the correct attribute/value and type
    arguments:
      data:
        a: 1
        b: 2
    cast_arguments:
    - field: data
      unpack: true
      caster: Data_Class
    assertions:
    - method: equals
      expected: 3
      field: result
    - method: type
      expected: Data_Class
  - description: Result should have the correct key/value and type
    arguments:
      data:
        a: 1
        b: 2
    cast_arguments:
    - field: data
      unpack: true
      caster: Data_Class
    cast_output:
    - caster: dc.asdict
    assertions:
    - method: equals
      field: result
      expected: 3
    - method: type
      expected: dict
```

<!-- markdownlint-disable MD024 -->
