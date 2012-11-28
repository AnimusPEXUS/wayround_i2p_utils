
import logging
#import signal

import org.wayround.utils.xmpp.core
import org.wayround.utils.xmpp.client

logging.basicConfig(level = 'DEBUG', format = "%(levelname)s :: %(threadName)s :: %(message)s")

jid = org.wayround.utils.xmpp.core.JID()

cinfo = org.wayround.utils.xmpp.core.C2SConnectionInfo(
    host = 'wayround.org',
    port = 5222,
    user_jid = jid,
    password = 'Az9bblTgiCQZ9yUAK/WGp9cz4F8='
    )

sbc = org.wayround.utils.xmpp.client.SampleBotClient(
    cinfo,
    jid
    )

sbc.start()
sbc.wait('stopped')

#signal.pause()

exit(0)
