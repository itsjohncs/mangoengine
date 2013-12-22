# mongoengine
import fields

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

        for k, v in dct.items():
            # If this attribute defines a field...
            if isinstance(v, fields.Field):
                # Set the name attribute of the field, this allows for better
                # error messages.
                v.name = k

                field_definitions[k] = v
            else:
                attributes[k] = v

        attributes["_fields"] = field_definitions

        return type.__new__(cls, clsname, bases, attributes)

class Model(object):
    """
    Derive from this class to make your own models.

    .. code-block:: python

        >>> class Foo(Model):
        ...     a = StringField()
        ...     b = ListField()
        ...
        >>> f = Foo(a = 3)
        >>> f
        Foo(a = 3, b = None)
        >>> f.a
        3
        >>> f.b = 4
        >>> f
        Foo(a = 3, b = 4)
        >>> f.validate()
        [...]
        ValidationFailure: For field 'a': expecting str, got int.

    """

    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        for k in kwargs.keys():
            if k not in self._fields:
                raise TypeError(
                    "'%s' is an invalid keyword argument for this "
                    "function." % (k, )
                )

        for k, v in self._fields.items():
            setattr(self, k, kwargs.get(k, None))

    def __repr__(self):
        arg_list = ((k, getattr(self, k)) for k in self._fields.keys())
        args = ", ".join("%s = %s" % (k, repr(v)) for k, v in arg_list)
        return "%s(%s)" % (type(self).__name__, args)

    def validate(self):
        """
        Validates the object to ensure each field has an appropriate value. An
        exception is thrown if validation fails.

        :returns: None

        :raises ValidationFailure: On failure.

        """

        for k, v in self._fields.items():
            v.validate(getattr(self, k))

    @classmethod
    def from_dict(cls, dictionary):
        """
        Creates a new instance of the model from the given dictionary.

        .. note::

            Validation is not performed. Make sure to call validate()
            afterwards if validation is desired.

        """

        # We're just going to directly plug the values in.
        instance = cls()
        for k, v in dictionary.items():
            setattr(instance, k, v)

        return instance

    def to_dict(self):
        """
        Tranforms the current object into a dictionary representation.

        .. note::

            It very uninterestingly calls the ``vars()`` built-in on itself,
            but should be used instead of calling ``vars()`` directly in case
            of implementation changes in the future.

        """

        return vars(self)
