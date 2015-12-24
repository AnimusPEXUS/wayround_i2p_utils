
import select
import ssl
import threading
import queue
import time

import wayround_org.mail.miscs


def nb_handshake(sock, stop_event=None, select_timeout=0.5):

    while True:

        if stop_event is not None and stop_event.is_set():
            break

        try:
            data = sock.do_handshake()
        except BlockingIOError:
            select.select([sock], [], [], select_timeout)
        except ssl.SSLWantReadError:
            select.select([sock], [], [], select_timeout)
        except ssl.SSLWantWriteError:
            select.select([], [sock], [], select_timeout)
        except OSError as err:
            if err.errno == 9:
                break
            else:
                raise
        else:
            break

    return


def nb_recv(sock, bs=4096, stop_event=None, select_timeout=0.5):
    """

    if len() of returned value is 0, then foreign socket is closed

    not returns until something recived from socket or socket is
    closed. use stop_event to terminate this function

    stop_event must be of threading.Event() type
    """

    if stop_event is not None:
        if not isinstance(stop_event, threading.Event):
            raise TypeError("`stop_event' must be of threading.Event type")

    data = b''

    while True:

        if stop_event is not None and stop_event.is_set():
            break

        try:
            data = sock.recv(bs)
        except BlockingIOError:
            select.select([sock], [], [], select_timeout)
        except ssl.SSLWantReadError:
            select.select([sock], [], [], select_timeout)
        except ssl.SSLWantWriteError:
            select.select([], [sock], [], select_timeout)
        except OSError as err:
            if err.errno == 9:
                ret = b''
                break
            else:
                raise
        else:
            break

    if False:
        print("recvd: {}".format(data))

    return data


def nb_sendall(sock, data, bs=4096, stop_event=None, select_timeout=0.5):

    if False:
        print("sending: {}".format(data))

    if stop_event is not None:
        if not isinstance(stop_event, threading.Event):
            raise TypeError("`stop_event' must be of threading.Event type")

    if type(data) != bytes:
        raise TypeError("`data' must be bytes")

    while True:

        try:
            sock.sendall(data)
        except BlockingIOError:
            select.select([], [sock], [], select_timeout)
        except ssl.SSLWantReadError:
            select.select([sock], [], [], select_timeout)
        except ssl.SSLWantWriteError:
            select.select([], [sock], [], select_timeout)
        except OSError as err:
            if err.errno == 9:
                ret = b''
                break
            else:
                raise
        else:
            break

        if stop_event is not None and stop_event.is_set():
            break

    return


