
import io
import logging
import os
import select
import subprocess
import threading

import org.wayround.utils.exec


def cat(
    stdin,
    stdout,
    threaded = False,
    write_method_name = 'write',
    close_output_on_eof = False,
    thread_name = 'Thread',
    bs = (2 * 1024 ** 2),
    convert_to_str = None,
    read_method_name = 'read',
    exit_on_input_eof = True,
    waiting_for_input = False,
    descriptor_to_wait_for_input = None,
    waiting_for_output = False,
    descriptor_to_wait_for_output = None,
    apply_input_seek = True,
    apply_output_seek = True,
    flush_on_input_eof = False,
    standard_write_method_result = True
    ):

    return dd(
        stdin,
        stdout,
        bs = bs,
        count = None,
        threaded = threaded,
        write_method_name = write_method_name,
        close_output_on_eof = close_output_on_eof,
        thread_name = thread_name,
        convert_to_str = convert_to_str,
        read_method_name = read_method_name,
        exit_on_input_eof = exit_on_input_eof,
        waiting_for_input = waiting_for_input,
        descriptor_to_wait_for_input = descriptor_to_wait_for_input,
        waiting_for_output = waiting_for_output,
        descriptor_to_wait_for_output = descriptor_to_wait_for_output,
        apply_input_seek = apply_input_seek,
        apply_output_seek = apply_output_seek,
        flush_on_input_eof = flush_on_input_eof,
        standard_write_method_result = standard_write_method_result
        )

def dd(
    stdin,
    stdout,
    bs = (2 * 1024 ** 2),
    count = None,
    threaded = False,
    write_method_name = 'write',
    close_output_on_eof = False,
    thread_name = 'Thread',
    convert_to_str = None,
    read_method_name = 'read',
    exit_on_input_eof = True,
    waiting_for_input = False,
    descriptor_to_wait_for_input = None,
    waiting_for_output = False,
    descriptor_to_wait_for_output = None,
    apply_input_seek = True,
    apply_output_seek = True,
    flush_on_input_eof = False,
    standard_write_method_result = True
    ):

    if not read_method_name.isidentifier():
        raise ValueError("Wrong `read_method_name' parameter")

    if not write_method_name.isidentifier():
        raise ValueError("Wrong `write_method_name' parameter")

    if not hasattr(stdin, read_method_name):
        raise ValueError(
            "Object `{}' have no '{}' method".format(stdin, read_method_name)
            )

    if not hasattr(stdout, write_method_name):
        raise ValueError(
            "Object `{}' have no '{}' method".format(stdout, write_method_name)
            )

    if convert_to_str == True:
        convert_to_str = 'utf-8'
    elif convert_to_str == False:
        convert_to_str = None

    if (convert_to_str != None
        and not isinstance(convert_to_str, str)
        ):
        raise ValueError(
            "convert_to_str can only be str(encoding name), bool or None"
            )

    if thread_name == None:
        thread_name = 'Thread'

    if threaded:

        return threading.Thread(
            target = dd,
            args = (stdin, stdout),
            kwargs = dict(
                bs = bs,
                count = count,
                threaded = False,
                close_output_on_eof = close_output_on_eof,
                write_method_name = write_method_name,
                thread_name = thread_name,
                convert_to_str = convert_to_str,
                read_method_name = read_method_name,
                exit_on_input_eof = exit_on_input_eof,
                waiting_for_input = waiting_for_input,
                descriptor_to_wait_for_input = descriptor_to_wait_for_input,
                waiting_for_output = waiting_for_output,
                descriptor_to_wait_for_output = descriptor_to_wait_for_output,
                apply_input_seek = apply_input_seek,
                apply_output_seek = apply_output_seek,
                flush_on_input_eof = flush_on_input_eof,
                standard_write_method_result = standard_write_method_result
                ),
            name = thread_name
            )

    else:

        if thread_name != 'Thread':
            logging.info("Starting `{}' thread".format(thread_name))

        buff = ' '

        c = 0
        bytes_counter = 0

        if apply_input_seek and hasattr(stdin, 'seek'):
            try:
                stdin.seek(0)
            except:
                pass

        while True:

            if waiting_for_input:
                logging.debug(
                    "waiting for input descriptor {}".format(
                        descriptor_to_wait_for_input
                        )
                    )

                in_poll = select.poll()
                in_poll.register(descriptor_to_wait_for_input, select.POLLIN)
                in_poll.poll()
#                select.select([descriptor_to_wait_for_input], [], [])

                logging.debug(
                    "got input from descriptor {}".format(
                        descriptor_to_wait_for_input
                        )
                    )

            if waiting_for_output:
                logging.debug(
                    "waiting for output descriptor {}".format(
                        descriptor_to_wait_for_output
                        )
                    )

                out_poll = select.poll()
                out_poll.register(descriptor_to_wait_for_output, select.POLLOUT)
                out_poll.poll()
