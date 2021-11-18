import tempfile
from .exceptions import *
from .validators import *


# TODO: MID, Check to see if the "directedness" of the algorithm could depend on the networkx.Graph at the input so that the parameter value is set automatically.
class PyMotifCounterParameterBase:
    """
    Represents a parameter that is used to pass data to an external program.
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

        :param name: The name of the parameter as it is expected by the binary (e.g. -s, --directed, etc)
        :type name: str
        :param alias: An alternative name by which this parameter can also be known as.
        :type alias: str
        :param is_required: Whether this parameter should always be present when calling a binary
        :type is_required: bool
        :param help_str: A short description of the parameter's use. Usually taken verbatim from the binary ``--help``
                         output.
        :type help_str: str
        :param pos: An integer denoting the position of a parameter. If this is set (i.e. not None and >0), it implies
                    that the parameter is positional.
        :type pos: int
        :param validation_callbacks: A regexp validation expression that describes the set of valid values for the parameter.
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
    def value(self):
        return self._value or self._default_value

    @value.setter
    def value(self, a_value):
        if self._check_value(a_value):
            self._value = a_value

    def is_set(self):
        return self._value is not None

    def __str__(self):
        try:
            self.validate()
            valid_part = ""
        except PyMotifCounterParameterError as e:
            valid_part = "INVALID"

        req_part = "MANDATORY" if self._is_required else "OPTIONAL"
        help_str_part = f"{self._help_str[0:15]}..." if self._help_str else ""
        str_label = f"{self._name} / {self._alias} -{help_str_part}- " \
                    f"({req_part}, DEFAULT:{self._default_value}, " \
                    f"{str(self._value)}:{valid_part}"
        return str_label

    def _check_value(self, a_value):
        """
        Checks that the current parameter value is valid for this parameter's use context.

        :param a_value: The value to check for validity
        :type a_value: Any
        :returns: True
        :rtype: bool
        :raises: Validation exception

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


class PyMotifCounterParameterInt(PyMotifCounterParameterBase):
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
    def __init__(self, name,
                 is_required=True,
                 default_value=0.0,
                 validation_callbacks=[],
                 alias=None,
                 help_str=None,
                 pos=None):
        validators = (of_type(float),) + validation_callbacks
        super().__init__(name, is_required, default_value, validators, alias=alias, help_str=help_str, pos=pos)


class PyMotifCounterParameterStr(PyMotifCounterParameterBase):
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
    def __init__(self, name,
                 is_required=True,
                 default_value="",
                 exists=False,
                 validation_callbacks=(),
                 alias=None,
                 help_str=None,
                 pos=None):
        validators = (of_type(str),) + validation_callbacks
        super().__init__(name, is_required, default_value, validators, alias=alias, help_str=help_str, pos=pos)

        if exists:
            self._validation_callbacks = self._validation_callbacks + (path_exists(), )