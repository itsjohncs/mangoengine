# internal
from mangoengine import *

class Foo(Model):
    version = StringField()
    compatible_with = DictField(
        of_value = ListField(of = StringField())
    )

def try_validate(obj):
    print "Validation of", obj,
    try:
        obj.validate()
        print "succeeded"
    except ValidationFailure as e:
        print "failed:", str(e)

f = Foo()
try_validate(f)

f.version = "1.0"
f.compatible_with = {"key": "value"}
try_validate(f)

f.compatible_with["key"] = ["value1", "value2"]
try_validate(f)
