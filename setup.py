#!/usr/bin/python3

import subprocess
import os.path

from setuptools import setup
from setuptools import Extension

py_compil_args = None
py_link_args = None

p = subprocess.Popen(
    ['pkg-config', '--cflags', 'python3'], stdout=subprocess.PIPE)
p.wait()
py_compile_args = str(p.communicate()[0], encoding='utf-8').split()

p = subprocess.Popen(
    ['pkg-config', '--libs', 'python3'], stdout=subprocess.PIPE)
p.wait()
py_link_args = str(p.communicate()[0], encoding='utf-8').split()

setup(
    name='org_wayround_utils',
    version='1.1',
    description='Various service modules',
    long_description="""\
This package contains various useful modules functions and classes.

""",

    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='https://github.com/AnimusPEXUS/org_wayround_utils',
    packages=[
        'org.wayround.utils',
        'org.wayround.utils.format'
        ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Development Status :: 5 - Production/Stable'
        ],
    ext_modules=[
        Extension(
            "org.wayround.utils.format.elf_bin",
            ["org/wayround/utils/format/elf_bin.c"],
            extra_compile_args=py_compile_args,
            extra_link_args=py_link_args,
            ),
        ],
    package_data={
        'org.wayround.utils': [
            'config.sub',
            os.path.join('format', '*.c'),
            os.path.join('format', '*.h')
            ]
        }
    )
