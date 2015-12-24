
import urllib.parse

import regex

import wayround_org.utils.types

URL_AUTHORITY_RE = r'^((?P<userinfo>.*)\@)?(?P<host>.*)(\:(?P<port>\d+))?$'
URL_AUTHORITY_RE_C = regex.compile(URL_AUTHORITY_RE)

URI_RE = (
    r'^('
    r'(?P<scheme>\p{L}\w*\:)'
    r'(?P<path>.*?)'
    r'(\?(?P<query>.*))?'
    r'(?P<fragment>\#.*)?'
    r')$'
    )

URI_RE_C = regex.compile(URI_RE)


class UserInfoLikeHttp:

    def __init__(self, value):

        if isinstance(value, AuthorityLikeHttp):
            value = value.userinfo

        if not isinstance(value, str):
            raise TypeError("`value' must be str")

        self.name = value
        self.password = None

        if ':' in self.name:
            self.name, self.password = self.name.split(':', 1)

        return

    def __str__(self):

        ret = self.name
        if self.password is not None:
            ret = '{}:{}'.format(ret, self.password)

        return ret


class AuthorityLikeHttp:

    @classmethod
    def new_from_string(cls, value):

        res = URL_AUTHORITY_RE_C.match(value)

        if res is None:
            raise ValueError("can't parse value as authority")

        userinfo = res.group('userinfo')
        host = res.group('host')
        port = res.group('port')

        return cls(userinfo, host, port)

    def __init__(self, userinfo, host, port):

        self._userinfo = None
        self._host = None
        self._port = None

        self.userinfo = userinfo
        self.host = host
        self.port = port
        return

    def __str__(self):

        ret = ''

        if self.userinfo is not None:
            ret += '{}@'.format(self.userinfo)

        ret += self.host

        if self.port is not None:
            ret += ':{}'.format(self.port)

        return ret

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        if not isinstance(value, str):
            raise TypeError("`host' must be str")
        self._host = value.lower()
        return

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, value):
        if isinstance(value, str):
            value = int(value)

        if value is not None and not isinstance(value, int):
            raise TypeError("`port' must be int")

        self._port = value
        return


class QueryLikeHttp:

    def __init__(self, value):
        self._value = None
        self.value = value
        return

    def to_str(self, encoding=None, errors=None):

        if encoding is None:
            encoding = 'utf-8'

        ret = []

        for i in self.value:
            ret.append(
                '{}={}'.format(
                    urllib.parse.quote(i[0], encoding=encoding, errors=errors),
                    urllib.parse.quote(i[1], encoding=encoding, errors=errors)
                    )
                )

        ret = '&'.join(ret)

        return ret

    def __str__(self):
        return self.to_str()

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        if isinstance(value, URI):
            value = value.query

        if isinstance(value, str):
            res_val = []
            for i in value.split('&'):
                res_val.append(tuple(i.split('=', 1)))

            value = res_val
            del res_val

        if not wayround_org.utils.types.struct_check(
                value,
                {'t': list,
                 'None': True,
                 '.': {
                     't': tuple,
                     '<': 2,
                     '>': 2,
                     '.': {
                         't': str
                         }
                     }
                 }
                ):
            raise TypeError("`query' must be list of 2-str-tuples")

        self._value = value
        return

    def keys(self):
        ret = []
        for i in self.value:
            ret.append(i[0])
        return ret

    def values(self):
        ret = []
        for i in self.value:
            ret.append(i[1])
        return ret

    def get(self, key, default=None):
        ret = default
        for i in self.value:
            if i[0] == key:
                ret = i[1]
        return ret

    def get_all(self, key):
        ret = []
        for i in self.value:
            if i[0] == key:
                ret.append(i[1])
        return ret

    def set(self, key, value):
        val = self.value
        for i in range(len(val) - 1, -1, -1):
            if val[i][0] == key:
                val[i] = tuple(key, value)
        return

    def remove(self, key):
        val = self.value
        for i in range(len(val) - 1, -1, -1):
            if val[i][0] == key:
                del val[i]
        return


class URI:

    @classmethod
    def new_from_string(cls, value):

        res = URI_RE_C.match(value)

        if res is None:
            raise ValueError("can't parse value as URI string")

        scheme = res.group('scheme')
        authority = None
        # authority = res.group('authority')
        path = res.group('path')
        query = res.group('query')
        fragment = res.group('fragment')

        if path.startswith('//'):
            authority = None
            path_splitted = path[2:].split('/')
            authority = path_splitted[0]
            path = '/'.join(path_splitted[1:])

        return cls(scheme, authority, path, query, fragment)

    def __init__(self, scheme, authority, path, query, fragment):

        self._scheme = None
        self._authority = None
        self._path = None
        self._query = None
        self._fragment = None

        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment

        return

    def __str__(self):
        ret = ''
        ret += str(self.scheme)
        ret += ':'
        if self.authority is not None:
            ret += str(self.authority)
        if self.path is not None:
            ret += str(self.path)
        if self.fragment is not None:
            ret += '#'
            ret += str(self.fragment)
        return ret

    def __repr__(self):
        ret = '{} {}'.format(
            repr(super()),
            ("scheme: `{}', authority: `{}', "
             "path: `{}', query: `{}', fragment: `{}'").format(
                self.scheme,
                self.authority,
                self.path,
                self.query,
                self.fragment
                )
            )
        return ret

    @property
    def scheme(self):
        return self._scheme

    @scheme.setter
    def scheme(self, value):
        if not isinstance(value, str):
            raise ValueError("`scheme' must be str")
        self._scheme = value.rstrip(':')
        # NOTE: scheme is case sensitive
        # self._scheme = self._scheme.lower()
        return

    @property
    def authority(self):
        return self._authority

    @authority.setter
    def authority(self, value):
        if value is not None:
            a_t = type(value)

            if a_t == str:
                value = AuthorityLikeHttp.new_from_string(value)

            elif a_t == AuthorityLikeHttp:
                pass

            else:
                raise TypeError("invalid `authority' type")

        self._authority = value

        return

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):

        if value is None:
            value = []

        if isinstance(value, str):

            if self.scheme.lower() == 'urn':
                value = value.split(':')
            else:
                value = value.split('/')

        if not wayround_org.utils.types.struct_check(
                value,
                {'t': list,
                 'None': True,
                 '.': {
                     't': str
                     }
                 }
                ):
            raise TypeError("`path' must be list of strings")

        self._path = value

        return

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):

        if not value is None and not isinstance(value, str):
            raise TypeError("`query' must be None or str")

        self._query = value

        return

    @property
    def fragment(self):
        return self._fragment

    @fragment.setter
    def fragment(self, value):

        if value is not None and not isinstance(value, str):
            raise ValueError("`fragment' must be str")

        self._fragment = value

        return


def run_examples():

    examples = [
        'ftp://ftp.is.co.za/rfc/rfc1808.txt',
        'http://www.ietf.org/rfc/rfc2396.txt',
        'ldap://[2001:db8::7]/c=GB?objectClass?one',
        'mailto:John.Doe@example.com',
        'news:comp.infosystems.www.servers.unix',
        'tel:+1-816-555-1212',
        'telnet://192.0.2.16:80/',
        'urn:oasis:names:specification:docbook:dtd:xml:4.1.2'
        ]

    for i in examples:
        print("{}\n\t{}\n".format(i, repr(URI.new_from_string(i))))
