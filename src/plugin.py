#!/usr/bin/env python3

import os
import pytz
import json
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GLib
from xdg.BaseDirectory import xdg_config_home
from datetime import datetime

PLUGIN_NAME        = 'World-Clock-Plugin'
PLUGIN_VERSION     = '0.1.0'
PLUGIN_DESCRIPTION = 'Simple World Clock Plugin Written In Python'
PLUGIN_AUTHOR      = 'Hanzala Ibn Zahid <hanzalarushnan@gmail.com>'
PLUGIN_ICON        = 'org.xfce.panel.clock'

CONFIG_BASE = """{
  "format": "%H:%M",
  "allocation": "auto",
  "timezones": [
    ["Europe/Amsterdam", "Amsterdam"]
  ]
}"""

class PanelPlugin(Gtk.Box):
    """
    Xfce4 PanelPlugin,
    This class got called from the C interface of Plugin to embedd the
    resulting python object as Gtk Widget in Xfce4 panel.
    
    Gtk.Box is taken only as example, 
    Any gobject widget can be used as parent class
    """
    def __init__(self) -> None:
        """
        This method is called by sample_py_new() method
        """
        super().__init__()
        self.load_config()

        button1 = Gtk.ToggleButton()
        self.main_label = Gtk.Label()
        button1.add(self.main_label)

        self.pack_start(button1, True, True, 0)

        self.all_time_labels = []

        self.new_win = Gtk.Window()
        self.new_win.set_decorated(False)
        self.new_win.set_skip_taskbar_hint(True)
        self.new_win.set_skip_pager_hint(True)

        self.new_win.set_border_width(15)
        self.new_win.set_keep_above(True)

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        self.table = Gtk.Table(n_rows=2, n_columns=2, homogeneous=True)

        self.time_label = Gtk.Label()
        self.calendar = Gtk.Calendar()
        button2 = Gtk.Button()
        button2.add(self.time_label)
        

        box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        box2.set_margin_right(20)
        box2.pack_start(button2, False, True, 1)
        box2.pack_start(Gtk.Separator(), True, False, 0)
        box2.pack_start(self.table, True, True, 1)
    
        box.pack_start(box2, True, True, 1)
        box.pack_end(self.calendar, True, True, 1)

        self.new_win.add(box)

        self.set_table()
        self.update_time_label()
        self.main_label.set_justify(Gtk.Justification.CENTER)

        button1.connect("button-press-event", self.click_label)
        button2.connect("button-press-event", self.reset_calendar)

        GLib.timeout_add(1000, self.update_self)


    def load_config(self):
        self.config_path = os.path.join(
            xdg_config_home, 
            "world_clock_plugin@hanzala123"
        )

        self.config_file = os.path.join(self.config_path, "config.json")
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
            with open(self.config_file, "w") as f:
                f.write(CONFIG_BASE)
            
            with open(os.path.join(self.config_path, "available_timezones.txt"), "w") as f:
                for timezone in pytz.all_timezones:
                    f.write(timezone)
                    f.write("\n")

        with open(self.config_file) as f:
            self.config = json.load(f)


    def click_label(self, a, b):
        if b.button == 1:
            if self.new_win.get_property("visible"):
                self.new_win.hide()
                a.set_active(True)

            else:
                if self.get_win_allocation() and self.get_win_allocation() != "auto":
                    win_location = self.get_win_allocation()

                else:
                    win_location = [b.x_root, b.y_root]
                    print("Location: ", str(win_location))
            
                a.set_active(False)
                self.new_win.move(*win_location)
                self.new_win.show_all()


    def reset_calendar(self, a=None, b=None):
        t_now = datetime.now()
        self.calendar.select_day(t_now.day)
        self.calendar.select_month(t_now.month - 1 , t_now.year)


    def get_win_allocation(self):
        return self.config.get("allocation")


    def get_time_fmt(self):
        return self.config["format"]


    def get_time_zones(self):
        return self.config["timezones"]


    def timezone_to_time_str(self, timezone):
        tz = pytz.timezone(timezone)
        time = (datetime.now(tz))
        time_str = time.strftime("%H:%M")
        if time.strftime("%d/%m/%Y") != datetime.now().strftime("%d/%m/%Y"):
            time_str = time.strftime("%H:%M (%d/%m/%Y)")

        return time_str


    def get_all_times(self):
        timezones = self.get_time_zones()   
        times = []
        for timezone, name in timezones:
            time_str = self.timezone_to_time_str(timezone)
            times.append([time_str, name, timezone])

        return times


    def set_table(self):
        self.all_time_labels = []
        for time_str, name, timezone in self.get_all_times():
            label = Gtk.Label(label=time_str)
            label.timezone = timezone
            label.timezone_name = name
            self.all_time_labels.append(label)

        for indx, label in enumerate(self.all_time_labels):
            self.table.attach(Gtk.Label(label=label.timezone_name), 0, 1, 0, indx+1)
            self.table.attach(label, 1, 2, 0, indx+1)


    def update_table(self):
        for label in self.all_time_labels:
            label.set_text(self.timezone_to_time_str(label.timezone))


    def update_time_label(self):
        t_now = datetime.now()
        if self.time_label.get_text() != t_now.strftime("%A, %B %d, %Y"):
            self.time_label.set_text(t_now.strftime("%A, %B %d, %Y"))

        if self.main_label.get_text() != t_now.strftime(self.get_time_fmt()):
            self.main_label.set_text(t_now.strftime(self.get_time_fmt()))


    def update_calendar(self):
        t_now = datetime.now()
        t_cal = self.calendar.get_date()
        if t_now.day != t_cal.day:
            self.reset_calendar()


    def update_self(self):
        self.update_table()
        self.update_time_label()
        self.update_calendar()
        return True
    

    def free(self):
        """
        Free method called by sample_py_free() when panel sends the "free"
        signal to plugin to clean up the allocations or post tasks
        like saving the configurations etc.
        """
        self.new_win.destroy()
        self.destroy()

    def orientation_changed(self, orientation: int):
        """
        When the panel orientation changes then it emits a signal of
        orientation changed to all child plugins with current orientation

        Parameters:
            orientation (int): current orientation of plugin
                               0 = Gtk.Orientation.HORIZONTAL
                               1 = Gtk.Orientation.VERTICAL
        """
        self.set_orientation(orientation)


    def about(self):
        """
        Xfce4 panel emit "about" signal whenever user request the information
        about the plugin from right-click-menu
        """
        dialog = Gtk.AboutDialog()
        dialog.set_title("About Dialog")
        dialog.set_program_name(PLUGIN_NAME)
        dialog.set_version(PLUGIN_VERSION)
        dialog.set_comments(PLUGIN_DESCRIPTION)
        dialog.set_website("https://github.com/hanzala123/world-clock-xfce-plugin")
        dialog.set_authors([PLUGIN_AUTHOR])
        dialog.set_logo_icon_name(PLUGIN_ICON)

        dialog.connect('response', lambda dialog, data: dialog.destroy())
        dialog.show_all()
