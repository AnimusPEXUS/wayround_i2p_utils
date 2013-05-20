
"""
Module with package names parsing facilities
"""

import copy
import fnmatch
import logging
import os.path
import re
import datetime

import org.wayround.utils.list
import org.wayround.utils.tag
import org.wayround.utils.text

#Difficult name examples:
DIFFICULT_NAMES = [
    'GeSHi-1.0.2-beta-1.tar.bz2',
    'Perl-Dist-Strawberry-BuildPerl-5101-2.11_10.tar.gz',
    'bind-9.9.1-P2.tar.gz',
    'boost_1_25_1.tar.bz2',
    'dahdi-linux-complete-2.1.0.3+2.1.0.2.tar.gz',
    'dhcp-4.1.2rc1.tar.gz',
    'dvd+rw-tools-5.5.4.3.4.tar.gz',
    'lynx2.8.7rel.1.tar.bz2',
    'name.tar.gz',
    'ogre_src_v1-8-1.tar.bz2',
    'openssl-0.9.7a.tar.gz',
    'org.apache.felix.ipojo.manipulator-1.8.4-project.tar.gz',
    'pkcs11-helper-1.05.tar.bz2',
    'qca-pkcs11-0.1-20070425.tar.bz2',
    'tcl8.4.19-src.tar.gz',
    'wmirq-0.1-source.tar.gz',
    'xc-1.tar.gz',
    'xf86-input-acecad-1.5.0.tar.bz2',
    'xf86-input-elo2300-1.1.2.tar.bz2'
    ]
"""
Testing tarbal names
"""

ACCEPTABLE_SOURCE_NAME_EXTENSIONS = [
    '.tar.gz',
    '.tar.bz2',
    '.tar.xz',
    '.tar.lzma',
    '.zip',
    '.7z',
    '.tgz',
    '.tbz2',
    '.tbz'
    ]
"""
Acceptable source name extensions
"""

ALL_DELIMITERS = ['.', '_', '-', '+', '~']



def _find_possible_chared_versions_and_singles(name_sliced, separator='.'):
    """
    From sliced package name, return all possible versions
    """

    versions = []
    logging.debug("(internal1) versions delimitered by `{}': {}".format(separator, versions))

    version_started = None
    version_ended = None

    index = -1

    for i in name_sliced:
        index += 1

        if i.isdecimal():

            if version_started == None:
                version_started = index

            version_ended = index

        else:

            if version_started != None:
                if i != separator:
                    versions.append((version_started, version_ended + 1,))
                    version_started = None


    if version_started != None:
        versions.append((version_started, version_ended + 1,))
        version_started = None

    logging.debug("(internal2) versions delimitered by `{}': {}".format(separator, versions))

    singles = []
    multiples = []

    for i in versions:
        if i[1] - i[0] == 1:
            singles.append(i)
        elif i[1] - i[0] > 1:
            multiples.append(i)
        else:
            raise Exception("Programming error")

    logging.debug("(internal3) versions delimitered by `{}': {}".format(separator, versions))

    return {'singles': singles, 'version': multiples}

def _find_all_versions_and_singles(name_sliced):
    """
    Find all versions using :func:`_find_possible_chared_versions_and_singles`
    function
    """
    ret = dict()
    for i in ALL_DELIMITERS:
        ret[i] = _find_possible_chared_versions_and_singles(name_sliced, i)
        logging.debug("versions delimitered by `{}': {}".format(i, ret[i]))
    return ret

def _find_most_possible_version(name_sliced, mute=False):
    """
    Find most possible version in sliced package name
    """

    ret = None

    possible_versions_and_singles_grouped_by_delimeter = \
        _find_all_versions_and_singles(name_sliced)

    logging.debug(
        "possible_versions_and_singles_grouped_by_delimeter: {}".format(
            repr(
                 possible_versions_and_singles_grouped_by_delimeter
                 )
            )
        )

    possible_versions_grouped_by_delimeter = {}
    possible_singles_grouped_by_delimeter = {}

    for i in ALL_DELIMITERS:

        possible_versions_grouped_by_delimeter[i] = \
            possible_versions_and_singles_grouped_by_delimeter[i]['version']

        possible_singles_grouped_by_delimeter[i] = \
            possible_versions_and_singles_grouped_by_delimeter[i]['singles']

    for i in ALL_DELIMITERS:

        if isinstance(ret, (tuple, int)):
            break

        l_possible_versions_grouped_by_delimeter_i = (
            len(possible_versions_grouped_by_delimeter[i])
            )

        if  l_possible_versions_grouped_by_delimeter_i == 0:
            pass

        elif l_possible_versions_grouped_by_delimeter_i == 1:
            ret = possible_versions_grouped_by_delimeter[i][0]
            break
        else:

            current_delimiter_group = possible_versions_grouped_by_delimeter[i]

            maximum_length = 0

            for j in current_delimiter_group:
                l = j[1] - j[0]
                if l > maximum_length:
                    maximum_length = l

            if maximum_length == 0:
                s = "Version not found in group `{}'".format(i)
                if not mute:
                    logging.error(s)
                else:
                    logging.debug(s)
            else:

                lists_to_compare = []

                logging.debug("lists_to_compare: {}".format(repr(lists_to_compare)))

                for j in current_delimiter_group:
                    l = j[1] - j[0]
                    if l == maximum_length:
                        lists_to_compare.append(j)

                l = len(lists_to_compare)
                if l == 0:
                    ret = None
                elif l == 1:
                    ret = lists_to_compare[0]
                else:

                    most_possible_version2 = lists_to_compare[0]

                    for j in lists_to_compare:
                        if j[0] < most_possible_version2[0]:
                            most_possible_version2 = j

                    logging.debug("most_possible_version2: {}".format(repr(most_possible_version2)))
                    ret = most_possible_version2
                    break

    if ret == None:
        for i in ALL_DELIMITERS:

            if isinstance(ret, (tuple, int)):
                break

            l_possible_singles_grouped_by_delimeter_i = (
                len(possible_singles_grouped_by_delimeter[i])
                )

            if  l_possible_singles_grouped_by_delimeter_i == 0:
                pass

            elif l_possible_singles_grouped_by_delimeter_i == 1:
                ret = possible_singles_grouped_by_delimeter[i][0]
                break
            else:

                most_possible_version3 = possible_singles_grouped_by_delimeter[i][0]

                for j in possible_singles_grouped_by_delimeter[i]:
                    if j[0] < most_possible_version3[0]:
                        most_possible_version3 = j

                logging.debug("most_possible_version3: {}".format(repr(most_possible_version3)))
                ret = most_possible_version3
                break


    logging.debug("most_possible_version: {}".format(repr(ret)))

    return ret


