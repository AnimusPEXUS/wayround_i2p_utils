
import logging
import subprocess

def se(program,
       stdin=subprocess.PIPE,
       stdout=subprocess.PIPE,
       stderr=subprocess.PIPE,
       options=[],
       bufsize=0,
       cwd=None):

    p = None

    try:
        p = subprocess.Popen(
            [program] + options,
            stdin=stdin, stdout=stdout, stderr=stderr,
            bufsize=bufsize,
            cwd=cwd
            )
    except:
        logging.exception("Error starting {} subprocess".format(program))
        p = None
        raise

    return p
