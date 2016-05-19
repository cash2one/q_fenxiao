#encoding:utf-8
__author__ = 'binpo'
import pytest
def f():
    raise SystemExit(1)

def test_mytest():
    with pytest.raises(SystemExit):
        f()

