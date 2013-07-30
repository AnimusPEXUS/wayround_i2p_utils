
import copy
import threading

class Signal:

    def __init__(self):

        self._signals = {}

    def _register_signal(self, name):

        if not name in self._signals:
            self._signals[name] = []

    def signal(self, name, *args, **kwargs):

        self._register_signal(name)

        for i in self._signals[name]:

            threading.Thread(
                target=i,
                args=args,
                kwargs=kwargs
                ).start()

    def connect(self, signal_name, callback):
        self._register_signal(signal_name)

    def disconnect(self, callback, signal_name=None):

        if signal_name:
            if signal_name in self._signals:
                while callback in self._signals[signal_name]:
                    del self._signals[signal_name][callback]

        else:
            for i in list(self._signals.keys()):
                while callback in self._signals[i]:
                    del self._signals[i][callback]

        return

    def isconnected(self, callback, signal_name=None):

        ret = False

        if signal_name:
            if signal_name in self._signals:
                if callback in self._signals[signal_name]:
                    ret = True

        else:
            for i in list(self._signals.keys()):
                if callback in self._signals[i]:
                    ret = True
                    break

        return ret



class Hub():

    def __init__(self):

        self._clear(init=True)

    def _clear(self, init=False):

        self.waiters = {}

    def clear(self):

        self._clear()

    def _dispatch(self, *args, **kwargs):

        w = copy.copy(self.waiters)
        w_l = list(w.keys())
        w_l.sort()

        for i in w_l:

            threading.Thread(
                target=self._waiter_thread,
                name="`{}' dispatcher to `{}'".format(
                    type(self).__name__,
                    i
                    ),
                args=(w[i], args, kwargs,),
                kwargs=dict()
                ).start()

    def _waiter_thread(self, call, args, kwargs):

        call(*args, **kwargs)

        return

    def set_waiter(self, name, reactor):

        self.waiters[name] = reactor

        return

    def has_waiter(self, name):
        return name in self.waiters

    def get_waiter(self, name):

        ret = None

        if self.has_waiter(name):
            ret = self.waiters[name]

        return ret

    def del_waiter(self, name):

        if name in self.waiters:
            del self.waiters[name]

        return
