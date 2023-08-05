# supported from python 3.6 and higher
from collections import OrderedDict

_TYPE_ERROR_TXT = 'Operation is supported only for {} type'


class PyObjectDict():
    _non_public_attrs = ['_dict_type']
    __name__ = 'PyObjectDict'

    def __init__(self, dictionary: dict=None, type_=None):
        self._dict_type = dict

        if dictionary is None:
            return

        if type_:
            if type_ not in [dict, OrderedDict, PyObjectDict]:
                raise TypeError('type_ can only be dict, OrderedDict, or ' + self.__name__)
            self._dict_type = type_
        elif type(dictionary) is OrderedDict:
            self._dict_type = OrderedDict
        elif type(dictionary) is PyObjectDict:
            self._dict_type = dictionary._dict_type
        elif type(dictionary) is dict:
            pass
        else:
            raise TypeError('Invalid object in place of dictionary argument passed. It has to be either instance of dict, OrderedDict, or ' + self.__name__)

        for key in dictionary:
            setattr(self, key, dictionary[key])


    @classmethod
    def form(cls, **kwargs):
        self = cls()
        for key in kwargs:
            setattr(self, key, kwargs[key])
        return self


    def get_dict(self):
        return self._dict_type({key: (self.__dict__[key] if type(self.__dict__[key]) is not self else self.__dict__[key].get_dict()) \
                                                            for key in self.__dict__ if key not in self._non_public_attrs})


    def length(self):
        return len(self.__dict__) - len(self._non_public_attrs)


    def __add__(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        new = PyObjectDict(self)
        new.__dict__.update(other.__dict__)
        return new


    def __iadd__(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        self.__dict__.update(other.__dict__)
        return self


    def __or__(self, other):
        return self.__add__(other)


    def __ior__(self, other):
        return self.__iadd__(other)


    def add(self, other):
        return self.__add__(other)


    def add_each_value(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        return PyObjectDict(self._dict_type({key: (value + other[key] if other.get(key) else value) for key, value in self.items()}))


    def update(self, other):
        self.__iadd__(other)


    def __sub__(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        return PyObjectDict(self._dict_type({key: value for key, value in self.items() if key not in other}))


    def __isub__(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        self.__dict__ = {key: value for key, value in self.items() if key not in other}
        return self


    def sub(self, other):
        return self.__sub__(other)


    def sub_by_value(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        return PyObjectDict(self._dict_type({key: value for key, value in self.items() if key not in other or value != other[key]}))


    def sub_each_value(self, other):
        if not isinstance(other, PyObjectDict):
            return TypeError(_TYPE_ERROR_TXT.format(self.__name__))

        return PyObjectDict(self._dict_type({key: (value - other[key] if other.get(key) else value) for key, value in self.items()}))


    def keys(self):
        return [key for key in self.__dict__ if key not in self._non_public_attrs]


    def values(self):
        return [self.__dict__[key] for key in self.__dict__ if key not in self._non_public_attrs]


    def items(self):
        return [(key, self.__dict__[key]) for key in self.__dict__ if key not in self._non_public_attrs]


    def iteritems(self):
        for key in self.__dict__:
            if key in self._non_public_attrs:
                continue
            yield key, self.__dict__[key]


    def __str__(self):
        return self.__name__ + '(' + str({key: (self.__dict__[key] if type(self.__dict__[key]) is not self else str(self.__dict__[key])) \
                                                            for key in self.__dict__ if key not in self._non_public_attrs}) + ')'


    def __len__(self):
        return self.length()


    def __iter__(self):
        for key in self.keys():
            yield key


    def __getitem__(self, item):
        return self.__dict__[item]


    def get(self, value, default=None):
        if self.__dict__.get(value):
            return self.__dict__[value]
        else:
            return default

