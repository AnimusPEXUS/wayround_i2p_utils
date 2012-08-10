
"""
This module is for XML and XHTML rendering
"""

import sys
import xml.sax.saxutils
import re
import urllib.parse
import logging

import org.wayround.utils.text
import org.wayround.utils.error
import org.wayround.utils.dict



def pi(content):
    return {
        'type': 'pi',
        'content': content
        }


def comment(text):
    return {
        'type': 'comment',
        'content': text
        }

def dtd(text):
    return {
        'type': 'dtd',
        'content': text
        }

def cdata(text):
    return {
        'type': 'cdata',
        'content': text
        }

def char(text):
    return {
        'type': 'char',
        'content': text
        }

def static(text):
    return {
        'type': 'static',
        'content': text
        }

def html(
    title='',
    description='',
    keywords=[],
    basic_css=[],
    basic_js=[],
    content=None
    ):

    return {
#        '00010_xml_pi': pi('xml version="1.0" encoding="UTF-8"'),
        '00015_html_dtd': dtd('html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'),
        '00020_html': tag(
            'html',
            attributes={
                'version': '-//W3C//DTD XHTML 1.1//EN',
                'xmlns': 'http://www.w3.org/1999/xhtml',
                'xml:lang': 'en',
                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                'xsi:schemaLocation': 'http://www.w3.org/1999/xhtml http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd'
                },
            closed=False,
            module=None,
            uid=None,
            required_css=[],
            required_js=[],
            content={
                '00010_head' : tag(
                   'head',
                   content={
                        '00010_title': tag(
                            'title',
                            content=title
                            ),
                        '00020_description': tag(
                            'meta',
                            closed=True,
                            attributes={
                                'name': 'description',
                                'content':description
                                }
                            ),
                        '00030_keywords': tag(
                            'meta',
                            closed=True,
                            attributes={
                                'name': 'keywords',
                                'content':' '.join(keywords)
                                }
                            ),
                        }
                   ),
                '00020_body': tag(
                    'body',
                    required_js=basic_js,
                    required_css=basic_css,
                    content=content
                    )
                }
            )
        }

def tag(
    name,
    attributes={},
    closed=False,
    module='basic-2e912bf9-c8c1-4dcd-871d-3cd2edc43614',
    uid=None,
    required_css=[],
    required_js=[],
    content=None,
    new_line_before_start=None,
    new_line_before_content=None,
    new_line_after_content=None,
    new_line_after_end=None
    ):
    ret = {
        'type': 'tag',
        'tag_info': {
            'name': name,
            'closed': closed,
            'attributes': attributes
            },
        'module': module,
        'uid': uid,
        'required_css': required_css,
        'required_js': required_js,
        'content': content
        }
    for i in [
        'new_line_before_start',
        'new_line_before_content',
        'new_line_after_content',
        'new_line_after_end'
        ]:
        if eval(i) != None:
            ret[i] = eval(i)

    return ret



class DictatorshipUnitTooDeep(Exception): pass
class MissingDictatorshipUnitAttribute(Exception): pass
class ModulesDirError(Exception): pass

