
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

class ProcessStream:

    def __init__(self):

        self.clear(init=True)

    def __del__(self):
        self.stop()

    def clear(self, init=False):

        ret = 0

        if not init and self.working:
            logging.error(
                "Program settings can not be cleaned while it is working"
                )

            ret = 1
        else:

            if not init:
                self.stop()

            self._working = False
            self.proc = None

            self.in_cat = None
            self.out_cat = None
            self.out_cat_write_error = False

            if not init:
                if self.stop_flag:
                    self.stop_flag.set()

            self.stop_flag = threading.Event()

            self.returncode = None

            self.proc_watcher = None


        return ret

    def setValues(
        self,
        program,
        stdin,
        stdout,
        stderr,
        options=[],
        proc_bufsize=0,
        cat_bufsize=(2 * 1024 ** 2),
        cwd=None,
        verbose=False,
        close_output_on_eof=False
        ):

        ret = 0

        if self.working:
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

        return ret

    def start(self):

        ret = 0

        if self.working:
            logging.error(
                "Program can not be started if it's already working"
                )

            ret = 1

        else:

            self.clear()

            self._working = True

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
                logging.exception("Error starting process `{}'".format(self.program))
                ret = 2
            else:
                try:
                    threading.Thread(
                        name="Thread Waiting for program `{}' exit".format(self.program),
                        target=self._proc_waiter
                        ).start()
                except:
                    logging.exception("Error starting thread")
                    ret = 3
                else:

                    try:
                        thread_name = ''

                        if self.verbose:
                            thread_name = 'in >> {}'.format(self.proc.pid)
                        else:
                            thread_name = 'Thread'

                        self.in_cat = org.wayround.utils.stream.cat(
                            self.stdin,
                            self.proc.stdin,
                            threaded=True,
                            close_output_on_eof=True,
                            bs=self.cat_bufsize,
                            thread_name=thread_name,
                            verbose=self.verbose,
                            termination_event=self.stop_flag,
                            on_exit_callback=self._close_in_cat,
                            on_input_read_error=self._read_error_in_cat,
                            on_output_write_error=self._write_error_in_cat
                            )

                        if self.verbose:
                            thread_name = '{} >> out'.format(self.proc.pid)
                        else:
                            thread_name = 'Thread'

                        self.out_cat = org.wayround.utils.stream.cat(
                            self.proc.stdout,
                            self.stdout,
                            threaded=True,
                            close_output_on_eof=self.close_output_on_eof,
                            bs=self.cat_bufsize,
                            thread_name=thread_name,
                            verbose=self.verbose,
                            termination_event=self.stop_flag,
                            on_exit_callback=self._close_out_cat,
                            on_input_read_error=self._read_error_out_cat,
                            on_output_write_error=self._write_error_out_cat
                            )

                        self.in_cat.start()
                        self.out_cat.start()

                    except:
                        logging.exception(
                            "Some exception while starting cat threads"
                            )
                        ret = 4

                    else:

                        self.wait('working')

        return ret

    def stop(self):

        if self.working:

            self.stop_flag.set()

            self._close_proc()

            if self.in_cat:
                self.in_cat.join()

            if self.out_cat:
                self.out_cat.join()

            self._working = False

            self.wait()

        return

    @property
    def working(self):
        return self.stat() != 'stopped'

    def stat(self):

        ret = 'unknown'

        if self.in_cat and self.out_cat and self.proc and self._working:
            ret = 'working'

        if not self.in_cat and not self.out_cat and not self.proc and not self._working:
            ret = 'stopped'

        logging.debug("""\
status:
self.in_cat     {}
self.out_cat    {}
self.proc       {}
self._working   {}
{}
""".format(self.in_cat, self.out_cat, self.proc, self._working, ret))

        return ret

    def wait(self, what='stopped'):

        if not what in ['stopped', 'working']:
            raise ValueError("wrong `what' value")

        if ((self.working and what == 'stopped')
            or (not self.working and what == 'working')):

            while True:

                logging.debug("Waiting for {}".format(what))

                if self.stat() == what:
                    break

                if self.stop_flag.is_set():
                    break

                time.sleep(0.2)

        return self.returncode

    def _read_error_in_cat(self):
        return

    def _write_error_in_cat(self):
        return

    def _close_in_cat(self):
        self.in_cat = None
        return

    def _read_error_out_cat(self):
        return

    def _write_error_out_cat(self):
        self.stop()
        return

    def _close_out_cat(self):
        self.out_cat = None
        return

    def _close_proc(self):

        p = self.proc

        logging.debug("Closing proc")

        if p:

            if isinstance(p.returncode, int):

                self.returncode = p.returncode
                logging.debug("Setting return code to {}".format(self.returncode))

            else:

                try:
                    p.terminate()
                except:
                    logging.exception(
                        "Exception while terminating "
                        "possibly dead process: {}".format(p.pid)
                        )

                self.returncode = None

            self.proc = None

        return

    def _proc_waiter(self):

        while True:

            try:
                self.proc.wait(0.2)
            except subprocess.TimeoutExpired:
                pass
            except:
                logging.exception("Exception while waiting for process")
                break
            else:
                break

        self.stop()

        return


