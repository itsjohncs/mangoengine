# internal
import errors

class Field(object):
    """
    A basic field. Can be inherited from.

    :ivar nullable: If False, the value of this field cannot be None.

    """

    _expected_type = None
    """
    The expected type of the field. Used internally by MangoEngine and can be
    leveraged when creating your own fields.

    """

    def __init__(self, nullable = False):
        self.nullable = nullable

    def validate(self, value):
        # Ensure that if the value is None, it's OK
        if not self.nullable and value is None:
            raise errors.ValidationFailure("value cannot be None.")

        # Ensure the that value is the corect type
        if (value is not None and
                self._expected_type is not None and
                not isinstance(value, self._expected_type)):
            raise errors.ValidationFailure(
                "Expecting %s, got %s." % (
                   self. _expected_type.__name__,
                    type(value).__name__
                )
            )

class StringField(Field):
    """
    A string field.

    """

    _expected_type = basestring

    def __init__(self, **default_kwargs):
        super(StringField, self).__init__(**default_kwargs)

    def validate(self, value):
        super(StringField, self).validate(value)

class DictField(Field):
    """
    A dictionary or map.

    :ivar of_key: A the type of field that every key must be. Example, if this
            is a StringField, all keys in the dictionary must be strings.
    :ivar of_value: Similar to of_key but affecting the values.

    """

    _expected_type = dict

    def __init__(self, of_key = None, of_value = None, **default_kwargs):
        self.of_key = of_key
        self.of_value = of_value
        super(DictField, self).__init__(**default_kwargs)

    def validate(self, value):
        if value is not None and self.of_key is not None:
            for k in value.keys():
                self.of_key.validate(k)
        if value is not None and self.of_value is not None:
            for v in value.values():
                self.of_value.validate(v)

        super(DictField, self).validate(value)

class ListField(Field):
    """
    A list.

    :ivar of: The type of field that each list item must be. For example, if
            StringField is given, all list items must be strings.

    """

    _expected_type = list

    def __init__(self, of = None, **default_kwargs):
        self.of = of
        super(ListField, self).__init__(**default_kwargs)

    def validate(self, value):
        if self.of is not None:
            for i in value:
                self.of.validate(i)

        super(ListField, self).validate(value)
