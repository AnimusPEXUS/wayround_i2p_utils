
import logging
import threading
import time

import xml.etree.ElementTree

import mako.template

import org.wayround.utils.stream
import org.wayround.utils.xml


def start_stream(
    fro,
    to,
    version = '1.0',
    xml_lang = 'en',
    xmlns = 'jabber:client',
    xmlns_stream = 'http://etherx.jabber.org/streams'
    ):

    return mako.template.Template(
        """\
<?xml version="1.0"?>
<stream:stream
    from="${ fro | x }"
    to="${ to | x }"
    version="${ version | x }"
    xml:lang="${ xml_lang | x }"
    xmlns="${ xmlns | x }"
    xmlns:stream="${ xmlns_stream | x }">
""").render(
            fro = fro,
            to = to,
            version = version,
            xml_lang = xml_lang,
            xmlns = xmlns,
            xmlns_stream = xmlns_stream
            )

def stop_stream():
    return '</stream:stream>'

def starttls():
    return """\
<starttls xmlns='urn:ietf:params:xml:ns:xmpp-tls'/>
"""

def check_stream_handler_correctness(handler):

    ret = 0


    return ret


def _info_dict_to_add(handler):

    return dict(
        handler = handler,
        name = handler.name,
        tag = handler.tag,
        ns = handler.ns
        )


class XMPPInputStreamReaderTarget:

    def __init__(
        self,
        on_stream_event = None,
        on_element_readed = None
        ):

        self._on_stream_event = on_stream_event
        self._on_element_readed = on_element_readed

        self.clear(init = True)


    def clear(self, init = False):
        self._tree_builder = None
        self._tree_builder_start_depth = None

        self._depth_tracker = []


    def start(self, name, attributes):

        logging.debug("{} :: start tag: `{}'; attrs: {}".format(type(self).__name__, name, attributes))

        if name == 'stream:stream':
            self._depth_tracker = []

        if len(self._depth_tracker) == 0:

            if name == 'stream:stream':
                if self._on_stream_event:
                    threading.Thread(
                        target = self._on_stream_event,
                        args = ('start',),
                        kwargs = {'attrs': attributes},
                        name = "Stream Start Thread"
                        ).start()

            else:
                if self._on_stream_start_error:
                    threading.Thread(
                        target = self._on_stream_event,
                        args = ('error',),
                        kwargs = {'attrs':None},
                        name = "Stream Start Error Thread"
                        ).start()

        else:

            if not self._tree_builder:

                self._tree_builder = xml.etree.ElementTree.TreeBuilder()

            self._tree_builder.start(name, attributes)

        self._depth_tracker.append(name)

        return

    def end(self, name):

        logging.debug("{} :: end `{}'".format(type(self).__name__, name))
        logging.debug("{} :: end len(trac) == `{}'".format(type(self).__name__, len(self._depth_tracker)))

        if len(self._depth_tracker) > 1:
            self._tree_builder.end(name)

        del self._depth_tracker[-1]

        if len(self._depth_tracker) == 1:

            element = self._tree_builder.close()
            self._tree_builder = None

            if self._on_element_readed:
                threading.Thread(
                    target = self._on_element_readed,
                    args = (element,),
                    name = 'Element Readed Thread'
                    ).start()

        if len(self._depth_tracker) == 0:

            if name == 'stream:stream':
                self.close()

        return

    def data(self, data):

        logging.debug("{} :: data `{}'".format(type(self).__name__, data))

        self._tree_builder.data(data)

        return

    def comment(self, text):

        logging.debug("{} :: comment `{}'".format(type(self).__name__, text))

        self._tree_builder.comment(text)

        return

    def close(self):

        logging.debug("{} :: close".format(type(self).__name__))

        if self._on_stream_end:
            threading.Thread(
                target = self._on_stream_event,
                args = ('end',),
                kwargs = {'attrs':None},
                name = "Stream Ended Thread"
                ).start()

        return




