#!/usr/bin/env python

from gi.repository import Gtk, GObject, Gdk, GdkPixbuf
import signal
import logging

from toolbar import *
from cx import *
from jobbook import *
from connection_dialog import *
   
class Flcx(Gtk.Window):

   def __init__(self):
      Gtk.Window.__init__(self, title="Flcx v0.1")
      self.set_size_request(800, 600) # Default to an 800 x 600 resolution.
      
      # Kills the application if the close button is clicked on the main window itself. 
      self.connect("delete-event", Gtk.main_quit)
      
      # The CX1 handler
      self.cx = CX()
            
      vbox_outer = Gtk.VBox()
      self.add(vbox_outer)
      
      self.toolbar = Toolbar(self)
      vbox_outer.pack_start(self.toolbar, False, False, 0)
      
      self.jobbook = JobBook(self, self.cx)
      self.jobbook.set_scrollable(True)
      
      vbox_outer.pack_start(self.jobbook, True, True, 0)
      
      self.show_all()

      return

   def cx_connect(self, widget=None):
      dialog = ConnectionDialog(self)
      response = dialog.run()
      if(response == Gtk.ResponseType.OK):
         user_details = dialog.get_sources()
         username = user_details["USERNAME"].get_text()
         password = user_details["PASSWORD"].get_text()
         dialog.destroy()
      else:
         dialog.destroy()
         return
      
      self.cx.login_connect(username, password)
      
      self.jobbook.jobs.populate() # Initial population of the jobs window.
      
      # Refresh the window every few minutes.
      self.query_event = GObject.timeout_add(300000, self.jobbook.jobs.refresh)
      return
   
   def cx_disconnect(self, widget=None):
      self.cx.login_disconnect()
      GObject.source_remove(self.query_event)
      return

if(__name__ == "__main__"):

   logging.basicConfig(level=logging.INFO, 
                       format="%(asctime)s %(levelname)s: %(message)s", 
                       datefmt="%Y-%m-%d %H:%M:%S")
   
   signal.signal(signal.SIGINT, signal.SIG_DFL) # Exit if a SIGINT signal is captured.
   application = Flcx() # Populate the main window and show it.
   Gtk.main() # Start up the event loop!
   
