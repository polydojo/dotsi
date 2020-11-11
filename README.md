
Dotsi
=====

Dot-accessible, update-aware Python dicts (& lists). Works recursively, like a charm.

Dotsi defines two classes, `dotsi.Dict` and `dotsi.List`, which *work together* to bring JavaScript-like dot-notation to Python dicts (and lists therein).

Installation
--------------
```
pip install dotsi
```
Alternately, download `dotsi.py` it into your project directory.

Usage
--------

Let's dive right in:

```py
>>> import dotsi
>>> 
>>> d = dotsi.Dict({"foo": {"bar": "baz"}})     # Basic
>>> d.foo.bar
'baz'
>>> d.users = [{"id": 0, "name": "Alice"}]   # List
>>> d.users[0].name
'Alice'
>>> d.users.append({"id": 1, "name": "Becca"}); # Append
>>> d.users[1].name
'Becca'
>>> d.users += [{"id": 2, "name": "Cathy"}];    # `+=`
>>> d.users[2].name
'Cathy'
>>> d.update({"tasks": [{"id": "a", "text": "Task A"}]});
>>> d.tasks[0].text
'Task A'
>>> d.tasks[0].tags = ["red", "white", "blue"];
>>> d.tasks[0].tags[2];
'blue'
>>> d.tasks[0].pop("tags")                      # `.pop()`
['red', 'white', 'blue']
>>> 
>>> import pprint
>>> pprint.pprint(d)
{'foo': {'bar': 'baz'},
 'tasks': [{'id': 'a', 'text': 'Task A'}],
 'users': [{'id': 0, 'name': 'Alice'},
           {'id': 1, 'name': 'Becca'},
           {'id': 2, 'name': 'Cathy'}]}
>>> 
>>> type(d.users)       # dotsi.Dict (AKA dotsi.DotsiDict)
<class 'dotsi.DotsiList'>
>>> type(d.users[0])    # dotsi.List (AKA dotsi.DotsiList)
<class 'dotsi.DotsiDict'> 
>>> 
```

In the above example, while we explicitly initialized `d` as an `dotsi.Dict`:
- `d.users` automatically became a `dotsi.List`.
- `d.users[0]` automatically became a `dotsi.Dict`.

Dotsi vs Others
-------------------

#### Addict:

At Polydojo, we've been using [Addict](https://github.com/mewwts/addict) for quite some time. It's a great library! But it doesn't play well with list-nested (inner) dicts.

```py
>>> import addict
>>> 
>>> d = addict.Dict({"foo": {"bar": "baz"}})
>>> d.foo
{'bar': 'baz'}
>>> d.users = [{"id": 0, "name": "Alice"}]
>>> d.users[0].name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'name'
>>> 
```

#### EasyDict:

