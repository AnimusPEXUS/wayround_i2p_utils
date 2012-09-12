
import copy

def remove_all_values(lst, lst2):
    for i in lst2:
        while i in lst:
            lst.remove(i)

def list_lstrip(lst, lst2):
    lst = copy.copy(lst)
    while (len(lst) > 0
           and  lst[0] in lst2):
        del lst[0]
    return lst

def list_rstrip(lst, lst2):
    lst = copy.copy(lst)
    while (len(lst) > 0
           and  lst[-1] in lst2):
        del lst[-1]
    return lst

def list_strip(lst, lst2):
    return list_lstrip(list_rstrip(copy.copy(lst), lst2), lst2)

def list_sort(lst, cmp=None):

    lst_l = len(lst)

    i = -1
    j = -1
    x = None


    if lst_l > 1:
        while True:
            if i == lst_l - 2:
                break
            i += 1
            j = i
            while True:

                if j == lst_l - 1:
                    break
                j += 1

                if cmp == None:
                    if lst[i] > lst[j]:
                        x = lst[i]
                        lst[i] = lst[j]
                        lst[j] = x
                else:
                    cmp_r = cmp(lst[i], lst[j])
                    if cmp_r == +1:
                        x = lst[i]
                        lst[i] = lst[j]
                        lst[j] = x

    return

def list_remove_empty_lines(lst):
    ret = []
    for i in lst:
        if i != '':
            ret.append(i)
    return ret

def list_remove_duplicated_lines(lst):
    ret = list(set(lst))
    return ret

def list_strip_lines(lst):
    ret = []
    for i in lst:
        ret.append(i.strip())
    return ret

def list_strip_remove_empty_remove_duplicated_lines(lst):
    return list_remove_duplicated_lines(
        list_remove_empty_lines(
            list_strip_lines(copy.copy(lst))
            )
        )

