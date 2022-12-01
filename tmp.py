# import gi

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk


# class ListBoxRowWithData(Gtk.ListBoxRow):
#     def __init__(self, data):
#         super().__init__()
#         self.data = data
#         self.add(Gtk.Label(label=data))


# class ListBoxWindow(Gtk.Window):
#     def __init__(self):
#         super().__init__(title="ListBox Demo")
#         self.set_border_width(10)

#         box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
#         self.add(box_outer)


#         listbox_2 = Gtk.ListBox()
#         items = "This is a sorted ListBox Fail".split()

#         for item in items:
#             listbox_2.add(ListBoxRowWithData(item))

#         def on_row_activated(listbox_widget, row):
#             print(row.data)

#         listbox_2.connect("row-activated", on_row_activated)

#         box_outer.pack_start(listbox_2, True, True, 0)
#         listbox_2.show_all()


# win = ListBoxWindow()
# win.connect("destroy", Gtk.main_quit)
# win.show_all()
# Gtk.main()


from datetime import datetime

print(datetime.now().strftime("%l"))