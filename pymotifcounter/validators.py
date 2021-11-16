"""
Stock lambda functions for performing standard pieces of parameter validation

:author: Athanasios Anastasiou
:date: Nov 2021
"""

import os


def path_exists():
    return lambda x: "OK" if os.path.exists(x) else f"{x} does not exist"


def validates_always():
    return lambda x: True


def is_le(a):
    return lambda x: "OK" if x <= a else f"{x} is not less or equal than {a}"


def is_l(a):
    return lambda x: "OK" if x < a else f"{x} is not less than {a}"


def is_g(a):
    return lambda x: "OK" if x > a else f"{x} is not greater than {a}"


def is_ge(a):
    return lambda x: "OK" if x >= a else f"{x} is not greater equal than {a}"


def is_eq(a):
    return lambda x: "OK" if x == a else f"{x} is not equal to {a}"


def within_range(a):
    return lambda x: "OK" if x in a else f"{x} not one of {a}"


def of_type(a):
    return lambda x: "OK" if type(x) is a else f"type of {x} is not {a}"