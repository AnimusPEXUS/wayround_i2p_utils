
import wayround_org.utils.types

LIST_OF_STR = {'t': list, '.': {'t': str}}
SET_OF_STR = {'t': set, '.': {'t': str}}


def is_list_of_str(value):
    ret = wayround_org.utils.types.struct_check(value, LIST_OF_STR)
    return ret


def is_set_of_str(value):
    ret = wayround_org.utils.types.struct_check(value, SET_OF_STR)
    return ret
