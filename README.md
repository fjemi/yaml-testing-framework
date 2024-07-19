# YAML Testing Framework

A simple, low-code framework for unit testing in Python with tests are defined in YAML files.

## Features


## Requirements

Python 3.7+


## Installation

```bash
pip install yaml-testing-framework
```


## Example


Create the files
- `test_entrypoint.py` - uses pytest to collect and run tests
```python
from types import SimpleNamespace as sns

import pytest


@pytest.mark.parametrize(argnames='test', argvalues=pytest.yaml_tests)
def test_(test: sns) -> None:
  assert test.expected == test.output
```

- `checks.py` - contains logic for verifying the output from a function
```python
from types import SimpleNamespace as sns
from typing import Any


 equals(expected: Any, output: Any) -> sns:
  passed = expected == output
  return sns(**locals())
```

- `add.py` - contains the function to test
```python
  def main(a: int, b: int) -> int:
    return a + b
```

- `add_test.yaml` - contains tests for the function
```yaml
resources:
- &CHECKS
  ./checks.py


tests:
- function: main
  tests:
  - arguments:
      a: 1
      b: 1
    checks:
    - method: checks.equals
      expected: 2
  - arguments:
      a: 1
      b: 2
    checks:
    - method: checks.equals
      expected: 3
  - arguments:
      a: 1
      b: '1'
    checks:
    - method: checks.equals
      field: 2
```

Execute the following command in your command line to run the tests.
```bash
pytest --project-path=add.py
```


## Configuration

The app can be configured within the pytest settings of a configuration file,
 such as a `pytest.ini`, or in the console when invoking pytest. The
 configurations are

| Field | Type | Description | Default |
| - | - | - | - |
| project-path | str | Location of a directory containing files or an an individual module or YAML file to test. | . |
| exclude-files | str or list| A list of patterns. Exclude files from testing that match a specified pattern . | [] |
| yaml-suffix | str | Suffix in the names of YAML files containing tests | _test |


#### Configure pytest.ini


```ini
[pytest]
project-path = .
exclude_files =
  matching
  patterns
yaml_suffix = _test
```

#### Configure command line command

```console
pytest \
--project-path=. \
--exclude_files exclusion patterns \
--include_files inclusion patterns \
--yaml-suffix _test
```


## YAML Test Files

Tests are defined in YAML files with the top level keys picked up by the app
being:
- `configurations` - Configurations to be used locally for each test in the YAML files
- `tests` - Configurations used for multiple of individual tests.


### Expanding and Collating Tests

