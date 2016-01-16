# This file is part of cxqwatch, released under the MIT license.

# The MIT License (MIT)

# Copyright (c) 2014, 2016 Christian T. Jacobs

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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


