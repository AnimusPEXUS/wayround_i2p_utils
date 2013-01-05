import re
import copy

"""
This module contains functions for parsing http uri(url) data.

It is also contains functions for comparing paths.
"""

from path import paths_by_path


def parse_parameters(data):
    """
    Parse URI parameter string to list and returns it

    Parameters can repeat

    examples:

       >>> parse_parameters('?a=1&b=2')
       [['a', '1'], ['b', '2']]

       >>> parse_parameters('a=1&b=2&a=3')
       [['a', '1'], ['b', '2'], ['a', '3']]

    """
    t_data = data.lstrip('?')

    data_splitted = t_data.split('&')

    para_list = []

    for i in data_splitted:
        para_splitted = i.split('=')
        if len(para_splitted) == 1:
            para_splitted.append(None)
        para_list.append(para_splitted)

    return copy.copy(para_list)

def parse_auth(data):
    """
    Parses URI authentication string to parts.

    Returns None if data == None or data == ''

    Else, returns dict with two values:

       - login: login part
       - password: password part

    examples:

       >>> parse_auth('123123@')
       {'login': '123123', 'password': None}

       >>> parse_auth('123123:@')
       {'login': '123123', 'password': ''}
       
       >>> parse_auth('123123:123@')
       {'login': '123123', 'password': '123'}
       
       >>> parse_auth(':123@')
       {'login': '', 'password': '123'}
       
       >>> parse_auth(':@')
       {'login': '', 'password': ''}
       
       >>> parse_auth(':')
       {'login': '', 'password': ''}
       
       >>> parse_auth('')
       None
       
       >>> parse_auth(None)
       None

    """
    if data == None or data == '':
        return None

    re_res = re.match(r'^(.*?)(:.*?)?@?$', data)

    if re_res != None:
        login = re_res.group(1)
        password = None
        if re_res.group(2) != None:
            password = re_res.group(2)[1:]
        else:
            password = None

        return {'login': login, 'password': password}
    else:
        return None

def parse_all_data(data):
    '''
    Can be deployed to strings like C{//agu:@wayround.org:21/1/2/3/4/?a#3}

    Such a string then will be parsed on several parts. Then thous
    parts will be worked out to dict like:

       >>> repr()
       {'anchor': '3',
        'auth': {'login': 'agu', 'password': ''},
        'host': 'wayround.org',
        'param_lst': [['a', None]],
        'path_lst': ['1', '2', '3', '4'],
        'path_str': '/1/2/3/4',
        'path_is_absolute': True,
        'last_el_type': 'file',
        'port': '21'}

    '''
    ret = dict(
        auth = None,            # or dict {'login':'', 'password':
            # ''}, where login must be string, and
        # password can be None
        host = None,
        port = None,
        path_str = None,
        path_lst = None,
        last_el_type = None,
        path_is_absolute = None,
        param_lst = None,
        anchor = None
        )

    re_res = re.match(r'^//(.*@)?(.*?)(:\d*)?(/.*?)?(\?.*?)?(\#.*)?$', data)

    if re_res != None:
        # print 'auth: '+ repr(re_res.group(1))
        # print 'host: '+ repr(re_res.group(2))
        # print 'port: '+ repr(re_res.group(3))
        # print 'path: '+ repr(re_res.group(4))
        # print 'para: '+ repr(re_res.group(5))
        # print '  id: '+ repr(re_res.group(6))
        # print

        ret['auth'] = parse_auth(re_res.group(1))

        if re_res.group(2) != None:
            ret['host'] = re_res.group(2)

        if re_res.group(3) != None:
            ret['port'] = re_res.group(3)[1:]

        if re_res.group(4) != None:
            t_p = paths_by_path(re_res.group(4))
            if t_p == None:
                ret['path_str'] = None
                ret['path_lst'] = None
                ret['last_el_type'] = None
                ret['path_is_absolute'] = None
            else:
                ret['path_str'] = t_p['path_str']
                ret['path_lst'] = t_p['path_lst']
                ret['last_el_type'] = t_p['last_el_type']
                ret['path_is_absolute'] = t_p['path_is_absolute']


        if re_res.group(5) != None:
            ret['param_lst'] = parse_parameters(re_res.group(5))

        if re_res.group(6) != None:
            ret['anchor'] = re_res.group(6)[1:]

        return ret
    return None

def combine_data(scheme     = 'http',
                 auth       = {'login': 'anonymous',
                               'password': 'myemail'},
                 host       = 'example.net',
                 port       = 80,
                 path       = '/',
                 parameters = {},
                 anchor     = ''):
    '''
    Constructs URI string from parameters

    auth tuple can be complitly None or password can be None. auth
    login must allways be string or unicode, password too.

    port automaticly set to 80 or 443 if http or https scheme
    accordingly.

    parameters can be None or dicrionary like {'name':'value'}
    '''
    res = ''

    auth_str   = ''
    port_str   = ''
    use_port   = False
    param_str  = ''
    use_param  = False
    anchor_str = ''
    use_anchor = False


    if auth != None:
        auth_str = auth[0]
        if auth[1] != None:
            auth_str += ':'+auth[1]
        auth_str += '@'


    if scheme == 'http' and port != 80:
        use_port = True

    if scheme == 'https' and port != 443:
        use_port = True

    if use_port:
        port_str = ':'+str(port)

    if parameters != None and len(parameters.keys()) > 0:
        use_param = True

    if isinstance(path, list):
        path_string = '/'.join(path)

    if use_param:
        param_str = '?'
        param_lst = []
        for i in parameters.keys():
            p2 = parameters[i]

            for  tpe in [int, long, float]:
                if isinstance(p2, tpe):
                    p2 = unicode(p2)

            if isinstance(p2, str):
                p2.decode('utf-8')

            param_lst.append(unicode(i)+'='+p2)

        param_str += '&'.join(param_lst)

    if anchor != None and anchor != '':
        use_anchor = True

    if use_anchor:
        anchor_str = '#'+anchor

    res = \
        scheme \
        + '://' \
        + auth_str \
        + host \
        + port_str \
        + path \
        + param_str \
        + anchor_str
    return res
