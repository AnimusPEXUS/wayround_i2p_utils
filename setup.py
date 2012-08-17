from distutils.core import setup

setup(name='org_wayround_utils',
      version='0.2',
      description='Various service modules required by wayround.org projects',
            long_description="""\
This package contains various useful modules functions and classes.
It is heavily used by My projects, aipsetup for instance.

""",

      author='Alexey Gorshkov',
      author_email='animus@wayround.org',
      url='http://wiki.wayround.org/soft/org_wayround_utils',
      packages=['org.wayround.utils'],
      requires=['org_wayround'],
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Development Status :: 1 - Planning'
        ]
     )
