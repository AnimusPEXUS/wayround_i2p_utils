
import logging

def is_wrong_opts(opts, allowed_opts):

    ret = 0

    if not isinstance(opts, dict):
        raise TypeError("opts must be dict, not {}".format(type(opts)))

    if not isinstance(allowed_opts, list):
        raise TypeError("allowed_opts must be list, not {}".format(type(allowed_opts)))

    for i in list(opts.keys()):
        if not i in allowed_opts:
            logging.error("Wrong option `{}'".format(i))
            ret = 1

    return ret
