
import lxml.etree

import org.wayround.utils.types


def subelems_to_object_props(element, obj, tagname_class_attrnames):
    """
    Find element by tag and convert it to object using additional information

    tagname_class_attrnames must have following structure:
    [('{ns}tag', ClassName, 'property_name'), ...]
    """

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

    return


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


def parse_element_tag(element, localname, namespaces=None):

    """
    Tag parse routine

    returns  (localname, namespace) where namespace is one of namespaces or
    (None, None)
    """

    if type(element) != lxml.etree._Element:
        raise ValueError("`element' must be lxml.etree._Element")

    if not isinstance(localname, str):
        raise ValueError("`localname' must be str")

    if not org.wayround.utils.types.struct_check(
        namespaces,
        {'t': list, 'None': True, '.': {'t': str}}
        ):
        raise TypeError("`namespaces' has invalid structure")

    qname = lxml.etree.QName(element)

    ret = None, None

    if localname == qname.localname:
        if namespaces == None:
            ret = qname.localname, qname.namespace
        else:
            if qname.namespace in namespaces:
                ret = qname.localname, qname.namespace

    return ret
