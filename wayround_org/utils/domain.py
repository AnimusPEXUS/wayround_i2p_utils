
# -*- coding: utf-8 -*-

import regex

HOST_NAME = r'([a-zA-Z0-9_\-]|\w)+'

DOMAIN_RE = (
    r'('
    r'(({HOST_NAME})(\.({HOST_NAME})\.)+({HOST_NAME}))'
    r'|'
    r'(({HOST_NAME})\.({HOST_NAME}))'
    r'|'
    r'({HOST_NAME})'
    r')'
    ).format(HOST_NAME=HOST_NAME)

DOMAIN_RE_C = regex.compile(DOMAIN_RE)


def test():
    for i in [
            'wayround.org',
            'xn--d1acvii6e.xn--p1ai',
            'президент.рф'
            ]:
        print('{}:'.format(i), end='')
        if DOMAIN_RE_C.match(i):
            print('ok')
        else:
            print('fail')
    return
