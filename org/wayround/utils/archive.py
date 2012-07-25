
import os.path
import subprocess
import sys
import tarfile
import io
import logging


import org.wayround.utils.stream
import org.wayround.utils.exec
import org.wayround.utils.file


# TODO: Add safeness to streamed functions
# TODO: Rework old functions to new tune

CANONICAL_COMPRESSORS = frozenset(['xz', 'lzma', 'bzip2', 'gz'])

def _extract_zip(file_name, output_dir):

    try:
        proc = org.wayround.utils.exec.simple_exec(
            'unzip', stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=sys.stderr,
            options=['-qq', file_name, '-d', output_dir],
            )
    except:
        logging.exception("unzip start error")

    return proc.wait()


def _extract_tar_7z(file_name, output_dir):

    try:
        proc_7z = org.wayround.utils.exec.simple_exec(
            '7z',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=None,
            options=['x', '-so', file_name],
            )
    except:
        logging.exception("7z start error")
        raise
    else:

        try:
            proc_tar = org.wayround.utils.exec.simple_exec(
                'tar',
                stdin=proc_7z.stdout,
                stdout=subprocess.PIPE,
                stderr=None,
                options=[
                    '--no-same-owner',
                    '--no-same-permissions',
                    '-xlRC' ,
                    output_dir
                    ]
                )
        except:
            logging.exception("tar start error")
            raise
        else:
            proc_tar.wait()

        finally:
            proc_tar.terminate()

        proc_7z.wait()

    return


def _extract_tar_arch(file_name, output_dir, arch):

    ret = extract_tar_canonical(
        file_name, output_dir, arch,
        verbose_tar=True, verbose_compressor=True
        )

    return ret


def extract(file_name, output_dir):

    ret = None

    if file_name.endswith('.tar.lzma'):
        ret = _extract_tar_arch(file_name, output_dir, 'lzma')

    elif file_name.endswith('.tar.bz2'):
        ret = _extract_tar_arch(file_name, output_dir, 'bzip2')

    elif file_name.endswith('.tar.gz'):
        ret = _extract_tar_arch(file_name, output_dir, 'gzip')

    elif file_name.endswith('.tar.xz'):
        ret = _extract_tar_arch(file_name, output_dir, 'xz')

    elif file_name.endswith('.tar.7z'):
        ret = _extract_tar_7z(file_name, output_dir)

    elif file_name.endswith('.tgz'):
        ret = _extract_tar_arch(file_name, output_dir, 'gzip')

    elif file_name.endswith('.zip'):
        # TODO: what's this?
        pass

    elif file_name.endswith('.7z'):
        # TODO: what's this?
        pass

    else:
        logging.error("unsupported extension")

    if ret == None:
        logging.error("Not implemented")
        raise Exception

    return ret


def canonical_compressor(
    compressor,
    stdin=None,
    stdout=None,
    stderr=None,
    verbose=False,
    options=[]
    ):

    """
    Canonical compressor shortcut

    Works only with `{}' compressors which
    must support -0 .. -9 , -v and -d options in canonical way
    """.format(
        repr(
             list(CANONICAL_COMPRESSORS)
             )
        )


    if not compressor in CANONICAL_COMPRESSORS:
        raise ValueError(
            "canonical_compressor supports only `{}'".format(
                repr(
                     list(CANONICAL_COMPRESSORS)
                     )
                )
            )

    ret = org.wayround.utils.exec.process_stream(
        compressor,
        stdin=stdin,
        stdout=stdout,
        stderr=stderr,
        options=options,
        verbose=verbose
        )

    return ret


def archive_tar_canonical(
    dirname, output_filename,
    compressor,
    verbose_tar=False,
    verbose_compressor=False
    ):

    ret = 0
    try:
        fobj = open(output_filename, 'wb')
    except:
        logging.exception("Error opening file for write")
        ret = 1
    else:
        try:
            ret = archive_tar_canonical_fobj(
                dirname, fobj, compressor,
                verbose_tar, verbose_compressor
                )
        finally:
            fobj.close()
    return ret


def archive_tar_canonical_fobj(
    dirname,
    output_fobj,
    compressor,
    verbose_tar=False,
    verbose_compressor=False
    ):

    ret = 0


    dirname = os.path.abspath(dirname)

    if not os.path.isdir(dirname):
        logging.error("Not a directory: %(dirname)s" % {
            'dirname': dirname
            })
        ret = 1
    else:

        options = []
        stderr = None

        if verbose_tar:
            options += ['-v']
            stderr = sys.stderr

        options += ['-c', '.']

        try:
            tarproc = org.wayround.utils.exec.simple_exec(
                'tar',
                options=options,
                stdin=None,
                stdout=subprocess.PIPE,
                cwd=dirname,
                bufsize=2 * 1024 ** 2,
                stderr=stderr
                )
        except:
            logging.exception("tar start error")
            ret = 2
        else:

            try:
                options = []
                stderr = None

                if verbose_compressor:
                    options += ['-v']
                    stderr = sys.stderr

                options += ['-9']

                if canonical_compressor(
                    compressor,
                    options=options,
                    stdin=tarproc.stdout,
                    stdout=output_fobj,
                    stderr=stderr,
                    verbose=verbose_compressor
                    ) != 0:
                    ret = 3
            finally:
                tarproc.terminate()

            tarproc.wait()

    return ret


