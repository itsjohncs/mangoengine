MangoEngine API Reference
=========================

The Model Class
---------------

.. autoclass:: mangoengine.Model
    :members:

Fields
------

.. automodule:: mangoengine
    :members: Field, StringField, UnicodeField, NumericField, IntegralField, DictField, ListField, ModelField

Errors
------

.. autoclass:: mangoengine.ValidationFailure
    :members:

.. autoclass:: mangoengine.UnknownAttribute
    :members:

The ModelMetaclass Metaclass
----------------------------

This metaclass is not a part of the MangoEngine public interface and should not be accessed directly. It is useful to look at to understand how the models work however.

.. autoclass:: mangoengine.models.ModelMetaclass
    :members:
