# mongoengine
import fields

class ModelMetaclass(type):
    def __new__(cls, clsname, bases, dct):
        data_fields = {}
        attributes = {}
        for k, v in dct.items():
            if not isinstance(v, fields.Field):
                attributes[k] = v
            else:
                data_fields[k] = v
        attributes["_fields"] = data_fields

        return type.__new__(cls, clsname, bases, attributes)

class Model(object):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        for k in kwargs.keys():
            if k not in self._fields:
                raise TypeError(
                    "'%s' is an invalid keyword argument for this "
                    "function" % (k, )
                )

        for k, v in self._fields.items():
            setattr(self, k, kwargs.get(k, None))

    def __repr__(self):
        arg_list = ((k, getattr(self, k)) for k in self._fields.keys())
        args = ", ".join("%s = %s" % (k, repr(v)) for k, v in arg_list)
        return "%s(%s)" % (type(self).__name__, args)

    def validate(self):
        for k, v in self._fields.items():
            v.validate(getattr(self, k))

    @classmethod
    def from_dict(cls, dictionary):
        return cls(**dictionary)

    def to_dict(self):
        return dict((k, getattr(self, k)) for k in self._fields.keys())
