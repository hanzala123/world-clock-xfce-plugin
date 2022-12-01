import gi
import pytz

from datetime import datetime
import json
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


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
        self.allocation_entry.set_text(self.main_plugin.get_win_allocation())
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
