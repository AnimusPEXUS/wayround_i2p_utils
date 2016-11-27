
# This module is only some test. it probably will be gone soon. it's not used
# in any my projects

import copy


class ClassApplicator:

    def __init__(self, obj, target_class):
        self._o = copy.copy(obj)
        self._o.__class__ = target_class
        return

    def __getattribute__(self, name):
        print("ClassApplicator getattribute: {}".format(name))
        return getattr(self._o, name)
