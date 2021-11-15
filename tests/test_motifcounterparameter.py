"""
Ensures the functionality of PyMotifCounterParameter.


:author: Athanasios nastasiou
:date: Nov 2021
"""
import pytest
import re
from pymotifcounter.abstractcounter import PyMotifCounterParameterBase
from pymotifcounter.exceptions import PyMotifCounterParameterError


def test_init_required_without_validation_rule_error():
    with pytest.raises(PyMotifCounterParameterError):
        p = PyMotifCounterParameterBase(name="s",
                                    alias="Size")


# def test_init_required_without_default_value_or():
#     with pytest.raises(PyMotifCounterParameterError):
#         p = PyMotifCounterParameterBase(name="s",
#                                     alias="Size",
#                                     validation_callback=re.compile("[0-9]+"),
#                                     default_value=None,
#                                     is_required=True)


# def test_init_required_with_invalid_default_value_error():
#     with pytest.raises(PyMotifCounterParameterError):
#         p = PyMotifCounterParameterBase(name="s", alias="Size",
#                                     validation_callback=re.compile("[0-9]+"),
#                                     default_value="FAIL",
#                                     is_required=True)


# def test_repr_flag_notflag_error():
#     p_is_flag = PyMotifCounterParameterBase(name="s",
#                                         alias="Size",
#                                         is_flag=True)
#
#     p_is_not_flag = PyMotifCounterParameterBase(name="s",
#                                             alias="Size",
#                                             validation_callback=re.compile("[0-9]+"),
#                                             default_value=22,
#                                             is_flag=False)
#
#     assert p_is_flag.get_parameter_form() == ["-s"]
#     assert p_is_not_flag.get_parameter_form() == ["-s", "22"]


# def test_set_invalid_value_error():
#     p = PyMotifCounterParameterBase(name="s",
#                                 alias="Size",
#                                 validation_callback=re.compile("[0-9]+"),
#                                 default_value=22)
#
#     with pytest.raises(PyMotifCounterParameterError):
#         p.set_value("Wrong")
#
#
# def test_validation_succesful():
#     p = PyMotifCounterParameterBase(name="s",
#                                 alias="Size",
#                                 validation_callback=re.compile("[0-9]+"),
#                                 default_value=22,
#                                 is_required=True)
#     assert p.validate() is True
