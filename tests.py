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

# ALL TESTS PASSED!
print("\nGreat! All tests passed.\n");

# End ######################################################
