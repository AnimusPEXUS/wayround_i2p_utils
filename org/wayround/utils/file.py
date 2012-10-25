
import os
import sys
import shutil
import glob
import logging
import fnmatch


import org.wayround.utils.text
import org.wayround.utils.terminal


def _copytree(src_dir, dst_dir, overwrite_files=False, copy_links=False,
              stop_on_overwrite_error=True):

    ret = 0

    full_src_dir = os.path.abspath(src_dir)
    full_dst_dir = os.path.abspath(dst_dir)

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
                                logging.info("installing `{}'".format(full_dst_file))
                                try:
                                    shutil.copy2(full_src_file, full_dst_file)
                                except:
                                    if stop_on_overwrite_error:
                                        logging.error("Can't overwrite dir `{}' with file".format(full_dst_file))
                                        ret = 4
                                    else:
                                        logging.warning("Can't overwrite dir `{}' with file. -- skipping".format(full_dst_file))

    return ret

def copytree(src_dir,
             dst_dir,
             overwrite_files=False,
             clear_before_copy=False,
             dst_must_be_empty=True):

    src_dir = os.path.abspath(src_dir)
    dst_dir = os.path.abspath(dst_dir)

    ret = 0

    logging.info("Copying `{}' to `{}'".format(src_dir, dst_dir))

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
                logging.error("Some errors occurred while copying `{}' to `{}'".format(src_dir, dst_dir))
                ret = 3
    #print('')
    return ret


def isdirempty(dirname):
    return len(os.listdir(dirname)) == 0

is_dir_empty = isdirempty

def remove_if_exists(file_or_dir):

    file_or_dir = os.path.abspath(file_or_dir)

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
        files[i] = os.path.abspath(
            dirname + os.path.sep + files[i]
            )

    for i in files:
        if remove_if_exists(i) != 0:
            ret = 1

    return ret


def list_files(path, mask):

    lst = glob.glob('{}/{}'.format(path, mask))

    lst.sort()

    len_lst = len(lst)

    semi = ''
    if len_lst > 0:
        semi = ':'

    print("found {} file(s){}".format(len_lst, semi))

    bases = []
    for each in lst:
        bases.append(os.path.basename(each))

    org.wayround.utils.text.columned_list_print(bases, fd=sys.stdout.fileno())
    if len_lst > 0:
        print("found {} file(s)".format(len_lst))

    return

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



def _list_files_recurcive(start_root, start_root_len, root_dir, fd):

    files = os.listdir(root_dir)

    files.sort()

    for each in files:

        full_path = os.path.abspath(
            os.path.join(
                root_dir,
                each
                )
            )

        if (
            os.path.isdir(full_path)
            and not
            os.path.islink(full_path)
            ):
            _list_files_recurcive(start_root, start_root_len, full_path, fd)
        else:

            fd.write("{}\n".format(full_path[start_root_len:]))
            # if not os.path.isdir(full_path):
            #     fd.write("{}\n".format(full_path[start_root_len:]))
            # else:
            #     # Sym-Link to dir hit. Ignore in this case.
            #     pass

    return

def list_files_recurcive(dirname, output_filename):

    try:
        fd = open(output_filename, 'w')
    except:
        logging.exception("Can't create file `{}'".format(output_filename))
        raise
    else:
        try:
            absp = os.path.abspath(dirname)
            _list_files_recurcive(absp, len(absp), absp, fd)
        finally:
            fd.close()
    return

def progress_write_finish():
    sys.stdout.write("\n")
    sys.stdout.flush()
    return

def progress_write(line_to_write, new_line=False):

    new_line_str = ''

    if line_to_write.endswith("\n"):
        new_line = True
        line_to_write = line_to_write.rstrip("\n")

    if new_line:
        new_line = True
        new_line_str = "\n"

    width = 80
    ts = org.wayround.utils.terminal.get_terminal_size(sys.stdout.fileno())
    if ts != None:
        width = ts['ws_col']

    line_to_write_l = len(line_to_write)

    line_to_out = "\r{ltw}{spaces}{new_line}\r".format_map(
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
    name = os.path.abspath(name)
    if not os.path.isdir(name):
        raise OSError("Not a dir `{}'".format(name))

    size = 0

    lst = os.listdir(name)
    for i in ['.', '..']:
        if i in lst:
            lst.remove(i)

    lst.sort()

    for i in lst:
        f_pth = os.path.abspath(name + os.path.sep + i)
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

    filename = os.path.abspath(filename)

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
                dir_name = os.path.abspath(os.path.dirname(filename))

                try:
                    lnk = os.readlink(filename)
                except:
                    ret = 2
                else:
                    if lnk[0] != '/':
                        lnk = os.path.abspath(dir_name + os.path.sep + lnk)

                    os.unlink(filename)
                    shutil.copy2(lnk, filename)

    return ret

def dereference_files_in_dir(dirname):

    ret = 0

    dirname = os.path.abspath(dirname)

    try:
        for dirpath, dirnames, filenames in os.walk(dirname):
            filenames.sort()
            dirnames.sort()
            dirpath = os.path.abspath(dirpath)

            for i in filenames:
                if dereference_file(os.path.join(dirpath , i)) != 0:
                    logging.error(
                        "Could not dereference `{}'".format(
                            os.path.relpath(
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

    in_dir = os.path.abspath(in_dir)
    out_dir = os.path.abspath(out_dir)

    ret = 0
    try:
        for dirpath, dirnames, filenames in os.walk(in_dir):
            filenames.sort()
            dirnames.sort()
            dirpath = os.path.abspath(dirpath)

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
