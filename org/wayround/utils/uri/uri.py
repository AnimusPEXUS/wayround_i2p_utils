import re

import path

from http import parse_all_data as parse_all_data_http

def parse_scheme_and_data(uri, ret_data=['scheme', 'data']):
    '''
    Parses URI and returns requested data.

    dici is returned if all ok. It will contain data relected by
    ret_data parameter.

    example:

       >>> parse_scheme_and_data('http://home.org:21/path')
       {'scheme': 'http', 'data': '//home.org:21/path'}
    '''

    ret = dict()

    re_res = re.match(r'(.*?):(.*)', uri)

    if re_res != None:
        scheme = re_res.group(1)
        data = re_res.group(2)

        for i in ['scheme', 'data']:
            if i in ret_data:
                ret[i] = eval(i)

        return ret
    else:
        return None

def _parse_r(uri, part):
    s = parse_scheme_and_data(uri, [part])
    if s is None or s[part] is None:
        ret = None
    else:
        ret = s[part]
    return ret

def parse_scheme(uri):
    """Returns URI scheme part"""
    return _parse_r(uri, 'scheme')

def parse_data(uri):
    """Returns URI data part"""
    return _parse_r(uri, 'data')

def parse(url = 'http://login:password@example.net:80/some/path?with=parameters&an=d#anchor'):
    """
    Parse URI and return None if error or dict structure accordingly
    to scheme name.

    This function, does not works with relative paths -- cases when
    there is no scheme present in URI -- None is returned.

    Currently, only http, https and ftp are allowed, and ftp treated
    as http.
    """
    scheme = parse_scheme(url)

    if scheme == None:
        return None

    re_res = re.match(r'(.*?):(.*)', url)

    if re_res != None:
        scheme = re_res.group(1)
        data = re_res.group(2)

        if scheme in ['http', 'https', 'ftp']:
            ret = parse_all_data_http(data)
            ret['scheme'] = scheme
            return ret
        else:
            return None


def is_same_host(uri1, uri2):

    return is_same_site(uri1, uri2, False, False)

def is_same_site(uri1,
                 uri2,
                 not_if_scheme_not_eql = True,
                 not_if_port_not_eql = True):

    u1 = parse(uri1)
    u2 = parse(uri2)

    lst = ['host']

    if not_if_scheme_not_eql:
        lst.append('scheme')

    if not_if_port_not_eql:
        lst.append('port')

    for i in lst:
        if u1[i] != u2[i]:
            return False

    return True

def del_not_same_hosts(uri, lst):
    ret = list()

    for i in lst:
        if is_same_host(uri, i):
            ret.append(i)

    return ret

def del_not_same_sites(uri,
                       lst,
                       not_if_scheme_not_eql = True,
                       not_if_port_not_eql = True
                       ):
    """
    Takes URI. Takes URI list. And then, compares lst items to uri,
    forming new list to return.

    If host not same, lst item not goes to returning list.

    Additional parameters adds filtering by scheme and post: usualy,
    if scheme is not same - site assumed not same, but not all
    software thinking this way. E.g. noscript, assumes http://s.s and
    https://s.s the same site, but Apache httpd - does not.
    """

    ret = list()

    for i in lst:
        if is_same_site(uri, i, not_if_scheme_not_eql, not_if_port_not_eql):
            ret.append(i)

    return ret

def is_child_uri(uri1, uri2,
                 not_if_scheme_not_eql = True,
                 not_if_port_not_eql = True):
    """
    Check is uri2 chiled to uri1
    """

    u1 = parse(uri1)
    u2 = parse(uri2)

    if u1 == None or u2 == None:
        return None

    if not is_same_site(uri1, uri2, not_if_scheme_not_eql, not_if_port_not_eql):
        return None

    if not path.is_child(u1['path_lst'], u2['path_lst']):
        return False

    return True



def del_not_child_uris(uri, lst):
    """
    Takes uri list, compares with uri and return list with uri childs
    """
    u = parse(uri)

    ret = list()

    for i in lst:
        if is_child_uri(uri, i):
            ret.append(i)

    return ret
