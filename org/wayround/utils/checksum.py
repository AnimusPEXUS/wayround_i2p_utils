
import os
import hashlib
import re
import logging

import org.wayround.utils.stream
import org.wayround.utils.file

def make_dir_checksums(dirname, output_filename):

    ret = 0

    dirname = os.path.abspath(dirname)

    if not os.path.isdir(dirname):
        logging.error("Not is dir %(name)s" % {
            'name': dirname
            })
        ret = 1

    else:

        try:
            sums_fd = open(output_filename, 'w')
        except:
            logging.exception("Error opening output file")
            ret = 2
        else:
            try:
                ret = make_dir_checksums_fo(dirname, sums_fd)
            finally:
                sums_fd.close()

    return ret

def make_dir_checksums_fo(dirname, output_fileobj):
    ret = 0
    dirname = os.path.abspath(dirname)
    if not os.path.isdir(dirname):
        logging.error("Not a dir %(name)s" % {
            'name': dirname
            })
        ret = 1

    else:

        dirname_l = len(dirname)

        if not hasattr(output_fileobj, 'write'):
            logging.error("Wrong output file object")
            ret = 2
        else:

            # TODO: may be optimizations needed

            logging.info("Creating checksums")
            for root, dirs, files in os.walk(dirname):
                for f in files:
                    org.wayround.utils.file.progress_write("    %(dir)s/%(file)s" % {
                        'dir': root,
                        'file': f
                        })
                    if os.path.isfile(root + '/' + f) and not os.path.islink(root + '/' + f):
                        m = hashlib.sha512()
                        try:
                            fd = open(root + '/' + f, 'r')
                        except:
                            logging.exception("Can't open file `{}'".format(root + '/' + f))
                            ret = 3
                        else:
                            try:
                                m.update(fd.read())
                                wfn = ('/' + (root + '/' + f)[1:])[dirname_l:]
                                output_fileobj.write(
                                    "%(digest)s *%(pkg_file_name)s\n" % {
                                        'digest': m.hexdigest(),
                                        'pkg_file_name':wfn
                                        }
                                    )
                            finally:
                                fd.close()

                        del(m)

    print("")
    return ret

def make_file_checksum(filename, method='sha512'):
    ret = 0
    try:
        f = open(filename, 'r')
    except:
        logging.exception("Can't open file `%(name)s'" % {
            'name': filename
            })
        ret = 1
    else:
        summ = make_fileobj_checksum(f, method)
        if not isinstance(summ, str):
            logging.error("Can't get checksum for file `%(name)s'" % {
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
        logging.exception("Error calling for hashlib method `%(method)s'" % {
            'method': method
            })
        ret = 1
    else:
        org.wayround.utils.stream.cat(
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
        logging.exception("Can't open file `%(name)s'" % {
            'name': filename
            })
        ret = 1
    else:
        txt = f.read()
        f.close()
        sums = parse_checksums_text(txt)
        if not isinstance(sums, dict):
            logging.error("Can't get checksums from file `%(name)s'" % {
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