class XMPPInputStreamReader:

    def __init__(
        self,
        read_from,
        xml_parser
        ):
        """
        read_from - xml stream input
        """

        self._read_from = read_from

        self._xml_parser = xml_parser

        self._clean(init = True)


    def _clean(self, init = False):

        if not init:
            if self.is_working():
                raise RuntimeError("Working. Cleaning not allowed")

        self._stream_reader_thread = None

        self._stopping = False

        self._termination_event = None
        return

    def start(self):


        thread_name_in = 'Thread feeding data to XML parser'

        if self.is_working():
            raise RuntimeError("Already working")

        else:
            self._stop_flag = False

            if not self._stream_reader_thread:

                self._termination_event = threading.Event()

                try:
                    self._stream_reader_thread = org.wayround.utils.stream.cat(
                        stdin = self._read_from,
                        stdout = self,
                        bs = (2 * 1024 ** 2),
                        threaded = True,
                        thread_name = thread_name_in,
                        verbose = True,
                        convert_to_str = False,
                        read_method_name = 'read',
                        write_method_name = '_feed',
                        exit_on_input_eof = True,
                        flush_after_every_write = False,
                        flush_on_input_eof = False,
                        close_output_on_eof = False,
                        waiting_for_input = True,
                        waiting_for_output = False,
                        descriptor_to_wait_for_input = self._read_from.fileno(),
                        descriptor_to_wait_for_output = None,
                        apply_input_seek = False,
                        apply_output_seek = False,
                        standard_write_method_result = True,
                        termination_event = self._termination_event,
                        on_exit_callback = self._on_stream_reader_thread_exit
                        )
                except:
                    logging.exception("Error on starting {}".format(thread_name_in))
                else:
                    self._stream_reader_thread.start()

        return


    def stop(self):

        if not self._stopping and self.is_working():
            self._stopping = True

            self._termination_event.set()

            self._wait()

            self._clean()

            self._stopping = False

        return

    def is_working(self):

        return bool(self._stream_reader_thread)

    def _wait(self):

        while True:
            if not self.is_working():
                break

            time.sleep(0.5)

        return

    def _on_stream_reader_thread_exit(self):
        self._stream_reader_thread = None


    def _feed(self, bytes_text):

        logging.debug("{} :: received feed of {}".format(type(self).__name__, repr(bytes_text)))

        if not isinstance(bytes_text, bytes):
            raise TypeError("bytes_text must be bytes type")

        ret = 0

        try:
            self._xml_parser.Parse(bytes_text, False)
        except:
            logging.exception("{} :: _feed {}".format(type(self).__name__, str(bytes_text, encoding = 'utf-8')))
            ret = 0
        else:
            ret = len(bytes_text)

        return ret




class XMPPOutputStreamWriter:

    def __init__(self, write_to):
        """
        read_from - xml stream input
        """

        self._write_to = write_to

        self._clean(init = True)


    def _clean(self, init = False):

        if not init:
            if self.is_working():
                raise RuntimeError("Working. Cleaning not allowed")

        self._stop_flag = False
        self._stopping = False

        self._stream_writer_thread = None

        self._output_queue = []
        return

    def start(self):

        thread_name_in = 'Thread sending data to socket streamer'

        if self.is_working():
            raise RuntimeError("Already working")

        else:
            self._stop_flag = False

            if not self._stream_writer_thread:
                try:
                    self._stream_writer_thread = threading.Thread(
                        target = self._output_worker,
                        name = thread_name_in,
                        args = tuple(),
                        kwargs = dict()
                        )
                except:
                    logging.exception("Error on starting {}".format(thread_name_in))
                else:
                    self._stream_writer_thread.start()

        return


    def stop(self):

        if not self._stopping:
            self._stopping = True

            self._stop_flag = True

            self._wait()

            self._clean()

            self._stopping = False

        return

    def is_working(self):

        return bool(self._stream_writer_thread)


    def _wait(self):

        while True:
            if not self.is_working():
                break

            time.sleep(0.5)

        return

    def send(self, obj):

        if self._stop_flag:
            raise RuntimeError("Stopping. No appending allowed")

        self._output_queue.append(obj)

        return

    def _output_worker(self):

        while True:
            if len(self._output_queue) > 0:

                while len(self._output_queue) > 0:
                    self._send_object(self._output_queue[0])
                    del self._output_queue[0]

            else:
                if self._stop_flag:
                    break
                time.sleep(0.5)

        self._stream_writer_thread = None

        return

    def _send_object(self, obj):

        snd_obj = None

        if isinstance(obj, bytes):
            snd_obj = obj
        elif isinstance(obj, str):
            snd_obj = bytes(obj, encoding = 'utf-8')
        elif isinstance(obj, xml.etree.ElementTree.Element):
            snd_obj = bytes(
                xml.etree.ElementTree.tostring(
                    obj,
                    encoding = 'utf-8'
                    ),
                encoding = 'utf-8'
                )
        else:
            raise Exception("Wrong obj type. Can be bytes, str or xml.etree.ElementTree.Element")


        self._write_to.write(snd_obj)

        return


