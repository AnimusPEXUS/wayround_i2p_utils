
import sys
import re
import os.path

registry = []

h_f = sys.argv[1]

if not h_f.endswith('.h'):
    raise ValueError("file name not ends with .h")

else:

    h = open(h_f, 'r')

    h_lines = h.readlines()

    h.close()

    h_name = os.path.basename(h_f)[0:-2]

    pxd_file_name = h_name + '_enum.py'

    py_fi = open(pxd_file_name, 'w')

    line = ''

    for i in h_lines:

        if i.startswith('#define') or i.startswith('#DEFINE'):
            line = i

            re_res = re.match(
                '^(#\w*?)\s+(?P<name>\w+)\s+(?P<value>.*?)\s*(/\*(?P<comment>.*))?$', line
                )

            if re_res:
                value = re_res.group('value')

                typ = 'int'
                if (value.startswith("'") and value.endswith("'")) or \
                    (value.startswith('"') and value.endswith('"')):
                    if len(value) > 3:
                        typ = 'string'


                registry.append(
                    {
                        'type': typ,
                        'name': re_res.group('name'),
                        'value':value,
                        'comment':re_res.group('comment')
                        }
                    )

    spc1 = 1
    for i in registry:
        if len(i['name']) > spc1:
            spc1 = len(i['name'])

    spc2 = 1
    for i in registry:
        if len(i['value']) > spc2:
            spc2 = len(i['value'])

    writting = None

    for i in registry:

        if i['type'] == 'string':

            writting = 'string'

            n_l = len(i['name'])
            v_l = len(i['value'])

            comment = i['comment']
            if comment == None:
                comment = ''

            comment = comment.replace('*/', '')

            py_fi.write(
                "{name} {spc1} = {value}{spc2} # {comment}\n".format(
                    name=i['name'],
                    value=i['value'],
                    comment=comment,
                    spc1=(' ' * spc1)[n_l:],
                    spc2=(' ' * spc2)[v_l:]
                    )
                )

#    for i in registry:

        if i['type'] == 'int':

            writting = 'int'

            n_l = len(i['name'])
            v_l = len(i['value'])

            comment = i['comment']
            if comment == None:
                comment = ''

            comment = comment.replace('*/', '')

            py_fi.write(
                "{name} {spc1} = {value}{spc2} # {comment}\n".format(
                    name=i['name'],
                    value=i['value'],
                    comment=comment,
                    spc1=(' ' * spc1)[n_l:],
                    spc2=(' ' * spc2)[v_l:]
                    )
                )



    py_fi.close()
