from ..models import Model
from ..fields import *

class TestModel:
    def test_unrelated_attributes(self):
        """
        This is primarily a test on the ModelMetaclass metaclass. It checks to
        see if class attributes that are not specifiying fields are left alone.
        For example...

        .. code-block:: python

            >>> class Foo(Model):
            ...     field1 = StringField()
            ...     unrelated = 2
            ...
            >>> Foo.unrelated
            2
            >>> Foo.field1
            Traceback (most recent call last):
            File "<stdin>", line 1, in <module>
            AttributeError: class Foo has no attribute 'field1'

        The above example is what is meant to happen. The ``field1`` attribute
        was taken to be a field definition, and the ``unrelated`` attribute was
        left alone.

        """

        # Create a simple class. We're going to test nearly exactly the
        # scenario described in the docstring above.
        class Foo(Model):
            field1 = StringField()
            unrelated = 2
            notafield = 3

        assert not hasattr(Foo, "field1")
        assert hasattr(Foo, "unrelated")
        assert hasattr(Foo, "notafield")
        assert "field1" in Foo._fields
        assert type(Foo._fields["field1"]) is StringField
