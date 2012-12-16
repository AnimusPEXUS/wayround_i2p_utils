
import readline
import sys
import traceback
import pprint

def return_exception_info(e, tb=False):
    txt = """
EXCEPTION: {type}
    VALUE: {val}
""".format(
        type=repr(e[0].__name__),
        val=repr(e[1])
        )

    if tb:
        txt += """
TRACEBACK:
{tb}
{feo}
    """.format(
            tb=''.join(traceback.format_list(traceback.extract_tb(e[2]))),
            feo=''.join(traceback.format_exception_only(e[0], e[1]))
            )

    return txt


def print_exception_info(e):
    txt = return_exception_info(e)
    print(txt)
    return

def control(g=None, l=None, prompt='-> '):
    bk = False

    while not bk:

        try:
            cmd = input(prompt)
            try:
                e = eval(cmd, g, l)
                if isinstance(e, dict):
                    pprint.pprint(e, indent=2)
                else:
                    print(repr(e))
            except SyntaxError:
                exec(cmd, g, l)

        except EOFError:
            bk = True
        except:
            print(return_exception_info(sys.exc_info(), tb=True))

    print('')
