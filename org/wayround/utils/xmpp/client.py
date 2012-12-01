
"""
Simple Client used while developing xmpp module of org.wayround.utils
"""

import logging
import select
import threading
import time

import lxml.etree

import org.wayround.utils.stream
import org.wayround.utils.xml
import org.wayround.utils.xmpp.core


class SampleC2SClient:

    def __init__(self, sock, connection_info, jid):

        self._sock = sock
        self._connection_info = connection_info
        self._jid = jid

        self._clear(init = True)

    def _clear(self, init = False):

        if not init:
            if not self.stat() == 'stopped':
                raise RuntimeError("Working. Cleaning restricted")

        self._connection = False
        self._driven = False
        self._starting = False
        self._stop_flag = False
        self._stopping = False
        self._stream_in = False
        self._stream_out = False
        self._stream_stop_sent = False

        self._sock_streamer = None

        self._input_machine = None
        self._output_machine = None

        self._connection_events_hub = None
        self._input_stream_events_hub = None
        self._input_stream_objects_hub = None
        self._output_stream_events_hub = None

        self._tls_driver = None

        self._tls_result = None

        self._features_iteration = None


    def start(self):

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            self._starting = True

            ######### DRIVERS

            self._tls_driver = org.wayround.utils.xmpp.core.STARTTLSClientDriver()

            self._m = org.wayround.utils.xmpp.core.Monitor()

            ######### HUBS

            self._connection_events_hub = org.wayround.utils.xmpp.core.ConnectionEventsHub()

            self._input_stream_events_hub = org.wayround.utils.xmpp.core.StreamEventsHub()
            self._input_stream_objects_hub = org.wayround.utils.xmpp.core.StreamObjectsHub()

            self._output_stream_events_hub = org.wayround.utils.xmpp.core.StreamEventsHub()

            self.reset_hubs()

            ######### SOCKET


            logging.debug('sock is {}'.format(self._sock))


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

            logging.debug("Starting shutdown sequence")
            self._shutdown(_forced = True)
            self.stop_violent(_forced = True)

    def stop_violent(self, _forced = False):


        if (not self._stopping and not self._starting) or _forced:
            self._stopping = True

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

            logging.debug('sock is {}'.format(self._sock))

            self._clear()

            self._stopping = False

        return

    def _shutdown(self, timeout_sec = 5.0, _forced = False):

        time_waited = 0.0

        if (not self._stopping and not self._starting) or _forced:

            self._stop_flag = True

            logging.debug("Stopping client correctly")

            if self._connection and not self._stream_stop_sent:
                logging.debug("Sending end of stream")
                self._output_machine.send(
                    org.wayround.utils.xmpp.core.stop_stream()
                    )
                self._stream_stop_sent = True


            while True:
                if self.stat() == 'stopped':
                    break

                logging.debug("Timeout in {:3.2f} sec".format(timeout_sec - time_waited))
                if time_waited >= timeout_sec:
                    break

                time.sleep(1.0)
                time_waited += 1.0


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


    def reset_hubs(self):

        self._connection_events_hub.clear()
        self._input_stream_events_hub.clear()
        self._input_stream_objects_hub.clear()
        self._output_stream_events_hub.clear()

        self._connection_events_hub.set_waiter(
            'main', self._on_connection_event,
            )
        self._connection_events_hub.set_waiter(
            'm', self._m.connection
            )

        self._input_stream_events_hub.set_waiter(
            'main', self._on_stream_in_event,
            )
        self._input_stream_events_hub.set_waiter(
            'm', self._m.stream_in
            )

        self._input_stream_objects_hub.set_waiter(
            'main', self._on_stream_object,
            )
        self._input_stream_objects_hub.set_waiter(
            'm', self._m.object
            )

        self._output_stream_events_hub.set_waiter(
            'main', self._on_stream_out_event,
            )
        self._output_stream_events_hub.set_waiter(
            'm', self._m.stream_out
            )


    def _on_connection_event(self, event, sock):

        if not self._driven:

            logging.debug("_on_connection_event `{}', `{}'".format(event, sock))

            if event == 'start':
                print("Connection started")

                self._connection = True

                self.wait('working')

                logging.debug("Ended waiting for connection. Opening output stream")


                self._output_machine.send(
                    org.wayround.utils.xmpp.core.start_stream(
                        fro = self._jid.bare(),
                        to = self._connection_info.host
                        )
                    )

                logging.debug("Stream opening tag was started")

            elif event == 'stop':
                print("Connection stopped")
                self._connection = False
                self.stop()

            elif event == 'error':
                print("Connection error")
                self._connection = False
                self.stop()


    def _on_stream_in_event(self, event, attrs = None):

        if not self._driven:

            logging.debug("Stream in event `{}' : `{}'".format(event, attrs))

            if event == 'start':

                self._stream_in = True

            elif event == 'stop':
                self._stream_in = False
                self.stop()

            elif event == 'error':
                self._stream_in = False
                self.stop()

    def _on_stream_out_event(self, event, attrs = None):

        if not self._driven:

            logging.debug("Stream out event `{}' : `{}'".format(event, attrs))

            if event == 'start':

                self._stream_out = True

            elif event == 'stop':
                self._stream_out = False
                self.stop()

            elif event == 'error':
                self._stream_out = False
                self.stop()

    def _on_stream_object(self, obj):

        logging.debug("_on_stream_object (first 255 bytes):`{}'".format(repr(lxml.etree.tostring(obj)[:255])))

        if obj.tag == '{http://etherx.jabber.org/streams}features':

            self._last_features = obj

            self._iterate_features()

    def _iterate_features(self):

        while self._driven:
            time.sleep(0.1)

        if not self._stop_flag:

            if self._features_iteration == None:

                self._features_iteration = 'tls'

                self._tls_driver.set_objects(
                    self._sock_streamer,
                    self._input_machine,
                    self._output_machine,
                    self._connection_events_hub,
                    self._input_stream_events_hub,
                    self._input_stream_objects_hub,
                    self._output_stream_events_hub,
                    self._connection_info,
                    self._jid
                    )

                self._tls_result = self._tls_driver.drive(self._last_features)
                if self._tls_result != 'success':
                    logging.error("TLS Failed")
                    self.stop()

                self._driven = False


            if self._features_iteration == 'tls':

                self._features_iteration = 'auth'
                logging.info("Auth to be implemented")

