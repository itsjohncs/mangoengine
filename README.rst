MangoEngine
===========

MangoEngine is a light-weight library for creating generic data models in Python.

.. code-block:: python

    class City(Model):
        name = StringField()
        officials = DictField(
            of_key = StringField(),
            of_value = StringField()
        )
        population = IntegerField(bounds = (0, None))

The models you create with MangoEngine are self-documenting and simple to create. Even better, you can populate them from unreliable sources and validate them to ensure your data is sane.

.. code-block:: python

    >>> city = City.from_dict({
    ...     "name": 12,
    ...     "officials": {1: 2},
    ...     "population": "alot"
    ... })
    >>> city.validate()
    ValidationError: For field 'name': expecting instance of basestring, got int.

You can leverage this library to create your own light-weight ORM for your application regardless of what your backing store is, without abstracting away important details like queries.

About the Project
-----------------

This library started as a means to create models for JSON objects, but has since evolved into a more general purpose library. Its interface is inspired by the fantastic `MongoEngine <http://mongoengine.org/>`_ library (thus its name). It was created by `John Sullivan <http://johnsullivan.name>`_ and he would greatly appreciate any contributions.

Licensing
---------

All code and literature within this repository is dedicated to the public domain per the terms of the `Unlicense <http://unlicense.org/>`_.
