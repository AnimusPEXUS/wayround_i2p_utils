
import sys
import subprocess

from . import error


def xz_check():
    pass

def xz_version():
    pass

def xz(stdin=subprocess.PIPE,
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE,
       options=[], bufsize=0, cwd=None):

    p = None

    try:
        p = subprocess.Popen(
            ['xz'] + options,
            stdin=stdin, stdout=stdout, stderr=stderr,
            bufsize=bufsize,
            cwd=cwd
            )
    except:
        print("-e- Error starting xz subprocess")
        p = None
        e = sys.exc_info()
        error.print_exception_info(e)
        raise e[1]

    return p
