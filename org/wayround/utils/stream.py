
import logging
import os
import select
import socket
import ssl
import threading
import time

import org.wayround.utils.threading

# blockables
CAT_READWRITE_B = ['file', 'pipe',
                   'socket', 'ssl', 'pyopenssl']

# non-blockables
CAT_READWRITE_NB = ['pipe-nb',
                    'socket-nb', 'ssl-nb', 'pyopenssl-nb']


CAT_READWRITE_TYPES = CAT_READWRITE_NB + CAT_READWRITE_B


SELECTABLE = ['socket-nb', 'ssl-nb', 'pyopenssl-nb', 'pipe-nb']


class CatTerminationFlagFound(Exception):
    pass


class Streamer:

    def __init__(
        self,
        stream_object,
        stream_object_read_meth,
        stream_object_write_meth,
        stream_object_mode='file',
        bs=2 * 1024 ** 2,
        descriptor_to_wait_for=None,
        flush_after_each_write=False,
        standard_write_method_result=None,
        thread_name='Thread',
        termination_event=None,
        verbose=False,
        debug=False,
        on_exit_callback=None,
        on_input_read_error=None,
        on_output_write_error=None
        ):

        if not stream_object_mode in CAT_READWRITE_TYPES:
            raise ValueError("invalid `descriptor_mode'")

        if bs < 1:
            raise ValueError("invalid `bs'")

        if not standard_write_method_result in [None, False, True]:
            raise ValueError("invalid `standard_write_method_result'")

        self._verbose = verbose
        self._debug = debug

        self._bs = bs

        self._stream_object = stream_object
        self._stream_object_mode = stream_object_mode

        self._stream_object_read_meth = stream_object_read_meth
        self._stream_object_write_meth = stream_object_write_meth

        self._descriptor_to_wait_for = descriptor_to_wait_for

        self._standard_write_method_result = standard_write_method_result

        self._thread_name = thread_name

        self._flush_after_each_write = flush_after_each_write

        self._on_input_read_error = on_input_read_error

        self._termination_event = termination_event

        return

    def _wait_input_avail(self):

        if self._debug:
            logging.debug(
                "{}: waiting for input descriptor {}".format(
                    self._thread_name,
                    self._descriptor_to_wait_for
                    )
                )

        while len(
            select.select([self._descriptor_to_wait_for], [], [], 0.2)[0]
            ) == 0:

            if (self._termination_event
                and self._termination_event.is_set()):
                raise CatTerminationFlagFound()

            if self._debug:
                logging.debug(
                    "{}: rewaiting for input descriptor {}".format(
                        self._thread_name,
                        self._descriptor_to_wait_for
                        )
                    )

        if self._debug:
            logging.debug(
                "{}: input descriptor {} - ready".format(
                    self._thread_name,
                    self._descriptor_to_wait_for
                    )
                )

        return

    def _wait_output_avail(self):

        if self._debug:
            logging.debug(
                "{}: waiting for output descriptor {}".format(
                    self._thread_name,
                    self._descriptor_to_wait_for
                    )
                )

        while len(
            select.select([], [self._descriptor_to_wait_for], [], 0.2)[1]
            ) == 0:

            if (self._termination_event
                and self._termination_event.is_set()):
                raise CatTerminationFlagFound()

            if self._debug:
                logging.debug(
            "{}: rewaiting for output descriptor {}".format(
                self._thread_name,
                self._descriptor_to_wait_for
                )
                    )

        if self._debug:
            logging.debug(
                "{}: output descriptor {} - ready".format(
                    self._thread_name,
                    self._descriptor_to_wait_for
                    )
                )

        return

    def read(self):

        """
        ret[0] == True - stream closed
        """

        ret_closed = False
        ret_buff = None

        try:

            if self._stream_object_mode in ['file', 'pipe', 'socket']:

                if self._stream_object_mode in SELECTABLE:
                    self._wait_input_avail()

                if (self._termination_event
                    and self._termination_event.is_set()):
                    raise CatTerminationFlagFound()

                res = self._stream_object_read_meth(self._bs)

                if len(res) == 0:
                    ret_closed = True
                    ret_buff = None
                    res = None

                else:

                    ret_closed = False
                    ret_buff = res
                    res = None

            elif (self._stream_object_mode
                  in ['socket-nb', 'ssl-nb', 'pipe-nb']):

                while True:

                    if self._stream_object_mode in SELECTABLE:
                        self._wait_input_avail()

                    if (self._termination_event
                        and self._termination_event.is_set()):
                        raise CatTerminationFlagFound()

                    try:
                        ret_buff = self._stream_object_read_meth(self._bs)

                    except BlockingIOError:
                        pass

                    except ssl.SSLWantReadError:
                        pass
                        # TODO: try to replace with self._wait_input_avail()
