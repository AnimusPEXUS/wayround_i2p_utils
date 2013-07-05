
import logging
import re

import org.wayround.utils.path

def _wrong_data_msg(mute_errors, filename, line_no, text='Wrong data'):
    if not mute_errors:
        logging.error(
            "{}: {} ({})".format(
                text,
                filename,
                line_no
                )
            )

def read_wavefront_obj_file(filename, mute_errors=False):

    filename = org.wayround.utils.path.abspath(filename)

    try:
        f = open(filename, 'r')
    except:
        ret = 1
        raise
    else:

        text = f.read()

        f.close()

        ret = parse_wavefront_obj_text(text, mute_errors, filename=filename)

    return ret

def parse_wavefront_obj_text(text, mute_errors=False, filename=None):

    ret = 0

    data = []

    lines = text.splitlines()

    lines_i = 0

    current_line = ''
    assembling_line = ''
    working_line = ''
    assembling = False

    for current_line in lines:

        lines_i += 1

        if not current_line.startswith('#'):
            assembling = current_line.endswith('\\')

        if assembling:

            if (current_line.startswith('#')
                or current_line == ''
                or current_line.isspace()):

                _wrong_data_msg(
                    mute_errors,
                    filename,
                    lines_i,
                    text="Invalid line translation"
                    )
                assembling = False
                assembling_line = ''
                working_line = ''
                ret = 5
            else:

                assembling_line += current_line[:-1]

        else:

            assembling = False
            assembling_line += current_line
            working_line = assembling_line
            assembling_line = ''


        if (
            not assembling
            and not working_line == ''
            and not working_line.isspace()
            and not working_line.startswith('#')
            ):

#            print("Worl: '{}'".format(working_line))

            line_splitted = working_line.split()


            func = line_splitted[0]
            data = line_splitted[1:]
            datal = len(data)

#            print("data: {}".format(data))

            res = None

            func_found = False
            for func_data in [
                ('v', 3, 4,),
                ('vp', 2, 3,),
                ('vn', 3, 3,),
                ('vt', 1, 3,),
                ('cstype', 1, 2,),
                ('deg', 2, 2,),
                ('bmat', None, None,),
                ('step', 2, 2,),
                ('p', None, None,),
                ('l', None, None,),
                ('f', None, None,),
                ('curv', None, None,),
                ('curv2', None, None,),
                ('surf', None, None,),
                ]:

                if func == func_data[0]:

                    func_found = True

                    if ((func_data[1] and func_data[2])
                        and (datal < func_data[1] or datal > func_data[2])):
                            _wrong_data_msg(mute_errors, filename, lines_i)
                            ret = 2

                    else:
                        try:
                            res = eval('{}(*data)'.format(func_data[0]))
                        except:
                            _wrong_data_msg(mute_errors, filename, lines_i)
                            ret = 6
                            res = None
                        else:
                            if not isinstance(res, dict):
                                _wrong_data_msg(mute_errors, filename, lines_i)
                                ret = 7
                                res = None


            if not func_found:
                _wrong_data_msg(
                    mute_errors,
                    filename,
                    lines_i,
                    text='Unsupported command ({})'.format(func)
                    )
                ret = 3

            if res != None:
                data.append(res)

    if ret == 0:
        ret = data

    return ret


def parse_vertex_sequence(in_str):

    str_values = in_str.split('/')

    values = []

    for i in str_values:
        values.append(float(i.strip()))

    return values

def v(x, y, z, w=1.0):
    return dict(
        function='v',
        values=[
            float(x),
            float(y),
            float(z),
            float(w)
            ]
        )

def vp(u, v, w=1.0):
    return dict(
        function='vp',
        values=[
            float(u),
            float(v),
            float(w)
            ]
        )

def vn(i, j, k):
    return dict(
        function='vn',
        values=[
            float(i),
            float(j),
            float(k)
            ]
        )

def vt(u, v=0, w=0):
    return dict(
        function='vt',
        values=[
            float(u),
            float(v),
            float(w)
            ]
        )


def cstype(*args):
    """
    Two arguments are allowed, first of which are optional

    rat = False
    typ - string
    """

    rat = False
    typ = None

    argsl = len(args)

    if argsl == 1:
        typ = args[0]
    elif argsl == 2:
        rat = bool(args[0])
        typ = args[1]
    else:
        raise ValueError

    if not typ in [
        'bmatrix',
        'bezier',
        'bspline',
        'cardinal',
        'taylor'
        ]:
        raise ValueError("invalid `typ' value")


    return dict(
        function='cstype',
        values=[
            rat,
            typ
            ]
        )

