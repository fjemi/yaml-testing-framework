# Pytest YAML

Pytest-YAML is a Pytest plugin for creating and running tests defined in YAML files. The plugin aims provide a zero-low code framework that simplifies testing code in Python. 

Supports:
- Data-driven testing
- Functional programming
- Patching objects
- Casting function arguments and results
- Multithreaded test executions

-------------

## Setup

### Install

The plugin can be installed from github or pypi using `pip`

#### From GitHub
```bash
pip install git+
```

#### From PyPi
```bash
pip install pytest-yaml
```

### Create Entrypoint File

Create the file, `test_entrypoint.py`, with the content below and place it in the project's root directory. It is used to collect and execute tests defined in YAML files.

This file is needed to:
- invoke `pytest`
- use the `pytest-yaml` plugin in order to collect and execute YAML defined tests
- pass collected tests as arguments to a parameterized test function.

```python
# test_entrypoint.py

import sys
import pytest


@pytest.mark.parametrize(
  argnames='test',
  argvalues=pytest.yml_tests,
  ids=lambda test: format_ids(test=test), )
def test_case(test: 'app.main.Test') -> None:
  if test.exception and test.assertions != test.result:
    print(test.exception.args)
  assert test.assertions == test.result
```

### Configure Pytest-YAML
  
The plugin can be configured within the pytest settings of a configuration file, such as a `pytest.ini`, or in the console when invoking pytest. The configurations are
- `project-path` - Absolute path to the directory containing the python files or to a python file.
- `exclude-match` - A list of string. If a python file has one of the strings in it's path, it will be excluded from being collected for testing.

#### Configure in pytest.ini

```
; pytest.ini

[pytest]
project-path = project_folder/
exclude_match =
  matching
  files
  to
  exclude
```

#### Configure in Console

```console
$ pytest --project-path=project_folder/ --exclude_match matching files to exclude
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

functions:
- name: add
  description: Returns the result of adding two numbers
  tests:
  - description: Add two integers
    arguments:
      a: 1
      b: 2
    assertions:
    - equals: 3
    - type: 
      - int
  - description: Add two floats
    arguments:
      a: 1.5
      b: 2.5
    assertions:
    - equals: 4
    - type: 
      - float
```

Then execute the following command in the console to collect and run the tests:

```console
pytest --project-path=/home/olufemij/example --exclude-match test_app.py -vvv
```

Here we see the results of the tests. Two tests were collected, **Add two integers** and **Add two floats**, and both passed.

![Alt text](./static/example_result.png?raw=true "Title")


## Creating Test Files

### Schema

```yaml
functions:
- name: 
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
    description: Cast keyword arguments before passing them to the function 
    type: object
    examples:
      'Cast argument `a` to an integer':
        value:
          a: int
      'Cast argument `a` to an float':
        value:
          b: float
    nullable: True
  cast_result: string
  assertions: Array[Assertion]
  tests: array[Test]


```

```yaml
functions:
- name: string
  description: string
  patch: array[Patch]
  cast_arguments: object
  cast_result: string
  assertions: Array[Assertion]
  tests: array[Test]
```

#### Test

### Test Resources

We can create a folder name `test_resources` in the same directory as a test file and add additional resources needed to run a test. 

#### Python Files

Python modules placed in `test_resources` will automatically be imported into the module being tested, and we can access the objects within module in the YAML test files: `test_resources.module_name.object_name`.

##### Example

In this example we create module `app.py` as a test resource, and use the dataclass in the module to cast arguments we will pass to the function when testing.

```python
# ./example/test_resources/app.py

import dataclasses as dc


@dc.dataclass
class Data
  a: int
  b: int
```

```yaml
# ./example/app_test.yml

functions:
- ...
  arguments:
    data:
      a: 0
      b: 0
  cast_arguments: 
    data: test_resources.app.Data
```

### Patch

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

functions:
- name: add
  cast_arguments:
    a: str
    b: str
  cast_result: int
  tests:
  - description: override function level casting
    cast_arguments:
      a: int
      b: int
    arguments:
      a: 0
      b: 1
    cast_result: str
    assertions:
      equals: '01'
  - description: use function level casting
    arguments: 
      a: 1
      b: 2
    assertions:
      equals: 12
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
# add.py

import dataclasses as dc


@dc.dataclass
class Data:
  a: int
  b: int
  result: int | None = None


def add_numbers(a, b):
  return a + b


def add_numbers_in_dataclass(data):
  data.result = data.a + data.b
  return data
```

```yaml
# add_test.yml

functions:
- name: add_numbers
  description: Returns the result of adding two numbers
  tests:
  - description: Result of adding two numbers
    arguments:
      a: 1
      b: 2
    assertions:
    - equals: 3
    - type: 
      - int
  - description: Result should be an type error
    arguments:
      a: 1
      b: string
    assertions:
    - equals: TypeError
- name: add_numbers_in_dataclass
  description: Returns a dataclass with the result of adding two numbers
  tests:
  - description: Result should have the correct attribute/value and type
    arguments:
      data:
        a: 1
        b: 2
    cast_arguments:
      data: 
      - Data
    assertions:
    - has_attributes:
        result: 3
    - type: 
      - Data
  - description: Result should have the correct key/value and type
    arguments:
      data:
        a: 1
        b: 2
    cast_arguments:
      data: 
      - Data
    cast_result: dict
    assertions:
    - has_keys:
        result: 3
    - type: 
      - dict
```



```yaml
# add_test.yml

functions:
- name: add_numbers
  ...
  tests:
  - description: Result of adding two numbers
    ...
    result:
    - equals: 3
    - type: 
      - int
  - description: Result should be an type error
    ...
    results:
    - equals: TypeError
- name: add_numbers_in_dataclass
  ...
  tests:
  - description: Result should have the correct attribute/value and type
    ...
    results:
    - has_attributes:
        result: 3
    - type: 
      - Data
  - description: Result should have the correct key/value and type
    ...
    results:
    - has_keys:
        result: 3
    - type: 
      - dict
```