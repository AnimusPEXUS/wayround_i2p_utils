import logging
import org.wayround.utils.xmpp

logging.basicConfig(level='DEBUG', format="%(levelname)s :: %(threadName)s :: %(message)s")


org.wayround.utils.xmpp.connect_xmpp(('wayround.org', 5222))
