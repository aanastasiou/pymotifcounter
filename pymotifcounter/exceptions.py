"""
PyMotifCounter specific exceptions.
    
:author: Athanasios Anastasiou
:date: Oct 2021
"""


class PyMotifCounterException(Exception):
    """
    Identifies a PyMotifCounter exception
    """
    pass


class PyMotifCounterParameterError(PyMotifCounterException):
    """
    Identifies errors related to parameters
    """
    pass


class PyMotifCounterError(PyMotifCounterException):
    """
    Identifies errors originating from PyMotifCounterBase
    """
    pass
