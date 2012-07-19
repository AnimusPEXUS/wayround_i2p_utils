
import subprocess
import logging
import sys
import io

import org.wayround.utils.stream
import org.wayround.utils.xz
import org.wayround.utils.bzip2


def pipe_subprocesses(processes_list,
                      processes_names,
                      bufsize=2 * 1024 ** 2,
                      verbose=False
                      ):

    if not isinstance(processes_list, list):
        raise ValueError("processes_list must be a list")

    for i in processes_list:
        if not isinstance(i, subprocess.Popen):
            raise ValueError("processes_list must be a list of Popen objects")

    if not isinstance(processes_names, list):
        raise ValueError("processes_names must be a list")

    for i in processes_names:
        if not isinstance(i, str):
            raise ValueError("processes_list must be a list of strings")

    if len(processes_list) != len(processes_names):
        raise ValueError("len(processes_list) != len(processes_names)")

    count = len(processes_list)
    cats = []
    for i in range(count - 1):

        if verbose:
            thread_name = "{} >> {}".format(processes_names[i], processes_names[i + 1])
        else:
            thread_name = 'Thread'

        logging.debug("Creating thread `{}'".format(thread_name))

        cats.append(
            org.wayround.utils.stream.cat(
                processes_list[i].stdout,
                processes_list[i + 1].stdin,
                threaded=True,
                close_output_on_eof=True,
                bs=bufsize,
                thread_name=thread_name
                )
            )

    for i in cats:
        i.start()

    for i in range(count - 1):
        cats[i].join()
        processes_list[i].wait()

    #    for i in processes_list:
    #        i.wait()
    #
    #    for i in cats:
    #        i.join()

    processes_list[-1].wait()

    return

def test_pipes():

    for i in [
        (logging.CRITICAL, '-c-'),
        (logging.ERROR   , '-e-'),
        (logging.WARN    , '-w-'),
        (logging.WARNING , '-w-'),
        (logging.INFO    , '-i-'),
        (logging.DEBUG   , '-d-')
        ]:
        logging.addLevelName(i[0], i[1])

    logging.basicConfig(level='DEBUG')

    f = open('/proc/cpuinfo', 'rb')
    text = f.read()
    f.close()

    # =========== xz based testing ===========    

    txt = None
    txt = io.BytesIO()
    txt.write(text)
    txt.seek(0)

    xz1 = org.wayround.utils.xz.xz(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    xz2 = org.wayround.utils.xz.xz(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-d'],
        bufsize=0
        )

    xz3 = org.wayround.utils.xz.xz(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    xz4 = org.wayround.utils.xz.xz(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-d'],
        bufsize=0
        )

    cat1 = org.wayround.utils.stream.cat(
        txt,
        xz1.stdin,
        threaded=True,
        close_output_on_eof=True,
        bs=200,
        thread_name="File >> xz1"
        )

    cat2 = org.wayround.utils.stream.cat(
        xz4.stdout,
        sys.stdout,
        threaded=True,
        close_output_on_eof=False,
        convert_to_str='utf-8',
        bs=200,
        thread_name="xz4 >> STDOUT"
        )

    cat1.start()
    cat2.start()

    pipe_subprocesses(
        [xz1, xz2, xz3, xz4],
        ['xz1', 'xz2', 'xz3', 'xz4'],
        bufsize=2 * 1024 ** 2,
        verbose=True
        )

    cat1.join()
    cat2.join()

    # =========== bzip2 based testing ===========    

#    txt = None
#    txt = io.BytesIO()
#    txt.write(text)
    txt.seek(0)

    bzip21 = org.wayround.utils.bzip2.bzip2(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    bzip22 = org.wayround.utils.bzip2.bzip2(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-d'],
        bufsize=0
        )

    bzip23 = org.wayround.utils.bzip2.bzip2(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    bzip24 = org.wayround.utils.bzip2.bzip2(
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-d'],
        bufsize=0
        )

    cat1 = org.wayround.utils.stream.cat(
        txt,
        bzip21.stdin,
        threaded=True,
        close_output_on_eof=True,
        bs=200,
        thread_name="File >> bzip2_1"
        )

    cat2 = org.wayround.utils.stream.cat(
        bzip24.stdout,
        sys.stdout,
        threaded=True,
        close_output_on_eof=False,
        convert_to_str='utf-8',
        bs=200,
        thread_name="bzip2_4 >> STDOUT"
        )

    cat1.start()
    cat2.start()

    pipe_subprocesses(
        [bzip21, bzip22, bzip23, bzip24],
        ['bzip2_1', 'bzip2_2', 'bzip2_3', 'bzip2_4'],
        bufsize=2 * 1024 ** 2,
        verbose=True
        )

    cat1.join()
    cat2.join()

    txt.close()
