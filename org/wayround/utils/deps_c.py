
import logging
import os.path

import org.wayround.utils.path
import org.wayround.utils.file



def find_so_problems_in_linux_system(verbose=False):

    """
    Look for dependency problems in current system
    """

    so_files, elf_files = get_so_and_elf_files(verbose)

    reqs = find_so_problems_in_linux_system_by_given_so_and_elfs(
        so_files, elf_files, verbose
        )

    return reqs

def find_so_problems_in_linux_system_by_given_so_and_elfs(
    so_files, elf_files, verbose=False
    ):

    """
    Look for dependency problems in current system
    """

    import org.wayround.utils.format.elf

    if verbose:
        so_files.sort()
        elf_files.sort()

    if verbose:
        logging.info("Looking for problems")

    reqs = {}


    elf_files_c = len(elf_files)
    elf_files_i = 0

    for i in elf_files:

        e = org.wayround.utils.format.elf.ELF(i)

        libs_elf_linked_to = e.needed_libs_list

        if not isinstance(libs_elf_linked_to, list):
            logging.error(
                "Can't get libs_elf_linked_to list for file: `{}'".format(i)
                )
        else:
            for j in libs_elf_linked_to:
                if not j in so_files:
                    if not j in reqs:
                        reqs[j] = list()
                    reqs[j].append(i)

        elf_files_i += 1

        if verbose:
            org.wayround.utils.file.progress_write(
                "Checked dependencies: {} of {} ({} missing found)".format(
                    elf_files_i,
                    elf_files_c,
                    len(reqs.keys())
                    )
                )

    if verbose:
        print("")
        logging.info("Libraries missing: {}".format(len(reqs.keys())))

    return reqs

def build_dependency_tree(verbose=False):

    """
    Look for dependency problems in current system
    """

    so_files, elf_files = get_so_and_elf_files(verbose)

    reqs = build_dependency_tree_by_given_so_and_elfs(
        so_files, elf_files, verbose
        )

    return reqs

def build_dependency_tree_by_given_so_and_elfs(
    so_files, elf_files, verbose=False
    ):

    """
    Build dependency tree by given so and elf lists
    """

    import org.wayround.utils.format.elf

    if verbose:
        so_files.sort()
        elf_files.sort()

    if verbose:
        logging.info("Building dependency tree")

    deps = {}


    elf_files_c = len(elf_files)
    elf_files_i = 0

    for i in elf_files:

        e = org.wayround.utils.format.elf.ELF(i)

        libs_elf_linked_to = e.needed_libs_list

        if not isinstance(libs_elf_linked_to, list):
            logging.error(
                "Can't get dependency list for file: `{}'".format(i)
                )
        else:
            if not i in deps:
                deps[i] = list()
            deps[i] = libs_elf_linked_to

        elf_files_i += 1

        if verbose:
            org.wayround.utils.file.progress_write(
                "Progress: {} ELF files of {}".format(
                    elf_files_i,
                    elf_files_c
                    )
                )

    if verbose:
        print("")

    return deps


def library_paths():

    LD_LIBRARY_PATH = []
    if 'LD_LIBRARY_PATH' in os.environ:
        LD_LIBRARY_PATH += os.environ['LD_LIBRARY_PATH'].split(':')

    LD_LIBRARY_PATH.append('/lib')
    LD_LIBRARY_PATH.append('/usr/lib')

    LD_LIBRARY_PATH = org.wayround.utils.path.realpaths(LD_LIBRARY_PATH)

    return LD_LIBRARY_PATH

def elf_paths():

    ret = os.environ['PATH'].split(':') + library_paths()

    ret = org.wayround.utils.path.realpaths(ret)

    return ret


def get_so_and_elf_files(verbose=False):

    """
    Get All system Shared Object Files and all elf files
    """

    LD_LIBRARY_PATH = library_paths()
    ELF_PATHS = elf_paths()

    if verbose:
        logging.info("Searching so files in paths: {}".format(LD_LIBRARY_PATH))

    so_files = find_all_so_files(LD_LIBRARY_PATH)

    if verbose:
        logging.info("Searching elf files in paths: {}".format(ELF_PATHS))

    elf_files = find_all_elf_files(ELF_PATHS, verbose)

    return (so_files, elf_files)


def find_all_so_files(paths, verbose=False):
    so_files = []

    """
    Get all shared object files in named dirs (only basenames returned)
    """

    for i in paths:
        so_files += find_so_files(i, verbose)

    so_files = list(set(so_files))

    return so_files

def find_so_files(directory, verbose=False):

    """
    Get all shared object files in named dir (only basenames returned)
    """

    import org.wayround.utils.format.elf

    ret = set()

    if not os.path.isdir(directory):
        logging.error(ValueError("Directory not exists `{}'".format(directory)))
        ret = set()
    else:

        files = os.listdir(directory)
        files_c = len(files)

        count = 0
        sos = 0

        for i in files:
            full_name = os.path.join(directory, i)

            if os.path.isfile(full_name):
                if full_name.find('.so') != -1:
                    elf = org.wayround.utils.format.elf.ELF(full_name)
                    if (
                        elf.is_elf_file
                        and elf.elf_type_name == 'ET_DYN'
                        ):
                        ret.add(i)
                        sos += 1

            count += 1

            if verbose:
                org.wayround.utils.file.progress_write(
                    "Looking for .so files: {} of {} files (sos: {}) in {}".format(
                        count,
                        files_c,
                        sos,
                        directory
                        )
                    )

    if verbose:
        print("")

    ret = list(ret)

    return ret


def find_all_elf_files(paths, verbose=False):

    """
    Get all elf files in named dirs (full paths returned)
    """

    elf_files = []

    for i in paths:
        elf_files += find_elf_files(i, verbose)

    elf_files = org.wayround.utils.path.realpaths(elf_files)

    elf_files = list(set(elf_files))

    return elf_files

def find_elf_files(directory, verbose=False):

    """
    Get all elf files in named dir (full paths returned)
    """

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

            elf = org.wayround.utils.format.elf.ELF(full_name)

            if os.path.isfile(full_name):
                if elf.is_elf:
                    ret.add(full_name)
                    elfs += 1

            count += 1

            if verbose:
                org.wayround.utils.file.progress_write(
                    "Looking for elf files: {} of {} files (elfs: {}) in {}".format(
                        count,
                        files_c,
                        elfs,
                        directory
                        )
                    )

    if verbose:
        print("")

    ret = list(ret)

    return ret
