"""
Dotsi: Dot-accessible, update-aware Python dicts (& lists).

Copyright (c) 2020 Polydojo, Inc.

SOFTWARE LICENSING
------------------
The software is released "AS IS" under the MIT License,
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. Kindly
see LICENSE.txt for more details.

NO TRADEMARK RIGHTS
-------------------
The above software licensing terms DO NOT grant any right in the
trademarks, service marks, brand names or logos of Polydojo, Inc.
""";

__version__ = "0.0.3";      # Req'd by flit.
__NOOP__ = lambda: None;    # Blank-ish reference.

def mapObject (func, dicty):
    "Helper. Like builtin `map()` for dict-like objects.";
    result = type(dicty)(); # Start blank   # Retain type(x)
    for k in dicty: result[k] = func(dicty[k]);
    return result;

def dotsify (x):
    "Returns dot-accessible versions of pure dicts (& lists).";
    if type(x) is dict: return DotsiDict(mapObject(dotsify, x));
    if type(x) is list: return DotsiList(map(dotsify, x));
    return x;
fy = dotsify;       # Short ALIAS, externally: dotsi.fy()

def undotsify (x):
    "The opposite of `dotsify()`.";
    if type(x) is DotsiDict: return dict(mapObject(undotsify, x));
    if type(x) is DotsiList: return list(map(undotsify, x));
    return x;
unfy = undotsify;   # Short ALIAS, externally: dotsi.unfy()

def extend (tgt, *srcs):
    "Utility. Similar to `_.extend()` from Underscore.js.";
    for src in srcs: tgt.update(src);
    return tgt;

def deepCopy (x):       # Undocumented, unused.
    "Deep-copy a dict, dotsi.Dict, list, or dotsi.List.";
    if type(x) in [dict, DotsiDict]:
        return mapObject(deepCopy, x);      # Retains type(x)
    if type(x) in [list, DotsiList]:
        return type(x)(map(deepCopy, x));   # Retain type(x)
    return x;

def shallowCopy (x):    # Undocumented, used internally.
    "Shallow-copy a dict, dotsi.Dict, list, or dotsi.List.";
    identity = lambda y: y;
    if type(x) in [dict, DotsiDict]:
        return mapObject(identity, x);      # Retains type(x)
    if type(x) in [list, DotsiList]:
        return type(x)(map(identity, x));   # Retain type(x)
    return x;

class DotsiDict (dict):
    "Extends `dict` to support dot-access.";
    def __setitem__ (self, key, value):     # PRIMARY
        super(DotsiDict, self).__setitem__(key, dotsify(value));

    __setattr__ = __setitem__;
    __getattr__ = dict.__getitem__;
    __delattr__ = dict.__delitem__;
    
    def __init__ (self, *args, **kwargs):
        for k, v in dict(*args, **kwargs).items():
            self.__setitem__(k, v);
    update = __init__;
    
    def __or__ (self, other):   # Op: `self | other`
        if type(other) not in [dict, DotsiDict]:
            return NotImplemented;
        return extend(DotsiDict(), self, other);

    def __ror__ (self, other):  # Op: `other | self`
        if type(other) not in [dict, DotsiDict]:
            return NotImplemented;
        return extend(type(other)(), other, self);
    
    def __ior__ (self, other):
        return extend(self, other);
    
    def setdefault (self, key, default=None):
        if key not in self:
            self.__setitem__(key, default); # Auto-dotsify.
        return self[key];   # Note: `self[key]`, not `default`.
    
    def copy (self):    # Shallow copy.
        "Shallow-copy.";
        return shallowCopy(self);
Dict = DotsiDict;   # Short ALIAS, externally: dotsi.Dict()

class DotsiList (list):
    "Extends `list` to support dot-access for nested dicts.";
    def __setitem__ (self, index, value):   # PRIMARY
        super(DotsiList, self).__setitem__(index, dotsify(value));
    
    def insert (self, index, value):        # PRIMARY
        super(DotsiList, self).insert(index, dotsify(value));
    
    def append (self, value):
        self.insert(len(self), value);

    def extend (self, iterable):
        for value in iterable: self.append(value);
        return self;
    __iadd__ = extend;  # x += [1] <==> x.extend([1]);
    
    def __init__ (self, *args, **kwargs):
        self.extend(list(*args, **kwargs));
    
    def __add__ (self, other):
        return dotsify(list(self) + list(other));
    
    def copy (self):    # Shallow copy.
        "Shallow-copy.";
        return shallowCopy(self);
List = DotsiList;   # Short alias, externally: dotsi.List()

def refresh (obj, k=__NOOP__):
    "Refreshes dot-accessibility of `obj`, at key/index `k`.";
    assert type(obj) in [DotsiDict, DotsiList];
    if k is not __NOOP__: obj[k] = obj[k];
    elif type(obj) is DotsiDict:
        for k in obj: obj[k] = obj[k];
    elif type(obj) is DotsiList:
        for i in range(len(obj)): obj[i] = obj[i];
    return obj;

def defaults(tgt, *srcs):
    "Utility. Similar to `_.defaults()` from Underscore.js.";
    for src in srcs:
        for k in src:
            if k not in tgt: tgt[k] = src[k];
    return tgt;

def mapdotsify (fn, seq, *seqs):
    "Like built-in map(), but returns a dotsi.List.";
    if not seqs and callable(seq) and not callable(fn):
        fn, seq = seq, fn;
    return DotsiList(map(fn, seq, *seqs));
mapfy = mapdotsify; # Short ALIAS, externally: dotsi.mapfy()

# End ######################################################
