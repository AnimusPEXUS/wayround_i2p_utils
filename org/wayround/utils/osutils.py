
import os
import copy


def env_vars_edit(var_list, mode='copy'):
    """
    Environment preparations
    """

    ret = {}

    if mode == 'copy':
        ret = copy.copy(os.environ)
    elif mode == 'clean':
        ret = {}
    else:
        raise ValueError

    if mode != 'clean':
        for i in list(var_list.keys()):
            if var_list[i] is None and i in ret:
                del(ret[i])
            else:
                ret[i] = var_list[i]

    return ret


def list_dirs_for_so_files():
    """
    Return list of system directories in which shared object (so) files are
    stored. basicly it is lines from /etc/ld.co.conf + splitted values from
    LD_LIBRARY_PATH environment variable
    """

    ret = []

    return ret
