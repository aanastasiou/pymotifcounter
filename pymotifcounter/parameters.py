"""
Defines classes for handling the inputs to underlying algorithms.

:author: Athanasios Anastasiou
:date: Nov 2021
"""

from .exceptions import *
from .validators import *


# TODO: MID, Check to see if the "directedness" of the algorithm could depend on the networkx.Graph at the input so that the parameter value is set automatically.
class PyMotifCounterParameterBase:
    """
    Represents a parameter that is used to pass data to an external program.

    Notes:
        * This class is not expected to be instantiated directly.
    """

    def __init__(self, name,
                 is_required,
                 default_value,
                 validation_callbacks,
                 alias=None,
                 help_str=None,
                 pos=None):
        """
        Initialises a raw parameter and performs some basic validation.

        :param name: The actual name of the parameter as it is expected by the binary (e.g. s, d, etc)
        :type name: str
        :param alias: An alternative name by which this parameter can also be known as.
        :type alias: str
        :param is_required: Whether this parameter should always have a valid value when calling a binary
        :type is_required: bool
        :param help_str: A short description of the parameter's use. Usually taken verbatim from the binary ``--help``
                         output.
        :type help_str: str
        :param pos: An integer denoting the position of a parameter. If this is set (i.e. not None and >0), it implies
                    that the parameter is positional.
        :type pos: int
        :param validation_callbacks: A tuple of unary functions that expresses the constraints for the parameter to be
                                     valid.
        :type validation_callbacks: tuple
        :param default_value: The default value for this parameter
        :type default_value: Any
        """

        self._value = None
        self._name = name
        self._alias = alias
        self._is_required = is_required
        self._help_str = help_str
        self._validation_callbacks = validation_callbacks
        self._default_value = default_value
        self._pos = pos

        if self._is_required and self._default_value is None:
            raise PyMotifCounterParameterError(f"Required parameter {self._name} / {self._alias} must specify "
                                               f"valid default value.")

        if self._is_required:
            try:
                self._check_value(self._default_value)
            except PyMotifCounterParameterError:
                raise PyMotifCounterParameterError(f"Required parameter {self._name} / {self._alias} must specify "
                                                   f"valid default value.")
        self.validate()

    @property
    def pos(self):
        return (self._pos or 65535) if self._pos is None else self._pos

    @property
    def default_value(self):
        return self._default_value

    @default_value.setter
    def default_value(self, new_value):
        if self._check_value(new_value):
            self._default_value=new_value

    @property
    def value(self):
        return self._value or self._default_value

    @value.setter
    def value(self, a_value):
        if self._check_value(a_value):
            self._value = a_value

    def _human_readable_form(self):
        """
        Returns a dictionary with human readable forms for the semantics of each parameter.

        :returns: A dictionary that maps a "parameter logical name" to a tuple
                  ("Human readable string", "value str to depict", optional integer ordering).
                  This information is then used by the ``__str__()`` of the same object to create the human
                  readable form that can be presented to users.
        :rtype: dict(str:tuple(str,str,[int]))
        """
        try:
            self.validate()
            valid_part = "Valid"
        except PyMotifCounterParameterError as e:
            valid_part = "Invalid"

        name_alias_part = f"{self._name}{('/' + str(self._alias)) if self._alias else ''}"
        req_part = "Mandatory" if self._is_required else "Optional"
        help_str_part = f"{self._help_str}" if self._help_str else ""
        current_value_part = str(self.value)
        default_value_part = str(self._default_value)
        return {"validation_state": ("Validation state  :", valid_part, 5),
                "name_alias": ("Name/Alias:      :", name_alias_part, 0),
                "required_state": ("Required          :", req_part, 2),
                "help_string": ("Help String       :", help_str_part, 1),
                "current_value": ("Current value     :", current_value_part, 4),
                "default_value": ("Default value     :", default_value_part, 3),
                }

    def __str__(self):
        """
        Constructs and returns a human readable string form for all the data that define a parameter.

        Notes:
            * This is a generic human readable form function that "renders" the information it obtains from
              ``_human_readable_form()``.
            * Parameter types that may have added more data that define the parameter are expected to override
              ``_human_readable_form()`` and enrich its returned dict, rather than modify this generic code of
              rendering that same information.

        :returns: A string that is formatted as name/alias followed by an indented list of ordered data followed
                  by the list of unordered data about the parameter.
        :rtype: str
        """
        param_data = self._human_readable_form()
        # Split param labels in two subsets based on whether they need to appear ordered or not
        params_with_ordering = "\n\t".join(list(map(lambda x: f"{x[1][0]}{x[1][1]}",
                                                    sorted(filter(lambda x: len(x[1]) > 2 and type(x[1][2]) is int and
                                                                            x[0] != "name_alias",
                                                                  param_data.items()),
                                                           key=lambda x:x[1][2]))))

        params_without_ordering = "\n\t".join(list(map(lambda x: f"{x[1][0]}{x[1][1]}",
                                                       filter(lambda x: len(x[1]) <= 2,
                                                              param_data.items()))))

        # Name / alias is included regardless of ordering
        str_label = f"{param_data['name_alias'][1]}\n\t" + \
                    params_with_ordering + "\n\t" + \
                    params_without_ordering

        return str_label

    def _check_value(self, a_value):
        """
        Checks that the current parameter value is valid for this parameter's use context.

        :param a_value: The value to check for validity
        :type a_value: Any
        :returns: True
        :rtype: bool
        :raises: PyMotifCounterParameterError
        """

        if a_value is None and self._is_required:
            raise PyMotifCounterParameterError(f"Parameter {self._name} / {self._alias} is required.")

        for a_callback in self._validation_callbacks:
            valid_status = a_callback(a_value)
            if valid_status != "OK":
                raise PyMotifCounterParameterError(f"Parameter {self._name} / {self._alias} invalid:{valid_status}")
        return True

    def validate(self):
        """
        Ensures that the parameter conforms to its specification
        """
        return self._check_value(self.value)

    def get_parameter_form(self):
        """
        Returns the parameter in the right representation expected by ``subprocess.popen``

        :return: An ``n`` element list depending on the parameter type.
        :rtype: list
        """
        if self._pos is not None:
            return [str(self.value), ]
        else:
            return [f"-{self._name}", str(self.value)]


