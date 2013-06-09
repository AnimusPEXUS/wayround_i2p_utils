
import fnmatch
import logging
import os
import select
import shutil
import sys
import threading
import time


import org.wayround.utils.path
import org.wayround.utils.terminal
import org.wayround.utils.text

POLL_CONSTS = {}

_l = dir(select)
for _i in [
    'POLLIN',
    'POLLPRI',
    'POLLOUT',
    'POLLERR',
    'POLLHUP',
    'POLLNVAL'
    ]:
    POLL_CONSTS[_i] = eval('select.{}'.format(_i))

del _i
del _l



def _copytree(
    src_dir,
    dst_dir,
    overwrite_files=False,
    copy_links=False,
    stop_on_overwrite_error=True
    ):

    ret = 0

    full_src_dir = org.wayround.utils.path.abspath(src_dir)
    full_dst_dir = org.wayround.utils.path.abspath(dst_dir)

    if not os.path.isdir(full_src_dir):
        logging.error("Source dir not exists `{}'".format(src_dir))
        ret = 1
    else:
        if create_if_not_exists_dir(full_dst_dir) != 0:
            logging.error("Error creating destination dir `{}'".format(full_dst_dir))
            ret = 2
        else:

            shutil.copystat(full_src_dir, full_dst_dir)

            files = os.listdir(full_src_dir)
            files.sort()

            for i in files:
                if ret != 0:
                    break
                full_src_file = os.path.join(full_src_dir, i)
                full_dst_file = os.path.join(full_dst_dir, i)

                if not os.path.islink(full_src_file) \
                    or (os.path.islink(full_src_file) and copy_links):
                    if os.path.isdir(full_src_file) and not os.path.islink(full_src_file):
                        if _copytree(full_src_file, full_dst_file,
                              overwrite_files=overwrite_files
                              ) != 0:
                            ret = 5
                    else:
                        if os.path.isfile(full_dst_file) and overwrite_files \
                            or not os.path.exists(full_dst_file):
                            if os.path.isdir(full_dst_file):
                                if stop_on_overwrite_error:
                                    logging.error("Can't overwrite dir `{}' with file".format(full_dst_file))
                                    ret = 3
                                else:
                                    logging.warning("Can't overwrite dir `{}' with file. -- skipping".format(full_dst_file))
                            else:
                                logging.info("copying `{}'".format(os.path.relpath(full_dst_file)))
                                try:
                                    shutil.copy2(full_src_file, full_dst_file)
                                except:
                                    if stop_on_overwrite_error:
                                        logging.error("Can't overwrite dir `{}' with file".format(full_dst_file))
                                        ret = 4
                                    else:
                                        logging.warning("Can't overwrite dir `{}' with file. -- skipping".format(full_dst_file))

    return ret

def copytree(
    src_dir,
    dst_dir,
    overwrite_files=False,
    clear_before_copy=False,
    dst_must_be_empty=True
    ):

    # TODO: think of symlinks

    src_dir = org.wayround.utils.path.abspath(src_dir)
    dst_dir = org.wayround.utils.path.abspath(dst_dir)

    ret = 0

    logging.info("Copying `{}' to `{}'".format(src_dir, dst_dir))

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok=True)

    if dst_must_be_empty:
        if isdirempty(dst_dir):
            logging.error("Destination dir `{}' not empty".format(dst_dir))
            ret = 1

    if ret == 0:

        if clear_before_copy:
            logging.info("Cleaning dir `{}'".format(dst_dir))
            cleanup_dir(dst_dir)

        if create_if_not_exists_dir(dst_dir) != 0:
            logging.error("Error creating dir `{}'".format(dst_dir))
            ret = 2
        else:
            if _copytree(src_dir, dst_dir, overwrite_files=overwrite_files) != 0:
                logging.error(
                    "Some errors occurred while copying `{}' to `{}'".format(
                        src_dir,
                        dst_dir
                    )
                )
                ret = 3

    return ret


def isdirempty(dirname):
    return len(os.listdir(dirname)) == 0

is_dir_empty = isdirempty


