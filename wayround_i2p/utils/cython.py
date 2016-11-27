

import subprocess
import os.path


def cythonize(file_list, verbose=True, cython_options=None):
    """
    My analog to cythonize, as original one does not support pep-420
    (by status on Sun Jul 10 03:45:19 MSK 2016)

    """
    ret = 0

    if cython_options is None:
        cython_options = []

    init_names = []

    for i in file_list:

        dir_name = os.path.dirname(i)

        work_on_inits = len(dir_name) != 0
        dir_name_splitted = dir_name.split(os.path.sep)

        if len(dir_name_splitted) != 0:
            for j in range(len(dir_name_splitted)):
                if j == 0:
                    continue
                init_name = os.path.join(
                    os.path.sep.join(
                        dir_name_splitted[0:j]
                        ),
                    '__init__.py'
                    )
                #print("touching {}".format(init_name))
                if not os.path.isfile(init_name):
                    init_names.append(init_name)

    for i in init_names:
        with open(i, 'w'):
            pass

    for i in file_list:

        dir_name = os.path.dirname(i)
        basename = os.path.basename(i)

        i_target = '{}.c'.format(i[:-4])

        is_stat = os.stat(i)
        it_stat = None
        if os.path.isfile(i_target):
            it_stat = os.stat(i_target)

        if it_stat is None or it_stat.st_mtime < is_stat.st_mtime:
            pass
        else:
            continue

        cmd = ['cython'] + cython_options + [i]
        if verbose:
            print("    {}".format(' '.join(cmd)))
        p = subprocess.Popen(cmd)
        res = p.wait()
        # res=0

        if res != 0:
            ret = 1
            break

    for i in init_names:
        os.unlink(i)

    return ret
