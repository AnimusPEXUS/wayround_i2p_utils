
import io
import logging
import os.path
import subprocess
import sys
import threading
import time

import org.wayround.utils.stream


def simple_exec(
    program,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=None,
    options=None,
    bufsize=(2 * 1024 ** 2),
    cwd=None
    ):

    if options == None:
        options = []

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
            thread_name = "{} >> {}".format(
                processes_names[i],
                processes_names[i + 1]
                )
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

    processes_list[-1].wait()

    return


def test_pipes():

    for i in [
        (logging.CRITICAL, '-c-'),
        (logging.ERROR, '-e-'),
        (logging.WARN, '-w-'),
        (logging.WARNING, '-w-'),
        (logging.INFO, '-i-'),
        (logging.DEBUG, '-d-')
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


class ProcessStream:

    def __init__(self):

        self.clear(init=True)

    def __del__(self):
        self.stop()

    def clear(self, init=False):

        ret = 0

        if not init and self.stat() != 'stopped':
            logging.error(
                "Program settings can not be cleaned while it is working"
                )

            ret = 1
        else:

            if not init:
                self.stop()

            self.program = None
            self.stdin = None
            self.stdout = None
            self.stderr = None
            self.options = None
            self.proc_bufsize = None
            self.cat_bufsize = None
            self.cwd = None
            self.verbose = None
            self.close_output_on_eof = None
            self.flush_on_input_eof = None

            self.proc = None

            self.in_cat = None
            self.out_cat = None

            if not init:
                if self.stop_flag:
                    self.stop_flag.set()

            self.stop_flag = threading.Event()

            if init:
                self.returncode = None

        return ret

    def setValues(
        self,
        program,
        stdin,
        stdout,
        stderr,
        options=None,
        proc_bufsize=0,
        cat_bufsize=(2 * 1024 ** 2),
        cwd=None,
        verbose=False,
        close_output_on_eof=False,
        flush_on_input_eof=False
        ):

        if options == None:
            options = []

        ret = 0

        if self.stat() != 'stopped':
            logging.error(
                "Program settings can not be changed while it is working"
                )

            ret = 1

        else:

            self.program = program
            self.stdin = stdin
            self.stdout = stdout
            self.stderr = stderr
            self.options = options
            self.proc_bufsize = proc_bufsize
            self.cat_bufsize = cat_bufsize
            self.cwd = cwd
            self.verbose = verbose
            self.close_output_on_eof = close_output_on_eof
            self.flush_on_input_eof = flush_on_input_eof

        return ret

    def start(self):

        ret = 0

        if self.stat() != 'stopped':
            logging.error(
                "Program can not be started if it's already working"
                )

            ret = 1

        if ret == 0:

            try:
                self.proc = simple_exec(
                    self.program,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=self.stderr,
                    options=self.options,
                    bufsize=self.proc_bufsize,
                    cwd=self.cwd
                    )
            except:
                logging.exception(
                    "Error starting process `{}'".format(self.program)
                    )
                ret = 2

        if ret == 0:
            try:
                threading.Thread(
                    name="Thread Waiting for program `{}' exit".format(
                        self.program
                        ),
                    target=self._proc_waiter
                    ).start()
            except:
                logging.exception("Error starting thread")
                ret = 3

        if ret == 0:

            try:
                thread_name = ''

                if self.verbose:
                    thread_name = 'in >> {}'.format(self.proc.pid)
                else:
                    thread_name = 'Thread'

                # TODO: add error handlers

                self.in_cat = org.wayround.utils.stream.cat(
                    self.stdin,
                    self.proc.stdin,
                    threaded=True,
                    flush_on_input_eof=True,
                    close_output_on_eof=True,
                    bs=self.cat_bufsize,
                    thread_name=thread_name,
                    verbose=self.verbose,
                    termination_event=self.stop_flag,
                    on_exit_callback=self._close_in_cat,
                    on_input_read_error=None,
                    on_output_write_error=None
                    )

                if self.verbose:
                    thread_name = '{} >> out'.format(self.proc.pid)
                else:
                    thread_name = 'Thread'

                self.out_cat = org.wayround.utils.stream.cat(
                    self.proc.stdout,
                    self.stdout,
                    threaded=True,
                    flush_on_input_eof=self.flush_on_input_eof,
                    close_output_on_eof=self.close_output_on_eof,
                    bs=self.cat_bufsize,
                    thread_name=thread_name,
                    verbose=self.verbose,
                    termination_event=self.stop_flag,
                    on_exit_callback=self._close_out_cat,
                    on_input_read_error=None,
                    on_output_write_error=None
                    )

                self.in_cat.start()
                self.out_cat.start()

            except:
                logging.exception(
                    "Some exception while starting cat threads"
                    )
                ret = 4

        if ret == 0:
            self.wait('working')
        else:
            self.stop()

        return ret

    def stop(self):

        logging.debug("Signaled stop for `{}'".format(self.program))

        if self.stat() != 'stopped':

            self.stop_flag.set()

            if self.in_cat:
                self.in_cat.join()

            if self.out_cat:
                self.out_cat.join()

            self.wait('stopped')

            self.clear()

        return

    def stat(self):

        ret = 'unknown'

        if (self.in_cat
            and self.out_cat
            and self.proc != None):
            ret = 'working'

        if (not self.in_cat
            and not self.out_cat
            and self.proc == None):
            ret = 'stopped'

        logging.debug("""\
status (for `{}'):
self.in_cat     {}
self.out_cat    {}
self.proc       {}
{}
""".format(self.program, self.in_cat, self.out_cat, self.proc, ret))

        return ret

    def wait(self, what='stopped'):

        # TODO: add timeout

        if not what in ['stopped', 'working']:
            raise ValueError("wrong `what' value")

        while True:

            logging.debug("Waiting for status `{}'".format(what))

            if self.stat() == what:
                break

            if self.stat() == 'stopped':
                if self.stop_flag.is_set():
                    break

            time.sleep(0.2)

        return self.returncode

    def _close_in_cat(self):
        self.in_cat.join()
        self.in_cat = None
        return

    def _close_out_cat(self):
        self.out_cat.join()
        self.out_cat = None
        return

    def _proc_waiter(self):

        #        if self.proc.returncode == None:
        #            self.wait('working')

        while True:

            self.proc.poll()

            if isinstance(self.proc.returncode, int):
                self.returncode = self.proc.returncode
                break

            time.sleep(0.2)

        self.proc = None
        self.stop()

        return


def process_stream(
    program,
    stdin,
    stdout,
    stderr,
    options=None,
    proc_bufsize=(2 * 1024 ** 2),
    cat_bufsize=(2 * 1024 ** 2),
    cwd=None,
    verbose=False,
    close_output_on_eof=False,
    flush_on_input_eof=False
    ):

    if options == None:
        options = []

    ps = ProcessStream()

    ps.setValues(
        program=program,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        options=options,
        proc_bufsize=proc_bufsize,
        cat_bufsize=cat_bufsize,
        cwd=cwd,
        verbose=verbose,
        close_output_on_eof=close_output_on_eof,
        flush_on_input_eof=flush_on_input_eof
        )

    res = ps.start()

    logging.debug("ps.start() == {}".format(res))

    ret = ps.wait()

    logging.debug("ps.wait() == {}".format(ret))

    if ret == None:
        ret = 222

    return ret


def process_file(
    program,
    infile,
    outfile,
    stderr,
    options=None,
    proc_bufsize=(2 * 1024 ** 2),
    cat_bufsize=(2 * 1024 ** 2),
    cwd=None,
    verbose=False
    ):

    if options == None:
        options = []

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

                    ec = process_stream(
                        program,
                        fi,
                        fo,
                        stderr=stderr,
                        options=options,
                        proc_bufsize=proc_bufsize,
                        cat_bufsize=cat_bufsize,
                        cwd=cwd,
                        verbose=verbose
                        )

                    if ec != 0:
                        logging.error(
                            "Error processing file {in} to {out} through"
                            " {proc} (code {code})".format_map(
                                {
                                 'in': infile,
                                 'out': outfile,
                                 'proc': program,
                                 'code': ec
                                 }
                                )
                            )
                        ret = 2
                finally:
                    fo.close()

            finally:
                fi.close()

    return ret
