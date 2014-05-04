
import copy
import os.path

S_SEP = os.path.sep
D_SEP = S_SEP * 2

# TODO: documentation for all functions

def _remove_double_sep(str_in):

    if not isinstance(str_in, str):
        raise ValueError("str_in must be str")

    while D_SEP in str_in:
        str_in = str_in.replace(D_SEP, S_SEP)

    return str_in

def _remove_tariling_slash(str_in):

    if not isinstance(str_in, str):
        raise ValueError("str_in must be str")

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

    if not isinstance(path, str):
        raise ValueError("path must be str")

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
    if not isinstance(path, str):
        raise ValueError("path must be str")
    return _remove_double_sep(os.path.normpath(path))

def abspath(path):
    if not isinstance(path, str):
        raise ValueError("path must be str")
    return _remove_double_sep(os.path.abspath(path))

def relpath(path, start):
    if not isinstance(path, str):
        raise ValueError("path must be str")
    if not isinstance(start, str):
        raise ValueError("start must be str")
    return _remove_double_sep(os.path.relpath(path, start))

def realpath(path):
    if not isinstance(path, str):
        raise ValueError("path must be str")
    return _remove_double_sep(os.path.realpath(path))

def realpaths(lst, remove_duplications=True):

    ret = list()

    for i in lst:
        ret.append(realpath(i))

    if remove_duplications:
        ret = list(set(ret))

    return ret

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

    if not isinstance(lst, list):
        raise TypeError("lst must be list")

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
    if not isinstance(path, str):
        raise ValueError("path must be str")
    return prepend_path([path], base)[0]

def remove_base(path, base):
    if not isinstance(path, str):
        raise ValueError("path must be str")
    return unprepend_path([path], base)[0]

def bases(lst):

    """
    Removes dirnames from paths
    """

    if not isinstance(lst, list):
        raise TypeError("lst must be list")

    ret = []

    for i in lst:
        ret.append(os.path.basename(i))

    return ret

def exclude_files_not_in_dirs(files, dirs):

    if not isinstance(files, list):
        raise TypeError("files must be list")

    if not isinstance(dirs, list):
        raise TypeError("dirs must be list")

    ret = []

    for i in files:

        d = os.path.dirname(i)

        if d in dirs:
            ret.append(i)

    return ret

def path_length(string):
    return len(split(string))
