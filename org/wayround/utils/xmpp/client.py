
"""
Simple Client used while developing xmpp module of org.wayround.utils
"""

import logging
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

        self._hub = None


    def start(self):

        if self.is_working():
            raise RuntimeError("Already working")

        self._sock = socket.create_connection((self._host, self._port))

        self._sock_streamer = org.wayround.utils.stream.SocketStreamer(
            self._sock,
            socket_transfer_size = 4096,
            on_connection_stopped = self._on_connection_stopped
            )

        self._sock_streamer.start()

        self._xml_parser = xml.parsers.expat.ParserCreate('UTF-8')

        self._input_stream_reader = org.wayround.utils.xmpp.core.XMPPInputStreamReader(
            self._sock_streamer.strout,
            self._xml_parser
            )

        self._output_stream_writer = org.wayround.utils.xmpp.core.XMPPOutputStreamWriter(
            self._sock_streamer.strin
            )

        self._xml_target = org.wayround.utils.xmpp.core.XMPPInputStreamReaderTarget(
            on_stream_start = self._on_stream_start,
            on_stream_start_error = self._on_stream_start_error,
            on_stream_end = self._on_stream_end,
            on_element_readed = self._on_element_readed
            )

        org.wayround.utils.xml.expat_parser_connect_target(
            self._xml_parser,
            self._xml_target
            )

        self._hub = org.wayround.utils.xmpp.core.XMPPInputStreamHub()

        self._hub.set_waiter('features', self._features_waiter)

        for i in [
            self._input_stream_reader.start,
            self._output_stream_writer.start,
            ]:

            threading.Thread(
                target = i
                ).start()

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

            for i in [
                self._input_stream_reader.stop,
                self._output_stream_writer.stop
                ]:

                threading.Thread(
                    target = i
                    ).start()


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

        print("Features received:\n{}".format(xml.etree.ElementTree.tostring(obj)))

        self._output_stream_writer.send(
            org.wayround.utils.xmpp.core.stop_stream()
            )

    def _on_connection_stopped(self):
        print("Stream stopped")
        self.stop()

    def _on_stream_start(self, attrs):

        print("Stream started")

    def _on_stream_start_error(self):
        pass

    def _on_stream_end(self):
        print("Stream stopped")
        self.stop()

    def _on_element_readed(self, obj):

        self._hub.dispatch(obj)

