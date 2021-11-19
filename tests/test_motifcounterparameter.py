"""
Ensures the functionality of PyMotifCounterParameter.


:author: Athanasios Anastasiou
:date: Nov 2021
"""
import pytest
from pymotifcounter.parameters import *


def test_init_required_without_default_value():
    """
    Ensures that required parameters set a default value.
    """
    with pytest.raises(PyMotifCounterParameterError):
        p = PyMotifCounterParameterInt(name="s",
                                       alias="Size",
                                       default_value=None,
                                       is_required=True)


def test_init_required_with_invalid_default_value_error():
    """
    Ensures that the default value conforms to the constraints.
    """
    with pytest.raises(PyMotifCounterParameterError):
        p = PyMotifCounterParameterInt(name="s",
                                       alias="Size",
                                       default_value="FAIL",
                                       is_required=True)


def test_set_invalid_value_error():
    """
    Ensures that parameter values are checked on entry.
    """
    p = PyMotifCounterParameterInt(name="s",
                                   alias="Size",
                                   default_value=22)

    with pytest.raises(PyMotifCounterParameterError):
        p.value = "Wrong"


def test_flag_output():
    """
    Ensures that a flag's output is only present when it is True and that only the paramter's name is returned.
    """

    p = PyMotifCounterParameterFlag("s",
                                    alias="size",
                                    default_value=True)

    assert p.get_parameter_form() == ["-s", ]


def test_non_flag_output():
    """
    Ensures that the default parameter's form is its name followed by a string representation of its value
    """
    p = PyMotifCounterParameterInt("s",
                                   alias="size",
                                   default_value=12)
    assert p.get_parameter_form() == ["-s", "12", ]


def test_file_path_exists():
    """
    Ensu that the filepath parameter can check the existence of its value.
    """
    p = PyMotifCounterParameterFilepath("f",
                                        alias="output_file",
                                        exists=True, )
    with pytest.raises(PyMotifCounterParameterError):
        p.value = "/ding/dong"


def test_validation_succesful():
    """
    Ensures parameters function as expected.
    """
    p = PyMotifCounterParameterInt(name="s",
                                   alias="Size",
                                   default_value=22,
                                   is_required=True)
    assert p.validate() is True
