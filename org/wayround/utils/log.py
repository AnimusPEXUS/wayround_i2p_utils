
import os
import logging

import org.wayround.utils.time

class Log:

    def __init__(self, log_dir, logname):

        ret = 0
        self.code = 0
        self.fileobj = None
        self.logname = logname

        if not os.path.exists(log_dir):
            try:
                os.makedirs(log_dir)
            except:
                logging.exception("Exception while creating building logs dir")
                ret = 1
        else:

            if not os.path.isdir(log_dir) \
                    or os.path.islink(log_dir):
                logging.error("Current file type is not acceptable: {}".format(
                    log_dir
                    ))
                ret = 2

        if ret == 0:
            timestamp = org.wayround.utils.time.currenttime_stamp()
            filename = os.path.abspath(
                os.path.join(
                    log_dir,
                    "%(ts)s-%(name)s.txt" % {
                        'ts': timestamp,
                        'name': logname
                        }
                    )
                )

            try:
                self.fileobj = open(filename, 'w')
            except:
                logging.exception("Error opening log file")
                ret = 3
            else:
                logging.info(
                    "[{ts}] =///////= Starting `{name}' log =///////=\n" .format_map({
                        'ts': timestamp,
                        'name': self.logname
                        }))
                self.fileobj.write(
                    "[{ts}] =///////= Starting `{name}' log =///////=\n".format_map({
                        'ts': timestamp,
                        'name': self.logname
                    }
                    )
                    )

        if ret != 0:
            raise Exception

        return

    def stop(self):
        if self.fileobj == None:
            raise Exception

        timestamp = org.wayround.utils.time.currenttime_stamp()
        logging.info("[{ts}] =///////= Stopping `{name}' log =///////=\n".formap_map({
            'ts': timestamp,
            'name': self.logname
            }))
        self.fileobj.write("[{ts}] =///////= Stopping `{name}' log =///////=\n".formap_map({
            'ts': timestamp,
            'name': self.logname
            }))
        self.fileobj.flush()
        self.fileobj.close()
        return

    def write(self, text, echo=True):
        if self.fileobj == None:
            raise Exception

        timestamp = org.wayround.utils.time.currenttime_stamp()
        if echo:
            logging.info("[{ts}] {}".format_map({
                'ts': timestamp,
                'text': text
                }))
        self.fileobj.write("[{ts}] {}".format_map({
                'ts': timestamp,
                'text': text
                }))
        return

    def error(self, text, echo=True):
        self.write("-e- " + text, echo=echo, typ='error')

    def info(self, text, echo=True):
        self.write("-i- " + text, echo=echo, typ='info')

    def warning(self, text, echo=True):
        self.write("-w- " + text, echo=echo, typ='warning')

    def __del__(self):
        if not self.fileobj.closed:
            try:
                self.stop()
            except:
                pass




