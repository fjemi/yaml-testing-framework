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
from typing import Any


 def check_equal(
  expected: Any,
  output: Any,
) -> dict:
  passed = expected == output
  return dict(
    passed=passed,
    output=output,
    expected=expected, )
```

- `add.py` - contains the function to test
```python
  def main(a, b):
    return a + b
```

- `add_test.yaml` - contains tests for the function
```yaml
resources:
- &CHECKS
  resource: ./checks.py


tests:
- function: main
  description: Returns the result of adding two integers
  tests:
  - description: Add one negative and one positive integer
    arguments:
      a: 1
      b: -1
    checks:
    - method: equals
      << : *CHECKS
      expected: 0
  - description: Add two positive integers
    arguments:
      a: 1
      b: 2
    checks:
    - method: equals
      << : *CHECKS
      expected: 3
  - description: Add integer and string
    arguments:
      a: 1
      b: '1'
    checks:
    - method: equals
      << : *CHECKS
      field: __class__.__name__
      expected: TypeError
```

Execute the following command in your command line to run the tests.
```bash
pytest --project-path=./add.py
```

## Configuration

The app can be configured within the pytest settings of a configuration file,
 such as a `pytest.ini`, or console command when invoking pytest. The
 configurations are

| Field | Type | Description | Default |
| - | - | - | - |
| project-path | str | Location of a directory containing files or an an individual module or YAML file to test. | . |
| exclude-files | str or list | Patterns found in the paths of files to exclude | [] |
| exclude-methods | str or list | Patterns found in the names of methods to exclude | [] |
| include-files | str or list | Patterns found in the paths of files to include | [] |
| include-methods | str or list | Patterns found in the names of methods to include | [] |
| yaml-suffix | str | Suffix in the names of YAML files containing tests | _test |
| setup | str | Defines resources to setup or teardown during tests | '' |

#### Configuration file


```ini
# ./pytest.ini


[pytest]
project-path = .
exclude_files =
  exclude
  patterns
exclude_methods =
  exclude
  patterns
include_files =
  include
  patterns
include_methods =
  include
  patterns
yaml_suffix = _test
setup = '''
  - name: api
    phase: global
    method: run_server
    arguments:
      host: localhost
      port: 1234
    resource: ./api.py
    timeout: -1
  '''
```

#### Console command

```bash
pytest --project-path=. --exclude_files exclude patterns --exclude_methods exclude patterns --include_files include patterns --include_method include patterns --yaml-suffix _test --setup '- name: api\nphase: global\nmethod: run_server\narguments:\n  host: localhost\n  port: 1234\nresource: ./api.py\ntimeout: -1\n'
```


## YAML Test Files

Tests are defined in YAML files with the top level keys picked up by the app
being:
- `configurations` - Configurations to be used locally for each test in the YAML files
- `tests` - Configurations used for multiple of individual tests.


### Expanding Tests

Using the app we can define configurations for tests at various levels
(configurations, tests, nested tests), expand those configurations out to
individual tests. This allows us to reuse configurations and reduce the
duplication of content across a YAML file; similar to
[anchors](https://yaml.org/spec/1.2.2/#anchors-and-aliases) in YAML, which we
can take advantage, along with the other features available in YAML.

#### Example

This is an abstract example of the expanding configurations done by
the app, where the configurations for tests are comprised of:
- `config_a` - a list
- `config_b` - an object
- `config_c` - a string
- `config_d` - null

In this example, we set these configurations at various levels, globally, tests,
and nested tests; and the expanded results are three individual tests
containing various values for each configuration.

```yaml
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
tests:  # Expanded
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


### Levels (Phases)

The testing process can be broken up into following four ordered phases:
1. global
2. module
3. function
4. check

These phases are synonymous with the levels configurations are be defined at.
Configurations described at higher levels are expanded to lower levels, and
objects created at higher phases are available at lower phases.


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
| spies | list or str | List of methods to spy on | append |
| setup | list or str | Defines objects to setup or teardown during test phases | append |
| tests | dict or list | Nested configurations that get expanded into individual tests | append |


## Checks

### Methods

We can define "check" methods or reusable functions used to compare expected
and actual output from a function being tested. These methods can have any of
the fields in the table below as parameters.

| Parameter | Type | Description |
| - | - | - |
| output | Any | Output from a method to check |
| expected | Any | Value to verify the output against |
| setup_ | dict | Access objects created or setup to facilitate testing |
| spies_ | dict | Access spies placed on methods |
| module | ModuleType | Module of the method being tested |

Check methods should return a dictionary (or object with **__dict__** attribute)
containing the fields `expected`, `output`, and `passed`; where `passed` is a
boolean indicating whether the check passed of failed.

