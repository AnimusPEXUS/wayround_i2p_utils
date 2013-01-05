import copy
import urllib

def paths_by_path(path, last_el_type=None, path_is_absolute=None):
    '''
    Returns dict with three values:

       - path_str: path string
       - path_lst: list of path components
       - last_el_type: last element type: 'dir' or 'file'
       - path_is_absolute: True if path_str begins with '/'

    Input value can ether be URI path part string ether list with path
    parts. If input type is list, then second parameter determines
    returning last_el_type.

    If input type is string, then last element type will be 'dir' if
    last char in string is '/', but it can be forced by last_el_type
    parameter.

    If input is list and second parameter is None, then returning
    last_el_type will be 'dir'. In both cases,

    if resulting last_el_type == 'dir', then path_str[-1:] == '/'.

    Parameter path_is_absolute can be used for manipulating '/' in
    begining of output path_str.

    examples:

    >>> urltools.paths_by_path('a/b/c/d')
    {'path_lst': ['a', 'b', 'c', 'd'], 'path_str': '/a/b/c/d', 'last_el_type': 'file'}

    >>> urltools.paths_by_path('a/b/c/d/')
    {'path_lst': ['a', 'b', 'c', 'd'], 'path_str': '/a/b/c/d/', 'last_el_type': 'dir'}

    >>> urltools.paths_by_path(['1','2','3','4'])
    {'path_lst': ['1', '2', '3', '4'], 'path_str': '/1/2/3/4/', 'last_el_type': 'dir'}

    >>> urltools.paths_by_path(['1','2','3','4'], 'file')
    {'path_lst': ['1', '2', '3', '4'], 'path_str': '/1/2/3/4', 'last_el_type': 'file'}

    '''
    if isinstance(path, list):
        path_str = '/'.join(path)
        path_lst = copy.copy(path)

        if last_el_type == None:
            last_el_type = 'dir'

    if isinstance(path, str) or isinstance(path, unicode):

        if last_el_type == None:
            if path[-1:] == '/':
                last_el_type = 'dir'
            else:
                last_el_type = 'file'

        if path_is_absolute == None:
            path_is_absolute = (path[0] == '/')

        t_path = path.strip('/')

        t_lst = t_path.split('/')

        path_str = '/' + t_path
        path_lst = []
        for i in t_lst:
            if i != '':
                path_lst.append(i)

    if last_el_type == 'dir':
        if path_str[-1:] != '/':
            path_str += '/'

    if path_is_absolute == None and path_str[0] != '/':
        path_str = '/' + path_str

    return {'path_str': path_str,
            'path_lst': copy.copy(path_lst),
            'last_el_type': last_el_type,
            'path_is_absolute': path_is_absolute}

def ischild(path1, path2):
    """
    Compairs two paths and returns True if path2 is child for path1
    """

    p1 = paths_by_path(path1)['path_lst']
    p2 = paths_by_path(path2)['path_lst']

    l1 = len(p1)
    l2 = len(p2)

    if l2 != (l1 + 1):
        return False

    for i in range(l1):
        if urllib.unquote(p1[i]) != urllib.unquote(p2[i]):
            return False

    return True

def is_child(path1, path2):
    """Sinonym for ischild"""
    return ischild(path1, path2)
