"""
Ensures the functionality of PyMotifCounterBase.

:author: Athanasios Anastasiou
:date: Nov 2021
"""
import pytest
import re
from pymotifcounter.abstractcounter import PyMotifCounterBase, PyMotifCounterParameter
from pymotifcounter.exceptions import PyMotifCounterError


def test_init_no_binary_location_error():
    """
    Tests the initialisation of a plain PyMotifCounter.

    :raises: PyMotifCounterError if the counter is initialised without pointing to a valid binary
    """
    with pytest.raises(PyMotifCounterError):
        bn = PyMotifCounterBase()


def test_set_duplicate_parameter_error():
    p1 = PyMotifCounterParameter("s", "Size", validation_expr=re.compile("[A-Z]+"), default_value="ALPHA")
    p2 = PyMotifCounterParameter("q", "Size", validation_expr=re.compile("[0-9]+"), default_value=22)

    b = PyMotifCounterBase(binary_location="/bin/bash")
    b.add_parameter(p1)
    with pytest.raises(PyMotifCounterError):
        b.add_parameter(p2)


def get_unknown_parameter_error():
    b = PyMotifCounterBase(binary_location="/bin/bash")

    with pytest.raises(PyMotifCounterError):
        b.get_parameter_value("s")


def set_unknown_parameter_error():
    b = PyMotifCounterBase(binary_location="/bin/bash")

    with pytest.raises(PyMotifCounterError):
        b.set_parameter_value("s", 55)


def set_value_succesfully():
    p1 = PyMotifCounterParameter("s", "Size", validation_expr=re.compile("[0-9]+"), default_value=22)

    # Ignore that it points to /bin/bash here, this is just for testing purposes.
    b = PyMotifCounterBase(binary_location="/bin/bash")
    b.add_parameter(p1)

    b.set_parameter_value("s",150)

    assert b.get_parameter_value("s") == 150