#                        select.select(
#                            [self._descriptor_to_wait_for],
#                            [self._descriptor_to_wait_for],
##                            [],
#                            []
#                            )

                    except ssl.SSLWantWriteError:
                        pass
                        # TODO: try to replace with self._wait_input_avail()
#                        select.select(
#                            [self._descriptor_to_wait_for],
##                            [],
#                            [self._descriptor_to_wait_for],
#                            []
#                            )
                    else:
                        #                        ret_closed = True
                        break

            else:
                raise Exception(
                    "Programming error: self._stream_object_mode == {}".format(
                        self._stream_object_mode
                        )
                    )

        except CatTerminationFlagFound:
            logging.debug(
                "Caught termination flag in read method of {}:{}".format(
                    self,
                    self._thread_name
                    )
                )

            ret_closed = True
            ret_buff = None

            raise

        except:
            if self._on_input_read_error:
                threading.Thread(
                    target=self._on_input_read_error,
                    name="{} Input Read Error Thread".format(
                        self._thread_name
                        )
                    ).start()

            ret_closed = True
            ret_buff = None

            raise

        if not ret_closed and not isinstance(ret_buff, bytes):
            ret_closed = True
            raise TypeError(
                (
                 "Can read only bytes buffer "
                 "(Not str or anything other), but "
                 "buffer is ({}):{}..."
                 ).format(
                    type(ret_buff),
                    repr(ret_buff)[:100]
                    )
                )

        ret = ret_closed, ret_buff

        return ret

    def write(self, buff):

        if buff:

            if (self._termination_event
                and self._termination_event.is_set()):
                raise CatTerminationFlagFound()

            try:

                while len(buff) != 0:

                    if self._stream_object_mode in SELECTABLE:
                        self._wait_output_avail()

                    sb = buff[:self._bs]
                    buff = buff[self._bs:]
                    self._stream_object_write_meth(sb)

                    if self._flush_after_each_write:
                        self._stream_object.flush()

            except TypeError as err_val:
                if err_val.args[0] == 'must be str, not bytes':
                    logging.warning(
    "{}: hint: check that output is in bytes mode or do"
    " conversion with convert_to_str option".format(self._thread_name)
                        )
                raise

            except CatTerminationFlagFound:
                logging.debug(
                    "Caught termination flag in write method of {}:{}".format(
                        self,
                        self._thread_name
                        )
                    )

                raise

            except:

                logging.error(
                    "{}: Can't use object's `{}' `{}' method.\n"
                    "    (Output process closed it's input. "
                    "It can be not an error)".format(
                        self._thread_name,
                        self._stream_object,
                        self._stream_object_write_meth
                        )
                    )

                if self._on_output_write_error:
                    threading.Thread(
                        target=self._on_output_write_error,
                        name="`{}' Output Error Thread".format(
                            self._thread_name
                            )
                        ).start()

                raise

        return


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
    flush_after_each_write=False,
    flush_on_input_eof=False,
    close_output_on_eof=False,
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
                flush_after_each_write=flush_after_each_write,
                flush_on_input_eof=flush_on_input_eof,
                close_output_on_eof=close_output_on_eof,
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

    #    if termination_event and termination_event.is_set():
    #        return None

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

    read_method = getattr(stdin, read_method_name)
    write_method = getattr(stdout, write_method_name)

    s1 = Streamer(
        stdin,
        read_method,
        None,
        stream_object_mode=read_type,
        bs=bs,
        descriptor_to_wait_for=descriptor_to_wait_for_input,
        thread_name='Input Streamer {}'.format(thread_name),
        termination_event=termination_event,
        verbose=verbose,
        debug=debug
        )

    s2 = Streamer(
        stdout,
        None,
        write_method,
        stream_object_mode=write_type,
        bs=bs,
        descriptor_to_wait_for=descriptor_to_wait_for_output,
        thread_name='Output Streamer {}'.format(thread_name),
        flush_after_each_write=flush_after_each_write,
        termination_event=termination_event,
        verbose=verbose,
        debug=debug
        )

    try:
        while True:

            if termination_event and termination_event.is_set():
                raise CatTerminationFlagFound()

            closed, buff = s1.read()

            if not closed:

                if debug:

                    buff_len = len(buff)
                    logging.debug(
                        "{}: Readed  {} bytes using method `{}'".format(
                            thread_name,
                            buff_len,
                            read_method
                            )
                        )
                    logging.debug(
                        "{}: buff data: {}".format(
                            thread_name,
                            repr(buff)
                            )
                        )
                    logging.debug(
                        "{}: Writing {} bytes using method `{}'".format(
                            thread_name,
                            buff_len,
                            write_method
                            )
                        )
                if convert_to_str != None:
                    buff = str(buff, encoding=convert_to_str)

                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

                s2.write(buff)

            else:
                if exit_on_input_eof:
                    break

            c += 1

            if isinstance(buff, (bytes, str)):
                if isinstance(buff, bytes):
                    bytes_counter += len(buff)
                if isinstance(buff, str):
                    bytes_counter += len(bytes(buff, 'utf-8'))

    except CatTerminationFlagFound:
        if debug:
            logging.debug(
                "{}: Termination flag caught".format(thread_name)
                )

    except:
        logging.exception(
            "{}: Exception in cat thread".format(thread_name)
            )

    if flush_on_input_eof:
        stdout.flush()

    if apply_output_seek and hasattr(stdout, 'seek'):
        try:
            stdout.seek(0, os.SEEK_END)
        except:
            pass

    if close_output_on_eof:
        if verbose:
            logging.info(" {}: Closing thread stdout".format(thread_name))

