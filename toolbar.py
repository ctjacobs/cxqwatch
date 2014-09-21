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
