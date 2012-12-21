#!/usr/bin/python3

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    name = 'org_wayround_utils',
    version = '0.4',
    description = 'Various service modules',
    long_description = """\
This package contains various useful modules functions and classes.

""",

    author = 'Alexey Gorshkov',
    author_email = 'animus@wayround.org',
    url = 'http://wiki.wayround.org/soft/org_wayround_utils',
    packages = [
        'org.wayround.utils',
        'org.wayround.utils.xmpp',
        'org.wayround.utils.format'
        ],
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Development Status :: 1 - Planning'
        ],
    ext_modules = [
#        Extension(
#            "org.wayround.utils.format.elf_h",
#            ["org/wayround/utils/format/elf_h.pyx"]
#            ),
        Extension(
            "org.wayround.utils.format.elf",
            ["org/wayround/utils/format/elf.pyx"]
            )
        ],
    cmdclass = {'build_ext': build_ext}
    )