def extract_tar_canonical(
    input_filename,
    dirname,
    compressor,
    verbose_tar=False,
    verbose_compressor=False
    ):

    ret = 0
    try:
        fobj = open(input_filename, 'rb')
    except:
        logging.exception("Error opening file for read")
        ret = 1
    else:
        try:
            ret = extract_tar_canonical_fobj(
                fobj, dirname, compressor, verbose_tar, verbose_compressor
                )
        finally:
            fobj.close()
    return ret


def extract_tar_canonical_fobj(
    input_fobj,
    dirname,
    compressor,
    verbose_tar=False,
    verbose_compressor=False
    ):

    dirname = os.path.abspath(dirname)

    ret = org.wayround.utils.file.create_if_not_exists_dir(dirname)

    if ret != 0:
        logging.error("Error while checking destination dir: %(dirname)s" % {
            'dirname': dirname
            })
        ret = 1
    else:

        # tar
        options = []

        if verbose_tar:
            options += ['-v']

        options += ['-x']

        tarproc = None
        try:
            tarproc = org.wayround.utils.exec.simple_exec(
                "tar",
                options=options,
                stdin=subprocess.PIPE,
                stdout=sys.stdout,
                cwd=dirname,
                bufsize=0,
                stderr=sys.stdout
                )
        except:
            logging.exception("tar error detected")
            ret = 2
        else:

            try:
                options = []

                if verbose_compressor:
                    options += ['-v']

                options += ['-d']

                if canonical_compressor(compressor,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        options=options,
                        bufsize=0,
                        stderr=sys.stderr
                        ) != 0:
                    ret = 3

            finally:
                tarproc.terminate()

            tarproc.wait()

    return ret


def pack_dir_contents_tar(
    dirname,
    output_filename,
    verbose_tar=False
    ):

    ret = 0

    dirname = os.path.abspath(dirname)

    if not os.path.isdir(dirname):
        logging.error("Not a directory: %(dirname)s" % {
            'dirname': dirname
            })
        ret = 1
    else:
        try:
            outf = open(output_filename, 'wb')
        except:
            logging.exception(
                "Coundn't open `{}' for write".format(output_filename)
                )
            ret = 2
        else:

            try:
                options = []
                stderr = subprocess.PIPE

                if verbose_tar:
                    options += ['-v']
                    stderr = sys.stderr

                options += ['-c', '.']

                tarproc = org.wayround.utils.exec.simple_exec(
                    "tar",
                    options=options,
                    stdin=None,
                    stdout=outf,
                    cwd=dirname,
                    bufsize=2 * 1024 ** 2,
                    stderr=stderr
                    )

                tarproc.wait()
            finally:
                outf.close()
    return ret


def tar_get_member(tarf, cont_name):
    ret = None

    try:
        ret = tarf.getmember(cont_name)
    except:
        logging.exception("Can't get tar member")
        ret = 1

    return ret


def tar_member_extract_file(tarf, member):
    ret = None

    try:
        ret = tarf.extractfile(member)
    except:
        logging.exception("Can't get tar member")
        ret = 1

    return ret


def tar_member_get_extract_file(tarf, cont_name):

    ret = None

    member = tar_get_member(tarf, cont_name)

    if not isinstance(member, tarfile.TarInfo):
        ret = 1
    else:
        fileobj = tar_member_extract_file(tarf, member)

        if not isinstance(fileobj, tarfile.ExFileObject):
            ret = 2
        else:
            ret = fileobj

    return ret


def tar_member_get_extract_file_to(tarf, cont_name, output_filename):

    ret = 0
    try:
        fd = open(output_filename, 'w')
    except:
        logging.error("Error creating output file %(name)s" % {
            'name': output_filename
            })
        ret = 1
    else:
        try:
            fobj = tar_member_get_extract_file(
                tarf, cont_name
                )
            try:
                if not isinstance(fobj, tarfile.ExFileObject):
                    logging.error("Error getting %(name)s from tar" % {
                        'name': cont_name
                        })
                    ret = 2
                else:
                    org.wayround.utils.stream.cat(fobj, fd)
            finally:
                fobj.close()
        finally:
            fd.close()

    return ret


def xzcat(stdin):

    ret = 0

    comprproc = None
    try:
        comprproc = org.wayround.utils.exec.simple_exec(
            'xz',
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            options=['-d'],
            bufsize=0,
            stderr=sys.stderr
            )
    except:
        ret = 1
    else:
        outstr = io.StringIO()

        try:
            cat_p1 = org.wayround.utils.stream.cat(
                stdin,
                comprproc.stdin,
                threaded=True,
                close_output_on_eof=True
                )
            cat_p1.start()

            cat_p2 = org.wayround.utils.stream.cat(
                comprproc.stdout,
                outstr,
                threaded=True,
                close_output_on_eof=False
                )
            cat_p2.start()

            comprproc.wait()
            cat_p1.join()
            cat_p2.join()

            if comprproc.returncode != 0:
                ret = comprproc.returncode

            if ret == 0:
                #outstr.seek(0)
                ret = outstr.getvalue()
        finally:
            outstr.close()
            del(outstr)

    return ret

