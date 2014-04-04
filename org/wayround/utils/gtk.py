
import logging
import os.path
import threading
import time

try:
    from gi.repository import Gtk
    from gi.repository import Gdk
except:
    pass
#    class InitException:
#
#        def __init__(self, *args, **kwargs):
#            raise Exception("Gtk not available")
#
#    class GtkIteratedLoop(InitException): pass
#    class MessageDialog(InitException): pass

else:

    class GtkSession:

        def __init__(self, force=False):

            if not force:
                raise Exception(
    "This code is deprecated but can be used to try Gtk.main() global locking"
                    )

            logging.debug("Init GtkSession")
            self._gtk_session_started = False
            self._thr = None

        def _thread(self):

            logging.debug("Thread Started")
            self._gtk_session_started = True
            Gtk.main()
            self._gtk_session_started = False
            logging.debug("Thread Exited")

        def start(self):

            if not self._gtk_session_started:
                logging.debug("Creating new thread")
                self._thr = threading.Thread(target=self._thread)
    #            self._thr = multiprocessing.Process(target=self._thread)
                self._thr.start()
                logging.debug("Started new thread")

        def stop(self):

            if self._gtk_session_started:
                logging.debug("Stopping main loop")
                Gtk.main_quit()
                logging.debug("Joining thread")
                self._thr.join()
                logging.debug("Joined thread")

    class TextView:

        def __init__(self):

            ui_file = os.path.join(
                os.path.dirname(__file__), 'ui', 'textview.glade'
                )

            ui = Gtk.Builder()
            ui.add_from_file(ui_file)

            self.ui = widget_dict(ui)

            self.ui['button1'].connect('clicked', self.onSaveAsActivated)

        def onSaveAsActivated(self, button):

            fc = Gtk.FileChooserDialog(
                "Select File To Save List",
                self.ui['window1'],
                Gtk.FileChooserAction.SAVE,
                (
                 Gtk.STOCK_SAVE, Gtk.ResponseType.OK,
                 Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL
                 )
                )

            rc_resp = fc.run()

            path = fc.get_filename()

            fc.destroy()

            if rc_resp == Gtk.ResponseType.OK:

                dialog_resp = Gtk.ResponseType.YES

                if os.path.exists(path) and os.path.isdir(path):
                    dialog_resp = Gtk.ResponseType.NO

                    dia = Gtk.MessageDialog(
                        self.ui['window1'],
                        Gtk.DialogFlags.MODAL,
                        Gtk.MessageType.ERROR,
                        Gtk.ButtonsType.OK,
                        "Directory not acceptable"
                        )

                    dia.run()
                    dia.destroy()

                elif os.path.exists(path) and os.path.isfile(path):

                    dialog_resp = Gtk.ResponseType.NO

                    dia = Gtk.MessageDialog(
                        self.ui['window1'],
                        Gtk.DialogFlags.MODAL,
                        Gtk.MessageType.QUESTION,
                        Gtk.ButtonsType.YES_NO,
                        "File exists. Rewrite?"
                        )

                    if dia.run() == Gtk.ResponseType.YES:
                        dialog_resp = Gtk.ResponseType.YES

                    dia.destroy()

                else:
                    pass

                if (
                    (os.path.exists(path)
                     and dialog_resp == Gtk.ResponseType.YES)
                    or
                    not os.path.exists(path)
                    ):

                    buff = self.ui['textview1'].get_buffer()
                    txt = buff.get_text(
                        buff.get_start_iter(), buff.get_end_iter(), False
                        )

                    try:
                        f = open(path, 'w')
                    except:
                        dia = Gtk.MessageDialog(
                            self.ui['window1'],
                            Gtk.DialogFlags.MODAL,
                            Gtk.MessageType.ERROR,
                            Gtk.ButtonsType.OK,
                            "Couldn't rewrite file `{}'".format(path)
                            )

                        dia.run()
                        dia.destroy()
                    else:

                        f.write(txt)
                        f.close()

            return

    class GtkIteratedLoop:

        # NOTE: this class is tending to be deprecated. we must obey to use
        #       Gtk+ threading rules

        def __init__(self, sleep_fraction=0.01):
            self._exit_event = threading.Event()
            self._started = False
            self._sleep_fraction = sleep_fraction

        def wait(self, timeout=None):

            if self._started:
                self._exit_event.wait(timeout)
            else:
                self._started = True

                self._exit_event.clear()

                while not self._exit_event.is_set():
                    while Gtk.events_pending():
                        Gtk.main_iteration_do(False)

                    time.sleep(self._sleep_fraction)

                self._started = False

        def stop(self):
            self._exit_event.set()

