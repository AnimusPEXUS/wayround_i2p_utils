
import lxml.etree

import org.wayround.utils.types


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

    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames, {'t': list, '.': {'t': tuple, '<': 3, '>': 3}}
        ):
        raise TypeError("`tagname_class_attrnames' has invalid structure")

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
    In distinction to subelems_to_object_props(), firsts values of tuples can
    end on '?' or '*', which indicates necessity of tag found in elements

    tagname_class_attrnames must have following structure:
    [('{ns}tag[?*]', ClassName, 'property_name'), ...]
    """

    ret = False

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames, {'t': list, '.': {'t': tuple, '<': 3, '>': 3}}
        ):
        raise TypeError("`tagname_class_attrnames' has invalid structure")

    must_be = []
    can_be = []
    multiples = []

    for i in tagname_class_attrnames:

        if i[0].endswith('?'):
            can_be.append((i[0][:-1], i[1], i[2]))

        elif i[0].endswith('*'):
            multiples.append((i[0][:-1], i[1], i[2]))

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
            element, obj, multiples
            )

    return ret


def subelemsm_to_object_propsm(element, obj, tagname_class_attrnames):
    """
    Find many elements by tag and convert them to objects using additional
    information

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'), ...]
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames,
        {'t': list, '.': {'t': tuple, '<': 3, '>': 3}}
        ):
        raise TypeError("`tagname_class_attrnames' has invalid structure")

    for i in tagname_class_attrnames:

        gt_func = getattr(obj, 'get_{}'.format(i[2]))

        objs = gt_func()

        vals = element.findall(i[0])

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
    end on '*', which indicates necessity to use function
    object_propsm_to_subelemsm()

    tagname_class_attrnames must have following structure:
    [('{ns}tag[*]', ClassName, 'property_name'), ...]
    """

    if type(element) != lxml.etree._Element:
        raise TypeError("`element' must be lxml.etree.Element")

    if not org.wayround.utils.types.struct_check(
        tagname_class_attrnames, {'t': list, '.': {'t': tuple, '<': 3, '>': 3}}
        ):
        raise TypeError("`tagname_class_attrnames' has invalid structure")

    must_be = []
    multiples = []

    for i in tagname_class_attrnames:

        if i[0].endswith('?'):
            must_be.append((i[0][:-1], i[1], i[2]))

        elif i[0].endswith('*'):
            multiples.append((i[0][:-1], i[1], i[2]))

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
    [('{ns}tag[?*]', ClassName, 'property_name'), ...]
    """

    for i in element:

        cls = None
        tag = None
        prop = None

        for j in tagname_class_attrnames:
            if (j[0] == i.tag
                or j[0] == i.tag + '*'
                or j[0] == i.tag + '?'
                ):
                cls = j[1]
                tag = i.tag
                if tag[-1] in ['*', '?']:
                    tag = tag[:-1]
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
