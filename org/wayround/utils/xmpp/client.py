
"""
Simple Client used while developing xmpp module of org.wayround.utils
"""

import logging
import socket
import xml.etree.ElementTree
import xml.parsers.expat

import org.wayround.utils.stream
import org.wayround.utils.xml
import org.wayround.utils.xmpp.core

_GLOBAL_DEFAULT_TIMEOUT = socket.getdefaulttimeout()


class SimpleBotClient:

    def __init__(self, host, port, domain, user_jid, password):


        org.wayround.utils.stream.SocketStreamer(
            )

        sock = socket.create_connection((host, port))

        sock_streamer = org.wayround.utils.stream.SocketStreamer(
            sock, socket_transfer_size = 4096, on_stream_stopped = self._on_stream_stopped
            )

        xml_parser = xml.parsers.expat.ParserCreate('UTF-8', False)

        org.wayround.utils.xmpp.core.XMPPInputStreamReader(
            sock_streamer.strout, xml_parser
            )

        xml_target = org.wayround.utils.xmpp.core.XMPPInputStreamReaderTarget(
            on_stream_start = self._on_stream_start,
            on_stream_start_error = self._on_stream_start_error,
            on_stream_end = self._on_stream_end,
            on_element_readed = self._on_element_readed
            )

        org.wayround.utils.xml.expat_parser_connect_target(xml_parser, xml_target)

    def _on_stream_stopped(self):
        pass

    def _on_stream_start(self):
        pass

    def _on_stream_start_error(self):
        pass

    def _on_stream_end(self):
        pass

    def _on_element_readed(self, obj):
        pass

