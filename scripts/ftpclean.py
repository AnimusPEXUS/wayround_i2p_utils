
import getopt
import os.path
import sys

from org.wayround.utils import ftpwalk


# TODO: cleanups and rewrites required

def main(server, fdir, tdir,verbose=False):


    fw = ftpwalk.FTPWalkSole(server, verbose)

    fw.connect()

    fdir = fdir.strip('/')
    # print 'fdir:'+fdir

    tdir = os.path.abspath(tdir)
    # print 'tdir:'+tdir

    rm_dirs = []
    rm_files = []

    for i in os.walk(tdir):

        i_p_abs = os.path.abspath(i[0])

        # print 'i[0]:'+i[0]
        i_p_rel = os.path.relpath(i[0], tdir)
        # print 'i_p_rel:'+i_p_rel

        # ftp_abs(must be a dir!) = root + fdir + (relative path from tdir to i[0])
        ftp_abs = ftpwalk.normpath(os.path.join('/', fdir, i_p_rel))
        # print 'ftp_abs:'+ftp_abs

        for j in i[1]:
            # print 'i[1]:'+j
            j_ftp_dir = ftpwalk.normpath(os.path.join('/', ftp_abs, j))
            # j_ftp_dir = ftpwalk.normpath(os.path.join(i_p_rel, j))
            # print 'j_ftp_dir:'+j_ftp_dir

            e = fw.is_dir(j_ftp_dir)

            if isinstance(e, str):
                if e == 'not connected':
                    raise Exception('Connection lost')

                elif e == 'errors':
                    raise Exception("Some error while walking ftp server dirs")

                else:
                    raise Exception("Some unknown error")

            if not isinstance(e, bool):
                raise TypeError(
                    "Internal error: ftpwalk library returned wrong response: {}".format(repr(e))
                    )


            if not e:
                tmp_name = ftpwalk.normpath(os.path.join(i_p_abs, j))
                if os.path.islink(tmp_name):
                    rm_files.append(tmp_name)
                else:
                    rm_dirs.append(tmp_name)
                del tmp_name

        for j in i[2]:
            # print 'i[2]:'+j
            j_ftp_file = ftpwalk.normpath(os.path.join('/', ftp_abs, j))
            # j_ftp_file = ftpwalk.normpath(os.path.join(i_p_rel, j))
            # print 'j_ftp_file1:'+j_ftp_file

            e = fw.is_not_dir(j_ftp_file)

            if isinstance(e, str):
                if e == 'not connected':
                    raise Exception("Connection lost")

                elif e == 'errors':
                    raise Exception("Some error while walking ftp server dirs")

                else:
                    raise Exception("Some unknown error")

            if not isinstance(e, bool):
                raise TypeError(
                    "Internal error: ftpwalk library returned wrong response: {}".format(repr(e))
                    )


            if not e:
                rm_files.append(ftpwalk.normpath(os.path.join(i_p_abs, j)))

    rm_dirs.sort()
    rm_files.sort()

    return (rm_dirs, rm_files)

def show_help(output_formats):
    r = """
 ftpcleaner [-f format] ftp.host ftpbasedir localftpbasedir

  This utilitie walks through files in localftpbasedir looking for
  thous which not found in ftpbasedir.

  On the end, the list of dirs and files is returned.

       -f fmt              Output format. Can be one of: %(formats)s.
       -v --verbose        Verbose ftp traversing.

""" % {'formats': ', '.join(output_formats)}
    print(r)

if __name__ == '__main__':

    __file__ = os.path.abspath(__file__)
    PPWD = os.path.dirname(__file__)

    output_formats = ['bash', 'sh', 'python', 'py-lst', 'lines', 'tlines']

    opts, args = getopt.gnu_getopt(sys.argv[1:], 'vf:', ['help', 'verbose'])

    for i in opts:
        if i[0] == '--help':
            show_help(output_formats)
            exit(0)

    output_format = 'bash'
    verbose = False

    for i in opts:
        if i[0] == '-f':
            if not i[1] in output_formats:
                print("-e- Wrong -f argument. Right values are: %(vals)s" % {
                    'vals': ', '.join(output_formats)})
                exit(1)
            else:
                output_format = i[1]

        if i[0] == '-v' or i[0] == '--verbose':
            verbose = True

    if len(args) != 3:
        print('-e- must be exactly 3 arguments')
        print()
        show_help(output_formats)
    elif not os.path.isdir(args[2]):
        print('-e- local ftp directory does not exists')
    else:
        tdir = os.path.abspath(args[2])
        result = main(args[0], args[1], tdir, verbose)


        ret = ''

        if output_format == 'bash' or output_format == 'sh':
            ret = '''\
#!/bin/bash

# Here come directories, which will be removed

'''
            for i in result[0]:
                ret += "rm -rfv '%(dir)s'\n" % {'dir': i}

            ret += '''\

# Here come files, which will be removed

'''

            for i in result[1]:
                ret += "rm -v '%(file)s'\n" % {'file': i}


            ret += '''\

# THE END

exit 0
'''
        elif output_format == 'python':
            ret = '''\
#!/usr/bin/python2.6
# -*- coding: utf-8 -*-


import os
import os.path
import shutil

'''
            for i in result[0]:
                ret += '''\
print '-i- removing directory %%(name)s' %% {'name' : '%(name)s'}
try:
    shutil.rmtree('%(name)s')
except:
    print '-e- exception'

''' % {'name': i}

            ret += '\n\n'

            for i in result[1]:
                ret += '''\
print '-i- removing file %%(name)s' %% {'name' : '%(name)s'}
try:
    os.unlink('%(name)s')
except:
    print '-e- exception'

''' % {'name': i}

            ret += '''\
exit(0)
'''

        elif output_format == 'py-lst':

            dirs = []
            for i in result[0]:
                dirs.append("""ur'%(name)s'""" % {'name': i})

            dirs = ', '.join(dirs)

            files = []
            for i in result[1]:
                files.append("""ur'%(name)s'""" % {'name': i})

            files = ', '.join(files)

            ret = '''\
#!/usr/bin/python2.6
# -*- coding: utf-8 -*-

dirs = [%(dirs)s]

files = [%(files)s]

''' % {'dirs': dirs, 'files': files}

        elif output_format == 'lines':

            ret = ''

            for i in result[0]:
                ret += '%(name)s\n' % {'name': i}

            for i in result[1]:
                ret += '%(name)s\n' % {'name': i}

        elif output_format == 'tlines':

            ret = ''

            for i in result[0]:
                ret += 'd%(name)s\n' % {'name': i}

            for i in result[1]:
                ret += '-%(name)s\n' % {'name': i}


        else:
            print('-e- Control not suposed tobe here')
            raise Exception

        print(ret)
else:
    print('-i- This file is not assumed to be used as a library O_o')
    raise Exception

exit(0)
