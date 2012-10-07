
import threading
#import multiprocessing
import logging

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