def remove_if_exists(file_or_dir):

    file_or_dir = org.wayround.utils.path.abspath(file_or_dir)

    if os.path.exists(file_or_dir):
        if not os.path.islink(file_or_dir):

            if os.path.isdir(file_or_dir):
                try:
                    shutil.rmtree(file_or_dir)
                except:
                    logging.exception(
                        "Can't remove dir {}".format(file_or_dir)
                        )
                    return 1
            else:
                try:
                    os.unlink(file_or_dir)
                except:
                    logging.exception(
                        "      can't remove file {}".format(file_or_dir)
                        )
                    return 1

        else:
            try:
                os.unlink(file_or_dir)
            except:
                logging.exception("      can't remove link {}".format(file_or_dir))
                return 1

    return 0


def create_if_not_exists_dir(dirname):
    ret = 0
    if not os.path.exists(dirname):
        try:
            os.makedirs(dirname)
        except:
            logging.error("Destination dir not exists and cant's be created")
            ret = 1
        else:
            ret = 0
    else:
        if os.path.isfile(dirname):
            logging.error("Destination exists but is file")
            ret = 2
        elif os.path.islink(dirname):
            logging.error("Destination exists but is link")
            ret = 3
        elif not os.path.isdir(dirname):
            logging.error("Destination exists but is not dir")
            ret = 4
        else:
            ret = 0
    return ret


def cleanup_dir(dirname):

    ret = 0

    files = os.listdir(dirname)

    for i in range(len(files)):
        files[i] = org.wayround.utils.path.abspath(
            dirname + os.path.sep + files[i]
            )

    for i in files:
        if remove_if_exists(i) != 0:
            ret = 1

    return ret


def inderictory_copy_file(directory, file1, file2):

    file1 = os.path.basename(file1)
    file2 = os.path.basename(file2)

    f1 = os.path.join(directory, file1)
    f2 = os.path.join(directory, file2)

    if os.path.isfile(f1):
        if os.path.exists(f2):
            logging.error("destination file or dir already exists")
        else:
            logging.info("copying {} to {}".format(f1, f2))
            try:
                shutil.copy(f1, f2)
            except:
                logging.exception("Error copying file")
    else:
        logging.error("source file not exists")


    return


def files_recurcive_list(
    dirname,
    onerror=None,
    followlinks=False,
    exclude_paths=None,
    relative_to=None,
    mute=True,
    sort=False,
    acceptable_endings=None,
    print_found=False,
    list_symlincs=True
    ):

    if relative_to and not isinstance(relative_to, str):
        raise ValueError("relative_to must be str or None")

    dirname = org.wayround.utils.path.normpath(dirname)

    absp = dirname.startswith('/')
    dirname = org.wayround.utils.path.abspath(dirname)

    lst = []

    if not mute:
        logging.info(
            "Setting list of files in `{}' and it's subdirs".format(dirname)
            )

    if isinstance(exclude_paths, list):
        exclude_paths2 = list()

        for i in exclude_paths:

            f_path = None

            if i.startswith('/'):
                f_path = org.wayround.utils.path.abspath(i)
            else:
                f_path = org.wayround.utils.path.abspath(
                    org.wayround.utils.path.join(
                        dirname, i
                        )
                    )

            if ((dirname == os.path.sep and f_path.startswith(os.path.sep)) or
                (f_path + os.path.sep).startswith(dirname + os.path.sep)):
                exclude_paths2.append(f_path)

        exclude_paths = exclude_paths2

    if not mute:
        logging.info("Walking...")

    for dire, dirs, files in os.walk(
        dirname,
        onerror=onerror,
        followlinks=followlinks
        ):

        if sort:
            dirs.sort()
            files.sort()

        if isinstance(exclude_paths, list):

            for i in dirs[:]:

                f_path = org.wayround.utils.path.abspath(
                    org.wayround.utils.path.join(
                        dire, i
                        )
                    )

                if f_path in exclude_paths:
                    while i in dirs:
                        dirs.remove(i)

        for f in files:

            f_path = org.wayround.utils.path.join(dire, f)

            append = True

            if not list_symlincs and os.path.islink(f_path):
                append = False

            if append:
                if acceptable_endings:

                    found = False

                    for i in acceptable_endings:
                        if f.endswith(i):
                            found = True
                            break

                    if not found:
                        append = False

            if append:
                if print_found and not mute:
                    print("    {}".format(f_path))
                lst.append(f_path)



        if not mute:
            pp = None
            if not relative_to:
                pp = dire
            else:
                pp = org.wayround.utils.path.relpath(dire, relative_to)

            progress_write("    ({} files): {}".format(len(lst), pp))

    if not mute:
        progress_write_finish()

    ret = lst

    if not relative_to:

        if not absp:

            p_path_s_l = len(dirname) + 1

            for i in range(len(ret)):
                ret[i] = ret[i][p_path_s_l:]

    else:

        for i in range(len(ret)):
            ret[i] = org.wayround.utils.path.relpath(ret[i], relative_to)

    return lst


