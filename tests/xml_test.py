

import org.wayround.utils.xml

class Test:


    def StartElementHandler(self, name, attributes):
        print("start {}, {}".format(name, attributes))

    def EndElementHandler(self, name):
        print("end {}".format(name))



sample_xmpp = """
<presence>
   <show/>
   </presence>

   <message to='foo'>
      <body/>
    </message>
    <iq to='bar'
        type='get'>
      <query/>
    </iq>
    """

xml.parsers.expat

t = Test(encoding = 'UTF-8')
t.Parse(bytes(sample_xmpp, encoding = 'utf-8'))
#a = lxml.etree.fromstring(

#    )
