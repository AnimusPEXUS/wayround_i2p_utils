import struct
import termios
import fcntl

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
