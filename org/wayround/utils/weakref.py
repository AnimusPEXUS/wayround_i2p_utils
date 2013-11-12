
import weakref
import logging
import threading


class WeakMethod:

    def __init__(self, method, callback=None):

        if not callable(method):
            raise ValueError("callable must be provided")

        if not hasattr(method, '__self__'):
            raise ValueError("provided callable not a method")

        if callback and not callable(callback):
            raise ValueError("callback must be callable")

        self._debug = False

        self._object = weakref.ref(method.__self__, self._object_finalizes)

        if self._debug:
            logging.debug(
                "{} installed weakref: {}".format(self, self._object)
                )

        self._callback = callback
        self._method_name = method.__name__

        return

    def _object_finalizes(self, wr):

        if self._debug:
            logging.debug("{} finalizing method: {}".format(self, wr))

        self._object = None
        self._method_name = None

        if self._callback:
            threading.Thread(
                target=self._callback,
                args=(self,)
                ).start()

    def __call__(self):

        ret = None

        if self._object:
            ret = getattr(self._object(), self._method_name, None)

        return ret
