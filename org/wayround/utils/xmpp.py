
import logging
import select
import socket
import xml.sax

import org.wayround.utils.stream

_GLOBAL_DEFAULT_TIMEOUT = socket.getdefaulttimeout()

class XMPPContentHandler(xml.sax.ContentHandler):

    def startDocument(self):
        print('startDocument')

    def endDocument(self):
        print('endDocument')

    def startElement(self, name, attrs):
        print('startElement({},{})'.format(name, attrs))

    def endElement(self, name):
        print('startElement({},{})'.format(name))

def connect_xmpp(address, timeout=_GLOBAL_DEFAULT_TIMEOUT, source_address=None):

    sock = socket.create_connection(address, timeout, source_address)

#    sock.send(b"asd\n")
#    print(str(sock.recv(1) + sock.recv(1), encoding='utf-8'))

    logging.debug("creating ss")
    ss = org.wayround.utils.stream.SocketStreamer(
        sock,
        socket_transfer_size=4096
        )

#    ch = XMPPContentHandler()
#    xml.sax.parse(ss.strout, ch)

    logging.debug("starting ss")
    ss.start()

    try:
        logging.debug("waiting input to be available")
        select.select([], [ss.strin.fileno()], [])

        logging.debug("writing test data")
        ss.strin.write(b"asd\n")
        ss.strin.flush()

        logging.debug("waiting output to be available")
        select.select([ss.strout.fileno()], [], [])

        logging.debug("reading response data")
        print(repr(ss.strout.read()))

        logging.debug("completed")
    except:
        logging.exception("error")

    logging.debug("closing 1")
    ss.close()
    logging.debug("closing 2")
    sock.close()

