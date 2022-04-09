#!/bin/env python

'''
   Helper script to preview the interface of plugin
'''

import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio

from src.plugin import PanelPlugin

class Preview(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title='Plugin Preview')

        self.set_default_size(400, 200)

        self.plugin = PanelPlugin()
        self.Box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.Box)
        self.Box.pack_start(self.plugin, True, True, 10)

        button_box = Gtk.ButtonBox()
        button_box.set_orientation(Gtk.Orientation.HORIZONTAL)
        button_box.set_spacing(2)
        self.Box.pack_start(button_box, False, False, 1)

        self.orientation = 0

        about_btn = Gtk.Button(label="About")
        about_btn.connect("clicked", self.emit_about_signal)
        button_box.add(about_btn)

        orientation_btn = Gtk.Button(label="Horizontal")
        orientation_btn.connect("clicked", self.emit_orientation_change)
        button_box.add(orientation_btn)
    
    def emit_about_signal(self, button: Gtk.Button) -> None:
        self.plugin.about()

    def emit_orientation_change(self, button: Gtk.Button) -> None:
        if self.orientation == 0:
            self.orientation = 1
            button.set_label("Veritcal")
        else:
            self.orientation = 0
            button.set_label("Horizontal")

        self.plugin.orientation_changed(self.orientation)


if __name__ == '__main__':
    win = Preview()
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()

