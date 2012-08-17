
import re

def append(indict, what_to_append):

    last_name = max(indict)

    re_val = re.match(r'.*_auto_appended_key_(\d{10})', last_name)

    placement_i = 0
    if re_val:
        placement_i = re_val.group(1) + 1

    new_key = '{last_placer_child_name}_auto_appended_key_{num!d010}' % {
        'last_placer_child_name': last_name,
        'num': placement_i
        }

    indict[new_key] = what_to_append

    return
