
import logging
import os
import select
import socket
import ssl
import threading
import time

import org.wayround.utils.signal

CAT_READWRITE_TYPES = [
    'file', 'pipe',
    'socket', 'ssl', 'pyopenssl',
    'socket-nb', 'ssl-nb', 'pyopenssl-nb'
    ]


class CatTerminationFlagFound(Exception): pass


def cat(
    stdin,
    stdout,
    bs=2 * 1024 ** 2,
    count=None,
    threaded=False,
    thread_name='Thread',
    verbose=False,
    convert_to_str=None,
    read_method_name='read',
    write_method_name='write',
    read_type='file',
    write_type='file',
    exit_on_input_eof=True,
    flush_after_every_write=False,
    flush_on_input_eof=False,
    close_output_on_eof=False,
    waiting_for_input=False,
    waiting_for_output=False,
    descriptor_to_wait_for_input=None,
    descriptor_to_wait_for_output=None,
    apply_input_seek=True,
    apply_output_seek=True,
    standard_write_method_result=True,
    termination_event=None,
    on_exit_callback=None,
    on_input_read_error=None,
    on_output_write_error=None,
    debug=False
    ):

    if not read_method_name.isidentifier():
        raise ValueError("Wrong `read_method_name' parameter")

    if not write_method_name.isidentifier():
        raise ValueError("Wrong `write_method_name' parameter")

    if not read_type in CAT_READWRITE_TYPES:
        raise ValueError("`read_type' must be file or socket")

    if not write_type in CAT_READWRITE_TYPES:
        raise ValueError("`write_type' must be file or socket")

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
            target=cat,
            args=(stdin, stdout),
            kwargs=dict(
                bs=bs,
                count=count,
                threaded=False,
                thread_name=thread_name,
                verbose=verbose,
                convert_to_str=convert_to_str,
                read_method_name=read_method_name,
                write_method_name=write_method_name,
                read_type=read_type,
                write_type=write_type,
                exit_on_input_eof=exit_on_input_eof,
                flush_after_every_write=flush_after_every_write,
                flush_on_input_eof=flush_on_input_eof,
                close_output_on_eof=close_output_on_eof,
                waiting_for_input=waiting_for_input,
                waiting_for_output=waiting_for_output,
                descriptor_to_wait_for_input=descriptor_to_wait_for_input,
                descriptor_to_wait_for_output=descriptor_to_wait_for_output,
                apply_input_seek=apply_input_seek,
                apply_output_seek=apply_output_seek,
                standard_write_method_result=standard_write_method_result,
                termination_event=termination_event,
                on_exit_callback=on_exit_callback,
                on_input_read_error=on_input_read_error,
                on_output_write_error=on_output_write_error,
                debug=debug
                ),
            name=thread_name
            )

    else:

        if termination_event and termination_event.is_set():
            raise CatTerminationFlagFound()

        if verbose:
            logging.info("Starting `{}' thread".format(thread_name))

        buff = None

        c = 0
        bytes_counter = 0

        if apply_input_seek and hasattr(stdin, 'seek'):
            try:
                stdin.seek(0)
            except:
                pass

        try:
            while True:

                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

                if waiting_for_input:
                    if debug:
                        logging.debug(
                            "{}: waiting for input descriptor {}".format(
                                thread_name,
                                descriptor_to_wait_for_input
                                )
                            )

                    while len(
                        select.select(
                            [descriptor_to_wait_for_input], [], [], 0.2
                            )[0]
                        ) == 0:

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        if debug:
                            logging.debug(
                                "{}: rewaiting for input descriptor {}".format(
                                    thread_name,
                                    descriptor_to_wait_for_input
                                    )
                                )

                    if debug:
                        logging.debug(
                            "{}: input descriptor {} - ready".format(
                                thread_name,
                                descriptor_to_wait_for_input
                                )
                            )

                if waiting_for_output:
                    if debug:
                        logging.debug(
                            "{}: waiting for output descriptor {}".format(
                                thread_name,
                                descriptor_to_wait_for_output
                                )
                            )

                    while len(
                        select.select(
                            [], [descriptor_to_wait_for_output], [], 0.2
                            )[1]
                        ) == 0:

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        if debug:
                            logging.debug(
                        "{}: rewaiting for output descriptor {}".format(
                            thread_name,
                            descriptor_to_wait_for_output
                            )
                                )

                    if debug:
                        logging.debug(
                            "{}: output descriptor {} - ready".format(
                                thread_name,
                                descriptor_to_wait_for_output
                                )
                            )

                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

                if debug:
                    logging.debug(
                        "{}: Reading stdin.{} using block size {}".format(
                            thread_name,
                            read_method_name,
                            bs
                            )
                        )

                buff = b''

                try:
                    if read_type in ['file', 'pipe']:
                        # waiting_for_input must be True in this case
                        buff = eval("stdin.{}(bs)".format(read_method_name))

                    elif read_type == 'socket':
                        # waiting_for_input must be True in this case
                        buff = eval("stdin.{}(bs)".format(read_method_name))

                    elif read_type == 'socket-nb':
                        # waiting_for_input must be True in this case
                        while True:
                            if (termination_event
                                and termination_event.is_set()):
                                raise CatTerminationFlagFound()
                            try:
                                buff = eval(
                                    "stdin.{}(bs)".format(read_method_name)
                                    )
                            except BlockingIOError:
                                pass
                            else:
                                break

                    elif read_type == 'ssl-nb':
                        while True:

                            if (termination_event
                                and termination_event.is_set()):
                                raise CatTerminationFlagFound()

                            try:
                                buff = eval(
                                    "stdin.{}(bs)".format(read_method_name)
                                    )

                            except BlockingIOError:
                                pass

                            except ssl.SSLWantReadError:
                                select.select(
                                    [descriptor_to_wait_for_input], [], []
                                    )

                            except ssl.SSLWantWriteError:
                                select.select(
                                    [], [descriptor_to_wait_for_output], []
                                    )
                            else:
                                break

                    else:
                        # TODO: this function need to be splitted, it such a
                        # mess now
                        raise Exception("Whoot?")

                except:
                    if on_input_read_error:
                        threading.Thread(
                            target=on_input_read_error,
                            name="{} Input Read Error Thread".format(
                                thread_name
                                )
                            ).start()

                    break

                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

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

                    if debug:
                        logging.debug(
                            "{}: Readed  {} bytes using stdin.{}".format(
                                thread_name,
                                buff_len,
                                read_method_name
                                )
                            )

                        logging.debug(
                            "{}: buff data: {}".format(
                                thread_name,
                                repr(buff)
                                )
                            )

                    if convert_to_str != None:
                        buff = str(buff, encoding=convert_to_str)

                    written_total = 0
                    this_time_written = 0

                    if termination_event and termination_event.is_set():
                        raise CatTerminationFlagFound()

                    while True:
                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        if debug:

                            logging.debug(
                                "{}: Writing {} bytes using stdout.{}".format(
                                    thread_name,
                                    buff_len,
                                    write_method_name
                                    )
                                )
                        try:
                            if standard_write_method_result:
                                this_time_written = eval(
                                    "stdout.{}(buff[written_total:])".format(
                                        write_method_name
                                        )
                                    )
                            else:
                                this_time_written = eval(
                                    "stdout.{}(buff)".format(
                                        write_method_name
                                        )
                                    )

                        except TypeError as err_val:
                            if err_val.args[0] == 'must be str, not bytes':
                                logging.warning(
                "{}: hint: check that output is in bytes mode or do"
                " conversion with convert_to_str option".format(thread_name)
                                    )
                            raise
                        except:
                            logging.error(
                                "{}: Can't use object's `{}' `{}' method.\n"
                                "    (Output process closed it's input. "
                                "It can be not an error)".format(
                                    thread_name,
                                    stdout,
                                    write_method_name
                                    )
                                )
                            if on_output_write_error:
                                threading.Thread(
                                    target=on_output_write_error,
                                    name="`{}' Output Error Thread".format(
                                        thread_name
                                        )
                                    ).start()

                            raise

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        if flush_after_every_write:
                            stdout.flush()

                        if standard_write_method_result:
                            if debug:
                                logging.debug(
                        "{}: Written {} bytes using stdout.{}".format(
                            thread_name,
                            this_time_written,
                            write_method_name
                            )
                                    )
                            if this_time_written == 0:
                                if on_output_write_error:
                                    threading.Thread(
                                        target=on_output_write_error,
                                        name="`{}' Output Error Thread".format(
                                            thread_name
                                            )
                                        ).start()
                                break
                            else:
                                written_total += this_time_written
                                if written_total >= buff_len:
                                    break
                        else:
                            if debug:
                                logging.debug(
                                    "{}: Written bytes using stdout.{}".format(
                                        thread_name,
                                        write_method_name
                                        )
                                    )
                            break

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                    if termination_event and termination_event.is_set():
                        raise CatTerminationFlagFound()

                    if isinstance(buff, bytes):
                        bytes_counter += buff_len

                    buff = None

                else:

                    if debug:
                        logging.debug(
                            "{}: Readed `None' or 0. -- EOF".format(
                                thread_name
                                )
                            )

                    if flush_on_input_eof:
                        stdout.flush()

                    if exit_on_input_eof:
                        break

                c += 1

                if count != None:
                    if c == count:
                        break

                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

        except CatTerminationFlagFound:
            if debug:
                logging.debug(
                    "{}: Termination flag caught".format(thread_name)
                    )
        except:
