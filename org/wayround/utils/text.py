
import os
import re

import org.wayround.utils.terminal


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

    if width == None:
        if (
            (isinstance(fd, int) and os.isatty(fd))
            or (hasattr(fd, 'isatty') and fd.isatty())
            ):

            size = org.wayround.utils.terminal.get_terminal_size(fd)
            if size == None:
                width = 80
            else:
                width = size['ws_col']
        else:
            width = 80

    #print "width " + str(width)

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

    if columns == None:
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
    char = str(char)

    if len(char) < 1:
        char = ' '

    ret = char[0] * count
    return ret


def slice_string_to_sections(stri):
    return re.findall(r'[a-zA-Z]+|\d+|[\.\-\_\~\+]', stri)
