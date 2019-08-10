# -*- coding: utf-8 -*-

import pytest
from drc_fosa_geolocalisation.skeleton import fib

__author__ = "Grégoire Lurton"
__copyright__ = "Grégoire Lurton"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
