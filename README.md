Dotsi
=====

Dot-accessible, update-aware Python dicts (& lists). Works recursively, like a charm.

Dotsi defines two classes `dotsi.Dict` and `dotsi.List`, which *work together* to bring JavaScript-like dot-notation to Python dicts (and lists therein).

Usage
--------

Let's dive right in:

```py
>>> import dotsi
>>> 
>>> d = dotsi.Dict({"foo": {"bar": "baz"}})     # Basic
>>> d.foo.bar
'baz'
>>> d["users"] = [{"id": 0, "name": "Alice"}]   # List
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

**Addict:**

At Polydojo, we've been using [Addict](https://github.com/mewwts/addict) for quite some time. It's a great library! But it doesn't play well with list-nested (inner) dicts.

```py
>>> import addict
>>> 
>>> d = addict.Dict({"foo": {"bar": "baz"}})
>>> d.foo
{'bar': 'baz'}
>>> d["users"] = [{"id": 0, "name": "Alice"}]
>>> d.users[0].name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'name'
>>> 
```

**EasyDict:**
[EasyDict](https://github.com/makinacorpus/easydict) is another great library. It works recursively, but doesn't fully support list-nested dict updates.

```py
>>> import easydict
>>> 
>>> d = easydict.EasyDict({"foo": {"bar": "baz"}})
>>> d.foo
{'bar': 'baz'}
>>> d["users"] = [{"id": 0, "name": "Alice"}]
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

In most cases, all you need is:
- `dotsi.fy(thing)`, where `thing` is a `dict` or `list`.

License
---------
Copyright (c) 2020 Polydojo, Inc.

The software is released "AS IS" under the MIT License, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. See [LICENSE.txt](https://github.com/polydojo/dotsi/blob/master/LICENSE.txt) for more details.
