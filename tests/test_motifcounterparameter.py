"""
Ensures the functionality of PyMotifCounterParameter.


:author: Athanasios nastasiou
:date: Nov 2021
"""
import pytest
import re
from pymotifcounter.abstractcounter import PyMotifCounterParameter


def test_init():
    """
    Instantiation should raise an exception if parameter is required but does not have a default value
    :return:
    """
    # TODO: LOW, Exchange the xception for the right one here.
    with pytest.raises(Exception):
        p = PyMotifCounterParameter(name="s", alias="Size", default_value=None, is_required=True)


def test_validation_fail():
    with pytest.raises(Exception):
        p = PyMotifCounterParameter(name="s",
                                    alias="Size",
                                    validation_expr=re.compile("[0-9]+"),
                                    default_value="FAIL", is_required=True)


def test_validation_pass():
    p = PyMotifCounterParameter(name="s",
                                alias="Size",
                                validation_expr=re.compile("[0-9]+"),
                                default_value=22, is_required=True)
    assert p._validate() is True


def test_repr_flag_notflag():
    p_is_flag = PyMotifCounterParameter(name="s",
                                        alias="Size",
                                        is_flag=True)

    p_is_not_flag = PyMotifCounterParameter(name="s",
                                            alias="Size",
                                            validation_expr=re.compile("[0-9]+"),
                                            default_value=22,
                                            is_flag=False)

    assert p_is_flag.__repr__() == ["-s"]
    assert p_is_not_flag.__repr__() == ["-s", "22"]


def test_set_invalid_value():
    p = PyMotifCounterParameter(name="s",
                                alias="Size",
                                validation_expr=re.compile("[0-9]+"),
                                default_value=22,
                                is_flag=False)

    with pytest.raises(Exception):
        p._set_value("Wrong")
