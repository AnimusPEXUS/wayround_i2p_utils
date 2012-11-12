
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