#                select.select([], [descriptor_to_wait_for_output], [])

                logging.debug(
                    "got output to descriptor {}".format(
                        descriptor_to_wait_for_output
                        )
                    )

            buff = None

            logging.debug(
                "Reading {} bytes from stdin.{}".format(
                    bs,
                    read_method_name
                    )
                )

            try:
                buff = eval("stdin.{}(bs)".format(read_method_name))
            except:
                raise

            if buff:

                if not isinstance(buff, bytes):
                    raise TypeError(
                        (
                         "Can read only bytes buffer "
                         "(Not str or anything other), but "
                         "buffer is ({}):{}"
                         ).format(
                            type(buff),
                            buff
                            )
                        )

                buff_len = len(buff)

                logging.debug(
                    "Readen  {} bytes using stdin.{}".format(
                        buff_len,
                        read_method_name
                        )
                    )

#                logging.debug("buff data: {}".format(repr(buff)))

                if convert_to_str != None:
                    buff = str(buff, encoding = convert_to_str)

                logging.debug(
                    "Writing {} bytes to stdout.{}".format(
                        bs,
                        read_method_name
                        )
                    )

                written_total = 0
                this_time_written = 0

                while True:
                    try:
                        this_time_written = eval(
                            "stdout.{}(buff[written_total:])".format(
                                write_method_name
                                )
                            )
                    except TypeError as err_val:
                        if err_val.args[0] == 'must be str, not bytes':
                            logging.warning(
                                "hint: check that output is in bytes mode or do"
                                " conversion with convert_to_str option"
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

                    if standard_write_method_result:
                        if this_time_written == 0:
                            raise RuntimeError("Output write error")
                        else:
                            written_total += this_time_written
                            if written_total >= buff_len:
                                break
                    else:
                        # TODO: I don't like this, but for now it is better when
                        #       was
                        break

                if isinstance(buff, bytes):
                    bytes_counter += buff_len
            else:

                logging.debug("Readed `None' or 0. -- EOF")

                if flush_on_input_eof:
                    stdout.flush()

                if exit_on_input_eof:
                    break

            c += 1

            if count != None:
                if c == count:
                    break

        if apply_output_seek and hasattr(stdout, 'seek'):
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


    return

def lbl_write(stdin, stdout, threaded = False, typ = 'info'):

    if not typ in ['info', 'error', 'warning']:
        raise ValueError("Wrong `typ' value")

    if threaded:
        return threading.Thread(
            target = lbl_write,
            args = (stdin, stdout),
            kwargs = dict(threaded = False)
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
    stdin = subprocess.PIPE,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    options = [],
    bufsize = 0,
    cwd = None
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

class SocketStreamer:

    def __init__(self, sock, socket_transfer_size = 4096):
        self.sock = sock

        self._pipe_outside = os.pipe()
        self._pipe_inside = os.pipe()

        # From remote process to current process.
        # For instance internals.
        self._strout = open(self._pipe_outside[1], 'wb', buffering = 4096)
        # For instance user.
        self.strout = open(self._pipe_outside[0], 'rb', buffering = 4096)


        # From current process to remote process.
        # For instance internals.
        self._strin = open(self._pipe_inside[0], 'rb', buffering = 4096)
        # For instance user.
        self.strin = open(self._pipe_inside[1], 'wb', buffering = 4096)


        # from strin to socket
        self.in_thread = cat(
            stdin = self._strin,
            stdout = self.sock,
            threaded = True,
            write_method_name = 'send',
            close_output_on_eof = False,
            thread_name = 'strin -> sock',
#            thread_name=None,
            bs = socket_transfer_size,
            convert_to_str = None,
            read_method_name = 'read',
            exit_on_input_eof = False,
            waiting_for_input = True,
            descriptor_to_wait_for_input = self._strin.fileno(),
            waiting_for_output = True,
            descriptor_to_wait_for_output = self.sock.fileno(),
            apply_input_seek = False,
            apply_output_seek = False,
            flush_on_input_eof = False
            )

        # from socket to strout
        self.out_thread = cat(
            stdin = self.sock,
            stdout = self._strout,
            threaded = True,
            write_method_name = 'write',
            close_output_on_eof = True,
            thread_name = 'sock -> strout',
#            thread_name=None,
            bs = socket_transfer_size,
            convert_to_str = None,
            read_method_name = 'recv',
            exit_on_input_eof = True,
            waiting_for_input = True,
            descriptor_to_wait_for_input = self.sock.fileno(),
            waiting_for_output = True,
            descriptor_to_wait_for_output = self._strout.fileno(),
            apply_input_seek = False,
            apply_output_seek = False,
            flush_on_input_eof = True
            )


    def start(self):
        self.in_thread.start()
        self.out_thread.start()


    def close(self):

        if not self.strout.closed:
            self.strout.close()

        if not self.strin.closed:
            self.strin.close()

        self.out_thread.join()
        self.in_thread.join()
