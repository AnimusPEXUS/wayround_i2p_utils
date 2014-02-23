
import lxml.etree

import org.wayround.utils.types


def _check_tagname_class_attrnames(tagname_class_attrnames):
    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames, {'t': list, '.': {'t': tuple, '<': 3, '>': 4}}
        ):
        raise TypeError("`tagname_class_attrnames' has invalid structure")

    for i in tagname_class_attrnames[:]:
        if len(i) == 3:
            inde = tagname_class_attrnames.index(i)
            new_val = i + ('',)
            tagname_class_attrnames[inde] = new_val

        if len(i) == 4 and i[3] == None:
            inde = tagname_class_attrnames.index(i)
            new_val = tuple(i[:3]) + ('',)
            tagname_class_attrnames[inde] = new_val

        if len(i) == 4:
            if not i[3] in ['', '?', '+', '*']:
                raise ValueError("invalid mode")

    return


def subelems_to_object_props(
    element, obj, tagname_class_attrnames,
    must_be=False
    ):

    """
    Find element by tag and convert it to object using additional information

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'), ...]

    return: False - no error, True - if must_be==True and some element not
        found
    """

    ret = False

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    _check_tagname_class_attrnames(tagname_class_attrnames)

    for i in tagname_class_attrnames:

        val = element.find(i[0])
        if val != None:
            getattr(obj, 'set_{}'.format(i[2]))(i[1].new_from_element(val))
        else:
            if must_be:
                ret = True

    return ret


def subelems_to_object_props2(element, obj, tagname_class_attrnames):
    """
    In distinction to subelems_to_object_props(), the forth values of tuples
    are not ignored and used to check the validity on element appearance.

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'[, '[\?\*\+]?']), ...]
    """

    ret = False

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    _check_tagname_class_attrnames(tagname_class_attrnames)

    must_be = []
    can_be = []
    multiples = []
    multiples_plus = []

    for i in tagname_class_attrnames:

        if i[3] == '?':
            must_be.append(i)

        elif i[3] == '*':
            multiples.append(i)

        elif i[3] == '+':
            multiples_plus.append(i)

        else:
            must_be.append(i)

    res = subelems_to_object_props(
        element,
        obj,
        tagname_class_attrnames=must_be,
        must_be=True
        )

    if res == True:
        ret = True

    else:
        subelems_to_object_props(
            element, obj, can_be
            )

        subelemsm_to_object_propsm(
            element, obj, multiples, must_be=False
            )

        subelemsm_to_object_propsm(
            element, obj, multiples_plus, must_be=True
            )

    return ret


def subelemsm_to_object_propsm(
    element, obj, tagname_class_attrnames, must_be=False
    ):
    """
    Find many elements by tag and convert them to objects using additional
    information

    must_be indicated necessarity of results to be len(lst) > 0

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'[, '[\?\*\+]?']), ...]
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    _check_tagname_class_attrnames(tagname_class_attrnames)

    for i in tagname_class_attrnames:

        gt_func = getattr(obj, 'get_{}'.format(i[2]))

        objs = gt_func()

        vals = element.findall(i[0])

        if must_be and len(vals) == 0:
            raise ValueError("Too few elements of `{}'".format(i[0]))

        for val in vals:
            objs.append(i[1].new_from_element(val))

        getattr(obj, 'check_{}'.format(i[2]))(objs)

    return


def elem_props_to_object_props(element, obj, names):
    """
    Get named element properties and apply them to object

    names must have following structure:
    [('element_prop_name', 'object_prop_name'), ...]
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        names,
        {'t': list, '.':
         {'t': tuple, '<': 2, '>': 2, '.': {'t': str}
          }
         }
        ):
        raise TypeError("`names' has invalid structure")

    for i in names:
        getattr(obj, 'set_{}'.format(i[1]))(element.get(i[0]))

    return