def progress_write_finish():
    sys.stdout.write('\n')
    sys.stdout.flush()
    return

def progress_write(line_to_write, new_line=False):

    new_line_str = ''

    if line_to_write.endswith('\n'):
        new_line = True
        line_to_write = line_to_write.rstrip('\n')

    if new_line:
        new_line = True
        new_line_str = '\n'

    width = 80
    ts = org.wayround.utils.terminal.get_terminal_size(sys.stdout.fileno())
    if ts != None:
        width = ts['ws_col']

    line_to_write_l = len(line_to_write)

    line_to_out = '\r{ltw}{spaces}{new_line}\r'.format_map(
        {
            'ltw': line_to_write,
            'spaces': org.wayround.utils.text.fill(
                ' ', width - line_to_write_l
                ),
            'new_line':new_line_str
            }
        )

    if len(line_to_out) > width:
        line_to_out = line_to_out[:width + 1] + new_line_str + '\r'

    # TODO: put sys.stdout to parameters

    sys.stdout.write(line_to_out)
    sys.stdout.flush()
    return

def null_file(filename):
    ret = 0
    try:
        f = open(filename, 'w')
    except:
        ret = 1
    else:
        f.close()
    return ret

def get_dir_size(name):
    name = org.wayround.utils.path.abspath(name)
    if not os.path.isdir(name):
        raise OSError("Not a dir `{}'".format(name))

    size = 0

    lst = os.listdir(name)
    for i in ['.', '..']:
        if i in lst:
            lst.remove(i)

    lst.sort()

    for i in lst:
        f_pth = org.wayround.utils.path.abspath(name + os.path.sep + i)
        if not os.path.islink(f_pth):
            if os.path.isfile(f_pth):
                s = os.stat(f_pth)
                size += s.st_size
            elif os.path.isdir(f_pth):
                size += get_dir_size(f_pth)

    return size

def get_file_size(name):

    ret = None

    if not os.path.exists(name):
        ret = None
    else:
        if os.path.isfile(name):
            s = os.stat(name)
            ret = s.st_size
        elif os.path.isdir(name):
            ret = get_dir_size(name)

    return ret

def dereference_file(filename):

    ret = 0

    filename = org.wayround.utils.path.abspath(filename)

    if not os.path.exists(filename):
        ret = 1

    else:
        if os.path.isdir(filename):
            ret = 0
        else:
            if not os.path.islink(filename):
                ret = 0
            else:
                lnk = None
                dir_name = org.wayround.utils.path.abspath(os.path.dirname(filename))

                try:
                    lnk = os.readlink(filename)
                except:
                    ret = 2
                else:
                    if lnk[0] != '/':
                        lnk = org.wayround.utils.path.abspath(dir_name + os.path.sep + lnk)

                    os.unlink(filename)
                    shutil.copy2(lnk, filename)

    return ret

def dereference_files_in_dir(dirname):

    ret = 0

    dirname = org.wayround.utils.path.abspath(dirname)

    try:
        for dirpath, dirnames, filenames in os.walk(dirname):
            filenames.sort()
            dirnames.sort()
            dirpath = org.wayround.utils.path.abspath(dirpath)

            for i in filenames:
                if dereference_file(os.path.join(dirpath , i)) != 0:
                    logging.error(
                        "Could not dereference `{}'".format(
                            org.wayround.utils.path.relpath(
                                dirname,
                                os.getcwd()
                                )
                            )
                        )

                    ret = 1
    except:
        logging.exception("Dir files dereferencing exception")
        ret = 2

    return ret

