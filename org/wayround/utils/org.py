

class ObjectRegistry: pass
#
#    def __init__(self):
#
#        self.clear()
#
#    def clear(self):
#
#        self._reg = {}
#
#    def _name_check(self, name):
#
#        if not isinstance(name, str):
#            raise TypeError("`name' must be a str")
#
#        if not name.isidentifier():
#            raise ValueError("`name' must be an identifier")
#
#    def __setitem__(self, name, obj):
#
#        self._name_check(name)
#
#        self._reg[name] = obj
#
#
#    def __getitem__(self, name, default = None):
#
#        self._name_check(name)
#
#        return self._reg.get(name, default)
#
#    def __delitem__(self, name):
#
#        self._name_check(name)
#
#        del self._reg[name]
