"""
Check object type by searching it's attributes

This module supports two kinds of operation:
    1. Stranded - using original method of type recognition
    2. Native - using Python isinstance built-in function

Examples of execution:

import lxml.etree

import org.wayround.utils.types

>org.wayround.utils.types.types_n(lxml.etree.Element('q'))
['Hashable', 'Sized', 'Iterable', 'Container']

>org.wayround.utils.types.types_s(lxml.etree.Element('q'))
['Hashable', 'Sized', 'Mapping', 'Iterable', 'Container']
"""

import collections.abc

# This table is taken from python-3.3.2-docs-html/library/collections.abc.html

COMPARISON_TABLE = {
    'Container': {
        'i': [],
        'a': ['__contains__'],
        'm': []
        },
    'Hashable': {
        'i': [],
        'a': ['__hash__'],
        'm': []
        },
    'Iterable': {
        'i': [],
        'a': ['__iter__'],
        'm': []
        },
    'Iterator': {
        'i': ['Iterable'],
        'a': ['__next__'],
        'm': ['__iter__']
        },
    'Sized': {
        'i': [],
        'a': ['__len__'],
        'm': []
        },
    'Callable': {
        'i': [],
        'a': ['__call__'],
        'm': []
        },
    'Sequence': {
        'i': ['Sized', 'Iterable', 'Container'],
        'a': ['__getitem__', '__len__'],
        'm': ['__contains__', '__iter__', '__reversed__', 'index', 'count']
        },
    'MutableSequence': {
        'i': ['Sequence'],
        'a': ['__getitem__', '__setitem__', '__delitem__', '__len__', 'insert'],
        'm': ['append', 'reverse', 'extend', 'pop', 'remove', '__iadd__']
        },
    'Set': {
        'i': ['Sized', 'Iterable', 'Container'],
        'a': ['__contains__', '__iter__', '__len__'],
        'm': ['__le__', '__lt__', '__eq__', '__ne__', '__gt__', '__ge__',
              '__and__', '__or__', '__sub__', '__xor__', 'isdisjoint']
        },
    'MutableSet': {
        'i': ['Set'],
        'a': ['__contains__', '__iter__', '__len__', 'add', 'discard'],
        'm': ['clear', 'pop', 'remove', '__ior__', '__iand__',
              '__ixor__', '__isub__']
        },
    'Mapping': {
        'i': ['Sized', 'Iterable', 'Container'],
        'a': ['__getitem__', '__iter__', '__len__'],
        'm': ['__contains__', 'keys', 'items', 'values', 'get', '__eq__',
              '__ne__']
        },
    'MutableMapping': {
        'i': ['Mapping'],
        'a': ['__getitem__', '__setitem__', '__delitem__', '__iter__',
              '__len__'],
        'm': ['pop', 'popitem', 'clear', 'update', 'setdefault']
        },
    }

def check_type_s(obj, name):

    """
    Check type using stranded method
    """

    if not name in COMPARISON_TABLE.keys():
        raise ValueError("Invalid type name")

    ret = True

    ref_type = COMPARISON_TABLE[name]

    for i in ref_type['i']:

        if not check_type_s(obj, i):
            ret = False
            break

    if ret:
        for i in ref_type['a']:
            if not hasattr(obj, i):
                ret = False
                break

    if ret:
        for i in ref_type['m']:
            if not hasattr(obj, i):
                ret = False
                break

    return ret

def types_s(obj):

    """
    Make list of types object in, using stranded method
    """

    ret = []

    for name in COMPARISON_TABLE.keys():
        if check_type_s(obj, name):
            ret.append(name)

    return ret

def check_type(obj, name):

    """
    Check type using native method
    """

    if not name in COMPARISON_TABLE.keys():
        raise ValueError("Invalid type name")

    return isinstance(obj, eval('collections.abc.{}'.format(name)))

def types(obj):

    """
    Make list of types object in, using native method
    """

    ret = []

    for name in COMPARISON_TABLE.keys():
        if check_type(obj, name):
            ret.append(name)

    return ret


for i in COMPARISON_TABLE.keys():
    exec(
"""
def is{name}_s(obj):
    return check_type_s(obj, {name})
""".format(name=i)
        )

del i

for i in COMPARISON_TABLE.keys():
    exec(
"""
def is{name}(obj):
    return check_type(obj, {name})
""".format(name=i)
        )

del i