Using the app we can define configurations for tests at various levels
(configurations, tests, nested tests), expand those configurations to lower
configurations, and collate individual tests. This allows us to reuse
configurations and reduce the duplication of content across a YAML file. This is
similar to [anchors](https://yaml.org/spec/1.2.2/#anchors-and-aliases) in YAML,
which we can take advantage, along with the other features available in YAML.

#### Example

This is an abstract example of the expanding/collating configurations done by
the app, where the configurations for tests are comprised of:
- `config_a` - a list
- `config_b` - an object
- `config_c` - a string
- `config_d` - null

In this example, we set these configurations at various levels, globally, tests,
and nested tests; and the expanded/collated results are three individual tests
containing various values for each configuration.

```yaml
# Defined

configurations:
  config_a:
  - A
  config_b:
    b: B
  config_c: C


tests:
- config_a:
  - B
- config_b:
    c: C
  tests:
  - config_a:
    - C
    config_c: C0
  - config_d: D
    tests:
    - config_a:
      - B
      config_b:
        b: B0
```

```yaml
# Expanded

tests:
- config_a: # test 1
  - A
  - B  # Appended item
  config_b:
    b: B
  config_c: C
  config_d: null  # Standard test config not defined
- config_a: # test 2
  - A
  - C  # Appended item
  config_b:
    b: B
    c: C  # Added key/value
  config_c: C0  # Replace string
  config_d: null
- config_a: # test 3
  - A
  config_b:
    b: B0  # Updated key/value pair
    c: C
  config_c: C
  config_d: D  # Standard test config defined
```


### Schema

Details for configurations or fields of an actual test are defined below. These
fields can be defined globally or at different test levels.

| Field | Type | Description | Expand Action |
| - | - | - | - |
| function | str | Name of function to test | replace |
| environment | dict | Environment variables used by functions in a module | update |
| description | str or list | Additional details about the module, function, or test | append |
| patches | dict or list | Objects in a module to patch for tests | append |
| cast_arguments | dict or list | Convert function arguments to other data types | append |
| cast_output | dict or list | Convert function output to other data types | append |
| checks | dict or list | Verifies the output of functions | append |
| spies | list or str | List of methods to spy on and see if called during test | append |
| tests | dict or list | Nested configurations that get expanded into individual tests | append |


## Checks

### Methods

We can define methods to compare expected and actual output from a function being tested. Methods should have the parameters `expected` and `output`, and return a **SimpleNamespace** object containing `expected`, `output`, `passed` (a boolean indicating whether the check passed or failed). Methods can also be reused between tests.

#### Example

Here we define a method for verifying that a function's output is of the correct type.

```python
from types import SimpleNamespace as sns
from typing import Any


def check_type(
  output: Any,
  expected: str,
) -> sns:
  passed = expected == type(output).__name__
  return sns(**locals())
```

### Schema

Checks are defined in YAML test files under the key `checks`, and a
single check has the following fields:

| Field | Type | Description | Default |
| - | - | - | - |
| method | str | Function or method used to verify the result of test | pass_through |
| expected | Any | The expected output of the function | null |
| field | str | Sets the output to a dot-delimited route to an attribute or key within the output. | null |
| cast_output | dict or list | Converts output or an attribute or key in the output before processing an check method | null |
| resource | str | Location of a module containing a resource to use during testing | '' |


And single test can have multiple checks

```yaml
checks:
- method: method
  expected: expected
  field: field
  resource: resource
  cast_output: []
```

## Cast arguments and output

We can convert arguments passed to functions and output from functions to other data types. To do this we define cast objects and list them under the keys `cast_arguments` and `cast_output` for tests or `cast_output` for checks.

### Schema

The following fields make up a cast object:

| Field | Description | Default |
| ----- | ----------- | ------- |
| method | Dot-delimited route to a function or object to cast a value to| null |
| field | Dot-delimited route to a field, attribute, or key of an object. When set the specified field of the object is cast | null |
| unpack | Boolean indicating whether to unpack an object when casting| False |
| resource | Location of a module containing a resource to use during testing | '' |

```yaml
cast_arguments:
- method: method
  field: field
  unpack: false
  resource: resource

cast_output:
- method: method
  field: field
  unpack: false
  resource: resource

checks:
- cast_output:
  - method: method
    field: field
    unpack: false
    resource: resource
...
```

## Patches

We can patch objects in the module to test before running tests, and since tests are run in individual threads we can different patches for the same object without interference between tests.

### Methods

There are four patch methods:

- `value` - A value to return when the patched object is used.
- `callable` - A value to return when the patched object is called as function.
- `side_effect_list` - A list of values to call based off of the number of
times the object is called. Returns the item at index `n - 1` of the list for
the `nth` call of the object. Reverts to index 0 when number of calls exceeds
the length of the list.
- `side_effect_dict` - A dictionary of key, values for to patch an object
with. When the patched object is called with a key, the key's associated value
is returned

### Schema

Patches are defined at a list of objects in YAML test files under the key
`patches`, and a single patch object has the following fields:

| Field | Type | Description | Default |
| - | - | - | - |
| method | str | One of the four patch methods defined above | null |
| value | Any | The value the patched object should return when called or used | null
| name | str | The dot-delimited route to the object we wish to patch, in the module to test | null |
| resource | str | Location of a module containing a resource to use during testing | '' |


```yaml
patches:
- method: value
  value: value
  route: route
  resource: resource
```


## Environment

For modules containing a global variable `CONFIG`, we can perform tests using different environment variables by the variables as adding key/value pairs under the key `environment` in YAML files. The environment variables are accessible from `CONFIG.environment.[route]`, where `[route]` is the dot-delimited route to the variable within the module.

### Example

```yaml
configurations:
  set_environment:
    NAME_A: a
    NAME_C: c
  

tests:
- set_environment:
    NAME_A: A
    NAME_B: b
```


## Spies

We can spy on methods to verify that the methods are called when the function being tested is executed. To do this we list the dot delimited routes to the methods to spy on under the key `spies` in YAML test files. Spies can be defined at the global, configuration, and test levels; and are combined into one. Spies are saved to the attribute `SPIES` in the module of the function being tests, and are accessible from an check method.

### Example

In this example, the methods to spy on are listed under the `spies` key at the individual test level, and an check method to verify spies is defined as a function.


```yaml
# ,/app_test.py

tests:
- spies:
  - route.method_a
  - route.method_b
  checks:
  - method: check_spies
    expected:
      route.method_a:
        called: True
        called_with: []
      route.method_b:
        called: False
        called_with: None
```

```python
# ./checks.py

from types import ModuleType
from types import SimpleNamespace as sns


def check_spies(
  module: ModuleType,
  output: Any,
  expected: dict
) -> sns:
  '''Example check method for verifying that a function was called'''
  spies = {}
  for key, value for expected.items():
    spy = module.SPIES.get(key, {})
      if spy != value
        continue
    spies[key] = spy
  passed = expected == spies
  return sns(
    output=spies,
    expected=expected,
    passed=passed, )
```

<br>
<a
  href="https://www.buymeacoffee.com/olufemijemo"
  target="_blank"
>
  <img
    src="https://cdn.buymeacoffee.com/buttons/default-orange.png"
    alt="Buy Me A Coffee"
    height="41"
    width="174"
  >
</a>
