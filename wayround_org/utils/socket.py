
import select
import ssl


def nb_recv(sock, bs=4096, stop_event=None, select_timeout=0.5):

    data = b''

    while True:

        if stop_event is not None and stop_event.is_set():
            break

        try:
            data = sock.recv(bs)
        except BlockingIOError:
            select.select([sock], [], [], select_timeout)
            # pass
        except ssl.SSLWantReadError:
            select.select([sock], [], [], select_timeout)
            # pass
        except ssl.SSLWantWriteError:
            select.select([], [sock], [], select_timeout)
            # pass
        else:
            # print('nb_recv, data (else): {}'.format(data))
            break

    # print('nb_recv, data: {}'.format(data))

    return data


def nb_sendall(sock, data, stop_event=None, bs=4096, select_timeout=0.5):
    
    print('nb_sendall, data: {}'.format(data))

    if type(data) != bytes:
        raise TypeError("`data' must be bytes")

    while True:

        try:
            sock.sendall(data)
        except BlockingIOError:
            select.select([], [sock], [], select_timeout)
        except ssl.SSLWantReadError:
            select.select([sock], [], [], select_timeout)
        except ssl.SSLWantWriteError:
            select.select([], [sock], [], select_timeout)
        else:
            break

        if stop_event is not None and stop_event.is_set():
            break

    return
