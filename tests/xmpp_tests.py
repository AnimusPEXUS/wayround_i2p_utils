
import logging
#import signal

import org.wayround.utils.xmpp.client

logging.basicConfig(level = 'DEBUG', format = "%(levelname)s :: %(threadName)s :: %(message)s")

sbc = org.wayround.utils.xmpp.client.SampleBotClient(
    host = 'wayround.org',
    port = 5222,
    domain = 'wayround.org',
    user_jid = 'test@wayround.org',
    password = 'Az9bblTgiCQZ9yUAK/WGp9cz4F8='
    )

sbc.start()
sbc.wait()

#signal.pause()

exit(0)