#    class GtkIteratedLoop:
#
#        def __init__(self, sleep_fraction=0.01):
#            self._exit_event = threading.Event()
#            self._started = False
#            self._sleep_fraction = sleep_fraction
#
#        def wait(self, timeout=None):
#
#            if self._started:
#                self._exit_event.wait(timeout)
#            else:
#                self._started = True
#
#                self._exit_event.clear()
#
#                Gtk.main()
#
##                while not self._exit_event.is_set():
##                    while Gtk.events_pending():
##                        Gtk.main_iteration_do(False)
##
##                    time.sleep(self._sleep_fraction)
#
#                self._started = False
#
#        def stop(self):
#            Gtk.main_quit()
#            self._exit_event.set()

    class MessageDialog(Gtk.MessageDialog):

        """
        Documentation same as for Gtk.MessageDialog
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.set_modal(True)
            self.set_transient_for(args[0])
            #            self.set_destroy_with_parent(True)
            self.set_type_hint(Gdk.WindowTypeHint.DIALOG)

            self.wayround_org_response = Gtk.ResponseType.NONE
            self.wayround_org_iteration_loop = GtkIteratedLoop()

        def run(self):

            self.show_all()

            self.connect('close', self.wayround_org_close_listener)
            self.connect('response', self.wayround_org_response_listener)

            self.wayround_org_iteration_loop.wait()

            return self.wayround_org_response

        def destroy(self, *args, **kwargs):
            self.wayround_org_iteration_loop.stop()
            self.wayround_org_iteration_loop = None
            return super().destroy(*args, **kwargs)

        def wayround_org_response_listener(self, dialog, response_id):
            self.wayround_org_response = response_id
            self.wayround_org_iteration_loop.stop()

        def wayround_org_close_listener(self, dialog):
            self.wayround_org_iteration_loop.stop()

    class Waiter:

        def __init__(
            self,
            wait_or_join_meth,
            ret_val_good_for_loop,
            is_alive_meth=None,
            timeout=0.2,
            waiter_sleep_time=0.01
            ):

            if not callable(wait_or_join_meth):
                raise TypeError("`wait_or_join_meth' must be callable")

            if is_alive_meth != None and not callable(is_alive_meth):
                raise TypeError("`is_alivemeth' must be callable")

            if is_alive_meth != None and waiter_sleep_time == 0:
                raise ValueError(
            "if `is_alivemeth' is set, `waiter_sleep_time' must not be 0"
                    )

            self._timeout = timeout
            self._is_alive_meth = is_alive_meth
            self._wait_or_join_meth = wait_or_join_meth
            self._waiter_sleep_time = waiter_sleep_time
            self._ret_val_good_for_loop = ret_val_good_for_loop
            self._thread = None
            self._stop_event = threading.Event()
            self._result = None
            self._iterated_loop = GtkIteratedLoop(
                sleep_fraction=waiter_sleep_time
                )

        def _start(self):

            if self._thread == None:

                self._thread = threading.Thread(
                    target=self._waiter,
                    )
                self._thread.start()

        def stop(self):
            self._iterated_loop.stop()
            self._stop_event.set()

        def wait(self, timeout=None):
            self._start()
            self._iterated_loop.wait(timeout)

        def _waiter(self):

            while True:

                if self._is_alive_meth != None:
                    if not self._is_alive_meth():
                        break
                else:

                    if (self._wait_or_join_meth(self._timeout)
                        != self._ret_val_good_for_loop):
                        break

                while Gtk.events_pending():
                    Gtk.main_iteration_do(False)

                time.sleep(self._waiter_sleep_time)

                if self._stop_event.is_set():
                    break

            self.stop()
            self._thread = None
            return

    class RelatedWindowCollector:

        def __init__(self):

            self._lock = threading.Lock()
            self.clear(init=True)

        def clear(self, init=False):

            self._constructor_cbs = {}

            self._singles = {}
            self._multiples = set()

        def _window_methods_check(self, window):

            for i in ['run', 'show', 'destroy']:

                if not hasattr(window, i):
                    raise KeyError(
                        "{} has not attribute `{}'".format(window, i)
                        )

                if not callable(getattr(window, i)):
                    raise KeyError(
                        "`{}' not callable in {}".format(i, window)
                        )

            return

        def set_constructor_cb(self, name, cb, single=True):

            if not isinstance(name, str):
                raise ValueError("`name' must be str")

            if not isinstance(single, bool):
                raise ValueError("`single' must be bool")

            if not callable(cb):
                raise ValueError("`cb' must be callable")

            self._lock.acquire()

            if name in self._constructor_cbs:
                logging.warning("{}:Redefining `{}'".format(self, name))

            self._constructor_cbs[name] = {'cb': cb, 'single': single}

            self._lock.release()

            return

        def _check_name(self, name):

            if not name in self._constructor_cbs:
                raise KeyError(
                    "{}:Constructor for `{}' not registered".format(
                        self,
                        name
                        )
                    )

            return

        def get(self, name):

            self._check_name(name)

            ret = None

            if name in self._singles:
                ret = self._singles[name]

            return ret

        def destroy_window(self, name):
            res = self.get(name)
            if res != None:
                res.destroy()
            return

        def show_threaded(self, name, *args, **kwargs):

            self._check_name(name)

            threading.Thread(
                name="Thread for window `{}'".format(name),
                target=self.show,
                args=(name,) + args,
                kwargs=kwargs
                ).start()

            return

        def show(self, name, *args, **kwargs):

            self._check_name(name)

            ret = None

            self._lock.acquire()

            try:
                cdata = self._constructor_cbs[name]

                if cdata['single']:
                    if name in self._singles:
                        self._singles[name].show()
                    else:
                        window = cdata['cb']()
                        self._window_methods_check(window)
                        self._singles[name] = window
                        self._lock.release()
                        ret = window.run(*args, **kwargs)
                        self._lock.acquire()
                        if name in self._singles:
                            self._singles[name].destroy()
                            del self._singles[name]

                else:
                    window = cdata['cb']()
                    self._window_methods_check(window)
                    self._multiples.add(window)
                    self._lock.release()
                    ret = window.run(*args, **kwargs)
                    self._lock.acquire()
                    while window in self._multiples:
                        self._multiples.remove(window)

            except:
                logging.exception("Exception")

            self._lock.release()

            return ret

        def destroy_windows(self):

            self._lock.acquire()

            names = list(self._singles)
            for i in names:
                self._singles[i].destroy()
                del self._singles[i]

            for i in list(self._multiples):
                i.destroy()
                self._multiples.remove(i)

            self._lock.release()

            return

        def destroy(self):
            self.destroy_windows()
            self.clear()

    def text_view(text, title=''):

        tw = TextView()

        tb = Gtk.TextBuffer()
        tb.set_text(str(text))

        tw.ui['textview1'].set_buffer(tb)

        tw.ui['window1'].set_title(str(title))

        tw.ui['window1'].show_all()

        return

    def widget_dict(builder):

        ret = {}

        all_objects = builder.get_objects()

        for i in all_objects:
            if isinstance(i, Gtk.Buildable):
                ret[Gtk.Buildable.get_name(i)] = i

        return ret

    def list_view_select_and_scroll_to_name(treeview, name):

        sel = treeview.get_selection()
        model = treeview.get_model()
        ind = -1
        if model:
            for i in model:
                ind += 1
                if i[0] == name:
                    path = Gtk.TreePath.new_from_string(str(ind))
                    sel.select_path(path)
                    treeview.scroll_to_cell(path, None, True, 0.5, 0.5)
                    break

        return

    def process_events():
        while Gtk.events_pending():
            Gtk.main_iteration_do(False)
