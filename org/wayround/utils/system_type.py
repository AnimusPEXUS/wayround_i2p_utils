
import os.path
import re
import subprocess

import org.wayround.utils.path


class SystemTypeInvalidFullName(Exception):
    pass


class SystemType:

    def __init__(
            self, fullname=None, cpu='i486', company='pc', kernel='linux', os='gnu'
            ):

        self.fullname = fullname

        if isinstance(self.fullname, str):

            self._sane(self.fullname)

        else:
            self.cpu = cpu
            self.company = company
            self.os = os
            self.kernel = kernel

            self._sane(
                format_triplet(
                    cpu=cpu, company=company, kernel=kernel, os=os
                    )
                )

        return

    def _sane(self, string):

        if not isinstance(string, str):
            raise SystemTypeInvalidFullName(
                "Not valid fullname type: {}".format(type(string))
                )

        res = parse_triplet(string)

        if not res:
            raise SystemTypeInvalidFullName(
                "Not valid fullname: {}".format(string)
                )
        else:
            self.cpu = res[0]
            self.company = res[1]
            self.kernel = res[2]
            self.os = res[3]
            self.fullname = res[4]

        return

    def __str__(self):
        return self.fullname


def parse_triplet(string):
    """
    Parse constitution triplet (``(.*?)-(.*?)-(.*)``), and return 3-tuple

    cpu-company-system

    where system can have one of these forms:

     os
     kernel-os

    """

    ret = None

    wd = os.path.dirname(org.wayround.utils.path.abspath(__file__))

    jd = os.path.join(wd, 'config.sub')

    if not os.path.isfile(jd):
        raise Exception("file not found: `{}'".format(jd))

    p = subprocess.Popen(
        ['bash',
         jd,
         string
         ],
        cwd=wd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL
        )

    res = p.wait()

    if res != 0:
        ret = None
    else:
        com_res = p.communicate()

        out = str(com_res[0].splitlines()[0].strip(), 'utf-8')

        a = re.match(r'(?P<cpu>.*?)-(?P<company>.*?)-(?P<system>.*)', out)
        if a:

            system = a.group('system')

            b = re.match(r'((?P<kernel>.*?)-)?(?P<os>.*)', system)

            if b:

                ret = (
                    a.group('cpu'),
                    a.group('company'),
                    b.group('kernel'),
                    b.group('os'),
                    out
                    )

    return ret


def format_triplet(cpu='i486', company='pc', kernel='linux', os='gnu'):

    system = os

    if kernel:
        system = kernel + '-' + system

    return '{cpu}-{company}-{system}'.format(
        cpu=cpu,
        company=company,
        system=system
        )
