
import logging
import threading
import time
import xml.etree.ElementTree
import xml.parsers.expat

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

class JID:

    def __init__(self, user = 'name', domain = 'domain', resource = 'default'):

        self.user = user
        self.domain = domain
        self.resource = resource

    def bare(self):
        return '{user}@{domain}'.format(
            user = self.user,
            domain = self.domain
            )

    def full(self):
        return '{user}@{domain}/{resource}'.format(
            user = self.user,
            domain = self.domain,
            resource = self.resource
            )


class C2SConnectionInfo:

    def __init__(
        self,
        host = 'localhost',
        port = 5222,
        password = 'secret',
        user_jid = None,
        priority = 'default'
        ):

        self.host = host
        self.port = port
        self.password = password
        self.user_jid = user_jid
        self.priority = priority



class XMPPStreamParserTarget:

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
                args = ('stop',),
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

        self._clear(init = True)

        self._stat = 'stopped'


    def _clear(self, init = False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError("Working. Cleaning not allowed")

        self._stream_reader_thread = None

        self._starting = False
        self._stopping = False

        self._termination_event = None

        self._stat = 'stopped'
        return

    def start(self):


        thread_name_in = 'Thread feeding data to XML parser'

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            self._stat = 'hard starting'
            self._starting = True

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

            self.wait('working')
            self._stat = 'hard started'
            self._starting = False

        return


    def stop(self):

        if not self._stopping and not self.starting and self.start() == 'working':
            self._stat = 'hard stopping'
            self._stopping = True

            self._termination_event.set()

            self.wait('stopped')

            self._clear()

            self._stopping = False
            self._stat = 'hard stopped'

        return

    def stat(self):

        ret = None

        if bool(self._stream_reader_thread):
            ret = 'working'

        elif not bool(self._stream_reader_thread):
            ret = 'stopped'

        else:
            ret = self._stat

        return ret


    def wait(self, what = 'stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            time.sleep(0.1)
            if self.stat() == what:
                break

        return

    def _on_stream_reader_thread_exit(self):
        self._stream_reader_thread = None


    def _feed(self, bytes_text):

        logging.debug(
            "{} :: received feed of {}".format(
                type(self).__name__, repr(bytes_text)
                )
            )

        if not isinstance(bytes_text, bytes):
            raise TypeError("bytes_text must be bytes type")

        ret = 0

        try:
            self._xml_parser.Parse(bytes_text, False)
        except:
            logging.exception(
                "{} :: _feed {}".format(
                    type(self).__name__, str(bytes_text, encoding = 'utf-8')
                    )
                )
            ret = 0
        else:
            ret = len(bytes_text)

        return ret




class XMPPOutputStreamWriter:

    def __init__(
        self,
        write_to,
        xml_parser
        ):
        """
        read_from - xml stream input
        """

        self._write_to = write_to

        self._xml_parser = xml_parser

        self._clear(init = True)

    def _clear(self, init = False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError("Working. Cleaning not allowed")

        self._stop_flag = False

        self._starting = False
        self._stopping = False

        self._stream_writer_thread = None

        self._output_queue = []

        self._stat = 'stopped'
        return

    def start(self):

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            thread_name_in = 'Thread sending data to socket streamer'

            self._stat = 'hard starting'
            self._starting = True
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

            self.wait('working')
            self._stat = 'hard started'
            self._starting = False

        return


    def stop(self):

        if not self._starting and not self._stopping and self.stat() == 'started':
            self._stopping = True
            self._stat = 'hard stopping'

            self._stop_flag = True

            self.wait('stopping')

            self._clear()

            self._stopping = False
            self._stat = 'hard stopped'

        return

    def stat(self):

        ret = 'unknown'

        if bool(self._stream_writer_thread):
            ret = 'working'

        elif not bool(self._stream_writer_thread):
            ret = 'stopped'

        else:
            ret = self._stat

        return ret


    def wait(self, what = 'stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            time.sleep(0.1)
            if self.stat() == what:
                break

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
                time.sleep(0.1)

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

        threading.Thread(
            target = self._xml_parser.Parse,
            args = (snd_obj, False,),
            name = "Output XMPP Stream Parser"
            ).start()

        return



class Hub():

    def __init__(self):

        self._clear(init = True)

    def _clear(self, init = False):

        self._waiters = {}

    def clean(self):

        self._clear()

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

    def get_waiter(self, name):

        ret = None

        if name in self._waiters:
            ret = self._waiters[name]

        return ret

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

    def dispatch(self, event, attrs = None):

        waiters = list(self._waiters.keys())
        waiters.sort()

        for i in waiters:

            threading.Thread(
                target = self._waiter_thread,
                name = 'Thread Dispatching Stream Events `{}'.format(i),
                args = (self._waiters[i], event,),
                kwargs = {'attrs':attrs}
                ).start()

    def _waiter_thread(self, call, event, attrs = None):

        call(event, attrs)

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



class XMPPStreamMachine:

    def __init__(self):

        self._clear(init = True)

    def _clear(self, init = False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError("Already Working")

        self._stopping = False
        self._starting = False

        self._xml_target = None
        self._xml_parser = None
        self._stream_worker = None

        self._sock_streamer = None
        self._stream_events_dispatcher = None
        self._stream_objects_dispatcher = None

    def set_objects(
        self,
        sock_streamer,
        stream_events_dispatcher,
        stream_objects_dispatcher
        ):

        self._sock_streamer = sock_streamer
        self._stream_events_dispatcher = stream_events_dispatcher
        self._stream_objects_dispatcher = stream_objects_dispatcher

    def start_stream_worker(self):

        raise RuntimeError("You need to override this")

    def start(self):

        if self.stat() == 'working':
            raise Exception("Working already")

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            self._starting = True

            self._xml_target = XMPPStreamParserTarget(
                on_stream_event = self._stream_events_dispatcher,
                on_element_readed = self._stream_objects_dispatcher
                )

            self._xml_parser = xml.parsers.expat.ParserCreate('UTF-8')

            self.start_stream_worker()

            org.wayround.utils.xml.expat_parser_connect_target(
                self._xml_parser,
                self._xml_target
                )

            self._stream_worker.start()

            self._starting = False

    def stop(self):

        if not self._stopping and not self._starting and self.stat() == 'working':

            self._stopping = True

            self._stream_worker.stop()
            self._clear()

            self._stopping = False

    def wait(self, what = 'stopped'):

        if self._stream_worker:
            self._stream_worker.wait(what = 'stopped')

    def stat(self):

        ret = None

        if self._stream_worker:
            ret = self._stream_worker.stat()

        if ret == None:
            ret = 'stopped'

        return ret

    def restart(self):
        self.stop()
        self.start()





class XMPPInputStreamReaderMachine(XMPPStreamMachine):

    def start_stream_worker(self):

        self._stream_worker = XMPPInputStreamReader(
            self._sock_streamer.strout,
            self._xml_parser
            )

class XMPPOutputStreamWriterMachine(XMPPStreamMachine):

    def start_stream_worker(self):

        self._stream_worker = XMPPOutputStreamWriter(
            self._sock_streamer.strin,
            self._xml_parser
            )

    def send(self, obj):
        threading.Thread(
            target = self._stream_worker.send,
            args = (obj,),
            name = "Send Object To Output Queue Thread"
            ).start()



class TLSDriver:

    def __init__(self):

        self._clear(init = True)


    def set_objects(
        self,
        sockstreamer,
        input_machine,
        output_machine,
        input_stream_events_hub,
        input_stream_objects_hub,
        output_stream_events_hub,
        connection_info,
        jid,
        on_finish
        ):

        self._sock_streamer = sockstreamer
        self._input_machine = input_machine
        self._output_machine = output_machine
        self._input_stream_events_hub = input_stream_events_hub
        self._input_stream_objects_hub = input_stream_objects_hub
        self._output_stream_events_hub = output_stream_events_hub
        self._connection_info = connection_info
        self._jid = jid
        self._on_finish = on_finish

    def _clear(self, init = False):

        self._sock_streamer = None
        self._output_machine = None
        self._connection_info = None
        self._jid = None
        self._on_finish = None
        self._input_stream_events_hub = None
        self._input_stream_objects_hub = None
        self._output_stream_events_hub = None

        self._drive_tls_features = False

        self.status = 'just created'

    def _start(self):

        if not self._drive_tls_features:

            self._drive_tls_features = True

            self._input_stream_events_hub.set_waiter(
                'tls_driver', self._input_stream_events_waiter
                )

            self._input_stream_objects_hub.set_waiter(
                'tls_driver', self._stream_objects_waiter
                )

    def _stop(self):

        if self._drive_tls_features:

            self._drive_tls_features = False

            self._input_stream_events_hub.del_waiter('tls_driver')

            self._input_stream_objects_hub.del_waiter('tls_driver')

    def drive(self, obj):

        if obj.tag == 'stream:features':
            self.status = 'looking for tls'

            if obj.find('starttls') != None:

                self.status = 'requesting tls'

                self._start()

                self._output_machine.send(
                    starttls()
                    )
            else:

                if self._on_finish:
                    threading.Thread(
                        target = self._on_finish,
                        name = "TLS Driver Finish Thread",
                        args = ('no tls',)
                        ).start()

                self._stop()

    def _input_stream_events_waiter(self, event, attrs = None):

        self._stop()

        if event == 'start':
            if self._on_finish:
                threading.Thread(
                    target = self._on_finish,
                    name = "TLS Driver Finish Thread (success)",
                    args = ('success',)
                    ).start()

        elif event == 'stop':
            if self._on_finish:
                threading.Thread(
                    target = self._on_finish,
                    name = "TLS Driver Finish Thread (stream stopped)",
                    args = ('stream stopped',)
                    ).start()

        elif event == 'error':
            if self._on_finish:
                threading.Thread(
                    target = self._on_finish,
                    name = "TLS Driver Finish Thread (stream error)",
                    args = ('stream error',)
                    ).start()


    def _stream_objects_waiter(self, obj):

        if (
            self._drive_tls_features and
            obj.get('xmlns', None) == 'urn:ietf:params:xml:ns:xmpp-tls'
            ):

            if self.status == 'requesting tls':

                if obj.tag in ['proceed', 'failure']:
                    self.tls_request_result = obj.tag

                    if self.tls_request_result == 'proceed':

                        if self._on_finish:
                            threading.Thread(
                                target = self._on_finish,
                                name = "TLS Driver Finish Thread (proceed)",
                                args = ('proceed',)
                                ).start()

                    else:
                        self._stop()
                        if self._on_finish:
                            threading.Thread(
                                target = self._on_finish,
                                name = "TLS Driver Finish Thread (failure)",
                                args = ('failure',)
                                ).start()

                else:
                    self._stop()
                    if self._on_finish:
                        threading.Thread(
                            target = self._on_finish,
                            name = "TLS Driver Finish Thread (response error)",
                            args = ('response error',)
                            ).start()

        return

    def proceed(self):
        self._sock_streamer.start_ssl()

        self._input_machine.restart()
        self._output_machine.restart()

        self._output_machine.send(
            start_stream(
                fro = self._connector._user_jid,
                to = self._connector._domain
                )
            )


