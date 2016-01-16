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
import logging

class Toolbar(Gtk.HBox):

   def __init__(self, parent):
      logging.debug("Setting up the toolbar...")  
 
      Gtk.HBox.__init__(self, spacing=2)

      self.buttons = {}

      # Connect
      icon = Gtk.Image()
      icon.set_from_stock(Gtk.STOCK_CONNECT, Gtk.IconSize.BUTTON)
      button = Gtk.Button()
      button.add(icon)
      button.set_tooltip_text('Connect to login node')
      button.connect("clicked", parent.cx_connect)
      self.pack_start(button, False, False, 0)
      self.buttons["CONNECT"] = button

      # Disconnect
      icon = Gtk.Image()
      icon.set_from_stock(Gtk.STOCK_DISCONNECT, Gtk.IconSize.BUTTON)
      button = Gtk.Button()
      button.add(icon)
      button.set_tooltip_text('Disconnect from login node')
      button.connect("clicked", parent.cx_disconnect)
      self.pack_start(button, False, False, 0)
      self.buttons["DISCONNECT"] = button
      
      logging.debug("Toolbar ready!") 

      return