class DictTreeToXMLRenderer:


    def __init__(
        self,
        xml_indent_size=2,
        generate_css=False,
        generate_js=False,
        log_size=100,
        space_before_closing_slash=False,
        css_and_js_holder=None
        ):

        # here linedup modules are listed. key is path
        self.units = {}

        # here will be stored
        self.tree_dict = {}

        # those four attributes are for code formatting
        # purposes
        self.xml_indent_size = xml_indent_size
        self.xml_indent = org.wayround.utils.text.fill(' ', xml_indent_size)

        self.css_and_js_holder = css_and_js_holder

        self.css_placeables = []
        self.js_placeables = []

        self.log = []

        self.log_size = log_size

        self.generate_css = generate_css
        self.generate_js = generate_js
        self.space_before_closing_slash = space_before_closing_slash

        return

    def do_log(self, text):

        log_l = len(self.log)

        if log_l >= self.log_size:
            self.log = self.log[-self.log_size:]

        self.log.append(text)


    def print_log(self):
        for i in self.log:
            print(i)

    def set_tree(self, indict):
        self.tree_dict = indict


    def _lineup_tree(self, indict, already_added, path=[]):

        logging.debug("_lineup_tree path {}".format('/'.join(path)))

        ret = 0

        if not isinstance(indict, (dict, list)):
            raise TypeError("This method accepts only dict or list")


        if self.check_range(indict) != 0:
            self.do_log("_lineup_tree wrong input data at path %(path)s" % {
                'path': '/'.join(path)
                })
            ret = 1
        else:

            index = -1

            if isinstance(indict, dict):
                keys = list(indict.keys())
                keys.sort()
            else:
                keys = indict

            for i in keys:

                index += 1


                if isinstance(indict, dict):
                    unit = indict[i]
                elif isinstance(indict, list):
                    unit = i


                if isinstance(indict, dict):
                    path_name = i
                    #print(1)
                elif isinstance(indict, list):
                    path_name = str(index)
                    #print(2)


                if not id(unit) in already_added:

                    try:
                        tmp = '/'.join(path + [path_name])
                    except:
                        #print("path(" + str(type(path)) + "): " + repr(path))
                        #print("path_name(" + str(type(path_name)) + "): " + repr(path_name))
                        raise

                    if not tmp in self.units:
                        self.units[tmp] = unit

                    del(tmp)

                    already_added.add(id(unit))

                if 'content' in unit:
                    if isinstance(unit['content'], (dict, list)):

                        if self._lineup_tree(
                            unit['content'], already_added, path=path + [path_name]
                            ) != 0:
                            ret = 2

        return ret


    def lineup_tree(self):
        self.units = {}
        already_added = set()
        ret = self._lineup_tree(
            self.tree_dict, already_added, path=[]
            )
        #print(repr(list(self.units.keys())))

        return ret


    def check_tree(self):
        ret = 0

        keys = list(self.units.keys())
        keys.sort()

        for i in keys:
            try:
                self.check_unit(
                    self.units[i], i.split('/')
                    )
            except:
                self.do_log(
                    "-e- Error while checking `%(path)s'\n%(exc_info)s" % {
                        'path': i,
                        'exc_info':
                            org.wayround.utils.error.return_exception_info(
                                sys.exc_info(),
                                tb=True
                                )
                        }
                    )
                ret = 1
                break

        return ret


    def find_required_css_and_js(self):

        self.css_placeables = []
        self.js_placeables = []

        keys = list(self.units.keys())
        keys.sort()


        for i in keys:

            if not self.generate_css and not self.generate_js:
                break

            if not 'module' in self.units[i] \
                or not 'uid' in self.units[i]:
                continue


            if self.generate_css:
                if 'required_css' in self.units[i]:
                    for j in self.units[i]['required_css']:
                        placeable_name = "%(module)s/%(uid)s/%(required)s" % {
                            'module': self.units[i]['module'],
                            'uid': self.units[i]['uid'],
                            'required': j,
                            }
                        if not placeable_name in self.css_placeables:
                            self.css_placeables.append(placeable_name)

            if self.generate_js:
                if 'required_js' in self.units[i]:
                    for j in self.units[i]['required_js']:
                        placeable_name = "%(module)s/%(uid)s/%(required)s" % {
                            'module': self.units[i]['module'],
                            'uid': self.units[i]['uid'],
                            'required': j,
                            }
                        if not placeable_name in self.js_placeables:
                            self.js_placeables.append(placeable_name)

        return


    def css_path_renderer(self, inname):
        module, uid, file = inname.split('/')[0:3]

        return "/css?module=%(module)s&uid=%(uid)s&file=%(file)s" % {
            'module': urllib.parse.quote(module, encoding='utf-8', errors='strict'),
            'uid': urllib.parse.quote(uid, encoding='utf-8', errors='strict'),
            'file': urllib.parse.quote(file, encoding='utf-8', errors='strict')
            }


    def js_path_renderer(self, inname):
        module, uid, file = inname.split('/')[0:3]

        return "/js?module=%(module)s&uid=%(uid)s&file=%(file)s" % {
            'module': urllib.parse.quote(module, encoding='utf-8', errors='strict'),
            'uid': urllib.parse.quote(uid, encoding='utf-8', errors='strict'),
            'file': urllib.parse.quote(file, encoding='utf-8', errors='strict')
            }

    def _place_found_css_or_js(
        self,
        i,
        placement_i,
        typ,
        css_path_renderer=css_path_renderer,
        js_path_renderer=js_path_renderer
        ):

        if not typ in ['css', 'js']:
            raise ValueError("Wrong `typ' parameter value")

        if typ == 'css':
            new_val = tag(
                'style',
                attributes={
                    'type': 'text/css',
                    'src': css_path_renderer(self, i)
                    }
                )

        elif typ == 'js':
            new_val = tag(
                'script',
                attributes={
                    'type': 'text/javascript',
                    'src': js_path_renderer(self, i)
                    }
                )
        else:
            raise Exception("Wrong programming")


        self.check_unit(new_val)

        if isinstance(self.css_and_js_holder['content'], dict):
            org.wayround.utils.dict.append(
                self.css_and_js_holder['content'],
                new_val
                )

        elif isinstance(self.css_and_js_holder['content'], list):
            self.css_and_js_holder['content'].append(new_val)


    def place_found_css_and_js(
        self,
        css_path_renderer=css_path_renderer,
        js_path_renderer=js_path_renderer
        ):

        if not isinstance(self.css_and_js_holder, dict):
            raise ValueError("Wrong self.css_and_js_holder")

        if not isinstance(self.css_and_js_holder['content'], (dict, list)):
            raise TypeError("self.css_and_js_holder['content'] can be only list or dict")

        placement_i = 0

        if self.generate_css:
            for i in self.css_placeables:

                self._place_found_css_or_js(
                    i,
                    placement_i,
                    'css',
                    css_path_renderer=css_path_renderer,
                    js_path_renderer=js_path_renderer
                    )

                placement_i += 1


        if self.generate_js:
            for i in self.js_placeables:

                self._place_found_css_or_js(
                    i,
                    placement_i,
                    'js',
                    css_path_renderer=css_path_renderer,
                    js_path_renderer=js_path_renderer
                    )

                placement_i += 1

        return


    def _render(self, root, indict, path=[]):

        ret = ''

        inaddr_l = len(path)

        indent = org.wayround.utils.text.fill(' ', inaddr_l * self.xml_indent_size)

        index = -1

        if isinstance(indict, dict):
            keys = list(indict.keys())
            keys.sort()
        else:
            keys = indict

        for i in keys:
            index += 1

            if isinstance(indict, dict):
                unit = indict[i]
            elif isinstance(indict, list):
                unit = i
            else:
                raise TypeError("This method accepts only dict or list")


            if isinstance(indict, dict):
                path_name = i
            elif isinstance(indict, list):
                path_name = str(index)

            rendered = ''

            new_line_before_start = ''
            if unit['new_line_before_start']:
                new_line_before_start = '\n%(indent)s' % {
                    'indent': indent
                    }

            new_line_before_content = ''
            if unit['new_line_before_content']:
                new_line_before_content = '\n'

            new_line_after_content = ''
            if unit['new_line_after_content']:
                new_line_after_content = '\n%(indent)s' % {
                    'indent': indent
                    }

            new_line_after_end = ''
            if unit['new_line_after_end']:
                new_line_after_end = '\n'


            start = ''
            content = ''
            end = ''

            if unit['type'] == 'comment':
                start = '<!-- '

                content = str(unit['content'])

                content = content.replace('--', '-')

                end = ' -->'

            elif unit['type'] == 'pi':
                start = '<?'
                content = str(unit['content'])
                end = '?>'

            elif unit['type'] == 'dtd':
                start = '<!DOCTYPE '
                content = str(unit['content'])
                end = '>'

            elif unit['type'] == 'cdata':
                start = '<![CDATA['
                content = str(unit['content']).replace(']]>', '')
                end = ']]>'

            elif unit['type'] == 'char':
                start = ''
                content = xml.sax.saxutils.escape(str(unit['content']))
                end = ''

            elif unit['type'] == 'static':
                start = ''
                content = str(unit['content'])
                end = ''

            elif unit['type'] == 'tag':

                attributes = ''
                if unit['tag_info']['attributes'] != None:
                    attributes = self.render_attributes(
                        unit['tag_info']['attributes'], path,
                        tagname=unit['tag_info']['name']
                        )

                    if not isinstance(attributes, str):
                        ret = 1

                if isinstance(ret, str):

                    closing_slash = ''
                    if unit['tag_info']['closed']:
                        closing_slash = '/'

                    space_before_attributes = ''
                    if attributes != '':
                        space_before_attributes = ' '

                    space_before_closing_slash = ''
                    if closing_slash != '':
                        if self.space_before_closing_slash:
                            space_before_closing_slash = ' '
                        else:
                            space_before_closing_slash = ''

                    start = '<%(tagname)s%(space_before_attributes)s%(attributes)s%(space_before_closing_slash)s%(closing_slash)s>' % {
                        'tagname': unit['tag_info']['name'],
                        'space_before_attributes': space_before_attributes,
                        'attributes': attributes,
                        'space_before_closing_slash': space_before_closing_slash,
                        'closing_slash': closing_slash
                        }

                    if not unit['tag_info']['closed']:

                        if isinstance(unit['content'], str):
                            content = xml.sax.saxutils.escape(unit['content'])
                        elif isinstance(unit['content'], (dict, list)):

                            content = self._render(
                                root, unit['content'], path=path + [path_name]
                                )
                        elif unit['content'] == None:
                            content = ''
                        else:
                            content = str(unit['content'])

                        end = '</%(tagname)s>' % {
                            'tagname': unit['tag_info']['name']
                            }
                    else:
                        content = ''
                        end = ''

            else:
                raise ValueError


            rendered = (""
                + "%(new_line_before_start)s"
                + "%(start)s"
                + "%(new_line_before_content)s"
                + "%(content)s"
                + "%(new_line_after_content)s"
                + "%(end)s"
                + "%(new_line_after_end)s") % {
                'new_line_before_start': new_line_before_start,
                'new_line_before_content': new_line_before_content,
                'new_line_after_content': new_line_after_content,
                'new_line_after_end': new_line_after_end,
                'start': start,
                'content': content,
                'end': end
                }

            ret += rendered

        return ret


    def render(self):

        ret = ''

        if self.lineup_tree() != 0:
            self.do_log("-e- Some errors liningup dict tree")
            ret = 1

        if isinstance(ret, str):
            if self.check_tree() != 0:
                ret = 2

        if isinstance(ret, str):

            if self.css_and_js_holder:
                self.find_required_css_and_js()
                self.place_found_css_and_js()


        if isinstance(ret, str):
            ret = self._render(self.tree_dict, self.tree_dict, path=[])

        return ret

    def render_attributes(self, indict, path=[], tagname=''):
        ret = ''

        inaddr_l = len(path)

        indent = org.wayround.utils.text.fill(' ', inaddr_l * self.xml_indent_size)
        nameindent = org.wayround.utils.text.fill(' ', len(tagname))

        attrs = []

        keys = list(indict.keys())
        keys.sort()

        for i in keys:

            if ret != '':
                ret += ' ';

            value = ''
            if isinstance(indict[i], str):
                value = indict[i]
            else:
                raise ValueError

            if isinstance(ret, str):


                try:
                    attrs.append('%(name)s=%(value)s' % {
                        'name': i,
                        'value': xml.sax.saxutils.quoteattr(value)
                        })
                except:
                    ret = 1
                    break

        if isinstance(ret, str):
            ind_req = False
            for i in attrs:
                if len(i) > 80:
                    ind_req = True
                    break


            first = True

            curr_attr_i = 0
            attrs_l = len(attrs)

            for i in attrs:
                ind = ''
                if ind_req and not first:
                    ind = "\n%(indent)s %(nameindent)s " % {
                        'indent': indent,
                        'nameindent': nameindent
                        }

                ret += "%(ind)s%(new_attr)s" % {
                    'ind': ind,
                    'new_attr': i
                    }

                if curr_attr_i < attrs_l - 1:
                    ret += ' '

                if first:
                    first = False


                curr_attr_i += 1

        return ret

    def check_range(self, indict):
        ret = 0

        if not isinstance(indict, (dict, list)):
            self.do_log("-e- Supplied data is not a dict and not list: {}".format(repr(indict)))
            ret = 1

        else:

            for i in indict:

                if isinstance(indict, dict):
                    value = indict[i]
                elif isinstance(indict, list):
                    value = i
                else:
                    raise TypeError("This method accepts only dict or list")


                if not isinstance(value, dict):
                    self.do_log("-e- Dictatorship `{}' element value is not a dict".format(str(value)))

                    ret = 2
                    break


        return ret

    def check_unit(self, indict, path=[]):

        logging.debug("check_unit path {}".format('/'.join(path)))

        if len(path) >= 255:
            raise DictatorshipUnitTooDeep("Dictatorship tree recursion limit reached `%(path)s'" % {
                    'path': '/'.join(path)
                    })

        # Supplied data defenetly must be a dict or list, othervice - error
        if not isinstance(indict, (dict, list)):
            raise ValueError("Supplied data is not a dict or a list")

        # 'type' must be supplied
        if not 'type' in indict:
            raise MissingDictatorshipUnitAttribute("Dictatorship unit type missing")

        # 'type' must be one of following
        if not indict['type'] in [
            'tag', 'dtd', 'comment', 'cdata', 'static',
            'pi', 'char'
            ]:
            raise ValueError("Wrong dictatorship unit type")

        # If 'type' is 'tag', then check 'tag_info' and everything,
        # what underlie
        if indict['type'] == 'tag':
            if not 'tag_info' in indict \
                or not isinstance(indict['tag_info'], dict):
                raise MissingDictatorshipUnitAttribute(
                    "Dictatorship unit type is `tag', but not `tag_info' supplied"
                    )

            else:
                # tag name MUST be supplied and must be a string!
                if not 'name' in indict['tag_info']:
                    raise MissingDictatorshipUnitAttribute(
                        "`name' not supplied in dictatorship unit `tag_info'"
                        )
                else:
                    if not isinstance(indict['tag_info']['name'], str):
                        raise TypeError("tag `name' must be a string")

                # attributes CAN be supplied or CAN be a None or a dict
                if 'attributes' in indict['tag_info']:
                    if indict['tag_info']['attributes'] == None:
                        indict['tag_info']['attributes'] = {}
                    else:
                        if not isinstance(indict['tag_info']['attributes'], dict):
                            raise TypeError("tag `attributes' must be dict")
                        else:
                            # attribute values can be a strings or callabels
                            for i in indict['tag_info']['attributes']:
                                if not isinstance(indict['tag_info']['attributes'][i], str):
                                    raise TypeError("tag `attributes' dict values must be strings")
                else:
                    indict['tag_info']['attributes'] = {}

                # 'tag_info' 'closed' attribute CAN be supplied and CAN be
                #  None or bool.
                if 'closed' in indict['tag_info']:
                    if not isinstance(indict['tag_info']['closed'], bool):
                        raise TypeError("tag `closed' attribute can be only bool")
                else:
                    indict['tag_info']['closed'] = False



        for i in ['required_css', 'required_js']:
            if i in indict:
                if indict[i] == None:
                    pass
                elif not isinstance(indict[i], list):
                    raise TypeError("`%(i)s' can be list or None" % {
                        'i': i
                        })
                else:
                    for j in indict[i]:
                        if not isinstance(j, str):
                            raise TypeError("All `%(i)s' values must be strings" % {
                                'i': i
                                })

            else:
                indict[i] = None


        for i in ['module', 'uid']:
            if i in indict:
                if indict[i] != None:
                    if isinstance(indict[i], str):
                        if not re.match(r'[a-zA-Z][\w-]*', indict[i]):
                            raise ValueError("Wrong `%(i)s' value at `%(path)s'" % {
                                'path': '/'.join(path),
                                'i': i
                                })
                    else:
                        raise ValueError("`{}' can be None or str".format(i))

            else:
                if ('required_css' in indict) and (indict['required_css'] != None) \
                    or ('required_js' in indict) and (indict['required_js'] != None):
                    raise MissingDictatorshipUnitAttribute(
                        "`%(i)s' required to be in unit!" % {
                            'i': i
                            }
                        )

        if not 'content' in indict:
            indict['content'] = ''
        elif indict['content'] == None:
            indict['content'] = ''
        elif isinstance(indict['content'], str):
            pass
        elif isinstance(indict['content'], dict):
            pass
        elif isinstance(indict['content'], list):
            pass
        else:
            raise ValueError("wrong unit content value")


        default_new_line_before_start = False
        default_new_line_before_content = False
        default_new_line_after_content = False
        default_new_line_after_end = False

        if indict['type'] == 'tag':
            default_new_line_before_start = True
            if indict['tag_info']['closed']:
                default_new_line_after_content = False
            else:
                if isinstance(indict['content'], (dict, list)):
                    default_new_line_after_content = True

        elif indict['type'] in ['tag', 'comment', 'dtd', 'pi']:
            default_new_line_after_end = True


        for i in [
            ('new_line_before_start', default_new_line_before_start),
            ('new_line_before_content', default_new_line_before_content),
            ('new_line_after_content', default_new_line_after_content),
            ('new_line_after_end', default_new_line_after_end)
            ]:
            if i[0] in indict:
                if not isinstance(indict[i[0]], bool):
                    raise TypeError("-e- wrong `%(name)s' value type" % {
                        'name': i[0]
                        })
            else:
                indict[i[0]] = i[1]

        return


