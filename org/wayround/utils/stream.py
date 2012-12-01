
import logging
import os
import select
import socket
import ssl
import threading
import time


class CatTerminationFlagFound(Exception): pass

def cat(
    stdin,
    stdout,
    bs = (2 * 1024 ** 2),
    count = None,
    threaded = False,
    thread_name = 'Thread',
    verbose = False,
    convert_to_str = None,
    read_method_name = 'read',
    write_method_name = 'write',
    exit_on_input_eof = True,
    flush_after_every_write = False,
    flush_on_input_eof = False,
    close_output_on_eof = False,
    waiting_for_input = False,
    waiting_for_output = False,
    descriptor_to_wait_for_input = None,
    descriptor_to_wait_for_output = None,
    apply_input_seek = True,
    apply_output_seek = True,
    standard_write_method_result = True,
    termination_event = None,
    on_exit_callback = None,
    on_input_read_error = None,
    on_output_write_error = None
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

#        return multiprocessing.Process(
        return threading.Thread(
            target = cat,
            args = (stdin, stdout),
            kwargs = dict(
                bs = bs,
                count = count,
                threaded = False,
                thread_name = thread_name,
                verbose = verbose,
                convert_to_str = convert_to_str,
                read_method_name = read_method_name,
                write_method_name = write_method_name,
                exit_on_input_eof = exit_on_input_eof,
                flush_after_every_write = flush_after_every_write,
                flush_on_input_eof = flush_on_input_eof,
                close_output_on_eof = close_output_on_eof,
                waiting_for_input = waiting_for_input,
                waiting_for_output = waiting_for_output,
                descriptor_to_wait_for_input = descriptor_to_wait_for_input,
                descriptor_to_wait_for_output = descriptor_to_wait_for_output,
                apply_input_seek = apply_input_seek,
                apply_output_seek = apply_output_seek,
                standard_write_method_result = standard_write_method_result,
                termination_event = termination_event,
                on_exit_callback = on_exit_callback,
                on_input_read_error = on_input_read_error,
                on_output_write_error = on_output_write_error
                ),
            name = thread_name
            )

    else:


        if termination_event and termination_event.is_set():
            raise CatTerminationFlagFound()

        if verbose:
            logging.info("Starting `{}' thread".format(thread_name))

        buff = ' '

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
                    logging.debug(
                        "waiting for input descriptor {}".format(
                            descriptor_to_wait_for_input
                            )
                        )

                    in_poll = select.poll()
                    in_poll.register(descriptor_to_wait_for_input, select.POLLIN)
                    while len(in_poll.poll(500)) == 0:

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        logging.debug("rewaiting input")

                    logging.debug(
                        "input descriptor {} ready".format(
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
                    while len(out_poll.poll(500)) == 0:

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        logging.debug("rewaiting output")

                    logging.debug(
                        "output descriptor {} ready".format(
                            descriptor_to_wait_for_output
                            )
                        )


                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

                buff = None

                logging.debug(
                    "Reading {} bytes using stdin.{}".format(
                        bs,
                        read_method_name
                        )
                    )


                try:
                    # TODO: some kind of timeout needed, or some kind of termination
                    buff = eval("stdin.{}(bs)".format(read_method_name))
                except:
                    if on_input_read_error:
                        threading.Thread(
                            target = on_input_read_error,
                            name = "{} Input Read Error Thread".format(thread_name)
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

                    logging.debug(
                        "Readed  {} bytes using stdin.{}".format(
                            buff_len,
                            read_method_name
                            )
                        )

                    logging.debug("buff data(255 bytes max): {}".format(repr(buff[:255])))

                    if convert_to_str != None:
                        buff = str(buff, encoding = convert_to_str)

                    written_total = 0
                    this_time_written = 0

                    if termination_event and termination_event.is_set():
                        raise CatTerminationFlagFound()

                    while True:
                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        logging.debug(
                            "Writing {} bytes using stdout.{}".format(
                                buff_len,
                                write_method_name
                                )
                            )
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
                            if on_output_write_error:
                                threading.Thread(
                                    target = on_output_write_error,
                                    name = "`{}' Output Error Thread".format(thread_name)
                                    ).start()

                            raise

                        if termination_event and termination_event.is_set():
                            raise CatTerminationFlagFound()

                        if flush_after_every_write:
                            stdout.flush()

                        if standard_write_method_result:
                            logging.debug(
                                "Written {} bytes using stdout.{}".format(
                                    this_time_written,
                                    write_method_name
                                    )
                                )
                            if this_time_written == 0:
                                if on_output_write_error:
                                    threading.Thread(
                                        target = on_output_write_error,
                                        name = "`{}' Output Error Thread".format(thread_name)
                                        ).start()
                                break
                            else:
                                written_total += this_time_written
                                if written_total >= buff_len:
                                    break
                        else:
                            logging.debug(
                                "Written bytes using stdout.{}".format(
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

                if termination_event and termination_event.is_set():
                    raise CatTerminationFlagFound()

        except CatTerminationFlagFound:
            logging.debug("Termination flag caught")
        except:
            raise

        if apply_output_seek and hasattr(stdout, 'seek'):
            try:
                stdout.seek(0, os.SEEK_END)
            except:
                pass

        if close_output_on_eof:
            if verbose:
                logging.info(" Closing `{}' thread stdout".format(thread_name))
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
        'num' : c,
        'size': bytes_counter,
        'sizem': (float(bytes_counter) / 1024 / 1024),
        'bufs': bs,
        'bufm': (float(bs) / 1024 / 1024)
        }
        )
    )

        if on_exit_callback:
            threading.Thread(
                target = on_exit_callback,
                name = "{} Exited Callback Thread".format(thread_name)
                ).start()

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



class SocketStreamer:
    """
    Featured class for flexibly handling socket connection
    """

    def __init__(
        self,
        sock,
        socket_transfer_size = 4096,
        on_connection_event = None
        ):

        self._sock = sock
        self._socket_transfer_size = socket_transfer_size

        self._on_connection_event = on_connection_event

        self._clear(init = True)

    def __del__(self):

        self._clear()

    def _clear(self , init = False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError("{} is not stopped".format(type(self).__name__))


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


        self._connection_stop_signalled = False
        self._starting = False
        self._stop_flag = False
        self._stopping = False
        self._stopping_threads = False

        self._output_availability_watcher_thread = None

        if not init:
            self._in_thread_stop_event.set()
            self._out_thread_stop_event.set()

        self._in_thread_stop_event = threading.Event()
        self._out_thread_stop_event = threading.Event()

        self._output_avalability_indicated = False

        self._stat = 'stopped'

        return

    def _close_pipe_descriptors(self):
        for i in [self._strout, self.strout, self._strin, self.strin]:
            if i:
                i.close()

    def _start_threads(self):
        self._stat = 'soft starting threads'

        self._in_thread = cat(
            stdin = self._strin,
            stdout = self._sock,
            threaded = True,
            write_method_name = 'send',
            close_output_on_eof = False,
            thread_name = 'strin -> _sock',
            bs = self._socket_transfer_size,
            convert_to_str = None,
            read_method_name = 'read',
            exit_on_input_eof = True,
            waiting_for_input = True,
            descriptor_to_wait_for_input = self._strin.fileno(),
            waiting_for_output = True,
            descriptor_to_wait_for_output = self._sock.fileno(),
            apply_input_seek = False,
            apply_output_seek = False,
            flush_on_input_eof = False,
            on_exit_callback = self._on_in_thread_exit,
            on_output_write_error = self._on_socket_write_error,
            termination_event = self._in_thread_stop_event
            )

        self._out_thread = cat(
            stdin = self._sock,
            stdout = self._strout,
            threaded = True,
            write_method_name = 'write',
            close_output_on_eof = False,
            thread_name = '_sock -> strout',
            bs = self._socket_transfer_size,
            convert_to_str = None,
            read_method_name = 'recv',
            exit_on_input_eof = True,
            waiting_for_input = True,
            descriptor_to_wait_for_input = self._sock.fileno(),
            waiting_for_output = True,
            descriptor_to_wait_for_output = self._strout.fileno(),
            apply_input_seek = False,
            apply_output_seek = False,
            flush_on_input_eof = True,
            on_exit_callback = self._on_out_thread_exit,
            on_input_read_error = self._on_socket_read_error,
            termination_event = self._out_thread_stop_event
            )

        self._in_thread.start()
        self._out_thread.start()
        self._stat = 'soft started threads'

    def _stop_threads(self, by_error = False):

        if not self._stopping_threads:

            self._stopping_threads = True

            self._stat = 'soft stopping threads'
            self._in_thread_stop_event.set()
            self._out_thread_stop_event.set()

            self.wait('stopped')

            self._in_thread_stop_event.clear()
            self._out_thread_stop_event.clear()
            self._stat = 'soft stopped threads'

            self._stopping_threads = False


            if not by_error:
                if not self._connection_stop_signalled:
                    self._connection_stop_signalled = True
                    if self._on_connection_event:
                        threading.Thread(
                            target = self._on_connection_event,
                            args = ('stop', self._sock,),
                            name = "Connection Stopped Thread"
                            ).start()


    def _restart_threads(self):
        self._stat = 'soft restarting threads'
        self._stop_threads()
        self._start_threads()
        self._stat = 'soft restarted threads'

        if self._on_connection_event:
            threading.Thread(
                target = self._on_connection_event,
                args = ('restart', self._sock,),
                name = "Connection Restarted Thread"
                ).start()



    def start(self):

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            self._stat = 'hard starting'
            self._starting = True
            self._stop_flag = False

            self._pipe_outside = os.pipe()
            self._pipe_inside = os.pipe()

            self._strout = open(self._pipe_outside[1], 'wb', buffering = 0)
            self.strout = open(self._pipe_outside[0], 'rb', buffering = 0)


            self._strin = open(self._pipe_inside[0], 'rb', buffering = 0)
            self.strin = open(self._pipe_inside[1], 'wb', buffering = 0)

            self._start_threads()

            self._output_availability_watcher_thread = threading.Thread(
                target = self._output_availability_watcher,
                name = "Socket Output Availability Watcher Thread"
                )

            self._output_availability_watcher_thread.start()

            self.wait('working')

            self._starting = False
            self._stat = 'hard started'

        return

    def stop(self):

        if not self._stopping and not self._starting and not self.stat() == 'stopped':

            self._stat = 'hard stopping'

            self._stopping = True

            self._stop_flag = True
#            self._close_pipe_descriptors()

            self._stop_threads()

            self.wait('stopped')

            if self.is_ssl_working():
                self.stop_ssl()

            self._clear()

            self._stopping = False

            self._stat = 'hard stopped'

        return

    def start_ssl(self, *args, **kwargs):
        """
        All parameters, same as for ssl.wrap_socket(). Exception is parameter
        _sock, which
        taken from self._sock
        """

        if len(args) > 0:
            if issubclass(args[0], socket.socket):
                del args[0]

        if 'sock' in kwargs:
            del kwargs['sock']

        s = None

        self._stop_threads()

        logging.debug('before wrap sock is {}'.format(self._sock))

        try:
            s = ssl.wrap_socket(
                self._sock,
                *args,
                **kwargs
                )
        except:
            logging.exception("ssl wrap error")
            if self._on_connection_event:
                threading.Thread(
                    target = self._on_connection_event,
                    args = ('ssl wrap error', self._sock,),
                    name = "Connection SSL Wrap Error Thread"
                    ).start()
        else:
            logging.info(
                """\
peer cert:
{}
cipher:
{}
compression:
{}""".format(
                    repr(s.getpeercert(binary_form = False)),
                    repr(s.cipher()),
                    repr(s.compression())
                    )
                )

            self._sock = s

            logging.debug('after wrap sock is {}'.format(self._sock))

            self._start_threads()


            if self._on_connection_event:
                threading.Thread(
                    target = self._on_connection_event,
                    args = ('ssl wrapped', self._sock,),
                    name = "Connection SSL Wrapped Thread"
                    ).start()


    def stop_ssl(self):

        self._stop_threads()

        logging.debug('before unwrap sock is {}'.format(self._sock))

        s = None
        try:
            s = self._sock.unwrap()
        except:
            logging.exception("ssl unwrap error")
            if self._on_connection_event:
                threading.Thread(
                    target = self._on_connection_event,
                    args = ('ssl unwrap error', self._sock,),
                    name = "Connection SSL Unwrap Error Thread"
                    ).start()

        else:
            self._sock = s

            logging.debug('after unwrap sock is {}'.format(self._sock))

            if self._on_connection_event:
                threading.Thread(
                    target = self._on_connection_event,
                    args = ('ssl unwrapped', self._sock,),
                    name = "Connection SSL Unwrapped Thread"
                    ).start()

    def is_ssl_working(self):

        return isinstance(self._sock, ssl.SSLSocket)

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

    def wait(self, what = 'stopped'):

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
        self._stop_threads()

    def _on_out_thread_exit(self):
        self._out_thread = None
        self._stop_threads()

    def _on_socket_write_error(self):
        self._on_socket_error()

    def _on_socket_read_error(self):
        self._on_socket_error()

    def _on_socket_error(self):

        if self._on_connection_event:
            threading.Thread(
                target = self._on_connection_event,
                args = ('error', self._sock,),
                name = "Connection Error Thread"
                ).start()

        self._stop_threads(by_error = True)

    def _output_availability_watcher(self):

        out_poll = select.poll()
        out_poll.register(self._sock.fileno(), select.POLLOUT)

        stopped_by_flag = 0

        while len(out_poll.poll(100)) == 0:

            if self._stop_flag:
                stopped_by_flag = 1
                break

        if stopped_by_flag == 0:

            if self._on_connection_event:
                threading.Thread(
                    target = self._on_connection_event,
                    args = ('start', self._sock,),
                    name = "Connection Started Thread"
                    ).start()

        self._output_availability_watcher_thread = None

        return
