class ValidationFailure(RuntimeError):
    """
    Raised by MangoEngine when the value given for a particular field is not
    valid.

    :ivar field_name: The value of the field's ``name`` attribute.
    :ivar description: A description of the failure.

    """

    def __init__(self, field_name, description):
        self.field_name = field_name
        self.description = description

    def __str__(self):
        return "In field '%s': %s" % (self.field_name, self.description)