def process_stream(
    program,
    stdin,
    stdout,
    stderr,
    options=[],
    proc_bufsize=0,
    cat_bufsize=(2 * 1024 ** 2),
    cwd=None,
    verbose=False,
    close_output_on_eof=False
    ):

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
        close_output_on_eof=close_output_on_eof
        )

    logging.debug("ps.start() == {}".format(ps.start()))


    ret = ps.wait()
    logging.debug("ps.wait() == {}".format(ret))

    if ret == None:
        ret = 222

    return ret


#def process_stream(
#    program,
#    stdin,
#    stdout,
#    stderr,
#    options=[],
#    proc_bufsize=0,
#    cat_bufsize=(2 * 1024 ** 2),
#    cwd=None,
#    verbose=False,
#    close_output_on_eof=False
#    ):
#    """
#    Starts `program' and uses it to process stdin to stdout
#
#    Streams are workedout using own-fashioned threading mechanisms
#    """
#
#    ret = 0
#
#    try:
#        proc = simple_exec(
#            program,
#            stdin=subprocess.PIPE,
#            stdout=subprocess.PIPE,
#            stderr=stderr,
#            options=options,
#            bufsize=proc_bufsize,
#            cwd=cwd
#            )
#    except:
#        logging.exception("Error starting process `{}'".format(program))
#        ret = 1
#    else:
#
#        try:
#            thread_name = ''
#
#            if verbose:
#                thread_name = 'in >> {}'.format(proc.pid)
#            else:
#                thread_name = 'Thread'
#
#            cat1 = org.wayround.utils.stream.cat(
#                stdin,
#                proc.stdin,
#                threaded=True,
#                close_output_on_eof=True,
#                bs=cat_bufsize,
#                thread_name=thread_name
#                )
#
#            if verbose:
#                thread_name = '{} >> out'.format(proc.pid)
#            else:
#                thread_name = 'Thread'
#
#            cat2 = org.wayround.utils.stream.cat(
#                proc.stdout,
#                stdout,
#                threaded=True,
#                close_output_on_eof=close_output_on_eof,
#                bs=cat_bufsize,
#                thread_name=thread_name
#                )
#
#            cat1.start()
#            cat2.start()
#
#            try:
#                while True:
#
#                    try:
#                        proc.wait(1)
#                    except subprocess.TimeoutExpired:
#                        pass
#                    except:
#                        break
#
#                    else:
#
#                        pass
#
#
#            except:
#                logging.exception(
#                    "Exception while waiting for process exit: {}".format(
#                        proc.pid
#                        )
#                    )
#
#            cat1.join()
#            cat2.join()
#        finally:
#            if proc.returncode == None:
#                try:
#                    proc.terminate()
#                except:
#                    logging.exception(
#                        "Exception while terminating "
#                        "possibly alive process: {}".format(proc.pid)
#                        )
#
#    return ret


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
                            "Error processing file {in} to {out} through {proc} (code {code})".format_map(
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
