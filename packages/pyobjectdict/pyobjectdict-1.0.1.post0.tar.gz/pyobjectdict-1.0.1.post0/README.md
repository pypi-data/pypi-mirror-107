# PyObjectDict

## Python dictionaries for more convenient use

![](https://img.shields.io/badge/license-MIT-green)

<br />

### Overview

**The problem**

When it comes to the Python `dict` syntax, what makes it clanky and annoying is the need to always pass keys as strings and use square brackets when accessing a `dict`'s value:
```python
x = {'a': 1, 'b': 2}
value = x['b'] # we have to write square brackets and use strings inside them
```

It is made quite concise in JavaScript language where all you need is access your value through the dot syntax like the following:
```javascript
x = {'a': 1, 'b': 2}
value = x.b // no need to use square brackets or strings!
```

**The solution**
This simple package introduces a new Python `dict` object which has some similarities to the JavaScript object in terms of dot syntax.
The object is called `PyObjectDict`.


### How to use

import the package and try to initialize your PyObjectDict in a preferred way:
```python
from object_dict import PyObjectDict

a = PyObjectDict({'a': 2, 'b': 3, 'c': 10, 'd': 8})
b = PyObjectDict.form(**{'a': 2, 'b': 3, 'c': 4, 'g': 8})
```

*Note:* `PyObjectDict` constructor works with types: `dict`, `OrderedDict`, and `PyObjectDict` (to create a copy)

you may add new attributes to the object by simply using the dot syntax:
```python
a.e = 1
a.f = 1
a.g = 1
a.h = 1
a.i = 1
```

you may then easily access any attribute by using:
```python
print(a.a) # will print 2
print(a.e) # will print 1
```

The `PyObjectDict` also exposes a lot of additional convenience methods as well as standard `dict` methods.
They are listed in the table above and an example of their usage can be seen below it.

<br />
<br />

### Methods of PyObjectDict

| Name              | Parameters                        | Return value                                | Description                                                                                                                               |
| -------------     | -------------                     |-------------                                | -------------                                                                                                                             |
| `length`          | -                                 | `int`                                       | returns the lenght of the dictionary                                                                                                      |
| `keys`            | -                                 | `list`                                      | returns the list of keys of the dictionary                                                                                                |
| `items`           | -                                 | `list` of `tuple`s                          | returns the list of tuples containing key, value pairs of each item in the dicrionary                                                     |
| `iteritems`       | -                                 | `iterator`                                  | iterator for `items` method                                                                                                               |
| `values`          | -                                 | `list`                                      | returns the list of values of the dictionary                                                                                              |
| `update`          | `other` (`PyObjectDict`)            | `None`                                      | updates one `PyObjectDict` with the other (merges them) in place. Returns nothing                                                           |
| `get`             | `key` (`str`), `default` (`None`) | type of `key` or type of `default` parameter| returns value of the `key` if key exists or `default` parameter (which is`None` by default)                                               |
| `add`             | `other` (`PyObjectDict`)            | `PyObjectDict`                                | merges two `PyObjectDict`s and returns a merged copy                                                                                        |
| `add_each_value`  | `other` (`PyObjectDict`)            | `PyObjectDict`                                | merges the keys of two `PyObjectDict`s and adds the corresponding key values together. returns a merged copy                                |
| `sub`             | `other` (`PyObjectDict`)            | `PyObjectDict`                                | subtracts one `PyObjectDict` from another and returns a copy containing not intersecting keys of the first `PyObjectDict` with their values   |
| `sub_each_value`  | `other` (`PyObjectDict`)            | `PyObjectDict`                                | subtracts the values of the corresponding keys of the first `PyObjectDict` from the second one. Returns a copy                              |
| `sub_by_value`    | `other` (`PyObjectDict`)            | `PyObjectDict`                                | the same as `sub` but subtraction happens by the unique `key: value` pairs not just the unique keys                                       |

<br />

### Operators of PyObjectDict

| Name              | Parameters                | Return value  | Description                                                                                           |
| -------------     | -------------             |-------------  | -------------                                                                                         |
| `+`               | `other` (`PyObjectDict`)    | `PyObjectDict`  | the same as `add` method                                                                              |
| `+=`              | `other` (`PyObjectDict`)    | `PyObjectDict`  | the same as `add` method but assigns the result to the `PyObjectDict` to the left side of the operator  |
| `\|`              | `other` (`PyObjectDict`)    | `PyObjectDict`  | the same as `add` method                                                                              |
| `\|=`             | `other` (`PyObjectDict`)    | `PyObjectDict`  | the same as `+=` operator                                                                             |
| `-`               | `other` (`PyObjectDict`)    | `PyObjectDict`  | the same as `sub` method                                                                              |
| `-=`              | `other` (`PyObjectDict`)    | `PyObjectDict`  | the same as `sub` method but assigns the result to the `PyObjectDict` to the left side of the operator  |

<br />

### Dunder methods of PyObjectDict

| Name              | Parameters    | Return value  | Description                                           |
| -------------     | ------------- |-------------  | -------------                                         |
| `len`             | -             | `int`         | returns the lenght of the dictionary                  |
| `str`             | -             | `str`         | returns the string representation of the dicrionary   |

<br />

### Constructors of PyObjectDict

| Name              | Parameters    | Return value  | Description                                                                                       |
| -------------     | ------------- |-------------  | -------------                                                                                     |
| `PyObjectDict`      | -             | `PyObjectDict`  | creates an `PyObjectDict` from `dict`, `OrderedDict`, or `PyObjectDict` (copy)                        |
| `PyObjectDict.from` | -             | `PyObjectDict`  | creates an `PyObjectDict` from the key value pairs that are successively passed to the constructor  |


<br />
<br />

### An Example of Usage

```python
from object_dict import PyObjectDict

a = PyObjectDict({'a': 2, 'b': 3, 'c': 10, 'd': 8})
b = PyObjectDict.form(**{'a': 2, 'b': 3, 'c': 4, 'g': 8})

print('a:', a)
print('b:', b)

c = a.sub_by_value(b)
print('c:', c)

print('c.length():', c.length())
print('c.keys():', c.keys())
print('c.items():', c.items())
print('c.iteritems():', list(c.iteritems()))
print('c.values():', c.values())
print('c.update(PyObjectDict({"a": 1, "b": 2, "c": 3})):', c.update(PyObjectDict({'a': 1, 'b': 2, 'c': 3})))
print('c.update(PyObjectDict({"a": 1, "b": 2, "c": 3})):', c.update(PyObjectDict({'a': 1, 'b': 2, 'c': 3})))

print('iteratibng over c:')
for k in c:
    print('key: ', k)


print('a + b:', a + b)
print('a | b:', a | b)
print('a.add(b):', a.add(b))
print('a.add_each_value(b):', a.add_each_value(b))
a.update(b)
print('a after a.update(b):', a)

a.cc = 12
b.cc = 12
print('a after adding "cc": 12:', a)
print('b after adding "cc": 12:', b)

print('a - b:', a - b)
print('a.sub(b):', a.sub(b))
print('a.sub_by_value(b):', a.sub_by_value(b))
print('a.sub_each_value(b):', a.sub_each_value(b))

a += b
print('a after a += b:', a)
a -= b
print('a after a -= b:', a)
a |= b
print('a after a |= b', a)
```
The result of the code above will be:

```
a: PyObjectDict({'a': 2, 'b': 3, 'c': 10, 'd': 8})
b: PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'g': 8})
c: PyObjectDict({'c': 10, 'd': 8})
c.length(): 2
c.keys(): ['c', 'd']
c.items(): [('c', 10), ('d', 8)]
list(c.iteritems()): [('c', 10), ('d', 8)]
c.values(): [10, 8]
c.update(PyObjectDict({"a": 1, "b": 2, "c": 3})): None
c.update(PyObjectDict({"a": 1, "b": 2, "c": 3})): None
iteratibng over c:
key:  c
key:  d
key:  a
key:  b
a + b: PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'd': 8, 'g': 8})
a | b: PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'd': 8, 'g': 8})
a.add(b): PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'd': 8, 'g': 8})
a.add_each_value(b): PyObjectDict({'a': 4, 'b': 6, 'c': 14, 'd': 8})
a after a.update(b): PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'd': 8, 'g': 8})
a after adding "cc": 12: PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'd': 8, 'g': 8, 'cc': 12})
b after adding "cc": 12: PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'g': 8, 'cc': 12})
a - b: PyObjectDict({'d': 8})
a.sub(b): PyObjectDict({'d': 8})
a.sub_by_value(b): PyObjectDict({'d': 8})
a.sub_each_value(b): PyObjectDict({'a': 0, 'b': 0, 'c': 0, 'd': 8, 'g': 0, 'cc': 0})
a after a += b: PyObjectDict({'a': 2, 'b': 3, 'c': 4, 'd': 8, 'g': 8, 'cc': 12})
a after a -= b: PyObjectDict({'d': 8})
a after a |= b PyObjectDict({'d': 8, 'a': 2, 'b': 3, 'c': 4, 'g': 8, 'cc': 12})
```

### Notes

Remember that in JavaScripts objects it is possible to access a non-existing attribute and receve an `undefined` value.
However, since Python has no concept of `undefined` and checking for `None` could be missleading (+ the limitations of Python objects), you cannot access an unexisting attribute of `PyObjectDict` without triggering an `AttributeError` exception. Alternatively you can use `get` method as in standard Python dicts to check if the attribute exists before accessing it.
