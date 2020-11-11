from collections import OrderedDict;
import dotsi;

# Basic dotsi.Dict:
d = dotsi.fy({"foo": "foo", "bar": "bar"});
assert d.foo == "foo" and d.bar == "bar";
d.update({"hello": "world", "bar": "baz"});
assert d.hello == "world" and d.bar == "baz";

# Nested dotsi.Dict:
d = dotsi.fy({"data": {"users": [
    {"id": 0, "name": "Alice"},
    {"id": 1, "name": "Becci"},
]}});
assert d.data.users[0].id == 0 and d.data.users[0].name == "Alice";
assert d.data.users[1].id == 1 and d.data.users[1].name == "Becci";

# Append within nested dotsi.Dict:
d.data.users.append({"id": 2, "name": "Cathy"});
d.data.users.append({"id": 3, "name": "Debra"});
assert d.data.users[2].id == 2 and d.data.users[2].name == "Cathy";
assert d.data.users[3].id == 3 and d.data.users[3].name == "Debra";

# Extend within nested dotsi.Dict:
d.data.users += [
    {"id": 4, "name": "Elina"},
    {"id": 5, "name": "Fiona"},
];
assert type(d.data.users[4]) == dotsi.Dict == type(d.data.users[5]);
assert d.data.users[4].id == 4 and d.data.users[4].name == "Elina";
assert d.data.users[5].id == 5 and d.data.users[5].name == "Fiona";

# Update within nested dotsi.Dict:
d.data.update({"tasks": [
    {"id": 0, "userId": 0, "text": "Zero", "done": False},
    {"id": 1, "userId": 1, "text": "One", "done": False},
]});
assert d.data.tasks[0].id == 0 == d.data.tasks[0].userId;
assert d.data.tasks[1].id == 1 == d.data.tasks[1].userId;

# Operator `in` with dotsi.List:
assert {"id": 0, "name": "Alice"} in d.data.users;
assert {"id": 5, "name": "Fiona"} in d.data.users;

# Operator `in` with dotsi.Dict:
assert "data" in d and "userId" in d.data.tasks[0];

# Set-Attr within nested dotsi.Dict:
d.data.posts = [
    {"id": 0, "author": 0, "title": "Zero"},
    {"id": 1, "author": 1, "title": "One"},
];
assert d.data.posts[0].id == 0 == d.data.posts[0].author;
assert d.data.posts[1].id == 1 == d.data.posts[1].author;

# Set-item within nested dotsi.List:
d.data.posts.extend([None, None]);
d.data.posts[2] = {"id": 2, "author": 2, "title": "Two"};
d.data.posts[3] = {"id": 3, "author": 3, "title": "Three"}
assert d.data.posts[2].id == 2 == d.data.posts[2].author;
assert d.data.posts[3].id == 3 == d.data.posts[3].author;

# Operator `+` with dotsi.List:
a = dotsi.fy([0, 1, 2]);
b = a + [3, 4, 5];
assert type(a) == dotsi.List == type(b);
a += [3, 4, 5];
assert type(a) == dotsi.List == type(b);
assert a == b;
c = [-3, -2, -1] + a;
assert type(c) is list; # Note: `list`, _not_ `dotsi.List`.

# Operator `|` with dotsi.Dict/dict:
assert dotsi.fy({"a": "b"}) | {"c": "d"} == {"a": "b", "c": "d"};
assert type(dotsi.fy({"a": "b"}) | {"c": "d"}) is dotsi.Dict;
assert {"c": "d"} | dotsi.fy({"a": "b"}) == {"a": "b", "c": "d"};
assert type({"c": "d"} | dotsi.fy({"a": "b"})) is dict;

# Operator `|=` with dotsi.Dict:
p = dotsi.fy({"a": "a"});
p |= {"b": "b"};
assert type(p) is dotsi.Dict and p == {"a": "a", "b": "b"};

# Maintaining references:
d1 = dotsi.Dict({"a": "a", "b": "b"});
d2 = dotsi.Dict({"d1": d1});
assert d2.d1 is d1;
d3 = dotsi.Dict(d1=d1);
assert d3.d1 is d1;
#
x = dotsi.Dict(a=1, b=2);
y = dotsi.Dict(x=x);
assert y.x is x;

# Non-conversion of dict-like objects:
d = OrderedDict({"foo": "bar"});
x = dotsi.fy(d);
assert type(x) is OrderedDict and x is d;
y = dotsi.Dict(d);
assert type(y) is dotsi.Dict and y is not d;
z = dotsi.fy(dict(d));
assert type(z) is dotsi.Dict and z is not d and z is not y;
assert d == x == y == z;

# Mapping:
assert dotsi.mapfy(lambda n: {"n": n}, [0,1,2])[0].n == 0;
assert dotsi.mapfy([0,1,2], lambda n: {"n": n})[0].n == 0; # Reverse order
assert dotsi.mapfy(lambda x, y: {x: y}, "ab", "AB")[0].a == "A";
assert dotsi.mapfy([{"x": {"y": "z"}}], lambda x: x)[0].x.y == "z";

# DotsiDict's copy method:
d = dotsi.fy({"data": {"users": [
    {"id": 0, "name": "Alice"},
    {"id": 1, "name": "Becci"},
]}});
c = d.copy();
assert c == d and c is not d;
assert c.data == d.data and c.data is d.data;       # Shallow
c.data.users[0].foo = "bar";
assert d.data.users[0].foo == "bar";
c.data.users[0].pop("foo");
assert "foo" not in d.data.users[0];

# DotsiList's copy method:
a = dotsi.fy([
    {"id": 0, "name": "Alice"},
    {"id": 1, "name": "Becci"},
    [],
]);
c = a.copy();
assert a == c and a is not c;
assert a[0] == c[0] and a[0] is c[0];               # Shallow
c[0].foo = "bar";
assert a[0].foo == "bar";
c[0].pop("foo");
assert "foo" not in a[0];
assert a[0] is c[0] and a[1] is c[1];
assert a[-1] is c[-1];
c[-1].append({"inner": "foo"});
assert a[-1][0].inner == "foo";       # As `a[-1] is c[-1]`.
c.pop(); assert len(c) == 2;
a.pop(); assert len(a) == 2;
c.append("topLevelElement");
assert len(c) == 3 and len(a) == 2;   # As `a is not c`.

# Deep-Copying:
d = dotsi.fy({"data": {"users": [
    {"id": 0, "name": "Alice"},
    {"id": 1, "name": "Becci"},
]}});
x = dotsi.deepCopy(d);
assert x == d and x is not d;
assert x.data == d.data and x.data is not d.data;   # Deep
assert x.data.users is not d.data.users;
assert x.data.users[0] is not d.data.users[0];
assert type(x) == type(d) == dotsi.Dict;
assert type(x.data.users) == type(d.data.users) == dotsi.List;
assert type(x.data.users[0]) == type(d.data.users[0]) == dotsi.Dict;
x.data.users[0].foo = "bar";
assert "foo" not in d.data.users[0];
assert x != d;
x.data.users[0].pop("foo");
assert x == d and x is not d;

# ALL TESTS PASSED!
print("\nGreat! All tests passed.\n");

# End ######################################################