def deg(degu, degv):
    return dict(
        function='deg',
        values=[
            float(degu),
            float(degv)
            ]
        )

def bmat(*args):
    """
    1 or more parameters supported

    typ - 'u' or 'v'
    """

    if len(args) < 1:
        raise ValueError("wrong parameters")

    typ = args[0]

    if not typ in ['u', 'v']:
        raise ValueError("wrong parameters")

    ret = dict(
        function='bmat',
        values=[
            typ,
            args[1:]
            ]
        )

    return ret


def step(stepu, stepv):
    return dict(
        function='step',
        values=[
            float(stepu),
            float(stepv)
            ]
        )

def p(*args):

    values = []
    for i in args:
        values.append(float(i))

    return dict(
        function='p',
        values=values
        )

def l(*args):

    values = []
    for i in args:
        values.append(parse_vertex_sequence(i))

    # TODO: add correctness checks

    return dict(
        function='l',
        values=values
        )

def f(*args):

    values = []
    for i in args:
        values.append(parse_vertex_sequence(i))

    # TODO: add correctness checks

    return dict(
        function='l',
        values=values
        )

def curv(*args):

    ret = 0

    values = []

    args_l = len(args)

    if args_l < 4:
        ret = 1

    else:

        for i in range(2):
            values.append(float(args[i]))

        for i in range(2, args_l):
            values.append(int(args[i]))

        ret = dict(
            function='curv',
            values=values
            )

    return ret

def curv2(*args):

    ret = 0

    values = []

    args_l = len(args)

    if args_l < 2:
        ret = 1

    else:

        for i in range(args_l):
            values.append(int(args[i]))

        ret = dict(
            function='curv2',
            values=values
            )

    return ret


def surf(*args):

    ret = 0

    values = []

    args_l = len(args)

    if args_l < 4:
        ret = 1

    else:

        for i in range(4):
            values.append(float(args[i]))

        for i in range(4, args_l):
            values.append(parse_vertex_sequence(args[i]))

        ret = dict(
            function='surf',
            values=values
            )

    return ret

def parm(*args):

    ret = 0

    values = []

    args_l = len(args)

    if args_l < 3:
        ret = 1

    if ret == 0:
        if not args[1] in ['u', 'v']:
            ret = 2

    if ret == 0:

        for i in range(args_l):
            values.append(float(args[i]))

        ret = dict(
            function='parm',
            values=values
            )

    return ret

def _op_x1(args, mode='trim'):

    ret = 0

    if not mode in ['trim', 'hole', 'scrv']:
        ret = 4

    if ret == 0:

        values = []

        args_l = len(args)

        if args_l < 1:
            ret = 1

        if ret == 0:
            if (args_l % 3) != 0:
                ret = 2

        if ret == 0:

            for i in range(0, args_l, 3):
                values += [
                    float(args[i]),
                    float(args[i + 1]),
                    int(args[i + 2])
                    ]

            ret = dict(
                function=mode,
                values=values
                )

    return ret

def trim(*args):
    return _op_x1(args, mode='trim')

def hole(*args):
    return _op_x1(args, mode='hole')

def scrv(*args):
    return _op_x1(args, mode='scrv')

def sp(*args):

    ret = 0

    values = []

    args_l = len(args)

    if args_l < 1:
        ret = 1

    else:

        for i in range(args_l):
            values.append(int(args[i]))

        ret = dict(
            function='sp',
            values=values
            )

    return ret

def end():
    return dict(
        function='end',
        values=[]
        )

def con(
    surf_1, q0_1, q1_1, curv2d_1,
    surf_2, q0_2, q1_2, curv2d_2
    ):
    values = [
        int(surf_1),
        float(q0_1),
        float(q1_1),
        int(curv2d_1),
        int(surf_2),
        float(q0_2),
        float(q1_2),
        int(curv2d_2)
        ]

    return dict(
        function='con',
        values=values
        )

def _g_name_check(name):

    ret = 0

    if not re.match(r'^[a-zA-Z0-9]+$', name):
        ret = 1

    return ret


