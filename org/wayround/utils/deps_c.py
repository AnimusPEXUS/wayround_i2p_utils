
import os
import io
import copy
import re
import logging

import org.wayround.utils.exec
import org.wayround.utils.stream

LDD_RESP_RES = {
    'not_found': r'(?P<name>.*) => not found',
    'pointed': r'(?P<name>.*) => (?P<path>.*) \((?P<address>.*)\)',
    'singleton': r'(?P<name>.*) \((?P<address>.*)\)'
    }

def elf_deps(filename, mute=True):

    ret = 0

    filename = os.path.abspath(filename)

    if not os.path.isfile(filename):
        #or os.path.islink(filename):
        if not mute:
            logging.error("Not a file")
        ret = 1
    else:

        str_file = io.StringIO()

        lddproc = ldd(
            options=[filename]
            )

        catproc = org.wayround.utils.stream.cat(
            lddproc.stdout,
            str_file,
            threaded=True,
            convert_to_str='utf-8'
            )
        catproc.start()

        lddproc.wait()

        catproc.join()

        str_file.seek(0)

        deps_txt = str_file.read()

        str_file.close()
        del(str_file)

        if lddproc.returncode == 0:
            dep_lst = parse_ldd_output(deps_txt)
            ret = copy.copy(dep_lst)
        else:
            if not mute:
                logging.error("`ldd' returned error")
            ret = 2

        del(lddproc)

    return ret

def parse_ldd_output(text):
    dep_lines = text.splitlines()

    dep_lst = []
    for i in dep_lines:

        i = i.strip(' \t\n')

        dep_tmpl = {
            'type'  : None,
            'values': {
                    'name': None,
                    'address':  None,
                    'path': None
                }
            }

        re_res = None
        for j in LDD_RESP_RES:
            re_res = re.match(LDD_RESP_RES[j], i)
            if re_res != None:
                dep_tmpl['type'] = j
                dep_tmpl['values']['name'] = re_res.group('name')
                if j == 'pointed':
                    dep_tmpl['values']['path'] = re_res.group('path')
                if j in ['pointed', 'singleton']:
                    dep_tmpl['values']['address'] = re_res.group('address')

                dep_lst.append(dep_tmpl)

                break

        if re_res == None:
            logging.error("Couldn't parse line `{}'".format(i))
            raise Exception

    ret = dep_lst

    return ret

def ldd(*args, **kwargs):
    return org.wayround.utils.exec.simple_exec('ldd', *args, **kwargs)
