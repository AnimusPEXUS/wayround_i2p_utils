

import subprocess
import os

import wayround_org.utils.file


def findtool(which=None, where=None):
    if which is None:

        which = 'pkg-config'

        if where is None:
            where = os.environ['PATH'].split(':')

        which = wayround_org.utils.file.which(
            'pkg-config',
            where
            )
    return which


def pkgconfig(names, options, which=None, where=None):

    which = findtool(which, where)

    if not isinstance(names, list):
        names = [names]

    if not isinstance(options, list):
        options = [options]

    cmd = [which] + options + names

    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )

    stdout, stderr = p.communicate()

    res = p.wait()

    ret = None

    if res != 0:
        pass

    else: 
        stdout = str(stdout, 'utf-8')
        stdout = stdout.strip()

        ret = stdout

    return ret