def g(*args):

    ret = 0

    args_l = len(args)

    if args_l < 1:
        ret = 1

    if ret == 0:

        values = []

        for i in args:
            if _g_name_check(i) != 0:
                ret = 2
                break
            else:
                values.append(i)

        if ret == 0:
            ret = dict(
                function='g',
                values=values
                )

    return ret

def s(value):

    ret = 0

    if not value in ['on', 'off'] or not re.match(r'^\d+$', value):
        ret = 1

    if ret == 0:

        if value.isdigit():
            if int(value) > 0:
                value = 'on'
            else:
                value = 'off'

        ret = dict(
            function='s',
            values=[value]
            )

    return ret

def mg(group_number, res='1'):

    values = [
        int(group_number),
        float(res)
        ]

    return dict(
        function='mg',
        values=values
        )

def o(object_name):

    values = [
        object_name
        ]

    return dict(
        function='o',
        values=values
        )

def _op_x2(value, mode='bevel'):

    ret = 0

    if not mode in ['bevel', 'c_interp', 'd_interp']:
        ret = 4

    if ret == 0:
        if not value in ['on', 'off']:
            ret = 1

    if ret == 0:
        value = value == 'on'

        ret = dict(
            function=mode,
            values=[value]
            )

    return ret

def bevel(value):
    return _op_x2(value, mode='bevel')

def c_interp(value):
    return _op_x2(value, mode='c_interp')

def d_interp(value):
    return _op_x2(value, mode='d_interp')

def lod(level):

    ret = 0

    level = int(level)

    if level < 0 or level > 100:
        ret = 1

    if ret == 0:
        ret = dict(function='level', values=[level])

    return ret

def maplib(*filenames):
    values = filenames
    return dict(
        function='maplib',
        values=values
        )

def usemap(map_name='off'):
    return dict(function='usemap', values=[map_name])

def usemtl(material_name=None):
    values = []
    if material_name:
        values.append(material_name)
    return dict(function='usemtl', values=values)

def mtllib(*filenames):
    values = filenames
    return dict(
        function='mtllib',
        values=values
        )

def shadow_obj(filename):
    return dict(
        function='shadow_obj',
        values=[filename]
        )

def trace_obj(filename):
    return dict(
        function='trace_obj',
        values=[filename]
        )

def ctech(*args):

    ret = 0

    values = []

    args_l = len(args)

    technique = None

    if args_l < 1:
        ret = 2

    else:

        technique = args[0]

        if not technique in ['cparm', 'cspace', 'curv']:
            ret = 3

        else:

            if technique in ['cparm', 'cspace']:

                if args_l != 2:
                    ret = 4

                else:
                    values = [args[1]]

            elif technique == 'curv':

                if args_l != 3:
                    ret = 4

                else:
                    values = args[1:2]

            else:
                raise Exception("Programming error")

            if ret == 0:

                ret = dict(
                    function=ctech,
                    values=values
                    )

    return ret

def stech(*args):

    ret = 0

    values = []

    args_l = len(args)

    technique = None

    if args_l < 1:
        ret = 2

    else:

        technique = args[0]

        if not technique in ['cparma', 'cparmb', 'cspace', 'curv']:
            ret = 3

        else:

            if technique in ['cparma', 'curv']:

                if args_l != 3:
                    ret = 4

                else:
                    values = args[1:2]

            elif technique in ['cparmb', 'cspace']:

                if args_l != 2:
                    ret = 4

                else:
                    values = [args[1]]

            else:
                raise Exception("Programming error")

            if ret == 0:

                ret = dict(
                    function=ctech,
                    values=values
                    )

    return ret

def _op_x3(args, mode='bsp'):

    ret = 0

    if not mode in ['bsp', 'bzp', 'cdp']:
        ret = 1
    else:

        args_l = len(args)

        if args_l != 16:
            ret = 2

        else:

            values = []

            for i in args:
                values.append(int(i))

            ret = dict(
                function=mode,
                values=values
                )

    return ret

def bsp(*args):
    return _op_x3(args, mode='bsp')

def bzp(*args):
    return _op_x3(args, mode='bzp')

def cdc(*args):

    values = []

    for i in args:
        values.append(int(i))

    return dict(
        function='cdc',
        values=values
        )

def cdp(*args):
    return _op_x3(args, mode='cdp')
