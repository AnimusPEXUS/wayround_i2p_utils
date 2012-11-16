
"""
Simple Client used while developing xmpp module of org.wayround.utils
"""

import logging
import select
import socket

import org.wayround.utils.stream

_GLOBAL_DEFAULT_TIMEOUT = socket.getdefaulttimeout()


def connect_xmpp(address, timeout = _GLOBAL_DEFAULT_TIMEOUT, source_address = None):

    sock = socket.create_connection(address, timeout, source_address)

#    sock.send(b"asd\n")
#    print(str(sock.recv(1) + sock.recv(1), encoding='utf-8'))

    logging.debug("creating ss")
    ss = org.wayround.utils.stream.SocketStreamer(
        sock,
        socket_transfer_size = 4096
        )

    ch = XMPPContentHandler()

    ss.start()

    xml.sax.parse(ss.strout, ch)

    ss.close()
    sock.close()

