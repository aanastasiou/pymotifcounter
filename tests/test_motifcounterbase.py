"""
Ensures the functionality of PyMotifCounterBase.

:author: Athanasios Anastasiou
:date: Nov 2021
"""
import pytest
import re
from pymotifcounter.abstractcounter import PyMotifCounterBase, PyMotifCounterParameter


def test_init():
    """
    Tests the initialisation of a plain PyMotifCounter.
    """
    with pytest.raises(Exception):
        bn = PyMotifCounterBase()

def test_set_duplicate_param():
    p1 = PyMotifCounterParameter("s", "Size", is_flag=True)
    p2 = PyMotifCounterParameter("q", "Size", validation_expr=re.compile("[0-9]+"), default_value=22)
    b = PyMotifCounterBase(binary_location="/bin/bash")
    b.add_parameter(p1)
    with pytest.raises(Exception):
        b.add_parameter(p2)