[EasyDict](https://github.com/makinacorpus/easydict) is another great library. It works recursively, but doesn't fully support list-nested dict updates.

```py
>>> import easydict
>>> 
>>> d = easydict.EasyDict({"foo": {"bar": "baz"}})
>>> d.foo
{'bar': 'baz'}
>>> d.users = [{"id": 0, "name": "Alice"}]
>>> d.users[0].name
'Alice'
>>> d.users.append({"id": 1, "name": "Becca"});
>>> d.users[1].name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'name'
>>> 
```

Shortcuts
------------
Classes:
- `dotsi.Dict` is a short alias for `dotsi.DotsiDict`.
- `dotsi.List` is a short alias for `dotsi.DotsiList`.

Functions:
- `dotsi.dotsify()` calls `dotsi.Dict`/`dotsi.List`, as appropriate.
- `dotsi.fy()` is a short alias for `dotsi.dotsify()`.
- `dotsi.mapdotsify()` is like the built-in `map()`, but returns a `dotsi.List`.
- `dotsi.mapfy` is a short alias for `dotsi.mapdotsify()`. (More on this below.)

In most cases, all you need is:
- `dotsi.fy(thing)`, where `thing` is a `dict` or `list`.

Dict-Like Objects
----------------------
While `dotsi.fy()` converts objects of type `dict` to `dotsi.Dict`, it ***doesn't*** touch other dict-like objects, such as those of type `collections.OrderedDict` or `http.cookies.SimpleCookie`.

To convert a non-`dict`, but dict-like object to `dotsi.Dict`, use `dotsi.Dict(.)` directly, or use `dotsi.fy(dict(.))`.

```py
>>> import dotsi
>>> from collections import OrderedDict
>>> 
>>> d = OrderedDict({"foo": {"bar": "baz"}})
>>> d
OrderedDict([('foo', {'bar': 'baz'})])
>>> type(d)
<class 'collections.OrderedDict'>
>>>
>>> x = dotsi.fy(d)
>>> x
OrderedDict([('foo', {'bar': 'baz'})])
>>> type(x)
<class 'collections.OrderedDict'>
>>> 
>>> y = dotsi.Dict(d)
>>> y
{'foo': {'bar': 'baz'}}
>>> type(y)
<class 'dotsi.DotsiDict'>
>>> 
>>> z = dotsi.fy(dict(d))
>>> z
{'foo': {'bar': 'baz'}}
>>> type(z)
<class 'dotsi.DotsiDict'>
```

Subclasses of `dict`, such as `http.cookie.SimpleCookie`, often implement custom behavior, which would be lost on conversion to `dotsi.Dict`. Thus, automatic conversion shouldn't be implemented.

Quick Plug
--------------
Dotsi is built and maintained by the folks at [Polydojo, Inc.](https://www.polydojo.com/), led by Sumukh Barve. If your team is looking for a simple project management tool, please check out our latest product: [**BoardBell.com**](https://www.boardbell.com/).

List-Like Objects
--------------------

Like with dicts, `dotsi.fy(.)` only converts objects of type `list` to `dotsi.List`, but doesn't touch other list-like objects or tuples. To convert a non-`list`, but list-like object to `dotsi.List`, directly call `dotsi.List(.)` or use `dotsi.fy(list(.))`

#### Identity Function

For non-`dict` and non-`list` objects, `dotsi.fy(.)` is equivalent to the identity function.

Kindly note that from Python3+, the built-in `map()` produces a non-`list` iterable. Thus, calling `dotsi.fy(map(.))` is equivalent to just `map(.)`. Instead, please use `dotsi.List(map(.))`.


#### Mapping Helper

As mapping is a pretty-common use case, we've included `dotsi.mapfy(.)`, which is essentially equivalent to `dotsi.List(map(.))`. But additionally, with `dotsi.mapfy(.)`, for mapping onto a *single* sequence, you may pass arguments in either order.

That is, the following lines are equivalent:
- `x = dotsi.mapfy(lambda n: {"n": n}, [0, 1, 2])`
- `x = dotsi.mapfy([0, 1, 2], lambda n: {"n": n})`

In either case, `x[0].n == 0` will be `True`.

When mapping onto *multiple* sequences, `dotsi.mapfy(.)` expects the same order of arguments as `map(.)`.

Overridden Methods
--------------------------
Excluding magic-methods like `.__init__(.)` etc., methods overridden by Dotsi are listed below.

#### `dotsi.Dict` overrides:
- `.update(.)`
- `.setdefault(.)`
- `.copy(.)`

#### `dotsi.List` overrides:
- `insert(.)`
- `append(.)`
- `extend(.)`
- `copy(.)`

Signatures for all overridden methods should be equivalent (if not exactly identical) to their non-overridden counterparts.


Licensing
------------
Copyright (c) 2020 Polydojo, Inc.

**Software Licensing:**  
The software is released "AS IS" under the **MIT license**, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Kindly see [LICENSE.txt](https://github.com/polydojo/dotsi/blob/master/LICENSE.txt) for more details.

**No Trademark Rights:**  
The above software licensing terms **do not** grant any right in the trademarks, service marks, brand names or logos of Polydojo, Inc.
