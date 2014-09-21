from gi.repository import Gtk, GObject

class DownloadDialog(Gtk.Dialog):
   
   def __init__(self, parent):
      Gtk.Dialog.__init__(self, title="Download Files", parent=parent, flags=Gtk.DialogFlags.DESTROY_WITH_PARENT, buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))

      self.sources = {}

      hbox_temp = Gtk.HBox(spacing=0)
      label = Gtk.Label("Pattern: ", halign=Gtk.Align.START)
      label.set_width_chars(12)
      label.set_alignment(0, 0.5)
      hbox_temp.pack_start(label, False, False, 6)
      self.sources["PATTERN"] = Gtk.Entry()
      hbox_temp.pack_start(self.sources["PATTERN"], True, True, 6)
      self.vbox.pack_start(hbox_temp, False, False, 6)

      self.show_all()
      return

   def get_sources(self):
      return self.sources


