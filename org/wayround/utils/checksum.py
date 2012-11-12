
import os
import hashlib
import re
import logging

import org.wayround.utils.file
import org.wayround.utils.path
import org.wayround.utils.stream


def make_dir_checksums(dirname, output_filename):

    ret = 0

    dirname = org.wayround.utils.path.abspath(dirname)

    if not os.path.isdir(dirname):
        logging.error("Not is dir {}".format(dirname))
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

def make_dir_checksums_fo(
    dirname,
    output_fileobj,
    rel_to=None,
    conv_to_rooted=False
    ):

    if not isinstance(rel_to, str):
        rel_to = dirname

    ret = 0

    dirname = org.wayround.utils.path.abspath(dirname)
    dirname_l = len(dirname)


    if not isinstance(rel_to, str):
        rel_to = dirname


    rel_to = org.wayround.utils.path.abspath(rel_to)
    rel_to_l = len(rel_to)

    if not os.path.isdir(dirname):
        logging.error("Not a dir {}".format(dirname))
        ret = 1

    else:

        if not hasattr(output_fileobj, 'write'):
            logging.error("Wrong output file object")
            ret = 2
        else:

            for root, dirs, files in os.walk(dirname):
                for f in files:
                    rel_path = org.wayround.utils.path.relpath(root + os.path.sep + f, dirname)
                    org.wayround.utils.file.progress_write(
                        "    {}".format(rel_path)
                        )
                    if (
                        (os.path.isfile(root + os.path.sep + f))
                        and
                        (not os.path.islink(root + os.path.sep + f))
                        ):
                        m = hashlib.sha512()
                        try:
                            fd = open(root + os.path.sep + f, 'rb')
                        except:
                            logging.exception(
                                "Can't open file `{}'".format(
                                    root + os.path.sep + f
                                    )
                                )
                            ret = 3
                        else:
                            try:
                                m.update(fd.read())

                                wfn = ('/' + (root + os.path.sep + f)[1:])[dirname_l:]

                                output_fileobj.write(
                                    "{digest} *{pkg_file_name}\n".format_map(
                                        {
                                            'digest': m.hexdigest(),
                                            'pkg_file_name':wfn
                                            }
                                        )
                                    )
                            finally:
                                fd.close()

                        del(m)

    org.wayround.utils.file.progress_write_finish()
    return ret

def make_file_checksum(filename, method='sha512'):
    ret = 0

    if not method.isidentifier() or not hasattr(hashlib, method):
        raise ValueError("hashlib doesn't have `{}'".format(method))

    try:
        f = open(filename, 'rb')
    except:
        logging.exception("Can't open file `{}'".format(filename))
        ret = 1
    else:
        summ = make_fileobj_checksum(f, method)
        if not isinstance(summ, str):
            logging.error("Can't get checksum for file `{}'".format(filename))
            ret = 2
        else:
            ret = summ

        f.close()

    return ret

def make_fileobj_checksum(fileobj, method='sha512'):
    ret = None
    m = None

    if not method.isidentifier() or not hasattr(hashlib, method):
        raise ValueError("hashlib doesn't have `{}'".format(method))

    try:
        m = eval("hashlib.{}()".format(method))
    except:
        logging.exception(
            "Error calling for hashlib method `{}'".format(method)
            )
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
        f = open(filename, 'rb')
    except:
        logging.exception("Can't open file `{}'".format(filename))
        ret = 1
    else:
        txt = f.read()
        f.close()
        sums = parse_checksums_text(txt)
        if not isinstance(sums, dict):
            logging.error("Can't get checksums from file `{}'".format(filename))
            ret = 2
        else:
            ret = sums

    return ret

def parse_checksums_text(text):
    ret = 0
    if isinstance(text, bytes):
        text = text.decode('utf-8')

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

def checksums_by_list(file_lst, method):

    if not method.isidentifier() or not hasattr(hashlib, method):
        raise ValueError("hashlib doesn't have `{}'".format(method))

    ret = {}

    for i in file_lst:
        ret[i] = make_file_checksum(i, method=method)

    return ret

def render_checksum_dict_to_txt(sums_dict, sort=False):

    keys = list(sums_dict.keys())

    if sort:
        keys.sort()

    ret = ''

    for i in keys:
        ret += '{sum} *{path}\n'.format(sum=str(sums_dict[i]), path=str(i))

    return ret
