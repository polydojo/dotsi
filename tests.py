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


# Operator `+` with dotsi.List:
a = dotsi.fy([0, 1, 2]);
b = a + [3, 4, 5];
assert type(a) == dotsi.List == type(b);
a += [3, 4, 5];
assert type(a) == dotsi.List == type(b);
assert a == b;
c = [-3, -2, -1] + a;
assert type(c) is list; # Note: `list`, _not_ `dotsi.List`.

# TODO: Write tests::
# Set-Item within nested dotsi.Dict:
# Set-item within nested dotsi.List:

li = dotsi.fy([0, 1, 2]);
li.append({"a": {"b": [0, 1, 2]}});
assert li[3].a.b == [0, 1, 2];

print("All tests passed.");

# End ######################################################
