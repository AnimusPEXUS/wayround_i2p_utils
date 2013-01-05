#!/usr/bin/python2.6

from __future__ import print_function

import uritools

passed = 0
failed = 0

def passed_proc():
    global passed
    passed += 1
    print('PASSED', end='')

def failed_proc():
    global failed
    failed += 1
    print('FAILED', end='')


print('Child paths filter\t[', end='')
res = uritools.uri.del_not_child_uris(
    'http://example.net/1/',
    [
        'http://example.net/1/2',
        'http://example.net/1/3',
        'http://example.net/1/4',
        'http://example.net/3/',
        'http://examples.net/1/5',
        'https://example.net/1/6'
        ]
    )


if len(res) == 3 \
        and 'http://example.net/1/2' in res \
        and 'http://example.net/1/3' in res \
        and 'http://example.net/1/4' in res:
    passed_proc()
else:
    failed_proc()

print(']')

print('TOTAL: ' + str(failed+passed) +
    ' PASSED: ' + str(passed) +
    ' FAILED: ' + str(failed))

if failed == 0:
    exit(0)
else:
    exit(1)
