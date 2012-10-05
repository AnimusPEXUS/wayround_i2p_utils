
import os.path
import subprocess
import logging
import sys
import io

import org.wayround.utils.stream


def simple_exec(
    program,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    options=[],
    bufsize=(2 * 1024 ** 2),
    cwd=None
    ):

    p = None

    try:
        p = subprocess.Popen(
            [program] + options,
            stdin=stdin, stdout=stdout, stderr=stderr,
            bufsize=bufsize,
            cwd=cwd
            )
    except:
        logging.exception("Error starting `{}' subprocess".format(program))
        p = None
        raise

    return p


def pipe_subprocesses(processes_list,
                      processes_names,
                      bufsize=(2 * 1024 ** 2),
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

    txt = io.BytesIO()
    txt.write(text)
    txt.seek(0)

    xz1 = simple_exec(
        'xz',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    xz2 = simple_exec(
        'xz',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-d'],
        bufsize=0
        )

    xz3 = simple_exec(
        'xz',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    xz4 = simple_exec(
        'xz',
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

    bzip21 = simple_exec(
        'bzip2',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    bzip22 = simple_exec(
        'bzip2',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-d'],
        bufsize=0
        )

    bzip23 = simple_exec(
        'bzip2',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        options=['-9'],
        bufsize=0
        )

    bzip24 = simple_exec(
        'bzip2',
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


def process_stream(
    program,
    stdin,
    stdout,
    stderr,
    options=[],
    proc_bufsize=0,
    cat_bufsize=(2 * 1024 ** 2),
    cwd=None,
    verbose=False
    ):
    """
    Starts `program' and uses it to process stdin to stdout

    Streams are workedout using own-fashioned threading mechanisms
    """

    ret = 0

    try:
        proc = simple_exec(
            program,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=stderr,
            options=options,
            bufsize=proc_bufsize,
            cwd=cwd
            )
    except:
        logging.exception("Error starting process `{}'".format(program))
        ret = 1
    else:

        try:
            thread_name = ''

            if verbose:
                thread_name = 'in >> {}'.format(proc.pid)
            else:
                thread_name = 'Thread'

            cat1 = org.wayround.utils.stream.cat(
                stdin,
                proc.stdin,
                threaded=True,
                close_output_on_eof=True,
                bs=cat_bufsize,
                thread_name=thread_name
                )

            if verbose:
                thread_name = '{} >> out'.format(proc.pid)
            else:
                thread_name = 'Thread'

            cat2 = org.wayround.utils.stream.cat(
                proc.stdout,
                stdout,
                threaded=True,
                close_output_on_eof=False,
                bs=cat_bufsize,
                thread_name=thread_name
                )

            cat1.start()
            cat2.start()

            proc.wait()

            cat1.join()
            cat2.join()
        finally:
            if proc.returncode == None:
                proc.terminate()

    return ret


def process_file(
    program,
    infile,
    outfile,
    stderr,
    options=[],
    proc_bufsize=0,
    cat_bufsize=(2 * 1024 ** 2),
    cwd=None,
    verbose=False
    ):

    ret = 0

    if not os.path.isfile(infile):
        logging.error("Input file not exists: {}".format(infile))
        ret = 1
    else:
        try:
            fi = open(infile, 'rb')
        except:
            logging.exception("Can't open file `{}'".format(infile))
        else:

            try:
                fo = open(outfile, 'wb')
            except:
                logging.exception("Can't rewrite file `{}'".format(outfile))
            else:

                try:
                    options = []

                    if process_stream(
                        program,
                        fi,
                        fo,
                        stderr=stderr,
                        options=options,
                        proc_bufsize=proc_bufsize,
                        cat_bufsize=cat_bufsize,
                        cwd=cwd,
                        verbose=verbose
                        ) != 0:
                        logging.error(
                            "Error processing file {in} to {out} through {proc}".format_map(
                                {
                                 'in': infile,
                                 'out': outfile,
                                 'proc': program
                                 }
                                )
                            )
                        ret = 2
                finally:
                    fo.close()

            finally:
                fi.close()

    return ret
