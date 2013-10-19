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


STRUCT_CHECK_KEYS = ['t', 'te', 'None', '<', '>', '.', '', ' ', '{}']

def struct_check(value, struct):

    """
    Check whatever value corresponds to struct

    This implementation can't check dict with non-str keys, so exception is
    raised in this case

    Examples of `struct':


    {
    't': list, # type or tuple of types (like in isinstance). can also be a
               # string or tuple of strings with type names. see desc below
    'te': True, # exact type check with `type' function. default is True.
    'None': False, # can value be None? (False - default)
    '<': 0, # min child count. None - is default - no check
    '>': None, # max child count. None - is default - no check
    '.': { # check children. for work with sequences. default is None - not
           #                                                 check children
         't': list,
         '<': 1,
         '>': None,
         '.': {
              't': _Element
              }
         } # - default is None

    # works only if 't' is str or bytes
    '': False,
    ' ': False,  # '' - string emptiness allow or not,
                 # ' ' - only spaces in string allow or not

    '{}': {}, # if 't' is dict and only dict: True - any keys are possible and
              # each child checked with '.' value (recursion). False - same
              # as True, but without values checking (dafault)
              # if '{}' is dict, then all values in this dict must be dicts
              # with structures like this.
    }

    if 't' value is of type str, then value type is checked using this module's
    types() or types_s(): if '!' in beginnonig of 't' value, then types_s() is
    used

    return False if value does not matches struct, and True otherwise
    """

    ret = True

    if not type(struct) == dict:
        raise TypeError("`struct' must be dict")

    for i in list(struct.keys()):
        if not i in STRUCT_CHECK_KEYS:
            raise ValueError("invalid `struct' key: {}".format(i))

    typ = struct['t']

    if type(typ) != tuple:
        typ = typ,

    iterable_type = types(value)
    iterable_type = (
        'Sequence' in iterable_type
        or 'Iterator' in iterable_type
        or 'Iterable' in iterable_type
        )


    for i in typ:
        t_type = type(i)
        if t_type == str:
            if i.startswith('!'):
                if not i[1:] in COMPARISON_TABLE.keys():
                    raise ValueError("Invalid type name")
            else:
                if not i in COMPARISON_TABLE.keys():
                    raise ValueError("Invalid type name")


    type_exact = True
    if 'te' in struct:
        type_exact = struct['te']
        if type(type_exact) != bool:
            raise TypeError("`te' must be bool")

    can_be_none = False
    if 'None' in struct:
        can_be_none = struct['None']
        if type(can_be_none) != bool:
            raise TypeError("`None' must be bool")

    min_child_count = None
    if '<' in struct:
        min_child_count = struct['<']
        if min_child_count != None and not type(min_child_count) == int:
            raise TypeError("`<' must be None or int")

    max_child_count = None
    if '>' in struct:
        max_child_count = struct['>']
        if max_child_count != None and not type(max_child_count) == int:
            raise TypeError("`>' must be None or int")

    string_emptiness = True
    if '' in struct:
        string_emptiness = struct['']
        if type(string_emptiness) != bool:
            raise TypeError("`' must be bool")

    string_is_space = True
    if ' ' in struct:
        string_is_space = struct[' ']
        if type(string_is_space) != bool:
            raise TypeError("` ' must be bool")

    next_test = None
    if '.' in struct:
        if value is not None:
            next_test = struct['.']
            if next_test != None and not type(next_test) == dict:
                raise TypeError("`.' must be None or dict")

            if next_test != None and not iterable_type:
                raise ValueError(
                    "`.' is not None so value must be a sequence or iterable"
                    )

    dict_info = False
    if '{}' in struct:
        dict_info = struct['{}']
        if not type(dict_info) in [bool, dict]:
            raise TypeError(
                "`{{}}' must be bool or dict, but it's a: {}".format(
                    type(dict_info)
                    )
                )

        keys = list(dict_info.keys())

        for i in keys:
            if not type(i) == str:
                raise ValueError("keys in struct dict must be str")

            if not type(dict_info[i]) == dict:
                raise ValueError("values in struct dict must be dict")

    if not can_be_none and value == None:
        ret = False

    if ret:
        if type_exact == True:
            found = False
            for i in typ:
                t_type = type(i)
                if t_type == str:
                    if i.startswith('!'):
                        if i[1:] in types_s(value):
                            found = True
                            break
                    else:
                        if i in types(value):
                            found = True
                            break
                else:
                    if type(value) == i:
                        found = True
                        break

            if not found:
                ret = False
        else:
            if not isinstance(value, typ):
                ret = False


    if ret:
        if min_child_count != None:
            if len(value) < min_child_count:
                ret = False

    if ret:
        if max_child_count != None:
            if len(value) > max_child_count:
                ret = False

    if ret:
        if type(value) == str and value == '' and string_emptiness == False:
            ret = False

    if ret:
        if type(value) == bytes and value == b'' and string_emptiness == False:
            ret = False

    if ret:
        if type(value) == str and value.isspace() and string_is_space == False:
            ret = False

    if ret:
        if type(value) == bytes and value.isspace() and string_is_space == False:
            ret = False

    if ret:
        if len(typ) == 1 and typ[0] == dict:
            if type(dict_info) == dict:

                keys = list(dict_info.keys())
                for i in keys:
                    if not i in value:
                        ret = False
                        break
                    else:
                        ret = struct_check(value[i], dict_info[i])
                        if ret == False:
                            break

                keys = list(value.keys())
                for i in keys:
                    if not i in dict_info:
                        ret = False
                        break

            elif dict_info == False:
                pass

            elif dict_info == True:
                vkeys = list(value.keys())
                for i in vkeys:
                    ret = struct_check(value[i], next_test)
                    if ret == False:
                        break
            else:
                raise Exception("Programming error")

    if ret:
        if next_test != None:
            if iterable_type:
                for i in value:
                    if struct_check(i, next_test) == False:
                        ret = False
                        break

            else:
                ret = False

    return ret








