# -*- coding: utf-8 -*-

import pytest
from mina_telemetry.skeleton import fib

__author__ = "Francesco Risitano"
__copyright__ = "Francesco Risitano"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
