
import os.path
import threading
import logging
import time

def widget_dict(builder):

    from gi.repository import Gtk

    ret = {}

    all_objects = builder.get_objects()

    for i in all_objects:
        if isinstance(i, Gtk.Buildable):
            ret[Gtk.Buildable.get_name(i)] = i

    return ret

def list_view_select_and_scroll_to_name(treeview, name):

    from gi.repository import Gtk

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

class GtkSession:

    def __init__(self, force=False):

        if not force:
            raise Exception("This code is deprecated but can be used to try Gtk.main() global locking")

        logging.debug("Init GtkSession")
        self._gtk_session_started = False
        self._thr = None

    def _thread(self):

        from gi.repository import Gtk

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

        from gi.repository import Gtk

        if self._gtk_session_started:
            logging.debug("Stopping main loop")
            Gtk.main_quit()
            logging.debug("Joining thread")
            self._thr.join()
            logging.debug("Joined thread")

class TextView:

    def __init__(self):

        from gi.repository import Gtk

        ui_file = os.path.join(
            os.path.dirname(__file__), 'ui', 'textview.glade'
            )

        ui = Gtk.Builder()
        ui.add_from_file(ui_file)

        self.ui = widget_dict(ui)

        self.ui['button1'].connect('clicked', self.onSaveAsActivated)

    def onSaveAsActivated(self, button):

        from gi.repository import Gtk

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
                (os.path.exists(path) and dialog_resp == Gtk.ResponseType.YES)
                or
                not os.path.exists(path)
                ):

                buff = self.ui['textview1'].get_buffer()
                txt = buff.get_text(buff.get_start_iter(), buff.get_end_iter(), False)

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


try:
    from gi.repository import Gtk
    from gi.repository import Gdk
except:
    class MessageDialog:

        def __init__(self, *args, **kwargs):
            raise Exception("Gtk not available")

else:

    class GtkIteratedLoop:

        def __init__(self):
            self._exit_event = threading.Event()
            self._started = False

        def wait(self):

            if self._started:
                raise Exception(
                    "Same GtkIteratedLoop must not be "
                    "started while it's already working"
                    )
            else:
                self._started = True

                self._exit_event.clear()

                while not self._exit_event.is_set():
                    while Gtk.events_pending():
                        Gtk.main_iteration()
                    # TODO: this number (0.01) is the guess
                    time.sleep(0.01)

                self._started = False

                # NOTE: making this class threaded will block Gtk,
                #       so don't implement threads here

        def stop(self):
            self._exit_event.set()


    class MessageDialog(Gtk.MessageDialog):

        """
        Documentation same as for Gtk.MessageDialog
        """

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.set_modal(True)
            self.set_transient_for(args[0])
            self.set_destroy_with_parent(True)
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

def text_view(text, title=''):

    from gi.repository import Gtk

    tw = TextView()

    tb = Gtk.TextBuffer()
    tb.set_text(str(text))

    tw.ui['textview1'].set_buffer(tb)

    tw.ui['window1'].set_title(str(title))

    tw.ui['window1'].show_all()

    return