def files_by_mask_copy_to_dir(in_dir, out_dir, mask='*.h'):

    in_dir = org.wayround.utils.path.abspath(in_dir)
    out_dir = org.wayround.utils.path.abspath(out_dir)

    ret = 0
    try:
        for dirpath, dirnames, filenames in os.walk(in_dir):
            filenames.sort()
            dirnames.sort()
            dirpath = org.wayround.utils.path.abspath(dirpath)

            for i in filenames:
                if fnmatch.fnmatch(i, mask):
                    shutil.copy2(
                        dirpath + os.path.sep + i,
                        out_dir + os.path.sep + i,
                        follow_symlinks=True
                        )

    except:
        logging.exception("Files by mask copy to dir exception")
        ret = 1

    return ret




class FDStatusWatcher:

    def __init__(self, on_status_changed=None):

        self._clear(init=True)

        self._on_status_changed = on_status_changed

    def __del__(self):
        self.stop()

    def _clear(self, init=False):

        if not init:
            if self.stat() != 'stopped':
                raise RuntimeError("Working. Cleaning restricted")

        if not init:
            if self._fd and self._poll:
                self._poll.unregister(self._fd)

        self._poll = None

        self._fd = None

        self._watching_thread = None

        self._stop_flag = False

        self.fd_status = None

        self._starting = False
        self._stopping = False

    def set_fd(self, fd):

        if not isinstance(fd, int):
            raise TypeError("`fd' must be instance of int")

        logging.debug(
            "Switching monitoring to new fd {}, previaus was {}".format(
                fd, self._fd
                )
            )

        worked = False
        if self.stat() == 'working':
            worked = True

            self.stop()

        self._fd = fd

        if worked:
            self.start()

    def get_fd(self):

        return self._fd

    def stop(self):

        if not self._starting and not self._stopping:

            self._stopping = True
            self._stop_flag = True
            self.wait('stopped')
            self._clear()
            self._stopping = False

    def start(self):

        threading.Thread(
            name="Thread Starting Socket Watcher",
            target=self._start
            ).start()

    def _start(self):

        if not isinstance(self._fd, int):
            raise TypeError("file descriptor must be given before start")

        if not self._starting and not self._stopping and self.stat() == 'stopped':

            self._starting = True

            self._poll = select.poll()
            self._poll.register(
                self._fd,
                select.POLLIN | select.POLLPRI | select.POLLOUT |
                select.POLLERR | select.POLLHUP | select.POLLNVAL
                )

            self._watching_thread = threading.Thread(
                name="Thread watching FD {}".format(self._fd),
                target=self._watching_method
                )

            self._watching_thread.start()

            self._starting = False

    def stat(self):

        ret = 'stopped'

        if bool(self._watching_thread):
            ret = 'working'
        else:
            ret = 'stopped'

        return ret

    def wait(self, what='stopped'):

        allowed_what = ['stopped', 'working']

        if not what in allowed_what:
            raise ValueError("`what' must be in {}".format(allowed_what))

        while True:
            time.sleep(0.1)
            if self.stat() == what:
                break

        return

    def _watching_method(self):

        while True:

            if self._stop_flag:
                break

            new_stat_lst = self._poll.poll(100)

            if len(new_stat_lst) > 0:

                new_stat_event = new_stat_lst[0][1]

                if new_stat_event != self.fd_status:
                    threading.Thread(
                        name="FD {} status changed to [{}]".format(
                            self._fd,
                            '|'.join(poll_stat_namer(new_stat_event))
                            ),
                        target=self._on_status_changed,
                        args=(self._fd, poll_stat_namer(new_stat_event),)
                        ).start()

                self.fd_status = new_stat_event

        self._watching_thread = None



def poll_stat_namer(event):

    if not isinstance(event, int):
        raise TypeError("`event' must be int, but it is `{}'".format(event))

    devided = poll_stat_devider(event)
    names = set()

    for i in POLL_CONSTS.keys():

        for j in devided:

            if POLL_CONSTS[i] == j:
                names.add(i)

    return list(names)

def poll_stat_devider(event):

    if not isinstance(event, int):
        raise TypeError("`event' must be int, but it is `{}'".format(event))

    devided = []

    for i in POLL_CONSTS:

        int_val = eval("select.{}".format(i))

        if int_val & event != 0:
            devided.append(int_val)

    return devided

def print_status_change(sock, stats):
    logging.info("Socket {} status changed to {}".format(sock, stats))

def which(name):
    ret = None

    os_path = os.environ['PATH'].split(':')

    for i in os_path:

        n_f_n = os.path.join(i, name)

        if os.path.isfile(n_f_n):
            ret = n_f_n

    return ret
