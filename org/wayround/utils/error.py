
import traceback

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