class Stanza:

    def __init__(self):
        pass


class Hub():

    def __init__(self):

        self._clean(init = True)

    def _clean(self, init = False):

        self._waiters = {}

    def dispatch(self):

        waiters = list(self._waiters.keys())
        waiters.sort()

        for i in waiters:

            threading.Thread(
                target = self._waiter_thread,
                name = 'Simple Dispatcher `{}'.format(self._name, i),
                args = (self._waiters[i],),
                kwargs = {}
                ).start()

    def _waiter_thread(self, call):

        call()

        return

    def set_waiter(self, name, reactor):

        self._waiters[name] = reactor

        return

    def del_waiter(self, name):

        if name in self._waiters:
            del self._waiters[name]

        return

class ConnectionEventsHub(Hub):

    def dispatch(self, event):

        waiters = list(self._waiters.keys())
        waiters.sort()

        for i in waiters:

            threading.Thread(
                target = self._waiter_thread,
                name = 'Connection Events Dispatch `{}'.format(i),
                args = (self._waiters[i], event,),
                kwargs = {}
                ).start()

    def _waiter_thread(self, call, event):

        call(event)

        return


class StreamEventsHub(Hub):

    def dispatch(self, start, attrs = None):

        waiters = list(self._waiters.keys())
        waiters.sort()

        for i in waiters:

            threading.Thread(
                target = self._waiter_thread,
                name = 'Thread Dispatching Stream Events `{}'.format(i),
                args = (self._waiters[i], start,),
                kwargs = {'attrs':attrs}
                ).start()

    def _waiter_thread(self, call, start, attrs = None):

        call(start, attrs)

        return

class StreamObjectsDispatchingHub(Hub):


    def dispatch(self, obj):

        waiters = list(self._waiters.keys())
        waiters.sort()

        for i in waiters:

            threading.Thread(
                target = self._waiter_thread,
                name = 'Input Stream Objects Hub `{}'.format(i),
                args = (self._waiters[i], obj,),
                kwargs = dict()
                ).start()

        return

    def _waiter_thread(self, call, obj):

        call(obj)

        return


class TLSDriver:

    def __init__(self):

        self._clean(init = True)


    def set_objects(
        self,
        socket_streamer,
        output_stream_writer,
        connector,
        on_finish
        ):

        self._socket_streamer = socket_streamer
        self._output_stream_writer = output_stream_writer
        self._connector = connector
        self._on_finish = on_finish

    def _clean(self, init = False):

        self._socket_streamer = None
        self._output_stream_writer = None
        self._connector = None
        self._on_finish = None

        self._drive_tls_features = False

        self.status = 'just created'

    def drive(self, obj):
        if obj.tag == 'stream:features':
            self.status = 'looking for tls'

            if obj.find('starttls') != None:

                self.status = 'requesting tls'

                self._drive_tls_features = True

                self._output_stream_writer.send(
                    starttls()
                    )
            else:

                if self._on_finish:
                    threading.Thread(
                        target = self._on_finish,
                        name = "TLS Driver Finish Thread",
                        args = ('tls not suggested',)
                        ).start()


    def _features_waiter(self, obj):

        if self._drive_tls_features and obj.tag == 'stream:features':

            if (
                self.status == 'requesting tls'
                and self.tls_request_result == 'proceed'
                and self._socket_streamer.is_ssl_working()
                ):

                self._drive_tls_features = False

                self.statu = 'tls started'

                if self._on_finish:
                    threading.Thread(
                        target = self._on_finish,
                        name = "TLS Driver Finish Thread",
                        args = ('tls started',),
                        kwargs = {'obj':obj}
                        ).start()

        return

    def _urn_ietf_params_xml_ns_xmpp_tls_waiter(self, obj):

        if (
            self._drive_tls_features and
            obj.get('xmlns', None) == 'urn:ietf:params:xml:ns:xmpp-tls'
            ):

            if self.status == 'requesting tls':

                if obj.tag in ['proceed', 'failure']:
                    self.tls_request_result = obj.tag
                else:
                    logging.error("TLS Request Error")
                    self.close()

                if self.tls_request_result == 'proceed':

                    self._sock_streamer.start_ssl()

                    self._connector._restart_xml_parser()

                    self._output_stream_writer.send(
                        start_stream(
                            fro = self._connector._user_jid,
                            to = self._connector._domain
                            )
                        )
                else:
                    logging.error("TLS Request Failure")
                    self.close()

        return
