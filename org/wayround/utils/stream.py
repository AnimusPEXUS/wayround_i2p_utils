# -*- coding: utf-8 -*-

import os
# TODO: migrate to multiprocessing
import threading
import subprocess
import logging

import org.wayround.utils.exec


def cat(stdin, stdout, threaded=False, write_method_name='write',
        close_output_on_eof=False, thread_name='Thread', bs=(2 * 1024 ** 2),
        convert_to_str=None):
    return dd(stdin, stdout, bs=bs, count=None,
              threaded=threaded, write_method_name=write_method_name,
              close_output_on_eof=close_output_on_eof,
              thread_name=thread_name, convert_to_str=convert_to_str)

def dd(stdin, stdout, bs=1, count=None, threaded=False,
       write_method_name='write', close_output_on_eof=False,
       thread_name='Thread', convert_to_str=None):

    if not write_method_name in ['write', 'update']:
        raise ValueError

    if not hasattr(stdin, 'read'):
        raise ValueError("Object `{}' have no 'read' function".format(stdin))

    if convert_to_str != None:
        if not isinstance(convert_to_str, str):
            raise ValueError("convert_to_str and ony be str or None")

    if threaded:
        return threading.Thread(
            target=dd,
            args=(stdin, stdout),
            kwargs=dict(
                bs=bs,
                count=count,
                threaded=False,
                close_output_on_eof=close_output_on_eof,
                write_method_name=write_method_name,
                thread_name=thread_name,
                convert_to_str=convert_to_str
                )
            )

    else:

        if thread_name != 'Thread':
            logging.info("Starting `%(name)s' thread" % {
                'name':thread_name
                })

        buff = ' '

        c = 0
        bytes_counter = 0

        if hasattr(stdin, 'seek'):
            try:
                stdin.seek(0)
            except:
                pass

        while True:
            buff = stdin.read(bs)

            if not isinstance(buff, bytes):
                raise ValueError("Can read only with (Not str or anything other)")

            if convert_to_str != None:
                buff = str(buff, encoding=convert_to_str)

            try:
                exec(
                    "stdout.{}(buff)".format(write_method_name)
                    )
            except TypeError as err_val:
                if err_val.args[0] == 'must be str, not bytes':
                    logging.warning("hint: check that output is in bytes mode or do conversion with convert_to_str option")
                raise

            buff_len = len(buff)
            if buff_len == 0:
                break
            else:
                bytes_counter += buff_len

            c += 1

            if count != None:
                if c == count:
                    break

        if hasattr(stdout, 'seek'):
            try:
                stdout.seek(0, os.SEEK_END)
            except:
                pass

        if close_output_on_eof:
            if thread_name != 'Thread':
                logging.info("Closing `%(name)s' thread stdout" % {
                    'name':thread_name
                    })
            stdout.close()

        if thread_name != 'Thread':
            logging.info("""\
  Ending `{name}' thread
        {{
           {num} cycles worked,
           {size} bytes ({sizem} MiB) transferred,
           with buffer size {bufs} bytes ({bufm} MiB)
        }}
""".format_map({
        'name': thread_name,
        'num' : c,
        'size': bytes_counter,
        'sizem': (float(bytes_counter) / 1024 / 1024),
        'bufs': bs,
        'bufm': (float(bs) / 1024 / 1024)
        }
        )
    )
        return

    # control shuld never reach this return
    return

def lbl_write(stdin, stdout, threaded=False):

    if threaded:
        return threading.Thread(
            target=lbl_write,
            args=(stdin, stdout),
            kwargs=dict(threaded=False))
    else:

        while True:
            l = stdin.readline()
            if l == '':
                break
            else:
                l = l.rstrip(' \0\n')

                stdout.write(l)

        return

    return

def unix_cat(
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    options=[],
    bufsize=0,
    cwd=None
    ):

    p = org.wayround.utils.exec.simple_exec(
        'cat',
        stdin,
        stdout,
        stderr,
        options,
        bufsize,
        cwd
        )

    return p
