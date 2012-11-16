import logging
import org.wayround.utils.xml

logging.basicConfig(level = 'DEBUG', format = "%(levelname)s :: %(threadName)s :: %(message)s")


#org.wayround.utils.xmpp.connect_xmpp(('wayround.org', 5222))

sample_xmpp1 = b"""
<presence>
   <show/>
   </presence><message to='foo'>
      <body/>
    </message>
    <iq to='bar'
        type='get'>
      <query/>
    </iq>
    """

sample_xmpp2 = """

    """

sample_xmpp3 = b"""
<presence>
   \xD0
   </presence> \xD0
    """

sample_xmpp4 = b"""
<presence>

   </presence
    """

sample_xmpp5 = b"""
<presence>

   </presenc
    """

sample_xmpp6 = b"""
<presence>


    """
sample_xmpp7 = b"""
<presence


    """
sample_xmpp8 = b'<presence></presence>'

sample_xmpp = sample_xmpp8

ret = org.wayround.utils.xml.find_next_tag_end(sample_xmpp)
print(repr(ret))

if ret != -1:
    print("First part:")
    print("'" + str(sample_xmpp[:ret ], encoding = 'utf-8', errors = 'replace') + "'")
    print("")
    print("Rest part:")
    print("'" + str(sample_xmpp[ret :], encoding = 'utf-8', errors = 'replace') + "'")
    print("")
