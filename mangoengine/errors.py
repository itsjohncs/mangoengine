class ValidationFailure(RuntimeError):
    """
    Raised by :meth:`Model.validate()` when the value given for a particular
    field is not valid.

    :ivar field_name: The value of the field's ``name`` attribute.
    :ivar description: A description of the failure.

    """

    def __init__(self, field_name, description):
        self.field_name = field_name
        self.description = description

    def __str__(self):
        return "In field '%s': %s" % (self.field_name, self.description)

class UnknownAttribute(ValidationFailure):
    """
    Raised by :meth:`Model.validate()` when ``allow_unknown_data`` is ``False``
    and an unknown attribute is encountered.

    Inherits from :class:`.ValidationFailure`.

    """

    def __init__(self, attribute_name):
        self.attribute_name = attribute_name

    def __str__(self):
        return "Unknown attribute '%s'." % (self.attribute_name, )
