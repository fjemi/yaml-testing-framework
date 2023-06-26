#!/usr/bin/env python3

import pytest

from app.main import Test

_ = Test


def pytest_configure(config) -> None:
  pytest.yml_tests = []
