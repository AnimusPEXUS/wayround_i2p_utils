
import logging

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
                ('v', 3, 4),
                ('vp', 2, 3),
                ('vn', 3, 3),
                ('vt', 1, 3),
                ('ctype', 1, 2),
                ('deg', 2, 2),
                ('bmat', None, None)
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


def ctype(*args):
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
        function='ctype',
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

# TODO: completion required
