#!/usr/bin/python3

import subprocess

from distutils.core import setup
from distutils.extension import Extension


py_compil_args = None
py_link_args = None

p = subprocess.Popen(['pkg-config', '--cflags', 'python3'], stdout=subprocess.PIPE)
p.wait()
py_compil_args = str(p.communicate()[0], encoding='utf-8').split()

p = subprocess.Popen(['pkg-config', '--libs', 'python3'], stdout=subprocess.PIPE)
p.wait()
py_link_args = str(p.communicate()[0], encoding='utf-8').split()

setup(
    name='org_wayround_utils',
    version='0.4',
    description='Various service modules',
    long_description="""\
This package contains various useful modules functions and classes.

""",

    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='http://wiki.wayround.org/soft/org_wayround_utils',
    packages=[
        'org.wayround.utils',
        'org.wayround.utils.xmpp',
        'org.wayround.utils.format'
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Development Status :: 1 - Planning'
        ],
    ext_modules=[
        Extension(
            "org.wayround.utils.format.elf_bin",
            ["org/wayround/utils/format/elf_bin.c"],
            extra_compile_args=py_compil_args + ['-g'],
            extra_link_args=py_link_args
            )
        ]
    )