#            if not threaded:
#                raise
#            else:
            logging.exception(
                "{}: Exception in cat thread".format(thread_name)
                )

        if apply_output_seek and hasattr(stdout, 'seek'):
            try:
                stdout.seek(0, os.SEEK_END)
            except:
                pass

        if close_output_on_eof:
            if verbose:
                logging.info(" {}: Closing thread stdout".format(thread_name))
            stdout.close()

        if verbose:
            logging.info("""\
  Ending `{name}' thread
        {{
           {num} cycles worked,
           {size} bytes ({sizem:4.2f} MiB) transferred,
           with buffer size {bufs} bytes ({bufm:4.2f} MiB)
        }}
""".format_map({
        'name': thread_name,
        'num': c,
        'size': bytes_counter,
        'sizem': (float(bytes_counter) / 1024 / 1024),
        'bufs': bs,
        'bufm': (float(bs) / 1024 / 1024)
        }
        )
    )

        if on_exit_callback:
            threading.Thread(
                target=on_exit_callback,
                name="{} Exited Callback Thread".format(thread_name)
                ).start()

        return

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


class SocketStreamer(org.wayround.utils.signal.Signal):
    """
    Featured class for flexibly handling socket connection

    Signals:
    'start' (self, self.socket)
    'stop' (self, self.socket)
    'error' (self, self.socket)
    'restart' (self, self.socket)
    'ssl wrap error' (self, self.socket)
    'ssl wrapped' (self, self.socket)
    'ssl ununwrapable' (self, self.socket)
    'ssl unwrap error' (self, self.socket)
    'ssl unwrapped' (self, self.socket)
    """

    def __init__(self, sock, socket_transfer_size=4096, debug=False):

        super().__init__(
            ['start',
             'stop',
             'error',
             'restart',
             'ssl wrap error',
             'ssl wrapped',
             'ssl ununwrapable',
             'ssl unwrap error',
             'ssl unwrapped'
             ]
            )

        if sock.gettimeout() != 0:
            raise ValueError("`sock' timeout must be 0")

        if not isinstance(sock, (socket.socket, ssl.SSLSocket)):
            raise TypeError(
                "sock must be of type socket.socket or ssl.SSLSocket"
                )

        self.socket = sock
        self._socket_transfer_size = socket_transfer_size
        self._debug = debug

        self._clear(init=True)

        self.connection = False

    def __del__(self):

        self._clear()

    def _clear(self, init=False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError(
                    "{} is not stopped".format(type(self).__name__)
                    )

        if not init:
            self._close_pipe_descriptors()

        self._pipe_outside = None
        self._pipe_inside = None

        # From remote process to current process.
        # For instance internals.
        self._strout = None
        # For instance user.
        self.strout = None

        # From current process to remote process.
        # For instance internals.
        self._strin = None
        # For instance user.
        self.strin = None

        # from strin to socket
        self._in_thread = None

        # from socket to strout
        self._out_thread = None

        self._connection_error_signalled = False
        self._connection_stop_signalled = False
        self._starting = False
        self._starting_threads = False
        self._stop_flag = False
        self._stopping = False
        self._stopping_threads = False
        self._wrapping = False

        self._output_availability_watcher_thread = None

        if not init:
            self._in_thread_stop_event.set()
            self._out_thread_stop_event.set()

        self._in_thread_stop_event = threading.Event()
        self._out_thread_stop_event = threading.Event()

        self._output_avalability_indicated = False

        self._stat = 'stopped'

        self.connection = False

        self._socket_status_printer = None

        return

    def get_socket(self):
        return self.socket

    def _close_pipe_descriptors(self):
        for i in [self._strout, self.strout, self._strin, self.strin]:
            if i:
                i.close()

    def _start_threads(self):

        if not self._starting_threads and not self._stopping_threads:

            self._starting_threads = True

            self._stat = 'soft starting threads'

            sock_type = 'socket-nb'
            wait_for_socket = False
            if self.is_ssl_working():
                sock_type = 'ssl-nb'

            self._in_thread = cat(
                stdin=self._strin,
                stdout=self.socket,
                threaded=True,
                write_method_name='send',
                close_output_on_eof=False,
                thread_name='strin -> socket',
                bs=self._socket_transfer_size,
                convert_to_str=None,
                read_method_name='read',
                read_type='pipe',
                write_type=sock_type,
                exit_on_input_eof=True,
                waiting_for_input=True,
                descriptor_to_wait_for_input=self._strin.fileno(),
                waiting_for_output=wait_for_socket,
                descriptor_to_wait_for_output=self.socket.fileno(),
                apply_input_seek=False,
                apply_output_seek=False,
                flush_on_input_eof=False,
                on_exit_callback=self._on_in_thread_exit,
                on_output_write_error=self._on_socket_write_error,
                termination_event=self._in_thread_stop_event,
                flush_after_every_write=False,
                debug=self._debug
                )

            self._out_thread = cat(
                stdin=self.socket,
                stdout=self._strout,
                threaded=True,
                write_method_name='write',
                close_output_on_eof=False,
                thread_name='socket -> strout',
                bs=self._socket_transfer_size,
                convert_to_str=None,
                read_method_name='recv',
                read_type=sock_type,
                write_type='pipe',
                exit_on_input_eof=True,
                waiting_for_input=wait_for_socket,
                descriptor_to_wait_for_input=self.socket.fileno(),
                waiting_for_output=True,
                descriptor_to_wait_for_output=self._strout.fileno(),
                apply_input_seek=False,
                apply_output_seek=False,
                flush_on_input_eof=True,
                on_exit_callback=self._on_out_thread_exit,
                on_input_read_error=self._on_socket_read_error,
                termination_event=self._out_thread_stop_event,
                flush_after_every_write=True,
                debug=self._debug
                )

            self._in_thread.start()
            self._out_thread.start()
            self._stat = 'soft started threads'

            self._starting_threads = False

        return

    def _stop_threads(self):

        if not self._starting_threads and not self._stopping_threads:

            self._stopping_threads = True

            self._stat = 'soft stopping threads'
            self._in_thread_stop_event.set()
            self._out_thread_stop_event.set()

            self.wait('stopped')

            self._in_thread_stop_event.clear()
            self._out_thread_stop_event.clear()
            self._stat = 'soft stopped threads'

            self._stopping_threads = False

    def _send_connection_stopped_event(self):
        if not self._wrapping:
            if not self._connection_stop_signalled:
                self._connection_stop_signalled = True

                self.emit_signal('stop', self, self.socket)

    def _send_connection_error_event(self):
        if not self._wrapping:
            if not self._connection_error_signalled:
                self._connection_error_signalled = True

                self.emit_signal('error', self, self.socket)

    def _restart_threads(self):
        self._stat = 'soft restarting threads'
        self._stop_threads()
        self._start_threads()
        self._stat = 'soft restarted threads'

        self.emit_signal('restart', self, self.socket)

    def start(self):

        if (not self._starting
            and not self._stopping
            and self.stat() == 'stopped'):

            self._starting = True
            self._stat = 'hard starting'
            self._stop_flag = False

            self._pipe_outside = os.pipe()
            self._pipe_inside = os.pipe()

            self._strout = open(self._pipe_outside[1], 'wb', buffering=0)
            self.strout = open(self._pipe_outside[0], 'rb', buffering=0)

            self._strin = open(self._pipe_inside[0], 'rb', buffering=0)
            self.strin = open(self._pipe_inside[1], 'wb', buffering=0)

            self._start_threads()

            self._output_availability_watcher_thread = threading.Thread(
                target=self._output_availability_watcher,
                name="Socket Output Availability Watcher Thread"
                )

            self._output_availability_watcher_thread.start()

            self.wait('working')

            self._starting = False
            self._stat = 'hard started'

        return

    def stop(self):

        if (not self._stopping
            and not self._starting
            and not self.stat() == 'stopped'):

            self._stat = 'hard stopping'

            self._stopping = True

            self._stop_flag = True
#            self._close_pipe_descriptors()

            self._stop_threads()

            self.wait('stopped')

            self._unwrap_procedure()

#            self._socket_status_printer.stop()
#            self._socket_status_printer.wait('stopped')

            self._clear()

            self._stopping = False

            self._stat = 'hard stopped'

        return

    def start_ssl(self, *args, **kwargs):
        """
        All parameters, same as for ssl.wrap_socket(). Exception is parameter
        socket, which
        taken from self.socket
        """

        #        logging.debug(
        #            """start_tls before if:
        #self._wrapping:      {}
        #self._stopping:      {}
        #self._starting:      {}
        #self.is_ssl_working: {}
        #""".format(self._wrapping , self._stopping, self._starting,
        #self.is_ssl_working()))

        if (
            not self._wrapping
            and not self._stopping
            and not self._starting
            and not self.is_ssl_working()
            ):

            self._wrapping = True

            if len(args) > 0:
                if issubclass(args[0], socket.socket):
                    del args[0]

            if 'sock' in kwargs:
                del kwargs['sock']

            kwargs['do_handshake_on_connect'] = False

            s = None

            self._stop_threads()

            logging.debug('before wrap sock is {}'.format(self.socket))

            try:
                s = ssl.wrap_socket(
                    self.socket,
                    *args,
                    **kwargs
                    )

                while True:
                    try:
                        s.do_handshake()
                        break
                    except ssl.SSLWantReadError:
                        select.select([s], [], [])
                    except ssl.SSLWantWriteError:
                        select.select([], [s], [])

            except:
                logging.exception("ssl wrap error")
                self.emit_signal('ssl wrap error', self, self.socket)
            else:
                logging.info(
                    """
peer cert:
{}
cipher:
{}
compression:
{}""".format(
                        repr(s.getpeercert(binary_form=False)),
                        repr(s.cipher()),
                        repr(s.compression())
                        )
                    )

                self.socket = s

#                self._socket_status_printer.set_fd(self.socket.fileno())

                logging.debug('after wrap sock is {}'.format(self.socket))

                self._start_threads()

                self.emit_signal('ssl wrapped', self, self.socket)

            self._wrapping = False

    def stop_ssl(self):

        if not self._wrapping and not self._stopping and not self._starting:

            if not self.connection:

                logging.debug(
                    "Connection already gone. "
                    "Unwrapping is pointless (and erroneous)"
                    )
                self.emit_signal('ssl ununwrapable', self, self.socket)

            else:

                self._wrapping = True

                logging.debug('before unwrap sock is {}'.format(self.socket))

                self._stop_threads()

                s = None
                try:
                    s = self.socket.unwrap()
                except:
                    logging.exception("ssl unwrap error")
                    self.emit_signal('ssl unwrap error', self, self.socket)

                else:
                    self.socket = s

#                    self._socket_status_printer.set_fd(self.socket.fileno())

                    self._start_threads()

                    logging.debug(
                        'after unwrap sock is {}'.format(self.socket)
                        )

                    self.emit_signal('ssl unwrapped', self, self.socket)

            self._wrapping = False

    def _unwrap_procedure(self):
        if self.is_ssl_working():
            self.stop_ssl()
        else:
            logging.debug("Socket not wrapped - unwrapping not needed")

    def is_ssl_working(self):

        return isinstance(self.socket, ssl.SSLSocket)

    def stat(self):

        ret = 'unknown'

        v1 = self._in_thread
        v2 = self._out_thread
        v3 = self._output_availability_watcher_thread

#        logging.debug("{}, {}, {}".format(v1, v2, v3))

        if (
            bool(v1)
            and bool(v2)
            ):
            ret = 'working'

        elif (
            not bool(v1)
            and not bool(v2)
            and not bool(v3)
            ):
            ret = 'stopped'

        else:
            ret = self._stat

        return ret

    def wait(self, what='stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            s = self.stat()
            if s == what:
                break
            time.sleep(0.1)

        return

    def _on_in_thread_exit(self):
        self._in_thread = None
        self._on_in_out_thread_exit()

    def _on_out_thread_exit(self):
        self._out_thread = None
        self._on_in_out_thread_exit()

    def _on_in_out_thread_exit(self):

        if not self._wrapping:
            self.connection = False
            self.socket.close()
            self._unwrap_procedure()
            self._send_connection_stopped_event()

        self._stop_threads()

    def _on_socket_write_error(self):
        self._on_read_write_error()

    def _on_socket_read_error(self):
        self._on_read_write_error()

    def _on_read_write_error(self):
        self.connection = False

        self._stop_threads()

        self._send_connection_error_event()

    def _output_availability_watcher(self):

        stopped_by_flag = 0

        while len(select.select([], [self.socket.fileno()], [], 0.2)[1]) == 0:

            if self._stop_flag:
                stopped_by_flag = 1
                break

        if stopped_by_flag == 0:

            if not self._wrapping:

                self.connection = True

                self.emit_signal('start', self, self.socket)

        self._output_availability_watcher_thread = None

        return
