
import logging
import signal
import lxml.etree


import org.wayround.utils.xmpp.core
import org.wayround.utils.xmpp.client

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

sbc = org.wayround.utils.xmpp.client.SampleBotClient(
    cinfo,
    jid
    )

sbc.start()

try:
    signal.pause()
except:
    pass

sbc.stop()

try:
    sbc.wait('stopped')
except:
    pass

exit(0)