def object_props_to_subelems(obj, element, names):
    """
    Get named object properties and generate subelements to element

    names must be list of names of object properties
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        names,
        {'t': list, '.': {'t': str}}
        ):
        raise TypeError("`names' must be list of strings")

    for i in names:
        val = getattr(obj, 'get_{}'.format(i))()
        if val != None:
            element.append(val.gen_element())

    return


def object_props_to_subelems2(obj, element, tagname_class_attrnames):
    """
    In distinction to object_props_to_subelems(), firsts values of tuples can
    end with '*', '+' or '?' , which indicates necessity to use function
    object_propsm_to_subelemsm()

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'[, '[\?\*\+]?']), ...]
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    _check_tagname_class_attrnames(tagname_class_attrnames)

    must_be = []
    multiples = []

    for i in tagname_class_attrnames:

        if i[3] == '?':
            must_be.append(i)

        elif i[3] == '*':
            multiples.append(i)

        elif i[3] == '+':
            multiples.append(i)

        else:
            must_be.append(i)

    object_props_to_subelems(
        obj,
        element,
        names=list(i[2] for i in must_be)
        )

    object_propsm_to_subelemsm(
        obj,
        element,
        names=list(i[2] for i in multiples)
        )

    return


def object_propsm_to_subelemsm(obj, element, names):
    """
    Get named object properties and generate subelements to element

    names must be list of names of object properties
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        names,
        {'t': list, '.': {'t': str}}
        ):
        raise TypeError("`names' must be list of strings")

    for i in names:
        vals = getattr(obj, 'get_{}'.format(i))()
        for val in vals:
            element.append(val.gen_element())

    return


def object_props_to_elem_props(obj, element, names):
    """
    Get named object properties and make element properties

    names must have following structure (seq of seqs of strings):
    [('object_prop_name', 'element_prop_name'), ...]
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        names,
        {'t': list, '.':
         {'t': tuple, '<': 2, '>': 2, '.': {'t': str}}
         }
        ):
        raise TypeError("`names' has invalid structure")

    for i in names:

        val = getattr(obj, 'get_{}'.format(i[0]))()
        if val != None:
            element.set(i[1], val)

    return


def subelems_to_order(element, order, tagname_class_attrnames):
    """
    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'[, '[\?\*\+]?']), ...]
    """

    _check_tagname_class_attrnames(tagname_class_attrnames)

    for i in element:

        cls = None
        tag = None
        prop = None

        for j in tagname_class_attrnames:
            if (j[0] == i.tag):
                cls = j[1]
                tag = i.tag
                prop = j[2]
                break

        if cls != None:
            order.append((tag, cls.new_from_element(i), prop))

    return


def order_to_subelems(order, element):

    for i in order:
        element.append(i[1].gen_element())

    return


def parse_element_tag(element, localname, namespaces=None):

    """
    Tag parse routine

    localname must be str or list of str

    returns  (localname, namespace) where namespace is one of namespaces or
    (None, None)
    """

    if type(element) != lxml.etree._Element:
        raise ValueError("`element' must be lxml.etree._Element")

    if localname == None:
        localname = []

    if not isinstance(localname, list):
        localname = [localname]

    if isinstance(namespaces, str):
        namespaces = [namespaces]

    if not org.wayround.utils.types.struct_check(
        localname,
        {'t': list, '.': {'t': str}}
        ):
        raise TypeError("`localname' must be list of strings")

    if not org.wayround.utils.types.struct_check(
        namespaces,
        {'t': list, 'None': True, '.': {'t': str}}
        ):
        raise TypeError("`namespaces' has invalid structure")

    qname = lxml.etree.QName(element)

    ret = None, None

    if len(localname) == 0 or qname.localname in localname:
        if namespaces == None:
            ret = qname.localname, qname.namespace
        else:
            if qname.namespace in namespaces:
                ret = qname.localname, qname.namespace

    return ret


