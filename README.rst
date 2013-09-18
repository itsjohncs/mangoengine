MangoEngine
===============================

MangoEngine is a simple library for creating models for JSON objects. Its interface is inspired by the fantastic [MongoEngine](http://mongoengine.org/) library, it resides (basically) in the public domain, and it has no dependencies.

.. code-block:: python

    from mangoengine import *

    class City(Model):
        name = StringField()
        officials = DictField(
            of_key = StringField(),
            of_value = ListField(of = StringField(), nullable = True)
        )

    city = City(name = "Gotham")
    city.officials = {
        "mayor": ["Theodore Cobblepot"],
        "batman": ["Bruce Wayne"],
        "citizens": ["Joe Schmoe", "Dick", "Jane"]
    }
    city.validate()
