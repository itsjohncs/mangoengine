# internal
from ..errors import ValidationFailure
from ..fields import *
from .. import models

# external
import pytest

class ExtendedValue:
    """
    Used in the TEST_CASES list below to describe a test case where
    particular arguments need to be fed into the constructor the Field before
    validating.

    :ivar args: Any positional arguments to pass into the Field's constructor.
    :ivar kwargs: Any keyword arguments to pass into the Field's constructor.
    :ivar value: The actual value to validate.

    """

    def __init__(self, args, kwargs, value):
        self.args = args
        self.kwargs = kwargs
        self.value = value

# This list is read by test_standard_cases() below and is fairly self-
# explanatory, though the use of the ExtendedValue class may require a
# moment of looking around to understand.
TEST_CASES = [
    {
        "field_type": StringField,
        "good_values": ["hello", ""],
        "bad_values": [2, 4.0, unicode("hello")]
    },
    {
        "field_type": UnicodeField,
        "good_values": [unicode("hello"), unicode()],
        "bad_values": [2, 4.0, "hello"]
    },
    {
        "field_type": NumericField,
        "good_values": [
            # No bounds
            1, 1.0, long(10), -2, -1.0, 0, True, False,

            # Upper bounds
            ExtendedValue([(None, 100)], {}, 2),
            ExtendedValue([(None, 100)], {}, 100),
            ExtendedValue([(None, 0)], {}, -2),

            # Lower bounds
            ExtendedValue([(0, None)], {}, 2),
            ExtendedValue([(0, None)], {}, 0),
            ExtendedValue([(-20, None)], {}, -2),

            # Both
            ExtendedValue([(0, 100)], {}, 0),
            ExtendedValue([(0, 100)], {}, 100),
            ExtendedValue([(-20, 100)], {}, -2)
        ],
        "bad_values": [
            # Bad types
            "hello", "4",

            # Upper bounds
            ExtendedValue([(None, 100)], {}, 102),
            ExtendedValue([(None, 100.3)], {}, long(9999)),
            ExtendedValue([(None, -3)], {}, -2.2),

            # Lower bounds
            ExtendedValue([(0, None)], {}, -1),
            ExtendedValue([(0.1, None)], {}, long(-9999)),
            ExtendedValue([(-20, None)], {}, -21),

            # Both
            ExtendedValue([(0, 100)], {}, -1),
            ExtendedValue([(0, 100.4)], {}, 101.5),
            ExtendedValue([(-20, 100)], {}, -21)
        ]
    },
    {
        "field_type": IntegralField,
        "good_values": [
            # No bounds
            1, long(10), -2, 0, True, False,

            # Upper bounds
            ExtendedValue([(None, 100)], {}, 2),
            ExtendedValue([(None, 100)], {}, 100),
            ExtendedValue([(None, 0)], {}, -2),

            # Lower bounds
            ExtendedValue([(0, None)], {}, 2),
            ExtendedValue([(0, None)], {}, 0),
            ExtendedValue([(-20, None)], {}, -2),

            # Both
            ExtendedValue([(0, 100)], {}, 0),
            ExtendedValue([(0, 100)], {}, 100),
            ExtendedValue([(-20, 100)], {}, -2)
        ],
        "bad_values": [
            # Bad types
            "hello", "4", 3.4, -2.3, 0.0,

            # Upper bounds
            ExtendedValue([(None, 100)], {}, 102),
            ExtendedValue([(None, 100)], {}, long(9999)),
            ExtendedValue([(None, -3)], {}, -2),

            # Lower bounds
            ExtendedValue([(0, None)], {}, -1),
            ExtendedValue([(0, None)], {}, long(-9999)),
            ExtendedValue([(-20, None)], {}, -21),

            # Both
            ExtendedValue([(0, 100)], {}, -1),
            ExtendedValue([(0, 100)], {}, 101),
            ExtendedValue([(-20, 100)], {}, -21)
        ]
    },
    {
        "field_type": ListField,
        "good_values": [
            [1, 2, 3], [1, "a", 2.3], [],

            ExtendedValue([NumericField()], {}, [1, 2, 3]),
            ExtendedValue([StringField()], {}, ["a", "b", "c"]),
            ExtendedValue(
                [ListField(of = NumericField())], {}, [[1, 2], [1, 2]])
        ],
        "bad_values": [
            1, "a", 1.2,

            ExtendedValue([NumericField()], {}, [1, 2, "c"]),
            ExtendedValue([StringField()], {}, ["a", 2, "c"]),
            ExtendedValue(
                [ListField(of = NumericField())], {}, [[1, 2], ["b", 2]])
        ]
    },
    {
        "field_type": DictField,
        "good_values": [
            {1: 2, "a": 2}, {}, {1: [2], 3: [3]},

            ExtendedValue([NumericField(), StringField()], {},
                {1: "a", 2: "b"}),
            ExtendedValue([NumericField(), ListField(NumericField())], {},
                {1: [1, 2], 3: []}),
            ExtendedValue([NumericField(bounds = (0, None))], {},
                {1: [1, 2], 2: "a"})
        ],
        "bad_values": [
            [1], 1, True, "b",

            ExtendedValue([NumericField(), StringField()], {},
                {1: 2, 3: 4}),
            ExtendedValue([NumericField(), ListField(NumericField())], {},
                {1: ["a", "b"], 3: []}),
            ExtendedValue([NumericField(bounds = (0, None))], {},
                {-1: [1, 2], 2: "a"})
        ]
    }
]

class TestFields:
    @pytest.mark.parametrize("test_case", TEST_CASES,
        ids = [i["field_type"].__name__ for i in TEST_CASES])
    def test_standard_cases(self, test_case):

        # This function will help us deal with the ExtendedValue objects
        # in our list of test cases.
        def create_field_value_tuple(value):
            """Returns a field instance and a value to validate."""

            field_type = test_case["field_type"]
            if isinstance(value, ExtendedValue):
                print "Testing %s(*%s, **%s) with value %s." % (
                    field_type.__name__,
                    repr(value.args),
                    repr(value.kwargs),
                    repr(value.value)
                )

                return (
                    field_type(*value.args, **value.kwargs),
                    value.value
                )
            else:
                print "Testing %s() with value %s." % (
                    field_type.__name__, repr(value))

                return field_type(), value

        for i in test_case["good_values"]:
            field, value = create_field_value_tuple(i)
            field.validate(value)

        for i in test_case["bad_values"]:
            field, value = create_field_value_tuple(i)
            with pytest.raises(ValidationFailure):
                field.validate(value)

    def test_modelfield(self):
        """
        We test the ModelField seperately because it depends on the model
        module working as well.

        """

        class Person(models.Model):
            name = StringField()
            age = IntegralField(bounds = (0, None))
            siblings = ListField(of = StringField())

        class NotAPerson(models.Model):
            not_name = StringField()

        field = ModelField(Person)

        person = Person(name = "joe", age = 3, siblings = ["bob"])
        field.validate(person)

        person = Person(name = "bill", age = -1, siblings = ["george"])
        with pytest.raises(ValidationFailure):
            field.validate(person)

        person = NotAPerson(not_name = "not joe")
        with pytest.raises(ValidationFailure):
            field.validate(person)

        person = "definitely not a person"
        with pytest.raises(ValidationFailure):
            field.validate(person)
