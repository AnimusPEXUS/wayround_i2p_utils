
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

    def __init__(self, host, port, domain, user_jid, password):

        self._host = host
        self._port = port
        self._domain = domain
        self._user_jid = user_jid
        self._password = password

        self._clean(init = True)

    def _clean(self, init = False):

        if not init:
            if self.is_working():
                raise RuntimeError("Working. Cleaning restricted")

        self._stop_flag = False
        self._stopping = False

        self._sock = None
        self._sock_streamer = None
        self._xml_parser = None

        self._input_stream_reader = None
        self._output_stream_writer = None
        self._xml_target = None

        self._input_stream_hub = None

        self.status = 'before start'
        self.tls_request_result = None

        self._ignore_next_stream_end = False


    def start(self):

        if self.is_working():
            raise RuntimeError("Already working")

        ######### HUBS

        self._connection_events_hub = org.wayround.utils.xmpp.core.ConnectionEventsHub()
        self._connection_events_hub.set_waiter('primary', self._on_connection_event)

        self._stream_events_hub = org.wayround.utils.xmpp.core.StreamEventsHub()

        self._input_stream_hub = org.wayround.utils.xmpp.core.StreamObjectsDispatchingHub()
        self._input_stream_hub.set_waiter('features', self._features_waiter)
        self._input_stream_hub.set_waiter('tls', self._urn_ietf_params_xml_ns_xmpp_tls_waiter)

        ######### SOCKET

        self._sock = socket.create_connection(
            (
             self._host,
             self._port
             )
            )

        ######### STREAMS

        self._sock_streamer = org.wayround.utils.stream.SocketStreamer(
            self._sock,
            socket_transfer_size = 4096,
            on_connection_event = self._connection_events_hub.dispatch
            )

        self._sock_streamer.start()


        self._output_stream_writer = org.wayround.utils.xmpp.core.XMPPOutputStreamWriter(
            self._sock_streamer.strin
            )

        self._output_stream_writer.start()

        ######### DRIVERS

        self._tls_driver = org.wayround.utils.xmpp.core.TLSDriver(
            )

        self._tls_driver.set_objects(
            self._sock_streamer,
            self._output_stream_writer,
            self,
            on_finish = self._on_tls_negotiated
            )

        ######### XML TARGET

        self._xml_target = org.wayround.utils.xmpp.core.XMPPInputStreamReaderTarget(
            on_stream_event = self._on_stream_event,
            on_element_readed = self._input_stream_hub.dispatch
            )

        org.wayround.utils.xml.expat_parser_connect_target(
            self._xml_parser,
            self._xml_target
            )


        ######### START XML PARSER AND XML INPUT FEEDER FOR IT

        self._start_xml_parser()



        ######## WAIT SOCKET OUTPUT AVAILABILITY AND START OUR OUTPUT STREAM

        p = select.Poll()

        self._output_stream_writer.send(
            org.wayround.utils.xmpp.core.start_stream(
                fro = self._user_jid,
                to = self._domain
                )
            )

        return

    def stop(self):


        if not self._stopping:
            self._stopping = True

            self._stop_flag = True

            self._sock_streamer.stop()

            self._stop_xml_parser()

            self._output_stream_writer.stop()

            self.wait()

            logging.debug("Cleaning client instance")

            self._sock.shutdown(socket.SHUT_RDWR)
            self._sock.close()

            self._clean()

            self._stopping = False


        return

    def wait(self):

        while True:

            if not self.is_working():
                break

            time.sleep(0.5)

        return

    def _start_xml_parser(self):
        self._xml_parser = xml.parsers.expat.ParserCreate('UTF-8')
        self._input_stream_reader = org.wayround.utils.xmpp.core.XMPPInputStreamReader(
            self._sock_streamer.strout,
            self._xml_parser
            )
        org.wayround.utils.xml.expat_parser_connect_target(
            self._xml_parser,
            self._xml_target
            )
        self._input_stream_reader.start()

    def _stop_xml_parser(self):
#        self._ignore_next_stream_end=True
#        self._xml_parser.Parse(b'</stream:stream>', True)
        self._input_stream_reader.stop()

    def _restart_xml_parser(self):
        self._stop_xml_parser()
        self._start_xml_parser()



    def is_working(self):

        v1_1 = self._sock_streamer
        v1_2 = None
        if v1_1:
            v1_2 = self._sock_streamer.is_working()
        v1_2 = bool(v1_2)

        v2_1 = self._input_stream_reader
        v2_2 = None
        if v2_1:
            v2_2 = self._input_stream_reader.is_working()
        v2_2 = bool(v2_2)


        v3_1 = self._output_stream_writer
        v3_2 = None
        if v3_1:
            v3_2 = self._output_stream_writer.is_working()
        v3_2 = bool(v3_2)


        logging.debug("""
self._sock_streamer.is_working() == {}
self._input_stream_reader.is_working() == {}
self._output_stream_writer.is_working() == {}
""".format(v1_2, v2_2, v3_2)
            )

        return (
            v1_2
            or
            v2_2
            or
            v3_2
            )

    def _features_waiter(self, obj):

        if obj.tag == 'stream:features':

            print("Features received:\n{}".format(xml.etree.ElementTree.tostring(obj)))

            self._


    def _urn_ietf_params_xml_ns_xmpp_tls_waiter(self, obj):

        if obj.get('xmlns', None) == 'urn:ietf:params:xml:ns:xmpp-tls':
            if self.status == 'requesting tls':

                if obj.tag in ['proceed', 'failure']:
                    self.tls_request_result = obj.tag
                else:
                    logging.error("TLS Request Error")
                    self.close()

                if self.tls_request_result == 'proceed':

                    self._sock_streamer.start_ssl()

                    self._restart_xml_parser()

                    self._output_stream_writer.send(
                        org.wayround.utils.xmpp.core.start_stream(
                            fro = self._user_jid,
                            to = self._domain
                            )
                        )
                else:
                    logging.error("TLS Request Failure")
                    self.close()


    def _on_connection_event(self, event):

        if event == 'started':
            print("Connection started")

        elif event == 'stopped':
            print("Connection stopped")

    def _on_stream_event(self, attrs):

        print("Stream started")

    def _on_stream_start_error(self):
        pass

    def _on_stream_end(self):
#        self._restart_xml_parser()
#
        if self.status == 'end of life':
            print("Stream stopped")
            self.stop()

    def _on_tls_negotiated(self, obj):

        pass
