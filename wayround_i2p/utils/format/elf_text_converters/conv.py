
"""
Convert substracted elf_enum.py lines to parsed list and dict
"""

import pprint


parsed_lines = []

t = open('123.txt').read()

t = t.replace('\t', ' ')

ft_lines = t.split('\n')

for i in ft_lines:

    splitted = i.split(' ')

    while ' ' in splitted:
        splitted.remove(' ')

    while '' in splitted:
        splitted.remove('')

    if len(splitted) != 0:
        if splitted[1] == '=':
            del splitted[1]

        hash = splitted.index('#')

        if hash != -1:
            splitted = splitted[: hash] + [' '.join(splitted[hash + 1:])]

        parsed_lines.append(splitted)

converted_dict = {}


print('{}'.format(pprint.pformat(parsed_lines)))

print('{')

for i in parsed_lines:
    print(
        "{} : {{\n\t'name': '{}',\n\t'descr': '{}' \n\t}},".format(
            i[0],
            i[0],
            i[2]))

print('}')
