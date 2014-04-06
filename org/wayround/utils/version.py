
"""
Version comparison utilities
"""

import logging

import org.wayround.utils.tarball_name_parser


def source_version_comparator(name1, name2):

    ret = 0

    d1 = org.wayround.utils.tarball_name_parser.parse_tarball_name(
        name1,
        mute=True
        )

    d2 = org.wayround.utils.tarball_name_parser.parse_tarball_name(
        name2,
        mute=True
        )

    if d1 == None or d2 == None:
        raise Exception("Can't parse filename")

    if d1['groups']['name'] != d2['groups']['name']:
        raise ValueError(
            "Files has different names: `{}' ({}) and `{}' ({})".format(
                d1['groups']['name'], name1,
                d2['groups']['name'], name2
                )
            )

    else:
        com_res = standard_comparison(
            d1['groups']['version_list'], d1['groups']['status_list'],
            d2['groups']['version_list'], d2['groups']['status_list']
            )

        if com_res != 0:
            ret = com_res
        else:
            ret = 0

    if ret == -1:
        logging.debug(name1 + ' < ' + name2)
    elif ret == 1:
        logging.debug(name1 + ' > ' + name2)
    else:
        logging.debug(name1 + ' = ' + name2)

    return ret


def standard_comparator(
    version1,
    version2
    ):

    logging.debug("standard_comparator: `{}', `{}'".format(version1, version2))

    int_v1 = version1
    int_v2 = version2

    i1_error = False
    i2_error = False

    if isinstance(version1, str):
        int_v1 = version1.split('.')

    if isinstance(version2, str):
        int_v2 = version2.split('.')

    if not isinstance(int_v1, list):
        i1_error = True
    else:
        for i in int_v1:
            if not isinstance(i, (int, str)):
                i1_error = True

    if not isinstance(int_v2, list):
        i2_error = True
    else:
        for i in int_v2:
            if not isinstance(i, (int, str)):
                i2_error = True

    if i1_error:
        raise ValueError(
            "standart_comparison parameters must be [lists of [str or int]]"
            " or [strings], not {}".format(int_v1)
            )

    if i2_error:
        raise ValueError(
            "standart_comparison parameters must be [lists of [str or int]]"
            " or [strings], not {}".format(int_v2)
            )

    ret = standard_comparison(int_v1, None, int_v2, None)
    logging.debug("standard_comparator ret: `{}'".format(ret))
    return ret


def standard_comparison(
    version_list1, status_list1,
    version_list2, status_list2
    ):

    vers_comp_res = None
    stat_comp_res = None

    vers1 = version_list1
    vers2 = version_list2

    longer = None

    v1l = len(vers1)
    v2l = len(vers2)

    #  length used in first comparison part
    el_1 = v1l

    if v1l == v2l:
        longer = None
        el_1 = v1l

    elif v1l > v2l:
        longer = 'vers1'
        el_1 = v2l

    else:
        longer = 'vers2'
        el_1 = v1l

    # first comparison part

    for i in range(el_1):

        if int(vers1[i]) > int(vers2[i]):
            logging.debug(vers1[i] + ' > ' + vers2[i])
            vers_comp_res = +1
            break
        elif int(vers1[i]) < int(vers2[i]):
            logging.debug(vers1[i] + ' < ' + vers2[i])
            vers_comp_res = -1
            break
        else:
            continue

    # second comparison part
    if vers_comp_res == None:
        if longer != None:
            if longer == 'vers1':
                logging.debug(str(vers1) + ' > ' + str(vers2))
                vers_comp_res = +1
            else:
                logging.debug(str(vers1) + ' > ' + str(vers2))
                vers_comp_res = -1

    if vers_comp_res == None:
        vers_comp_res = 0

    if vers_comp_res == 0:
        if status_list1 != None and status_list2 != None:
            s1 = '.'.join(status_list1)
            s2 = '.'.join(status_list2)
            if s1 > s2:
                stat_comp_res = +1
            elif s1 < s2:
                stat_comp_res = -1
            else:
                stat_comp_res = 0

            vers_comp_res = stat_comp_res

    ret = vers_comp_res

    return ret