def _source_name_parse_delicate(filename, mute=False):

    """
    Main source name parsing function

    Do not use this directly, use source_name_parse() instead.
    """

    filename = os.path.basename(filename)

    logging.debug("Parsing source file name {}".format(filename))

    ret = None

    extension = None
    for i in ACCEPTABLE_SOURCE_NAME_EXTENSIONS:
        if filename.endswith(i):
            extension = i

    if extension == None:
        s = "Wrong extension"
        if not mute:
            logging.error(s)
        else:
            logging.debug(s)
        ret = 1
    else:
        without_extension = filename[:-len(extension)]

        name_sliced = org.wayround.utils.text.slice_string_to_sections(without_extension)

        most_possible_version = _find_most_possible_version(name_sliced, mute)

        if not isinstance(most_possible_version, tuple):
            ret = None
        else:
            ret = {
                'name': None,
                'groups': {
                    'name'              : None,
                    'extension'         : None,

                    'version'           : None,
                    'version_list_dirty': None,
                    'version_list'      : None,
                    'version_dirty'     : None,

                    'status'            : None,
                    'status_list_dirty' : None,
                    'status_dirty'      : None,
                    'status_list'       : None,
                    }
                }

            ret['name'] = filename

            ret['groups']['name'] = ''.join(
                name_sliced[:most_possible_version[0]]
                ).strip(''.join(ALL_DELIMITERS))

            # version operations

            ret['groups']['version_list_dirty'] = (
                name_sliced[most_possible_version[0]:most_possible_version[1]]
                )

            ret['groups']['version_list'] = (
                copy.copy(ret['groups']['version_list_dirty'])
                )

            org.wayround.utils.list.remove_all_values(
                ret['groups']['version_list'],
                ALL_DELIMITERS
                )

            ret['groups']['version'] = (
                '.'.join(ret['groups']['version_list'])
                )

            ret['groups']['version_dirty'] = (
                ''.join(ret['groups']['version_list_dirty'])
                )

            # status operations

            ret['groups']['status_list_dirty'] = (
                name_sliced[most_possible_version[1]:]
                )

            ret['groups']['status_list_dirty'] = (
                org.wayround.utils.list.list_strip(
                    ret['groups']['status_list_dirty'],
                    ALL_DELIMITERS
                    )
                )

            ret['groups']['status_list'] = (
                copy.copy(ret['groups']['status_list_dirty'])
                )


            org.wayround.utils.list.remove_all_values(
                ret['groups']['status_list'],
                ALL_DELIMITERS
                )

            ret['groups']['status_list'] = (
                org.wayround.utils.list.list_strip(
                    ret['groups']['status_list'],
                    ALL_DELIMITERS
                    )
                )

            ret['groups']['status'] = '.'.join(ret['groups']['status_list'])

            ret['groups']['status_dirty'] = ''.join(ret['groups']['status_list_dirty'])

            # extension

            ret['groups']['extension'] = extension


    return ret

def parse_tarball_name(
    filename,
    mute=False
    ):
    """
    Parse source file name and do some more actions on success

    If this function succeeded but not passed version check -
    return None.

    If this function succided, passeed version check and
    \`modify_info_file\' is True -
    update infofile in info directory.

    If this function succeeded, dict is returned::

        {
            'name': None,
            'groups': {
                'name'              : None,
                'extension'         : None,

                'version'           : None,
                'version_list_dirty': None,
                'version_list'      : None,
                'version_dirty'     : None,

                'status'            : None,
                'status_list_dirty' : None,
                'status_dirty'      : None,
                'status_list'       : None,
                }
            }

    .. NOTE:: version numbers are always joined with \`.\'
    """

    ret = _source_name_parse_delicate(filename, mute)

    if not isinstance(ret, dict):
        if not mute:
            logging.info("No match `{}'".format(filename))

        ret = None

    return ret

def parse_test():
    """
    Run parser on all difficult names (:data:`DIFFICULT_NAMES`) in test purposes
    """

    for i in DIFFICULT_NAMES:
        logging.info("====== Testing parser on `{}' ======".format(i))
        if not isinstance(parse_tarball_name(i), dict):
            logging.error("Error parsing file name `{}' - parser not matched".format(i))

    return
