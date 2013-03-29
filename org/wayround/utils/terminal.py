
import sys
import struct
import termios
import fcntl
import pprint

import org.wayround.utils.error

def get_terminal_size(fd=1):
    res = None
    io_res = None
    arg = struct.pack('HHHH', 0, 0, 0, 0)

    try:
        io_res = fcntl.ioctl(
            fd,
            termios.TIOCGWINSZ,
            arg
            )
    except:
        res = None
    else:
        try:
            res = struct.unpack('HHHH', io_res)
        except:
            res = None

    if res != None:
        res = {
            'ws_row': res[0],
            'ws_col': res[1],
            'ws_xpixel': res[2],
            'ws_ypixel': res[3]
            }

    return res

def prompt(g=None, l=None, prompt='-> '):

    import readline

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
            print(
                org.wayround.utils.error.return_exception_info(
                    sys.exc_info(),
                    tb=True
                    )
                )

    print('')
