#!/usr/bin/env python3

import imp
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

CONFIG_BASE = {
    "format": "%H:%M", 
    "date_format": "%m/%d/%y", 
    "allocation": "auto", 
    "timezones": ["Europe/Amsterdam", "Etc/UTC"]
}


class ConfigWindow(Gtk.Window):
    def __init__(self, main_plugin):
        super().__init__(title="World Clock Plugin Settings")

        self.set_border_width(10)
        self.existing_tz = main_plugin.get_time_zones()
        self.tz_store = {}
        for tz in pytz.all_timezones:
            if len(tz.split("/", 1)) < 2:
                continue

            z, t = tz.split("/", 1)
            if z not in self.tz_store:
                self.tz_store[z] = []
                
            self.tz_store[z].append(t)

        self.main_plugin = main_plugin
        self.time_fmt_entry = Gtk.Entry()
        self.time_fmt_entry.set_text(self.main_plugin.get_time_fmt())

        self.date_fmt_entry = Gtk.Entry()
        self.date_fmt_entry.set_text(self.main_plugin.get_date_fmt())
        
        self.allocation_entry = Gtk.Entry()
        allocation = self.main_plugin.get_win_allocation()
        if allocation != "auto":
            allocation = ", ".join([str(i) for i in allocation])
        self.allocation_entry.set_text(allocation)
        self.allocation_entry.set_tooltip_text("Set to auto or the postion in x, y format i.e. 10, 230")

        self.zone_combo = Gtk.ComboBoxText()
        self.zone_combo.set_entry_text_column(0)
        self.zone_combo.connect("changed", self.on_zone_combo_changed)

        for z in self.tz_store:
            self.zone_combo.append_text(z)

        self.tz_combo = Gtk.ComboBoxText()
        self.tz_combo.set_entry_text_column(0)
        self.zone_combo.set_active(0)

        add_btn = Gtk.Button(label="Add")
        add_btn.connect("clicked", self.add_new)

        self.listbox = Gtk.ListBox()
        self.load_existing_tz()
        del_btn = Gtk.Button(label="Delete")
        del_btn.connect("clicked", self.delete_tz)

        mbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(mbox)

        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        vbox.pack_start(self.zone_combo, False, False, 0)
        vbox.pack_start(self.tz_combo, False, False, 0)
        vbox.pack_start(add_btn, False, False, 0)

        bbox = Gtk.ButtonBox()
        bbox.set_orientation(Gtk.Orientation.HORIZONTAL)
        bbox.set_spacing(2)

        close_btn = Gtk.Button(label="Close")
        apply_btn = Gtk.Button(label="Apply")

        close_btn.connect("clicked", lambda dialog: self.destroy())
        apply_btn.connect("clicked", self.save_new_config)

        bbox.add(close_btn)
        bbox.add(apply_btn)
        
        mbox.pack_start(Gtk.Label(label="Main Time Format"), False, False, 0)
        mbox.pack_start(self.time_fmt_entry, False, False, 0)
        
        l = Gtk.Label(label="Date Format For World Clocks")
        l.set_margin_top(15)
        mbox.pack_start(l, False, False, 0)
        mbox.pack_start(self.date_fmt_entry, False, False, 0)

        l = Gtk.Label(label="Calendar Window Allocation")
        l.set_margin_top(15)
        mbox.pack_start(l, False, False, 0)
        mbox.pack_start(self.allocation_entry, False, False, 0)

        l = Gtk.Label(label="Existing Timezone(s)")
        l.set_margin_top(15)
        mbox.pack_start(l, False, False, 0)
        self.listbox.set_margin_top(5)
        mbox.pack_start(self.listbox, True, True, 0)
        mbox.pack_start(del_btn, False, False, 0)

        l = Gtk.Label(label="Add New Timezone")
        l.set_margin_top(15)
        mbox.pack_start(l, False, False, 0)
        mbox.pack_start(vbox, False, False, 0)

        self.status_label = Gtk.Label()
        self.status_label.set_margin_top(20)
        mbox.pack_start(self.status_label, False, False, 0)

        bbox.set_margin_top(20)
        mbox.pack_start(bbox, False, False, 0)


    def set_status(self, text, success=False):
        color = "#f24646"
        if success:
            color = "#80f246"
        self.status_label.set_markup(f"<span foreground=\"{color}\">{text}</span>")


    def save_new_config(self, *args):
        config = self.main_plugin.config

        time_fmt = self.time_fmt_entry.get_text()
        try:
            datetime.now().strftime(time_fmt)

        except Exception:
            self.set_status("Error in parsing `Main Time Format`")
            return


        date_fmt = self.date_fmt_entry.get_text()
        try:
            datetime.now().strftime(date_fmt)
            
        except Exception:
            self.set_status("Error in parsing `Date Format For World Clocks`")
            return


        allocation = self.allocation_entry.get_text()

        try:
            if allocation != "auto":
                allocation = [int(i.strip()) for i in allocation.split(",")]

        except Exception:
            self.set_status("Calendar Window Allocation must be in `x:integer, y:integer` format or `auto`")
            return


        if self.main_plugin.new_win.get_property("visible"):
            self.main_plugin.new_win.move(*allocation)

        config = {
          "format": time_fmt,
          "date_format": date_fmt,
          "allocation": allocation,
          "timezones": self.existing_tz
        }
        with open(self.main_plugin.config_file, "w") as f:
            json.dump(config, f)

        self.set_status("Configuration Saved!!", success=True)
        self.main_plugin.load_config()
        self.main_plugin.clear_table()


    def load_existing_tz(self):
        for w in self.listbox.get_children():
            w.destroy()

        for item in self.existing_tz:
            l = Gtk.ListBoxRow()
            l.data = item
            l.add(Gtk.Label(label=item))
            self.listbox.add(l)

        self.listbox.show_all()


    def on_zone_combo_changed(self, combo):
        text = combo.get_active_text()

        if text is not None:
            self.tz_combo.remove_all()
            for z in self.tz_store[text]:
                self.tz_combo.append_text(z)

            self.tz_combo.set_active(0)


    def add_new(self, *args):
        tz = self.zone_combo.get_active_text()
        tz += "/" 
        tz += self.tz_combo.get_active_text()
        self.existing_tz.append(tz)
        self.load_existing_tz()


    def delete_tz(self, *args):
        tz = self.listbox.get_selected_row()
        if tz is not None:
            tz = tz.data
            self.existing_tz.remove(tz)
            self.load_existing_tz()



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

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.table = Gtk.Table(n_rows=2, n_columns=2, homogeneous=True)
        self.table.set_row_spacings(10)

        self.time_label = Gtk.Label()
        self.calendar = Gtk.Calendar()
        button2 = Gtk.Button()
        button2.add(self.time_label)
        

        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.box2.set_margin_right(20)
        self.box2.pack_start(button2, False, True, 1)
        self.box2.pack_start(Gtk.Separator(), True, False, 12)
        self.box2.pack_start(self.table, False, False, 0)
    
        box.pack_start(self.box2, False, False, 1)
        box.pack_end(self.calendar, False, False, 1)

        self.new_win.add(box)

        self.set_table()
        self.update_time_label()
        self.main_label.set_justify(Gtk.Justification.CENTER)

        button1.connect("button-press-event", self.click_label)
        button2.connect("button-press-event", self.reset_calendar)

        GLib.timeout_add(1000, self.update_self)


    def open_config_window(self):
        ConfigWindow(self).show_all()


    def load_config(self):
        self.config_path = os.path.join(
            xdg_config_home, 
            "world_clock_plugin@hanzala123"
        )

        self.config_file = os.path.join(self.config_path, "config.json")
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
            with open(self.config_file, "w") as f:
                json.dump(CONFIG_BASE, f)     


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
                    # print("Location: ", str(win_location))
            
                a.set_active(False)
                self.new_win.move(*win_location)
                self.new_win.show_all()


    def reset_calendar(self, a=None, b=None):
        t_now = datetime.now()
        self.calendar.select_day(t_now.day)
        self.calendar.select_month(t_now.month - 1 , t_now.year)


    def get_win_allocation(self):
        return self.config.get("allocation", "auto")


    def get_time_fmt(self):
        return self.config["format"]


    def get_time_zones(self):
        return self.config["timezones"]


    def get_date_fmt(self):
        return self.config["date_format"]


    def timezone_to_time_str(self, timezone):
        tz = pytz.timezone(timezone)
        time = (datetime.now(tz))
        time_str = time.strftime("%H:%M")
        date_fmt = self.get_date_fmt()
        if time.strftime("%d/%m/%Y") != datetime.now().strftime("%d/%m/%Y"):
            time_str = time.strftime(f"%H:%M ({date_fmt})")

        return time_str


    def get_all_times(self):
        timezones = self.get_time_zones()   
        times = []
        for timezone in timezones:
            time_str = self.timezone_to_time_str(timezone)
            times.append([time_str, timezone])

        return times


    def clear_table(self, *args):
        self.table.destroy()
        self.table = Gtk.Table(n_rows=2, n_columns=2, homogeneous=True)
        self.table.set_row_spacings(10)
        self.box2.pack_start(self.table, False, False, 0)
        self.set_table()
        if self.new_win.get_property("visible"):
            self.new_win.show_all()


    def set_table(self):
        self.all_time_labels = []
        for time_str, timezone in self.get_all_times():
            label = Gtk.Label(label=time_str)
            label.timezone = timezone
            label.timezone_name = timezone.split("/", 1)[1]
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