def test():
    # Upper dict element with names (like folloving) is called
    # `dictatorship range'.
    # Dictatorship range's keys must point only on dict-s,
    # othervice it is an error.

    logging.basicConfig(level='DEBUG')

    a = {
        '000_xml_pi': {
            'type': 'pi',
            'content': 'xml version="1.1" encoding="UTF-8"',
            },
        '010_xhtml_doctype': {
            'type': 'dtd',
            'content': 'html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"'
            },
        '100_html_tag': {
            # Dictatorship gange pointet dicts (like this)
            # is called `dictatorship unit'

            # Any dict can be one of folloving types:
            # 'tag', 'dtd', 'comment', 'cdata', 'static', 'char'
            # 'pi' (Processing instructions).
            # If type is 'tag',then 'tag_info' subdict is required
            'type': 'tag',

            # inserts new lines
            # 'new_line_before_start': False,
            # 'new_line_before_content': False,
            # 'new_line_after_content': False,
            # 'new_line_after_end': False,

            # 'tag_info' required to present if type is 'tag'.
            # 'tag_info' must be a dict.
            'tag_info': {
                # any valid tag name
                'name': 'html',

                # None or dict
                # dict values must be strings 
                'attributes': {
                    'version': '-//W3C//DTD XHTML 1.1//EN',
                    'xmlns': 'http://www.w3.org/1999/xhtml',
                    'xml:lang': 'en',
                    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                    'xsi:schemaLocation': 'http://www.w3.org/1999/xhtml http://www.w3.org/MarkUp/SCHEMA/xhtml11.xsd'
                    },

                # (bool) if True - no contents is
                # passible and any info supplied in 'contents'
                # will be omited. Default is False.
                'closed': False
                },

            # str, dict, None, callable
            # None - exchenged to empty string
            # string - used as is
            # dict - assumed tobe new
            # `dictatorship range'
            # callable - must return string
            'content': {
                '10_head': {
                    'type': 'tag',
                    'tag_info': {
                        'name': 'head'
                        },
                    'content': {
                        'title': {
                            'type': 'tag',
                            'tag_info': {
                                'name': 'title'
                                },
                            'content': 'Page Title'
                            }
                        }
                    },
                '20_body': {
                    'type': 'tag',
                    'tag_info': {
                        'name': 'body'
                        },
                    'module': 'core',
                    'uid': 'body',
                    'required_css': ['main.css', 'body.css'],
                    'required_js': ['main.js'],
                    }
                }

            }
        }

    print("Dictator test #1")
    b = DictTreeToXMLRenderer(2, True, True)
    b.set_tree(a)
    ret = b.render()
    print(repr(b.units))
    b.print_log()
    print(ret)
    return

def test2():
    logging.basicConfig(level='DEBUG')
    print("Dictator test #2")
    b = DictTreeToXMLRenderer(2, True, True)
    b.set_tree(html())
    ret = b.render()
    print(repr(b.units))
    b.print_log()
    print(ret)