def checker_factory(cls, tagname_class_attrnames):
    """
    Factories check methods for pointed class using tagname_class_attrnames
    structure

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'[, '[\?\*\+]?']), ...]
    """

    _check_tagname_class_attrnames(tagname_class_attrnames)

    for i in tagname_class_attrnames:

        lst = False
        none = False
        if i[3] == '?':
            lst = False
            none = True
        elif i[3] == '+':
            lst = True
            none = False
        elif i[3] == '*':
            lst = True
            none = True
        else:
            lst = False
            none = False

        typ = i[1]

        check = ''
        doc = ''
        if lst == False and none == False:
            check = """
    if not type(value) == typ:
        raise TypeError("`{name}' must be of type {typ}")
            """.format(name=i[2], typ=typ)
            doc = 'value must be single value of type {}'.format(typ)

        elif lst == False and none == True:
            check = """
    if value != None and not type(value) == typ:
        raise TypeError("`{name}' must be None or of type {typ}")
            """.format(name=i[2], typ=typ)
            doc = 'value must be single value of None or of type {}'.format(typ)

        elif lst == True and none == False:
            check = """
    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames, {'t': list, '.': {'t': typ}}
        ) or len(value) == None:
        raise TypeError("`{name}' must be not empty list of type {typ}")
"""
            doc = 'value must be unempty list of type {}'.format(typ)

        elif lst == True and none == True:
            check = """
    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames, {'t': list, '.': {'t': typ}}
        ):
        raise TypeError("`{name}' must be list of type {typ}")
"""
            doc = 'value must be list of type {}'.format(typ)
        else:
            raise Exception("programming error")

        exec("""
def check(self, value):

{check}

cles.check_{name} = check
cles.check_{name}.__doc__ = doc

del check
        """.format(name=i[2], check=check),
        {'typ': typ, 'cles': cls, 'doc': doc}
        )

    return


def simple_exchange_class_factory(
    cls,
    tag,
    namespace,
    subelements_struct,
    properties_list,
    value_name=None
    ):

    """
    Factories simple class structure to handle simple lxml elements

    see org.wayround.xmpp.xcard for example usage

    Yes, this is not as beautiful as using class inheritance, but match simpler
    and obvious

    if value_name != None methods generated by this factory, requires following
    methods to be present in class at runtime:
    --
    set_{value_name}(value)
    get_{value_name}(value)
    --
    You can use
    org.wayround.utils.factory.class_generate_attributes_and_check()
    to generate set_this_element_text_value() and get_this_element_text_value()
    automatically
    """

    gw1 = ''
    gw2 = ''
    if value_name != None:
        gw1 = 'cl.set_{value_name}(element.text)'.format(
            value_name=value_name
            )
        gw2 = 'el.text = cl.get_{value_name}()'.format(
            value_name=value_name
            )

    exec("""
def __init__(self, **kwargs):

    for i in PROPERTIES_LIST:
        set_func = getattr(self, 'set_{{}}'.format(i))
        set_func(kwargs.get(i))

    return

def new_from_element(cls, element):

    import org.wayround.utils.lxml

    tag = org.wayround.utils.lxml.parse_element_tag(
        element,
        tag,
        NAMESPACE
        )[0]

    if tag is None:
        raise ValueError("invalid element tag or namespace")

    cl = cls()

    {gw1}

    org.wayround.utils.lxml.subelems_to_object_props2(
        element, cl,
        SUBELEMENTS_STRUCT
        )

    return cl

def gen_element(self):

    import lxml.etree
    import org.wayround.utils.lxml

    self.check()

    el = lxml.etree.Element(tag)

    {gw2}

    org.wayround.utils.lxml.object_props_to_subelems2(
        self, el,
        SUBELEMENTS_STRUCT
        )

    return el

clas.__init__ = __init__
clas.new_from_element = classmethod(new_from_element)
clas.gen_element = gen_element

del __init__
del new_from_element
del gen_element

""".format(
    gw1=gw1,
    gw2=gw2
    ),
    {
     'PROPERTIES_LIST': properties_list,
     'tag': tag,
     'SUBELEMENTS_STRUCT': subelements_struct,
     'NAMESPACE': namespace,
     'clas': cls
    }
    )
