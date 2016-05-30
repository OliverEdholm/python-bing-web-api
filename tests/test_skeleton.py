#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from bing_search.skeleton import fib

__author__ = "Oliver Edholm"
__copyright__ = "Oliver Edholm"
__license__ = "none"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
