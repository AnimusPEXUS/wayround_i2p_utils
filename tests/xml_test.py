

import xml.parsers.expat

def StartElementHandler(name, attributes):
    print("start {}, {}".format(name, attributes))




sample_xmpp1 = b"""\
<stream:stream
       from='juliet@im.example.com'
       to='im.example.com'
       version='1.0'
       xml:lang='en'
       xmlns='jabber:client'
       xmlns:stream='http://etherx.jabber.org/streams'>
     <message>
       <body>foo</body>
     </message>
   </stream:stream>
"""

sample_xmpp2 = b"""\
<stream
       from='juliet@im.example.com'
       to='im.example.com'
       version='1.0'
       xml:lang='en'
       xmlns='http://etherx.jabber.org/streams'>
     <message xmlns='jabber:client'>
       <body>foo</body>
     </message>
   </stream>
"""

sample_xmpp = sample_xmpp2

p = xml.parsers.expat.ParserCreate('UTF-8', ' ')

p.StartElementHandler = StartElementHandler

p.Parse(sample_xmpp)
