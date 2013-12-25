# internal
from ..errors import ValidationFailure
from ..fields import *

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
        "field_type": IntegralField,
        "good_values": [1, 5, long(9999), 0, -2, True, False],
        "bad_values": ["hello", 1.0]
    }
    # {
    #     # Checking
    #     "field_type": DictField,
    #     "good_values"
    # }
]

class TestFields:
    @pytest.mark.parametrize("test_case", TEST_CASES)
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
