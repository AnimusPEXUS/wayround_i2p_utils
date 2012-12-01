
import logging
import lxml.etree
import signal
import socket


import org.wayround.utils.xmpp.core
import org.wayround.utils.xmpp.client

# TODO: Try to remove
lxml.etree.register_namespace('stream', 'http://etherx.jabber.org/streams')

logging.basicConfig(level = 'DEBUG', format = "%(levelname)s :: %(threadName)s :: %(message)s")

jid = org.wayround.utils.xmpp.core.JID(
    user = 'test', domain = 'wayround.org'
    )

cinfo = org.wayround.utils.xmpp.core.C2SConnectionInfo(
    host = 'wayround.org',
    port = 5222,
    jid = jid,
    password = 'Az9bblTgiCQZ9yUAK/WGp9cz4F8='
    )

sock = socket.create_connection(
    (
     cinfo.host,
     cinfo.port
     )
    )

sbc = org.wayround.utils.xmpp.client.SampleC2SClient(
    sock,
    cinfo,
    jid
    )

sbc.start()

#try:
#    signal.pause()
#except:
#    pass
#
#sbc.stop()
while True:
    if sock._closed:
        break

logging.debug("Socket have been closed right now")

sbc.wait('stopped')

logging.debug("Reached the end. socket is {}".format(sock))

exit(0)