class LblRecvReaderBuffer:

    def __init__(
            self,
            sock,
            recv_size=4096,
            line_terminator=wayround_org.mail.miscs.STANDARD_LINE_TERMINATOR
            ):
        """

        line_terminator=b'\0\n' (0x10, 0x13) is mail system message terminator
        style
        """

        self.sock = sock
        self.line_terminator = line_terminator
        self.recv_size = recv_size

        self._socket_is_closed = False
        self._line_terminator_len = len(self.line_terminator)

        self._01_worker_thread = None
        self._02_worker_thread = None

        self._stop_flag = threading.Event()

        self._recv_buffer_queue = queue.Queue()

        # this buffer is here and not in thread look function for make
        # available it's size information
        self._input_bytes_buff = b''
        self._input_bytes_buff_lock = threading.Lock()

        # this list not supposed to be accessible for outsiders
        # and the only way to get items from it is special method
        self._lines = []
        self._lines_lock = threading.Lock()

        return

    def start(self):
        if self._01_worker_thread is None:

            self._01_worker_thread = threading.Thread(
                target=self._worker_thread_target_01
                )
            self._01_worker_thread.start()

        if self._02_worker_thread is None:

            self._02_worker_thread = threading.Thread(
                target=self._worker_thread_target_02
                )
            self._02_worker_thread.start()

        return

    def stop(self):
        self._stop_flag.set()
        self.wait()
        self._01_worker_thread = None
        self._02_worker_thread = None
        return

    def wait(self):
        if self._01_worker_thread is not None:
            self._01_worker_thread.join()

        if self._02_worker_thread is not None:
            self._02_worker_thread.join()

        return

    def _worker_thread_target_01(self):
        """
        Recive data from socket and put it in queue.

        with this thread I just want server to read input data fast as I
        think it is important.
        """

        _debug = False

        while True:
            if self._stop_flag.is_set():
                break

            res = nb_recv(self.sock, stop_event=self._stop_flag)

            if len(res) == 0:
                self._socket_is_closed = True
                break

            if _debug:
                print("_worker_thread_target_01 res: {}".format(res))

            self._recv_buffer_queue.put(res)

        threading.Thread(target=self.stop).start()

        return

    def _worker_thread_target_02(self):
        """
        Takes data from queue and glues it with bytes string, after
        what - searches and slices it by line separators, adding result to
        dedicated list. warning: line separator is not stripped from lines!
        """

        _debug = False

        while True:

            if self._stop_flag.is_set():
                break

            res_empty = False
            try:
                res = self._recv_buffer_queue.get(block=True, timeout=0.5)
            except queue.Empty:
                res_empty = True

            if res_empty:
                if _debug:
                    print("_worker_thread_target_02 res_empty")
                continue

            if _debug:
                print("_worker_thread_target_02 res: {}".format(res))

            with self._input_bytes_buff_lock:

                if _debug:
                    print("_worker_thread_target_02 buff_1: {}".format(
                        self._input_bytes_buff
                        ))

                self._input_bytes_buff += res

                if _debug:
                    print("_worker_thread_target_02 buff_2: {}".format(
                        self._input_bytes_buff
                        ))

                while True:
                    if self._stop_flag.is_set():
                        break

                    if _debug:
                        print("_worker_thread_target_02 line_terminator: {}".format(
                            self.line_terminator
                            ))

                    sep_pos = self._input_bytes_buff.find(
                        self.line_terminator
                        )

                    if _debug:
                        print("_worker_thread_target_02 sep_pos: {}".format(
                            sep_pos
                            ))

                    if sep_pos == -1:
                        break

                    cut_pos = sep_pos + self._line_terminator_len

                    if _debug:
                        print("_worker_thread_target_02 cut_pos: {}".format(
                            cut_pos
                            ))

                    res_line_bytes = self._input_bytes_buff[:cut_pos]

                    self._input_bytes_buff = self._input_bytes_buff[cut_pos:]

                    if _debug:
                        print("_worker_thread_target_02 buff_3: {}".format(
                            self._input_bytes_buff
                            ))

                    with self._lines_lock:
                        if _debug:
                            print("_worker_thread_target_02 list app: {}".format(
                                res_line_bytes
                                ))

                        self._lines.append(res_line_bytes)

        threading.Thread(target=self.stop).start()

        return

    def get_next_line(self):
        """
        Returns next line, or None if there is not yet any. If socket is
        closed - and empty line with terminator is returned.

        this method is async. if self._lines has any items, this method
        returns first of them, and removes it from self._lines.

        this method supposed to be the only way to get data from self._lines,
        as there shuld be thread safety to work with self._lines.
        """

        ret = None

        if self._socket_is_closed:
            ret = self.line_terminator
        else:
            with self._lines_lock:
                if len(self._lines) != 0:
                    ret = self._lines[0]
                    del self._lines[0]

        return ret

    def nb_get_next_line(self, stop_event, retry_interval=0.2):
        if not isinstance(stop_event, threading.Event):
            raise TypeError("`stop_event' must be of threading.Event type")

        ret = None

        while True:

            if stop_event.is_set():
                break

            ret = self.get_next_line()

            if ret is not None:
                break

            time.sleep(retry_interval)

        return ret

    def get_bytes_buffer_byte_size(self):
        with self._input_bytes_buff_lock:
            ret = len(self._input_bytes_buff)
        return ret

    def get_lines_buffer_byte_size(self):
        ret = 0
        with self._lines_lock:
            for i in self._lines:
                ret += len(i)
        return ret

    def get_lines_count(self):
        with self._lines_lock:
            ret = len(self._lines)
        return ret
