# internal
import errors

class Field(object):
    """
    The base Field class. Should be inherited from and not used directly.

    :ivar name: The name of the field in the model. For example, if the model
        defines a field ``hair_color`` as a :class:`.StringField`, that :class:`.StringField`'s
        ``name`` should be set to ``"hair_color"``.
    :ivar nullable: If False, the value of this field may not be None.

    """

    _expected_type = None
    """
    The expected type of the field's value. Should always be set in new fields.
    Will be tested using ``isinstance()`` so any type that derives from this
    type will also be accepted.

    If set to None type checking will not be performed during validation.

    """

    def __init__(self, nullable = False):
        self.name = "unknown"
        self.nullable = nullable

    def validate(self, value):
        # Check if the value is None
        if not self.nullable and value is None:
            raise errors.ValidationFailure(self.name, "value cannot be None.")

        # If we should perform type checking
        if value is not None and self._expected_type is not None:
            # Ensure the type of value is correct
            if not isinstance(value, self._expected_type):
                # Build a human readable string for the type(s)
                if type(self._expected_type) in (list, tuple):
                    type_string_list = ", ".join(
                        i.__name__ for i in self._expected_type)
                    type_string = "(one of %s)" % (type_string_list, )
                else:
                    type_string = self._expected_type.__name__

                raise errors.ValidationFailure(self.name,
                    "expected type %s, got %s." % (
                        type_string,
                        type(value).__name__
                    )
                )

class StringField(Field):
    """A string field. Only values of type ``str`` are accepted."""

    _expected_type = str

    def __init__(self, **default_kwargs):
        super(StringField, self).__init__(**default_kwargs)

class UnicodeField(Field):
    """A unicode string field. Only values of type ``unicode`` are accepted."""

    _expected_type = unicode

    def __init__(self, **default_kwargs):
        super(UnicodeField, self).__init__(**default_kwargs)

class NumericField(Field):
    """
    A numeric field. Only types of int, long, and double are accepted.

    :ivar bounds: A two-tuple containing a lower and upper inclusive bound.

    """

    _expected_type = (int, long, float)

    def __init__(self, bounds = (None, None), **default_kwargs):
        self.bounds = bounds

        super(NumericField, self).__init__(**default_kwargs)

    def validate(self, value):
        if (self.bounds[0] is not None and value < self.bounds[0]) or \
                (self.bounds[1] is not None and value > self.bounds[1]):
            raise errors.ValidationFailure(
                self.name,
                "%s is out of bounds of %s." % (
                    repr(value), repr(self.bounds))
            )

        super(NumericField, self).validate(value)

class IntegralField(NumericField):
    """
    An integral field. Only types of int and long are accepted.

    :ivar bounds: A two-tuple containing a lower and upper inclusive bound.

    """

    _expected_type = (int, long)

    def __init__(self, bounds = (None, None), **default_kwargs):
        super(IntegralField, self).__init__(bounds, **default_kwargs)

class DictField(Field):
    """
    A dictionary field. Only values of type ``dict`` are accepted.

    :ivar of_key: The type of field that every key must be. Example, if this
        is a :class:`.StringField`, all keys in the dictionary must be strings.
    :ivar of_value: Similar to ``of_key`` but affecting the values.

    """

    _expected_type = dict

    def __init__(self, of_key = None, of_value = None, **default_kwargs):
        self.of_key = of_key
        self.of_value = of_value
        super(DictField, self).__init__(**default_kwargs)

    def validate(self, value):
        # Validate all of the keys
        if value is not None and self.of_key is not None:
            for k in value.keys():
                self.of_key.validate(k)

        # Validate all of the values
        if value is not None and self.of_value is not None:
            for v in value.values():
                self.of_value.validate(v)

        super(DictField, self).validate(value)

class ListField(Field):
    """
    A list field. Only values of type ``list`` are accepted.

    :ivar of: The type of field that each list item must be. For example, if
        a :class:`.StringField` is given, all list items must be strings.

    """

    _expected_type = list

    def __init__(self, of = None, **default_kwargs):
        self.of = of

        super(ListField, self).__init__(**default_kwargs)

    def validate(self, value):
        # Validate all of the list items
        if value is not None and self.of is not None:
            for i in value:
                self.of.validate(i)

        super(ListField, self).validate(value)

class ModelField(Field):
    """
    A field that can wrap any Model class.

    :ivar model: The type of Model it accepts.

    """

    def __init__(self, model, **default_kwargs):
        self._expected_type = self.model = model

        super(ModelField, self).__init__(**default_kwargs)

    def validate(self, value):
        # We perform our base class's validation first so it can do type
        # checking before we try and call .validate() on the value.
        super(ModelField, self).validate(value)

        value.validate()

