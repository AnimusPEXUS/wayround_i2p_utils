# -*- coding: utf-8 -*-

import os
import sys
import hashlib
import re

from . import stream
from . import error
from . import file

def make_dir_checksums(dirname, output_filename):

    ret = 0

    dirname = os.path.abspath(dirname)

    if not os.path.isdir(dirname):
        print("-e- Not is dir %(name)s" % {
            'name': dirname
            })
        ret = 1

    else:

        try:
            sums_fd = open(output_filename, 'w')
        except:
            print("-e- Error opening output file")
            error.print_exception_info(sys.exc_info())
            ret = 2
        else:
            ret = make_dir_checksums_fo(dirname, sums_fd)

            sums_fd.close()

    return ret

def make_dir_checksums_fo(dirname, output_fileobj):
    ret = 0
    dirname = os.path.abspath(dirname)
    if not os.path.isdir(dirname):
        print("-e- Not a dir %(name)s" % {
            'name': dirname
            })
        ret = 1

    else:

        dirname_l = len(dirname)

        if not isinstance(output_fileobj, file):
            print("-e- Wrong output file object")
            ret = 2
        else:
            sums_fd = output_fileobj
            print("-i- Creating checksums")
            for root, dirs, files in os.walk(dirname):
                for f in files:
                    file.progress_write("    %(dir)s/%(file)s" % {
                        'dir': root,
                        'file': f
                        })
                    if os.path.isfile(root + '/' + f) and not os.path.islink(root + '/' + f):
                        m = hashlib.sha512()
                        fd = open(root + '/' + f, 'r')
                        m.update(fd.read())
                        fd.close()
                        wfn = ('/' + (root + '/' + f)[1:])[dirname_l:]
                        sums_fd.write(
                            "%(digest)s *%(pkg_file_name)s\n" % {
                                'digest': m.hexdigest(),
                                'pkg_file_name':wfn
                                }
                            )
                        del(m)
    print("")
    return ret

def make_file_checksum(filename, method='sha512'):
    ret = 0
    try:
        f = open(filename, 'r')
    except:
        print("-e- Can't open file `%(name)s'" % {
            'name': filename
            })
        error.print_exception_info(sys.exc_info())
        ret = 1
    else:
        summ = make_fileobj_checksum(f, method)
        if not isinstance(summ, str):
            print("-e- Can't get checksum for file `%(name)s'" % {
                'name': filename
                })
            ret = 2
        else:
            ret = summ
        f.close()
    return ret

def make_fileobj_checksum(fileobj, method='sha512'):
    ret = None
    m = None
    try:
        m = eval("hashlib.%(method)s()" % {
            'method': method
            })
    except:
        print("-e- Error calling for hashlib method `%(method)s'" % {
            'method': method
            })
        error.print_exception_info(sys.exc_info())
        ret = 1
    else:
        stream.cat(
            fileobj, m, write_method_name='update'
            )
        ret = m.hexdigest()
        del(m)
    return ret

def parse_checksums_file_text(filename):
    ret = 0
    try:
        f = open(filename)
    except:
        print("-e- Can't open file `%(name)s'" % {
            'name': filename
            })
        error.print_exception_info(sys.exc_info())
        ret = 1
    else:
        txt = f.read()
        f.close()
        sums = parse_checksums_text(txt)
        if not isinstance(sums, dict):
            print("-e- Can't get checksums from file `%(name)s'" % {
                'name': filename
                })
            ret = 2
        else:
            ret = sums

    return ret

def parse_checksums_text(text):
    ret = 0
    lines = text.splitlines()
    sums = {}
    for i in lines:
        ist = i.strip(' \n\t\0')
        if ist != '':
            re_res = re.match(r'(.*?) \*(.*)', ist)

            if re_res == None:
                ret = 1
                break
            else:
                sums[re_res.group(2)] = re_res.group(1)

    if ret == 0:
        ret = sums

    return ret
