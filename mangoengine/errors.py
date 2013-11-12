class ValidationFailure(RuntimeError):
    """
    Occurs when the value given for a particular field is not valid.

    For example, if the integer value 13 is given as the value for a
    StringField, a ValidationFailure will be raised when
    StringField.validate() is called.

    """

    def __init__(self, *args, **kwargs):
        RuntimeError.__init__(self, *args, **kwargs)
