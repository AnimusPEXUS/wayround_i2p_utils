
import os
import threading
import subprocess
import logging

import org.wayround.utils.exec


def cat(
    stdin,
    stdout,
    threaded=False,
    write_method_name='write',
    close_output_on_eof=False,
    thread_name='Thread',
    bs=(2 * 1024 ** 2),
    convert_to_str=None
    ):

    return dd(
        stdin,
        stdout,
        bs=bs,
        count=None,
        threaded=threaded,
        write_method_name=write_method_name,
        close_output_on_eof=close_output_on_eof,
        thread_name=thread_name,
        convert_to_str=convert_to_str
        )

def dd(
    stdin,
    stdout,
    bs=1,
    count=None,
    threaded=False,
    write_method_name='write',
    close_output_on_eof=False,
    thread_name='Thread',
    convert_to_str=None
    ):

    if not write_method_name in ['write', 'update']:
        raise ValueError("Wrong `write_method_name' parameter")

    if not hasattr(stdin, 'read'):
        raise ValueError("Object `{}' have no 'read' method".format(stdin))

    if not hasattr(stdout, 'read') and not hasattr(stdout, 'update'):
        raise ValueError("Object `{}' have no 'read' nor 'update' methods".format(stdout))

    if convert_to_str == True:
        convert_to_str = 'utf-8'
    elif convert_to_str == False:
        convert_to_str = None

    if (convert_to_str != None
        and not isinstance(convert_to_str, str)
        ):
        raise ValueError("convert_to_str can ony be str, bool or None")

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
            logging.info("Starting `{}' thread".format(thread_name))

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
                raise ValueError(
                    "Can read only binary (bytes) buffer (Not str or anything other)"
                    )

            if convert_to_str != None:
                buff = str(buff, encoding=convert_to_str)

            try:
                exec(
                    "stdout.{}(buff)".format(write_method_name)
                    )
            except TypeError as err_val:
                if err_val.args[0] == 'must be str, not bytes':
                    logging.warning(
                        "hint: check that output is in bytes mode or do conversion with convert_to_str option"
                        )
                raise
            except:
                logging.error(
                    "Can't use object's `{}' `{}' method".format(
                        stdout,
                        write_method_name
                        )
                    )
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
                logging.info(" Closing `{}' thread stdout".format(thread_name))
            stdout.close()

        if thread_name != 'Thread':
            logging.info("""\
  Ending `{name}' thread
        {{
           {num} cycles worked,
           {size} bytes ({sizem:4.2f} MiB) transferred,
           with buffer size {bufs} bytes ({bufm:4.2f} MiB)
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

    # control should never reach this return
    return

def lbl_write(stdin, stdout, threaded=False, typ='info'):

    if not typ in ['info', 'error', 'warning']:
        raise ValueError("Wrong `typ' value")

    if threaded:
        return threading.Thread(
            target=lbl_write,
            args=(stdin, stdout),
            kwargs=dict(threaded=False)
            )
    else:

        while True:
            l = stdin.readline()
            if isinstance(l, bytes):
                l = l.decode('utf-8')
            if l == '':
                break
            else:
                l = l.rstrip(' \0\n')

                if typ == 'info':
                    stdout.info(l)
                elif typ == 'error':
                    stdout.error(l)
                elif typ == 'warning':
                    stdout.warning(l)

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
