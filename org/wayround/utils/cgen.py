
import logging

class Translatated:
    """
    Must be extended by element, which wants to be translated
    """

class Communicated:
    """
    Must be extended be element, which must be communicated with python
    """

class Var:

    def __init__(self, typ='void', name='name'):
        self.typ = typ
        self.name = name

    def __str__(self):
        spc = ''
        if len(self.name) > 0:
            spc = ' '
        return "{}{}{}".format(self.typ, spc, self.name)

class Source:

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return self.text

class Struct:

    def __init__(self, tag='', lst=None):

        self.tag = tag
        self.lst = lst

    def __str__(self):

        lst = []
        for i in self.lst:
            lst.append(str(i))

        lst = ';\n    '.join(lst)

        return """\
struct {tag} {{
    {lst}
    }}
""".format(tag=self.tag, lst=lst)


class Union:
    pass

class Function:
    def __init__(self, ret_type='void', name='some', args=None, body=''):
        self.ret_type = ret_type
        self.name = name
        self.args = args
        self.body = body

    def __str__(self):

        args = []
        for i in self.args:
            args.append(str(i))

        args = ', '.join(args)

        return """\
{ret_type} {name}({args}) {{
{body}
}}
""".format(
            ret_type=self.ret_type,
            name=self.name,
            args=args,
            body=self.body
            )


class Class:
    pass

class Import:
    def __init__(self, name, local=False):
        self.name = name
        self.local = False

    def __str__(self):
        quote_sign1 = '<'
        quote_sign2 = '>'
        if self.local:
            quote_sign1 = '"'
            quote_sign2 = '"'
        return "#include {qs1}{name}{qs2}\n".format(
            qs1=quote_sign1,
            qs2=quote_sign2,
            name=self.name
            )

class Instruction:

    def __init__(self, typ, data):
        pass

class WrongElementType(Exception): pass

class Cfile:

    def __init__(self):

        self.template = []

    def add_element(self, element):

        if not isinstance(element, (Import, Function, Source, Struct)):
            raise WrongElementType("Wrong element Type")

        self.template.append(element)

    def translate(self):

        ret = ''

        for i in self.template:
            ret += str(i)

        return ret
