
import copy
import os.path

D_SEP = os.path.sep * 2
S_SEP = os.path.sep


def _remove_double_sep(str_in):

    while D_SEP in str_in:
        str_in = str_in.replace(D_SEP, S_SEP)

    return str_in

def _remove_tariling_slash(str_in):

    ret = str_in

    while ret.endswith('/'):
        ret = ret[:-1]

    return ret

def join(*args):

    ret = ''

    for i in args:
        ret += i + S_SEP

    ret = _remove_double_sep(ret)
    ret = _remove_tariling_slash(ret)

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
    lst item. it item not starts with sep, inserts set between base and item
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

def insert_base(path, base_dir):

    """
    Parameters always absolute
    Result is always absolute
    """

    path = abspath(path)
    base_dir = abspath(base_dir)

    return abspath(join(base_dir, path))

def remove_base(path, base_dir):

    """
    Parameters always absolute
    Result is always absolute
    """
    path = abspath(path)
    base_dir = abspath(base_dir)

    ret = path

    if base_dir != '/' and ret.startswith(base_dir):
        ret = ret[len(base_dir):]

    return abspath(ret)
