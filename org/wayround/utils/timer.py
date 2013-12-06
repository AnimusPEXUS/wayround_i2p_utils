
import threading
import time


class LoopedTimer:

    def __init__(self, interval, action, args, kwargs):

        self._interval = interval
        self._action = action
        self._args = args
        self._kwargs = kwargs

        self._thread = None

        self._stop_event = threading.Event()
        self._stoped_event = threading.Event()

    def start(self):
        if not self._thread:
            self._stop_event.clear()
            self._stoped_event.clear()
            self._thread = threading.Thread(
                target=self._thread_target
                )
            self._thread.start()

    def stop(self):

        self._stop_event.set()
        self._stoped_event.wait()

    def _thread_target(self):

        while True:
            if self._stop_event.is_set():
                break

            time.sleep(self._interval)

            if self._stop_event.is_set():
                break

            self._action(*self._args, **self._kwargs)

        self._thread = None

        self._stoped_event.set()