#        if write_type in CAT_READWRITE_NB:
#            stdout.write(b'')

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


class SocketStreamer:
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

        self.signal = org.wayround.utils.threading.Signal(
            self,
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

        self._pipe_inside = os.pipe2(os.O_NONBLOCK)
        self._pipe_outside = os.pipe2(os.O_NONBLOCK)

        # From remote process to current process.
        # For instance internals.
        self._strout = open(self._pipe_outside[1], 'wb', buffering=0)
        # For instance user.
        self.strout = open(self._pipe_outside[0], 'rb', buffering=0)

        # From current process to remote process.
        # For instance internals.
        self._strin = open(self._pipe_inside[0], 'rb', buffering=0)
        # For instance user.
        self.strin = open(self._pipe_inside[1], 'wb', buffering=0)

        # from strin to socket
        self._in_thread = None

        # from socket to strout
        self._out_thread = None

        self._connection_error_signalled = False
        self._connection_stop_signalled = False

        self._wrapping = False

        # flag indicating stop for instance threads
        self._stop_flag = False

        self._output_availability_watcher_thread = None
        self.connection = False

        self._in_thread_stop_event = threading.Event()
        self._out_thread_stop_event = threading.Event()

        return

    def __del__(self):
        try:
            self.destroy()
        except:
            logging.exception("Error destroying {}".format(self))
        return

    def destroy(self):
        self.stop()
        self._close_pipe_descriptors()
        return

    def get_socket(self):
        return self.socket

    def _close_pipe_descriptors(self):
        for i in [self._strout, self.strout, self._strin, self.strin]:
            if i:
                i.close()

        return

    def _start_threads(self):

        if self._stat_threads() == 'stopped':

            sock_type = 'socket-nb'
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
                read_type='pipe-nb',
                write_type=sock_type,
                exit_on_input_eof=True,
                descriptor_to_wait_for_input=self._strin.fileno(),
                descriptor_to_wait_for_output=self.socket.fileno(),
                apply_input_seek=False,
                apply_output_seek=False,
                flush_on_input_eof=False,
                on_exit_callback=self._on_in_thread_exit,
                on_output_write_error=self._on_socket_write_error,
                termination_event=self._in_thread_stop_event,
                flush_after_each_write=False,
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
                write_type='pipe-nb',
                exit_on_input_eof=True,
                descriptor_to_wait_for_input=self.socket.fileno(),
                descriptor_to_wait_for_output=self._strout.fileno(),
                apply_input_seek=False,
                apply_output_seek=False,
                flush_on_input_eof=True,
                on_exit_callback=self._on_out_thread_exit,
                on_input_read_error=self._on_socket_read_error,
                termination_event=self._out_thread_stop_event,
                flush_after_each_write=True,
                debug=self._debug
                )

            self._in_thread.start()
            self._out_thread.start()

            self._wait_threads('working')

        return

    def _stop_threads(self):

        if self._stat_threads() != 'stopped':

            t_in = self._in_thread
            t_out = self._out_thread

            self._in_thread_stop_event.set()
            self._out_thread_stop_event.set()

            if t_in != None:
                t_in.join()

            if t_out != None:
                t_out.join()

            self._wait_threads('stopped')

            self._in_thread_stop_event.clear()
            self._out_thread_stop_event.clear()

        return

    def _restart_threads(self):
        self._stop_threads()
        self._start_threads()

        self.signal.emit('restart', self, self.socket)

        return

    def _stat_threads(self):

        ret = 'unknown'

        v1 = self._in_thread
        v2 = self._out_thread

        if v1 != None and v2 != None:
            ret = 'working'

        elif v1 == None and v2 == None:
            ret = 'stopped'

        return ret

    def _send_connection_stopped_event(self):
        if not self._wrapping:
            if not self._connection_stop_signalled:
                self._connection_stop_signalled = True

                self.signal.emit('stop', self, self.socket)

        return

    def _send_connection_error_event(self):
        if not self._wrapping:
            if not self._connection_error_signalled:
                self._connection_error_signalled = True

                self.signal.emit('error', self, self.socket)

        return

    def start(self):

        if self.stat() == 'stopped':

            self._stop_flag = False

            self._connection_error_signalled = False
            self._connection_stop_signalled = False

            self._start_threads()

            self._output_availability_watcher_thread = threading.Thread(
                target=self._output_availability_watcher,
                name="Socket Output Availability Watcher Thread"
                )

            self._output_availability_watcher_thread.start()

            self.wait('working')

            self.signal.emit('start', self, self.socket)

        return

    def stop(self):

        if self.stat() != 'stopped':

            if self.is_ssl_working():
                self.stop_ssl()

            self._stop_flag = True

            self._stop_threads()

            self.wait('stopped')

            self.signal.emit('stop', self, self.socket)

        return

    def start_ssl(self, *args, **kwargs):
        """
        All parameters, same as for ssl.wrap_socket(). Exception is parameter
        socket, which
        taken from self.socket
        """

        if not self.is_ssl_working():

            self._wrapping = True

            if len(args) > 0:
                if issubclass(args[0], socket.socket):
                    del args[0]

            if 'sock' in kwargs:
                del kwargs['sock']

            kwargs['do_handshake_on_connect'] = False

            socket_wrap_result = None

            logging.debug("stopping threads before wrapping")

            self._stop_threads()

            logging.debug('before wrap sock is {}'.format(self.socket))

            try:
                socket_wrap_result = ssl.wrap_socket(
                    self.socket,
                    *args,
                    **kwargs
                    )

                while True:

                    try:
                        socket_wrap_result.do_handshake()

                    except ssl.SSLWantReadError:
                        select.select(
                            [socket_wrap_result.fileno()], [], [], 0.2
                            )

                    except ssl.SSLWantWriteError:
                        select.select(
                            [], [socket_wrap_result.fileno()], [], 0.2
                            )

                    except:
                        raise

                    else:
                        break

            except:
                logging.exception("ssl wrap error")
                self.signal.emit('ssl wrap error', self, self.socket)
            else:
                logging.debug(
                    """
peer cert:
{}
cipher:
{}
compression:
{}
""".format(
                        socket_wrap_result.getpeercert(binary_form=False),
                        socket_wrap_result.cipher(),
                        socket_wrap_result.compression()
                        )
                    )

                self.socket = socket_wrap_result

                logging.debug('after wrap sock is {}'.format(self.socket))

                logging.debug("starting threads after wrapping")

                self._start_threads()

                self.signal.emit('ssl wrapped', self, self.socket)

            self._wrapping = False

        return

    def stop_ssl(self):

        if self.is_ssl_working():

            if not self.connection:

                logging.debug(
                    "Connection already gone. "
                    "Unwrapping is pointless (and erroneous)"
                    )
                self.signal.emit('ssl ununwrapable', self, self.socket)

            else:

                self._wrapping = True

                logging.debug('before unwrap sock is {}'.format(self.socket))

                self._stop_threads()

                s = None
                try:
                    s = self.socket.unwrap()
                except:
                    logging.exception("ssl unwrap error")
                    self.signal.emit('ssl unwrap error', self, self.socket)

                else:
                    self.socket = s

                    self._start_threads()

                    logging.debug(
                        'after unwrap sock is {}'.format(self.socket)
                        )

                    self.signal.emit('ssl unwrapped', self, self.socket)

                self._wrapping = False

        return

    def _unwrap_procedure(self):
        if self.is_ssl_working():
            self.stop_ssl()
        else:
            logging.debug("Socket not wrapped - unwrapping not needed")
        return

    def is_ssl_working(self):
        return isinstance(self.socket, ssl.SSLSocket)

    def stat(self):

        ret = 'unknown'

        threads = self._stat_threads()
        v3 = self._output_availability_watcher_thread

        logging.debug(
            "{} :: status :: threads == {}, {}".format(self, threads, v3)
            )

        if threads == 'working':
            #  and v3 != None
            ret = 'working'

        elif threads == 'stopped' and v3 == None:
            ret = 'stopped'

        return ret

    def wait(self, what='stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            logging.debug(
                "{} :: waiting for `{}`".format(
                    self.wait,
                    what
                    )
                )
            if self.stat() == what:
                break
            time.sleep(0.2)

        return

    def _wait_threads(self, what='stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            logging.debug(
                "{} :: waiting for `{}`".format(
                    self._wait_threads,
                    what
                    )
                )
            if self._stat_threads() == what:
                break
            time.sleep(0.2)

        return

    def _on_in_thread_exit(self):
        self._in_thread = None
        self._any_thread_exited()
        return

    def _on_out_thread_exit(self):
        self._out_thread = None
        self._any_thread_exited()
        return

    def _any_thread_exited(self):

        if not self._wrapping:
            self.connection = False
            self._unwrap_procedure()
            self.socket.close()

        self._stop_threads()
        return

    def _on_socket_write_error(self):
        self._on_socket_read_write_error()
        return

    def _on_socket_read_error(self):
        self._on_socket_read_write_error()
        return

    def _on_socket_read_write_error(self):
        self.connection = False

        self.stop()

        self._send_connection_error_event()
        return

    def _output_availability_watcher(self):

        stopped_by_flag = False

        while len(select.select([], [self.socket.fileno()], [], 0.2)[1]) == 0:

            if self._stop_flag:
                stopped_by_flag = True
                break

        if not stopped_by_flag:

            if not self._wrapping:

                self.connection = True
                self.signal.emit('start', self, self.socket)

        self._output_availability_watcher_thread = None

        return
