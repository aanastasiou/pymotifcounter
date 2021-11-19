"""
Ensures the functionality of PyMotifCounterBase.

:author: Athanasios Anastasiou
:date: Nov 2021
"""
import pytest
import re
from pymotifcounter.abstractcounter import (PyMotifCounterBase,
                                            PyMotifCounterInputTransformerBase,
                                            PyMotifCounterOutputTransformerBase)

from pymotifcounter.parameters import (PyMotifCounterParameterInt,
                                       PyMotifCounterParameterStr,
                                       PyMotifCounterParameterFilepath)

from pymotifcounter.exceptions import PyMotifCounterError


def test_init_binary_is_invalid():
    """
    Tests the initialisation of a plain PyMotifCounter.

    :raises: PyMotifCounterError if the counter is initialised without pointing to a valid binary
    """
    with pytest.raises(PyMotifCounterError):
        bn = PyMotifCounterBase(binary_location="/some/path",
                                input_parameter=PyMotifCounterParameterFilepath("i", alias="test_input", ),
                                output_parameter=PyMotifCounterParameterFilepath("o", alias="test_output", ),
                                input_transformer=PyMotifCounterInputTransformerBase(),
                                output_transformer=PyMotifCounterOutputTransformerBase(),
                                parameters=[])


def test_set_duplicate_parameter_error():
    """
    Ensures that PyMotifCounterBase object does not allow overwriting of parameters
    """
    p1 = PyMotifCounterParameterStr("s", alias="Size",  default_value="ALPHA")
    p2 = PyMotifCounterParameterInt("q", alias="Size", default_value=22)
    p3 = PyMotifCounterParameterStr("m", alias="Method",  default_value="Gaussian")
    p4 = PyMotifCounterParameterInt("m", alias="MethaneLevel", default_value=22)

    b = PyMotifCounterBase(binary_location="/bin/bash",
                           input_parameter=PyMotifCounterParameterFilepath("i", alias="test_input",),
                           output_parameter=PyMotifCounterParameterFilepath("o", alias="test_output",),
                           input_transformer=PyMotifCounterInputTransformerBase(),
                           output_transformer=PyMotifCounterOutputTransformerBase(),
                           parameters=[p1, p3])

    # Test same alias, this should fail
    with pytest.raises(PyMotifCounterError):
        b.add_parameter(p2)

    # Test same name, this should fail
    with pytest.raises(PyMotifCounterError):
        b.add_parameter(p4)


def get_unknown_parameter_error():
    """
    Ensures that PyMotifCounterBase raises an error if an attempt is made to address an unknown parameter.
    """
    p1 = PyMotifCounterParameterStr("s", alias="Size", default_value="ALPHA")
    p3 = PyMotifCounterParameterStr("m", alias="Method", default_value="Gaussian")

    b = PyMotifCounterBase(binary_location="/bin/bash",
                           input_parameter=PyMotifCounterParameterFilepath("i", alias="test_input", ),
                           output_parameter=PyMotifCounterParameterFilepath("o", alias="test_output", ),
                           input_transformer=PyMotifCounterInputTransformerBase(),
                           output_transformer=PyMotifCounterOutputTransformerBase(),
                           parameters=[p1, p3])

    with pytest.raises(PyMotifCounterError):
        b.get_parameter("l")

