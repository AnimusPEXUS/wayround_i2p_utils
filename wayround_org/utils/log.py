
import logging
import os

import wayround_org.utils.path
import wayround_org.utils.stream
import wayround_org.utils.time


def process_output_logger(process, log):
    t = wayround_org.utils.stream.lbl_write(
        process.stdout,
        log,
        True
        )
    t.start()

    t2 = wayround_org.utils.stream.lbl_write(
        process.stderr,
        log,
        True,
        typ='error'
        )
    t2.start()

    t.join()
    t2.join()

    return


class Log:

    def __init__(self, log_dir, logname, echo=True, timestamp=None):

        ret = 0
        self.code = 0
        self.fileobj = None
        self.logname = logname
        self.log_filename = None

        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except:
                logging.exception("Exception while creating building logs dir")
                ret = 1
        else:

            if (
                    not os.path.isdir(log_dir)
                    or os.path.islink(log_dir)
                    ):
                logging.error(
                    "Current file type is not acceptable: {}".format(
                        log_dir
                        )
                    )
                ret = 2

        if ret == 0:
            if timestamp is None:
                timestamp = wayround_org.utils.time.currenttime_stamp()
            filename = wayround_org.utils.path.abspath(
                os.path.join(
                    log_dir,
                    "{name}-{ts}.txt".format_map(
                        {
                            'ts': timestamp,
                            'name': logname
                            }
                        )
                    )
                )

            self.log_filename = filename

            try:
                self.fileobj = open(filename, 'w')
            except:
                logging.exception("Error opening log file")
                ret = 3
            else:
                self.info(
                    "=///////= Starting `{}' log =///////=" .format(
                        self.logname
                        ),
                    echo=echo,
                    timestamp=timestamp
                    )

        if ret != 0:
            raise Exception

        return

    def __del__(self):
        if self:
            if self.fileobj:
                if not self.fileobj.closed:
                    try:
                        self.stop()
                    except:
                        pass

    def stop(self, echo=True):
        if self.fileobj is None:
            raise Exception

        timestamp = wayround_org.utils.time.currenttime_stamp()
        self.info(
            "=///////= Stopping `{}' log =///////=" .format(
                self.logname
                ),
            echo=echo,
            timestamp=timestamp
            )
        self.fileobj.flush()
        self.fileobj.close()
        return

    close = stop

    def write(self, text, echo=False, typ='info', timestamp=None):

        if not typ in ['info', 'error', 'warning']:
            raise ValueError("Wrong `typ' parameter")

        if self.fileobj is None:
            raise Exception("Log output file object is None")

        if timestamp:
            pass
        else:
            timestamp = wayround_org.utils.time.currenttime_stamp()

        if echo:
            msg1 = "[{}] {}".format(
                timestamp,
                text
                )

            if typ == 'info':
                logging.info(msg1)
            elif typ == 'error':
                logging.error(msg1)
            elif typ == 'warning':
                logging.warning(msg1)

        icon = '-i-'
        if typ == 'info':
            icon = '-i-'
        elif typ == 'error':
            icon = '-e-'
        elif typ == 'warning':
            icon = '-w-'

        msg2 = "[{}] {} {}".format(
            timestamp,
            icon,
            text
            )

        self.fileobj.write(msg2 + '\n')
        return

    def error(self, text, echo=True, timestamp=None):
        self.write(text, echo=echo, typ='error', timestamp=timestamp)

    def info(self, text, echo=True, timestamp=None):
        self.write(text, echo=echo, typ='info', timestamp=timestamp)

    def warning(self, text, echo=True, timestamp=None):
        self.write(text, echo=echo, typ='warning', timestamp=timestamp)
