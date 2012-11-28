
"""
Simple Client used while developing xmpp module of org.wayround.utils
"""

import logging
import select
import socket
import threading
import time
import xml.etree.ElementTree
import xml.parsers.expat

import org.wayround.utils.stream
import org.wayround.utils.xml
import org.wayround.utils.xmpp.core

_GLOBAL_DEFAULT_TIMEOUT = socket.getdefaulttimeout()


class SampleBotClient:

    def __init__(self, connection_info, jid):


        self._connection_info = connection_info
        self._jid = jid

        self._clear(init = True)

    def _clear(self, init = False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError("Working. Cleaning restricted")

        self._stop_flag = False
        self._starting = False
        self._stopping = False

        self._sock = None
        self._sock_streamer = None

        self._connection_events_hub = None

        self._input_stream_events_hub = None
        self._input_stream_objects_hub = None

        self._output_stream_events_hub = None


        self.status = 'stopped'

        self._tls_request_result = None

        self._tls_driver = None

        self._connection = False

        self._input_machine = None
        self._output_machine = None


    def start(self):

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            self._starting = True

            ######### DRIVERS

            self._tls_driver = org.wayround.utils.xmpp.core.TLSDriver()

            ######### HUBS

            self._connection_events_hub = org.wayround.utils.xmpp.core.ConnectionEventsHub()

            self._input_stream_events_hub = org.wayround.utils.xmpp.core.StreamEventsHub()
            self._input_stream_objects_hub = org.wayround.utils.xmpp.core.StreamObjectsDispatchingHub()

            self._output_stream_events_hub = org.wayround.utils.xmpp.core.StreamEventsHub()

            self._connection_events_hub.set_waiter(
                'main', self._on_connection_event
                )

            self._input_stream_events_hub.set_waiter(
                'main', self._on_stream_event
                )

            self._input_stream_objects_hub.set_waiter(
                'main', self._on_stream_object
                )

            ######### SOCKET

            self._sock = socket.create_connection(
                (
                 self._connection_info.host,
                 self._connection_info.port
                 )
                )

            ######### STREAMS

            self._sock_streamer = org.wayround.utils.stream.SocketStreamer(
                self._sock,
                socket_transfer_size = 4096,
                on_connection_event = self._connection_events_hub.dispatch
                )

            threading.Thread(
                name = "Socket Streamer Starting Thread",
                target = self._sock_streamer.start
                ).start()

            ######### MACHINES

            threading.Thread(
                target = self._start_input_machine,
                name = "Input Machine Start Thread"
                ).start()

            threading.Thread(
                target = self._start_output_machine,
                name = "Output Machine Start Thread"
                ).start()

            self._starting = False

        return

    def stop(self):


        if not self._stopping and not self._starting:
            self._stopping = True

            self._stop_flag = True

            stop_list = [
                self._stop_input_machine,
                self._stop_output_machine
                ]

            if self._sock_streamer:
                stop_list.append(self._sock_streamer.stop)

            for i in stop_list:
                threading.Thread(
                    target = i,
                    name = "Stopping Thread ({})".format(i)
                    ).start()


            self.wait('stopped')

            logging.debug("Cleaning client instance")

            if self._sock:
                self._sock.shutdown(socket.SHUT_RDWR)
                self._sock.close()

            self._clear()

            self._stopping = False


        return

    def wait(self, what = 'stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            time.sleep(0.1)
            if self.stat() == what:
                break

        return

    def stat(self):

        ret = 'various'

        v1 = None
        v2 = None
        v3 = None

        if self._sock_streamer:
            v1 = self._sock_streamer.stat()

        if self._input_machine:
            v2 = self._input_machine.stat()

        if self._output_machine:
            v3 = self._output_machine.stat()


#        logging.debug("""
#self._sock_streamer.stat() == {}
#self._input_machine.stat() == {}
#self._output_machine.stat() == {}
#""".format(v1, v2, v3)
#            )

        logging.debug("{}, {}, {}".format(v1, v2, v3))

        if v1 == v2 == v3 == 'working':
            ret = 'working'
        elif v1 == v2 == v3 == 'stopped':
            ret = 'stopped'

        elif v1 == v2 == v3 == None:
            ret = 'stopped'

        return ret

    def start_stream_stop(self):

        if self._connection:
            self._output_machine.send(
                org.wayround.utils.xmpp.core.stop_stream()
                )


    def _start_input_machine(self):

        self._input_machine = org.wayround.utils.xmpp.core.XMPPInputStreamReaderMachine()
        self._input_machine.set_objects(
            self._sock_streamer,
            stream_events_dispatcher = self._input_stream_events_hub.dispatch,
            stream_objects_dispatcher = self._input_stream_objects_hub.dispatch
            )
        self._input_machine.start()

    def _stop_input_machine(self):
        if self._input_machine:
            self._input_machine.stop()

    def _restart_input_machine(self):
        self._stop_input_machine()
        self._start_input_machine()



    def _start_output_machine(self):

        self._output_machine = org.wayround.utils.xmpp.core.XMPPOutputStreamWriterMachine()
        self._output_machine.set_objects(
            self._sock_streamer,
            stream_events_dispatcher = self._output_stream_events_hub.dispatch,
            stream_objects_dispatcher = None
            )
        self._output_machine.start()

    def _stop_output_machine(self):
        if self._output_machine:
            self._output_machine.stop()

    def _restart_output_machine(self):
        self._stop_output_machine()
        self._start_output_machine()


    def _features_waiter_second(self, obj):

        if obj.tag == 'stream:features':

            print("Second Features received:\n{}".format(xml.etree.ElementTree.tostring(obj)))

    def _on_connection_event(self, event):

        if event == 'start':
            print("Connection started")

            self._connection = True

            self.wait('working')

            logging.debug("ended waiting for nonnection")

#            self._tls_driver.set_objects(
#                self._sock_streamer,
#                self._input_machine,
#                self._output_machine,
#                self._input_stream_events_hub,
#                self._input_stream_objects_hub,
#                self._output_stream_events_hub,
#                self._connection_info,
#                self._jid,
#                on_finish = self._tls_driver_finish_waiter
#                )
#
#            self._output_machine.send(
#                org.wayround.utils.xmpp.core.start_stream(
#                    fro = self._jid.full(),
#                    to = self._connection_info.host
#                    )
#                )


        elif event == 'stop':
            print("Connection stopped")
            self._connection = False
            self.stop()

        elif event == 'error':
            print("Connection error")


    def _on_stream_event(self, event, attrs = None):

        print("Stream event {} : {}".format(event, attrs))

        if event == 'start':
            pass

        elif event == 'stop':
            self.start_stream_stop()
            self.stop()

        elif event == 'error':
            pass

    def _on_stream_object(self, obj):

        if obj.tag == 'stream:features':

            self._last_features = obj


    def _features_waiter_first(self, obj):

        if obj.tag == 'stream:features':

            print("First Features received:\n{}".format(xml.etree.ElementTree.tostring(obj)))
            print("Driving to TLS")

            self._input_stream_objects_hub.set_waiter(
                'features', self._features_waiter_second
                )

            self._tls_driver.drive(obj)


    def _tls_driver_finish_waiter(self, result):

        if result == 'no tls':
            logging.error("Peer not supports TLS. exiting...")
            self.stop()

        elif result == 'response error':
            logging.error("Some Error")
            self.stop()

        elif result == 'failure':
            logging.error("TLS request failure")
            self.stop()

        elif result == 'proceed':
            threading.Thread(
                target = self._tls_driver.proceed,
                name = "Thread Proceeding STARTTLS negotiations"
                ).start()

        elif result == 'stream error':
            logging.error("Stream Error while STARTTLS negotiations")
            self.stop()

        elif result == 'stream stopped':
            logging.error("Peer closed stream while STARTTLS negotiations")
            self.stop()

        elif result == 'success':
            pass

        else:
            raise ValueError("Wrong TLS driver result")
