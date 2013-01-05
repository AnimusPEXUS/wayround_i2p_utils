
import copy
import os.path

D_SEP = os.path.sep * 2
S_SEP = os.path.sep


def _remove_double_sep(str_in):

    while D_SEP in str_in:
        str_in = str_in.replace(D_SEP, S_SEP)

    return str_in


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

