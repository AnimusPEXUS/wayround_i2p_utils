
import os
import re

import wayround_i2p.utils.terminal
import wayround_i2p.utils.types
import wayround_i2p.utils.range


def columned_list_print(
        lst, width=None, columns=None,
        margin_right=' | ', margin_left=' | ', spacing=' | ',
        fd=1
        ):
    print(
        return_columned_list(
            lst, width=width, columns=columns,
            margin_right=margin_right, margin_left=margin_left,
            spacing=spacing, fd=fd
            )
        )


def return_columned_list(
        lst, width=None, columns=None,
        margin_right=' | ', margin_left=' | ', spacing=' | ',
        fd=1
        ):

    if not wayround_i2p.utils.types.struct_check(
            lst,
            {'t': list, '.': {'t': str}}
            ):
        raise TypeError("`lst' must be list of str")

    if width is None:
        if (
                (isinstance(fd, int) and os.isatty(fd))
                or (hasattr(fd, 'isatty') and fd.isatty())
                ):

            size = wayround_i2p.utils.terminal.get_terminal_size(fd)
            if size is None:
                width = 80
            else:
                width = size['ws_col']
        else:
            width = 80

    # print "width " + str(width)

    longest = 0
    lst_l = len(lst)
    for i in lst:
        l = len(i)
        if l > longest:
            longest = l

    mrr_l = len(margin_right)
    mrl_l = len(margin_left)
    spc_l = len(spacing)

    int_l = width - mrr_l - mrl_l

    if columns is None:
        columns = int((int_l / (longest + spc_l)))

    if columns < 1:
        columns = 1

    ret = ''
    for i in range(0, lst_l, columns):
        # print "i == " + str(i)
        l2 = lst[i:i + columns]

        l3 = []
        for j in l2:
            l3.append(j.ljust(longest))

        while len(l3) != columns:
            l3.append(''.ljust(longest))

        ret += "{mrl}{row}{mrr}\n".format_map(
            {
                'mrl': margin_left,
                'mrr': margin_right,
                'row': spacing.join(l3)
                }
            )

    return ret


def fill(char=' ', count=80):
    raise Exception("Deprecated")
    char = str(char)

    if len(char) < 1:
        char = ' '

    ret = char[0] * count
    return ret


def slice_string_to_sections(stri):
    return re.findall(r'[a-zA-Z]+|\d+|[\.\-\_\~\+]', stri)


def get_line_ranges(txt, nl='\n'):

    # TODO: make fix to correct lenght of nl

    ret = []

    x = 0

    while True:

        y = txt.find(nl, x)

        if y == -1:
            ret.append(range(x, len(txt)))
            break
        else:
            ret.append(range(x, y + 1))
            x = y + 1

    return ret


def get_line_index_at_offset(offset, ranges):
    return wayround_i2p.utils.range.get_range_first_index(offset, ranges)


def str_to_encoded_bytes_list(in_str, encoding='utf-8'):

    if not isinstance(in_str, str):
        raise TypeError("`in_str' must be str")

    ret = []
    for i in in_str:
        ret.append(i.encode(encoding))

    return ret


def encoded_bytes_list_size(in_list):
    ret = 0
    for i in in_list:
        ret += len(i)
    return ret


def encoded_bytes_list_split_by_size(in_list, size):

    if not isinstance(size, int):
        raise TypeError("`size' must be int")

    if size < 0:
        raise ValueError("`size' must be positive")

    if size < 10:
        raise ValueError("`size' must be value of 10 or larger")

    ret = []

    new_lst = []
    new_lst_size = 0

    for i in in_list:

        len_i = len(i)

        if (new_lst_size + len_i) > size:
            ret.append(new_lst)
            new_lst = [i]
            new_lst_size = len_i
        else:
            new_lst.append(i)
            new_lst_size += len_i

    if len(new_lst) != 0:
        ret.append(new_lst)

    return ret


def merge_encoded_bylentes_lists_inside_list(in_list):
    for i in range(len(in_list)):
        in_list[i] = b''.join(in_list[i])
    return
