
import logging
import os
import os.path
import pprint
import sys

import org.wayround.utils.path
import org.wayround.utils.file

def elf_deps(filename):

    import org.wayround.utils.format.elf

    ret = org.wayround.utils.format.elf.get_libs_list(filename)

    return ret

def find_so_problems_in_linux_system():

    LD_LIBRARY_PATH = []
    if 'LD_LIBRARY_PATH' in os.environ:
        LD_LIBRARY_PATH += os.environ['LD_LIBRARY_PATH'].split(':')

    LD_LIBRARY_PATH.append('/lib')
    LD_LIBRARY_PATH.append('/usr/lib')

    PATH = os.environ['PATH'].split(':')
    ELF_PATHS = PATH + LD_LIBRARY_PATH

    logging.info("Searching so files in paths: {}".format(LD_LIBRARY_PATH))
    so_files = []

    for i in LD_LIBRARY_PATH:
        so_files += find_so_files(i)

#    for i in range(len(so_files)):
#        so_files[i] = os.path.realpath(so_files[i])

    so_files = list(set(so_files))
    so_files.sort()

    logging.info("Searching elf files in paths: {}".format(ELF_PATHS))

    elf_files = []

    for i in ELF_PATHS:
        elf_files += find_elf_files(i)

    for i in range(len(elf_files)):
        elf_files[i] = os.path.realpath(elf_files[i])

    elf_files = list(set(elf_files))
    elf_files.sort()

    logging.info("Looking for problems")
    reqs = {}


    elf_files_c = len(elf_files)
    elf_files_i = 0

    for i in elf_files:

        libs = org.wayround.utils.format.elf.get_libs_list(i)

        if not isinstance(libs, list):
            logging.error("Can't get libs list for file: `{}'".format(i))
        else:
            for j in libs:
                if not j in so_files:
                    if not j in reqs:
                        reqs[j] = list()
                    reqs[j].append(i)

        elf_files_i += 1

        org.wayround.utils.file.progress_write(
            "Checked dependencies: {} of {} ({} missing found)".format(
                elf_files_i,
                elf_files_c,
                len(reqs.keys())
                )
            )

    print("")
    logging.info("Libraries missing: {}".format(len(reqs.keys())))

    return reqs

def find_so_files(directory):

    import org.wayround.utils.format.elf

    ret = set()

    if not os.path.isdir(directory):
        logging.error(ValueError("Directory not exists `{}'".format(directory)))
        ret = set()
    else:

        files = os.listdir(directory)
        files_c = len(files)

        count = 0
        elfs = 0

        for i in files:
            full_name = os.path.join(directory, i)

            if os.path.isfile(full_name):
                if full_name.find('.so') != -1:
                    if org.wayround.utils.format.elf.is_elf_file(full_name):
                        ret.add(i)
                        elfs += 1

            count += 1

            org.wayround.utils.file.progress_write(
                "Looking for .so files: {} of {} files (elfs: {}) in {}".format(
                    count,
                    files_c,
                    elfs,
                    directory
                    )
                )

    print("")

    ret = list(ret)
    ret.sort()

    return ret

def find_elf_files(directory):

    import org.wayround.utils.format.elf

    ret = set()

    if not os.path.isdir(directory):
        logging.error(ValueError("Directory not exists `{}'".format(directory)))
        ret = set()
    else:

        files = os.listdir(directory)
        files_c = len(files)

        count = 0
        elfs = 0

        for i in files:
            full_name = os.path.join(directory, i)

            if os.path.isfile(full_name):
                if org.wayround.utils.format.elf.is_elf_file(full_name):
                    ret.add(full_name)
                    elfs += 1

            count += 1

            org.wayround.utils.file.progress_write(
                "Looking for elf files: {} of {} files (elfs: {}) in {}".format(
                    count,
                    files_c,
                    elfs,
                    directory
                    )
                )

    print("")

    ret = list(ret)
    ret.sort()

    return ret
