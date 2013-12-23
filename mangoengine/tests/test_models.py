# internal
from ..models import Model
from ..fields import *
from ..errors import *

# external
import pytest

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
            unrelated = 2
            notafield = 3

        assert hasattr(Foo, "unrelated")
        assert Foo.unrelated == 2

        assert hasattr(Foo, "notafield")
        assert Foo.notafield == 3

    def test_fields(self):
        """
        This will ensure that a model's ``_fields`` attribute gets set
        correctly and that all field defintion attributes get removed from the
        class.

        """

        class Foo(Model):
            field1 = StringField()
            field2 = IntegralField()

        assert hasattr(Foo, "_fields")
        assert type(Foo._fields) is dict

        assert not hasattr(Foo, "field1")
        assert "field1" in Foo._fields
        assert type(Foo._fields["field1"]) is StringField

        assert not hasattr(Foo, "field2")
        assert "field2" in Foo._fields
        assert type(Foo._fields["field2"]) is IntegralField

    def test_empty_model(self):
        """
        A simple smoke test to ensure that an empty model doesn't cause any
        errors. I don't see a use case for an empty model but that doesn't mean
        it should be taken off the table.

        """

        class Foo(Model):
            pass

        assert hasattr(Foo, "_fields")
        assert type(Foo._fields) is dict
        assert len(Foo._fields.items()) == 0

    def test_from_dict(self):
        """Tests to ensure Model.from_dict() works as advertised."""

        class Person(Model):
            name = StringField()
            age = IntegralField(bounds = (0, None))
            siblings = ListField(of = StringField())

        # In the normal case where all the data coincides with fields
        # correctly.
        person1 = Person.from_dict({
            "name": "Joe Shmoe",
            "age": 21,
            "siblings": ["Dick Shmoe", "Jane Shmoe"]
        })
        assert person1.name == "Joe Shmoe"
        assert person1.age == 21
        assert person1.siblings == ["Dick Shmoe", "Jane Shmoe"]

        # In the less normal case where the data does not coincide with fields
        person2 = Person.from_dict({
            "notaname": 2,
            "age": "lots"
        })
        assert person2.notaname == 2
        assert person2.age == "lots"
        assert person2.name is None
        assert person2.siblings is None

        # In the even less normal case where no data exists at all
        person3 = Person.from_dict({})
        assert person3.name is None
        assert person3.age is None
        assert person3.siblings is None

    def test_to_dict(self):
        """Ensures that Model.to_dict() works as advertised."""

        class Person(Model):
            name = StringField()
            age = IntegralField(bounds = (0, None))
            siblings = ListField(of = StringField())

        data1 = {
            "name": "Joe Shmoe",
            "age": 21,
            "siblings": ["Dick Shmoe", "Jane Shmoe"]
        }
        person1 = Person(**data1)
        assert person1.to_dict() == data1

        # The defined but unset fields should still be present, but set to none
        data2 = {"notaname": 2, "age": "lots"}
        person2 = Person.from_dict(data2)
        assert person2.to_dict() == {
            "notaname": 2,
            "age": "lots",
            "name": None,
            "siblings": None
        }

    def test_validate(self):
        class Person(Model):
            name = StringField()
            age = IntegralField(bounds = (0, None))
            siblings = ListField(of = StringField())

        data1 = {
            "name": "Joe Shmoe",
            "age": 21,
            "siblings": ["Dick Shmoe", "Jane Shmoe"]
        }
        person1 = Person(**data1)
        person1.validate() # Should not raise an exception

        # Create a copy of the dictionary with the additional keyvalue
        # "chocolate": "chips".
        data2 = dict(data1.items() + [("chocolate", "chips")])
        person2 = Person.from_dict(data2)
        person2.validate()
        with pytest.raises(UnknownAttribute):
            person2.validate(allow_unknown_data = False)

        # Make sure we can override the default properly
        class Person2(Model):
            _allow_unknown_data = False

            name = StringField()
            age = IntegralField(bounds = (0, None))
            siblings = ListField(of = StringField())
        person3 = Person2.from_dict(data2)
        with pytest.raises(UnknownAttribute):
            person3.validate()
