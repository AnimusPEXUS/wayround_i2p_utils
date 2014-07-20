#!/usr/bin/python3

import subprocess
import os.path

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

py_compil_args = None
py_link_args = None

p = subprocess.Popen(['pkg-config', '--cflags', 'python3'], stdout=subprocess.PIPE)
p.wait()
py_compile_args = str(p.communicate()[0], encoding='utf-8').split()

p = subprocess.Popen(['pkg-config', '--libs', 'python3'], stdout=subprocess.PIPE)
p.wait()
py_link_args = str(p.communicate()[0], encoding='utf-8').split()

setup(
    name='org_wayround_utils',
    version='0.14',
    description='Various service modules',
    long_description="""\
This package contains various useful modules functions and classes.

""",

    author='Alexey Gorshkov',
    author_email='animus@wayround.org',
    url='http://wiki.wayround.org/soft/org_wayround_utils',
    packages=[
        'org.wayround.utils',
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
            extra_compile_args=py_compile_args,
            extra_link_args=py_link_args,
            ),
#        Extension(
#            "org.wayround.utils.version",
#            ["org/wayround/utils/version.pyx"],
#            # TODO: pkg-config
#            )
        ],
#    cmdclass={'build_ext': build_ext},
    package_data={
        'org.wayround.utils': [
            'config.sub', 
            os.path.join('format', '*.c'),
            os.path.join('format', '*.h')
            ]
        }
    )