#### Example

Here we define a method that verifies the type of output. If the type matches
the expected value the check passes.

- `./checks.py`
```python
from typing import Any


def check_type(
  output: Any,
  expected: str,
) -> dict:
  passed = expected == type(output).__name__
  return dict(
    output=output,
    expected=expected,
    passed=passed, )
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
- method: check_type
  expected: str
  field: null
  resource: ./checks.py
  cast_output:
  - method: __builtins__.str
    resource: ./resource.py
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
- method: __builtins__.str  # Cast arguments as a string
  field: null
  unpack: false
  resource: ./resource.py
- method: SimpleNamespace  # Cast an output field as a SimpleNamespace
  field: field.key
  unpack: true
  resource: ./resource.py

cast_output:
- method: do_nothing  # Call a casting method
  field: null
  unpack: false
  resource: ./resource.py
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
| route | str | The dot-delimited route to the object we wish to patch, in the module to test | null |
| callable_route | str | Dot-delimited route to a function if the patch method is `callable` | '' |
| resource | str | Location of a module containing a resource to use during testing | '' |


```yaml
patches:
# Value patch
- method: value
  value: 1
  route: num_a
  resource: ./resource.py
# Callable patch
- method: callable
  callable_route: hello_world
  resource: ./resource.py
```


## Environment

For modules containing a global variable `CONFIG`, we can perform tests using different environment variables by the variables as adding key/value pairs under the key `environment` in YAML files. The environment variables are accessible from `CONFIG.environment.[route]`, where `[route]` is the dot-delimited route to the variable within the module.

### Example

```yaml
environment:
  NAME_A: a
  NAME_C: c
  

tests:
- environment:
    NAME_A: A
    NAME_B: b
```


## Spies

We can spy on methods to verify that methods are called when the function being tested is executed. To do this we list the dot delimited routes to the methods to spy on under the key `spies` in YAML test files. Spies can be defined at the global, configuration, and test levels; and are combined into one. Spies are saved to the attribute `spies_` in the module of the function being tests, and are accessible from an check method.

### Example

In this example, the methods to spy on are listed under the `spies` key at the individual test level, and an check method to verify spies is defined as a function.

- `./app_test.py`
```yaml
resources:
- &CHECKS
  resource: ./checks.py


spies:
- method_a


tests:
- spies:
  - method_b
  checks:
  - method: check_spies
    << : *CHECKS
    expected:
      method_a:
        called: True
        called_with: []
      method_b:
        called: False
        called_with: None
```

- `./checks.py`
```python
def check_spies(
  spies_: dict,
  expected: dict,
) -> sns:
  spies = {}
  for key, value for expected.items():
    spy = spies_.get(key, {})
      if spy != value
        continue
    spies[key] = spy
  passed = expected == spies
  return dict(
    output=spies,
    expected=expected,
    passed=passed, )
```


## Setup

We can setup (create) or teardown (destroy) resources to use during tests. These
resources can be defined as a list of objects under the `setup` key in YAML test
files or under configurations options. The resources are created at the start of
the different phases.

### Schema

A single setup object has the following fields:

| Field | Type | Description | Default |
| - | - | - | - |
| name | str | The name of the resource | null |
| phase | Any | The phase the resource should be created before and destroyed after | null
| method | str | The method to call to setup or teardown the resource | null |
| arguments | dict | Arguments to pass to the method | {} |
| unpack | bool | Indicates whether arguments should be unpacked or packed when passed to method | false |
| timeout | int | Number of seconds to keep the resource alive for:<br>- `-1` to keep the process running<br>- `0` to get immediate value from resource<br>- Any other integer to keep process| 0 |

### Example

In this example, we define a setup resource for the module phase. The resource stays alive during the phase, or for all of the tests for the module. The method, `run_server`, starts an api; and we have define a method and check to verify the response from the api.

- `./checks.py`
```python
def check_equals(
  output: str,
  expected: str,
) -> dict:
  passed = output == expected
  return dict(
    passed=passed,
    output=output,
    expected=expected, )
```

- `./app.py`
```python
import requests


def get_json_response(url: str) -> str:
  return requests.get(url).json()
```

- `./app_test.py`
```yaml
resources:
- &CHECKS
  resource: ./checks.py
- &RESOURCE
  resource: ./resource.py
- &URL
  url: localhost:1234/hello_world


setup:
- name: api
  phase: module
  << : *RESOURCE
  method: run_server
  arguments:
    << : *URL
  unpack: true
  timeout: -1


tests:
- function: get_json_response
  arguments:
    << : *URL
  checks:
  - method: check_equals
    << : *CHECKS
    expected: '{"hello": "world"}'
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
