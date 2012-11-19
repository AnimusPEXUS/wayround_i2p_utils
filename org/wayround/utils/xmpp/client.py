
"""
Simple Client used while developing xmpp module of org.wayround.utils
"""

import logging
import select
import socket

import org.wayround.utils.stream

import org.wayround.utils.xmpp.core

_GLOBAL_DEFAULT_TIMEOUT = socket.getdefaulttimeout()


class Client:

    def __init__(self):

        self._clear()


    def _clear(self):
        self.socket_streamer = None
        self.stanza_processor = None
        self.input_stream_handler = None


    def connect(self, address, timeout = _GLOBAL_DEFAULT_TIMEOUT, source_address = None):

        sock = socket.create_connection(address, timeout, source_address)

        self.socket_streamer = org.wayround.utils.stream.SocketStreamer(
            sock,
            socket_transfer_size = 4096
            )

        self.XMPPInputStreamHandler_target = XMPPInputStreamReaderTarget(
            on_stream_start,
            on_stream_start_error,
            on_stream_end,
            on_element_readed
            )

        self.lxml_parser = lxml.etree.XMLParser(
            target = self.XMPPInputStreamHandler_target
            )


        self.input_stream_handler = org.wayround.utils.xmpp.core.XMPPInputStreamHandler(
            on_stream_close = self.on_stream_close_reciver,
            on_stanza_read = None,
            on_protocol_start = None
            )

#        self.stanza_processor = org.wayround.utils.xmpp.core.XMPPStreamProcessor(
#            self.socket_streamer.strout,
#            self.socket_streamer.strin,
#            on_input_read_error,
#            on_input_cutter_error
#            )

        self.socket_streamer.start()


        self.socket_streamer.stop()
        sock.close()



    def on_stream_close_reciver(self):
        pass

    def on_next_stanza_read(self):
        pass