class PyMotifCounterParameterFlag(PyMotifCounterParameterBase):
    """
    Defines a flag type parameter.

    Notes:
        * Beyond establishing its value as bool, a flag's parameter name only
          appears in the command line if it is True.
    """
    def __init__(self, name,
                 is_required=True,
                 default_value=True,
                 alias=None,
                 help_str=None,
                 pos=None):
        super().__init__(name, is_required, default_value, (of_type(bool), ), alias=alias, help_str=help_str, pos=pos)

    def get_parameter_form(self):
        if self._value or self._default_value:
            return [f"-{self._name}", ]
        else:
            return []

    def _human_readable_form(self):
        """
        Adds the ``is_flag`` information to the human readable form dict of data.

        """
        hrf = super()._human_readable_form()
        hrf.update({"is_flag": ("Is flag           :", "Yes")})
        return hrf


class PyMotifCounterParameterInt(PyMotifCounterParameterBase):
    """
    Defines an integer parameter.

    Notes:
        * The actual range of the integer can be further customised with
          ``is_g, is_ge, is_l, is_le`` validator callbacks.
    """
    def __init__(self, name,
                 is_required=True,
                 default_value=0,
                 validation_callbacks=(),
                 alias=None,
                 help_str=None,
                 pos=None):
        validators = (of_type(int),) + validation_callbacks
        super().__init__(name, is_required, default_value, validators, alias=alias, help_str=help_str, pos=pos)


class PyMotifCounterParameterReal(PyMotifCounterParameterBase):
    """
    Defines a Real parameter.

    Notes:
        * The actual range of the real can be further customised with ``is_g, is_ge, is_l, is_le`` validator callbacks.
        * The data type for this is assumed to be **float**.
    """
    def __init__(self, name,
                 is_required=True,
                 default_value=0.0,
                 validation_callbacks=(),
                 alias=None,
                 help_str=None,
                 pos=None):
        validators = (of_type(float),) + validation_callbacks
        super().__init__(name, is_required, default_value, validators, alias=alias, help_str=help_str, pos=pos)


class PyMotifCounterParameterStr(PyMotifCounterParameterBase):
    """
    Defines a string parameter.

    Notes:
        * Further structural properties of the string can be customised with ``is_eq, within_range`` validator
          callbacks.
    """
    def __init__(self, name,
                 is_required=True,
                 default_value="",
                 validation_callbacks=(),
                 alias=None,
                 help_str=None,
                 pos=None):
        validators = (of_type(str),) + validation_callbacks
        super().__init__(name, is_required, default_value, validators, alias=alias, help_str=help_str, pos=pos)


class PyMotifCounterParameterFilepath(PyMotifCounterParameterBase):
    """
    Defines a file-path parameter

    Notes:
        * This is the primary class by which PyMotifCounter I/O parameters are defined
        * If an input parameter is stdin then set its default_value to "-"
    """
    def __init__(self, name,
                 is_required=True,
                 default_value="",
                 exists=False,
                 validation_callbacks=(),
                 alias=None,
                 help_str=None,
                 pos=None):
        """
        Initialises a filepath parameter.

        Notes:
            * For all parameters except ``exists`` see the documentation of ``PyMotifCounterParameterBase``.

        :exists: Whether the file path must point to an existing file
        :type exists: bool
        """
        validators = (of_type(str),) + validation_callbacks
        super().__init__(name, is_required, default_value, validators, alias=alias, help_str=help_str, pos=pos)

        if exists:
            self._validation_callbacks = self._validation_callbacks + (path_exists(), )
