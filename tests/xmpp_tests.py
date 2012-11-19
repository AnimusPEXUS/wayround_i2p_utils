import logging
import socket
import sys

import lxml.etree

import org.wayround.utils.stream
import org.wayround.utils.xmpp.core

logging.basicConfig(level = 'DEBUG', format = "%(levelname)s :: %(threadName)s :: %(message)s")

def on_stream_stopped():
    print("Server closed Connection")

def on_stream_start(attr):
    print("New Stream Start Responsed. Attributes: {}".format(repr(attr)))

def on_stream_start_error():
    print("Stream Start error")

def on_stream_end():
    print("Stream End")

def on_element_readed(element):
    print(str("Read element:".format(element)))


sock = socket.create_connection(('wayround.org', 5222))


ss = org.wayround.utils.stream.SocketStreamer(
    sock, on_stream_stopped = on_stream_stopped
    )


xml_parser_target = org.wayround.utils.xmpp.core.XMPPInputStreamReaderTarget(
    on_stream_start = on_stream_start,
    on_stream_start_error = on_stream_start_error,
    on_stream_end = on_stream_end,
    on_element_readed = on_element_readed
    )

xml_parser = lxml.etree.XMLParser(
    target = xml_parser_target,
    encoding = 'utf-8'
    )

sp = org.wayround.utils.xmpp.core.XMPPInputStreamReader(
    ss.strout, xml_parser
    )

ss.start()
sp.start()

ss.strin.write(
    bytes(
        org.wayround.utils.xmpp.core.start_stream(
            fro = 'test@wayround.org',
            to = 'wayround.org',
            ),
        encoding = 'utf-8'
        )
    )

#ss.strout.flush()
#print(ss.strout.read())

sys.stdout.flush()

exit(0)
