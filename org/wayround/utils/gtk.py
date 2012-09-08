
from gi.repository import Gtk

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
