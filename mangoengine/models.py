# mongoengine
from .fields import Field
from .errors import UnknownAttribute

class ModelMetaclass(type):
    """
    A simple metaclass responsible for setting up Model classes appropriately.

    The created class will have a ``_fields`` class variable that contains a
    dictionary mapping field names to instances of Field. For example...

    .. code-block:: python

        >>> class Foo(Model):
        ...     a = StringField()
        ...     b = ListField()
        ...     unrelated = "string"
        ...
        >>> Foo._fields
        {'a': <mangoengine.fields.StringField object at 0x7fc8db7bb210>,
        'b': <mangoengine.fields.ListField object at 0x7fc8db7bb990>}

    Further, the original class variables that define fields are not preserved,
    but any other class variables are. Continuing from above...

    .. code-block:: python

        >>> Foo.a
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AttributeError: type object 'Foo' has no attribute 'a'
        >>> Foo.unrelated
        'string'

    .. note::

        For a fantastic overview of metaclasses, see
        http://stackoverflow.com/a/6581949/1989056.

    """

    def __new__(cls, clsname, bases, dct):
        # These will be any attributes that define a field
        field_definitions = {}

        # These will be any other attributes (unrelated attributes that we
        # don't want to touch)
        attributes = {}

        # Inherit any fields from our base classes. We go right to left in
        # order to give fields on the left higher precedence in the case of
        # name conflicts.
        for i in reversed(bases):
            # Check if the current base class is a Model
            if getattr(i, "__metaclass__", None) is ModelMetaclass:
                field_definitions.update(i._fields)

        for k, v in dct.items():
            # If this attribute defines a field...
            if isinstance(v, Field):
                # Set the name attribute of the field, this allows for better
                # error messages.
                v.name = k

                field_definitions[k] = v
            else:
                attributes[k] = v

        attributes["_fields"] = field_definitions

        return type.__new__(cls, clsname, bases, attributes)

class BaseModel(object):
    """
    Base class of both DictModel and Model. Do not inherit directly from this
    class from outside of Mango Engine's internal code.

    """

    def _set_value(self, k, v):
        """Called internally to set the value of a field."""

        raise NotImplemented()

    def _get_value(self, k):
        """Called internally to get the value of a field."""

        raise NotImplemented()

    def _has_value(self, k):
        raise NotImplemented()

    def __init__(self):
        for k in self._fields.keys():
            if not self._has_value(k):
                self._set_value(k, None)

        super(BaseModel, self).__init__()

    def __repr__(self):
        arg_list = ((k, self._get_value(k)) for k in self._fields.keys())
        args = ", ".join("%s = %s" % (k, repr(v)) for k, v in arg_list)
        return "%s(%s)" % (type(self).__name__, args)

    def validate(self):
        """
        Validates the object to ensure each field has an appropriate value. A
        :class:`mangoengine.ValidationFailure` will be thrown if validation
        fails.

        :returns: ``None``

        """

        for k, v in self._fields.items():
            v.validate(self._get_value(k))

    def to_dict(self):
        """Tranforms the current object into a dictionary representation."""

        return vars(self)

    def assign(self, dictionary, allow_unknown_data = None):
        # Default to the class attribute if the user didn't specify a value
        if allow_unknown_data is None:
            allow_unknown_data = getattr(self, "_allow_unknown_data", True)

        # We're just going to directly plug the values in.
        for k, v in dictionary.items():
            if k not in self._fields and not allow_unknown_data:
                raise UnknownAttribute(k)

            self._set_value(k, v)

class Model(BaseModel):
    """
    Derive from this class to make your own models.

    :cvar _fields: A dictionary mapping any field names to their
        :class:`mangoengine.Field` instances.
    :cvar _allow_unknown_data: Sets the default value for the
        ``allow_unknown_data`` parameter in :meth:`.validate()`.

    .. code-block:: python

        >>> class Person(Model):
        ...     name = StringField()
        ...     unrelated = 3
        ...
        >>> Person.name
        Traceback (most recent call last):
          File "<stdin>", line 1, in <module>
        AttributeError: type object 'Person' has no attribute 'name'
        >>> Person.unrelated
        3
        >>> Person._fields
        {'name': <mangoengine.fields.StringField object at 0x2200d50>}
        >>> person = Person(name = "John")
        >>> person
        Person(name = 'John')

    .. note::

        The magic handling of the class attributes is made possible through the
        :class:`mangoengine.models.ModelMetaclass` metaclass.

    """

    __metaclass__ = ModelMetaclass

    def _set_value(self, k, v):
        return setattr(self, k, v)

    def _get_value(self, k):
        return getattr(self, k)

    def _has_value(self, k):
        return hasattr(self, k)

    def __init__(self, **kwargs):
        for k in kwargs.keys():
            if k not in self._fields:
                raise TypeError(
                    "'%s' is an invalid keyword argument for this "
                    "function." % (k, )
                )

        self.assign(kwargs)

        super(Model, self).__init__()

    @classmethod
    def from_dict(cls, dictionary, allow_unknown_data = None):
        """
        Creates a new instance of the model from the given dictionary.

        .. note::

            Validation is not performed. Make sure to call validate()
            afterwards if validation is desired.

        :param dictionary: The dictionary to pull the values from.
        :param allow_unknown_data: If True, when an unknown attribute is found
            the validation will fail. Uses the value of
            ``self._allow_unknown_data`` if ``None`` is specified, or ``True``
            if no such attribute exists.

        """

        instance = cls()
        instance.assign(dictionary, allow_unknown_data)

        return instance
