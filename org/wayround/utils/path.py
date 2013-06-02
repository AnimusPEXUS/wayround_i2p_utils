
import copy
import os.path

S_SEP = os.path.sep
D_SEP = S_SEP * 2

# TODO: documentation for all functions

def _remove_double_sep(str_in):

    while D_SEP in str_in:
        str_in = str_in.replace(D_SEP, S_SEP)

    return str_in

def _remove_tariling_slash(str_in):

    ret = str_in

    while ret.endswith(S_SEP):
        ret = ret[:-1]

    if len(ret) == 0:
        ret = S_SEP

    return ret

def join(*args):

    for i in args:
        if not isinstance(i, (str, list,)):
            raise ValueError("arguments must be strings or lists")

    if len(args) == 0:
        raise TypeError("missing 1 required positional argument: 'args'")

    abso = False
    if len(args) != 0 and len(args[0]) != 0:
        abso = args[0][0] == S_SEP

    ret_l = []

    for i in args:

        if isinstance(i, list):

            ret_l += join(*i).split(S_SEP)

        else:
            ret_l += i.split(S_SEP)


    while '' in ret_l:
        ret_l.remove('')

    ret = S_SEP.join(ret_l)

    if abso:
        ret = S_SEP + ret

    return ret

def split(path):

    absp = path.startswith('/')

    path = _remove_double_sep(path)
    path = _remove_tariling_slash(path)

    ret = path.split('/')

    while '' in ret:
        ret.remove('')

    if absp:

        ret.insert(0, '/')

    return ret


def normpath(path):
    return _remove_double_sep(os.path.normpath(path))

def abspath(path):
    return _remove_double_sep(os.path.abspath(path))

def relpath(path, start):
    return _remove_double_sep(os.path.relpath(path, start))

def realpath(filename):
    return _remove_double_sep(os.path.realpath(filename))

def realpaths(lst):

    lst = copy.copy(lst)

    for i in range(len(lst)):
        lst[i] = realpath(lst[i])

    lst = list(set(lst))

    return lst

# NOTE: does not work
#def eval_abs_paths(lst, g, l):
#
#    """
#    Ensure(make) listed variables are(be) absolute path
#    """
#
#    for i in lst:
#        if i in l:
#            l[i] = abspath(l[i])
#
#    return

def prepend_path(lst, base):
    """
    Removes any trailing sep from base, and inserts it in the start of every
    lst item. if item not starts with separator, inserts it between base and item
    """

    lst = copy.copy(lst)

    while base.endswith(S_SEP):
        base = base[:-1]

    for i in range(len(lst)):
        sep = ''

        if lst[i][0] != S_SEP:
            sep = S_SEP

        lst[i] = base + sep + lst[i]

    lst = list(set(lst))

    return lst

def unprepend_path(lst, base):
    """
    Removes any trailing sep from base, and removes it from the start of every
    lst item.
    """

    while base.endswith(S_SEP):
        base = base[:-1]

    for i in lst:
        if not (i + S_SEP).startswith(base + S_SEP):
            raise ValueError("Not all items in lst have base `{}'".format(base))

    lst = copy.copy(lst)

    base_l = len(base)

    for i in range(len(lst)):

        lst[i] = lst[i][base_l:]

    lst = list(set(lst))

    return lst

def insert_base(path, base):
    return prepend_path([path], base)[0]

def remove_base(path, base):
    return unprepend_path([path], base)[0]
