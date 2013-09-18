# internal
import errors

class Field(object):
    _expected_type = None

    def __init__(self, nullable = False):
        self.nullable = nullable

    def validate(self, value):
        if not self.nullable and value is None:
            raise errors.ValidationFailure("value cannot be None.")

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
    _expected_type = basestring

    def __init__(self, **default_kwargs):
        super(StringField, self).__init__(**default_kwargs)

    def validate(self, value):
        super(StringField, self).validate(value)

class DictField(Field):
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
    _expected_type = list

    def __init__(self, of = None, **default_kwargs):
        self.of = of
        super(ListField, self).__init__(**default_kwargs)

    def validate(self, value):
        if self.of is not None:
            for i in value:
                self.of.validate(i)

        super(ListField, self).validate(value)
