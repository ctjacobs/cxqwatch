from gi.repository import Gtk, GObject

from jobs import *
from cx import *
from download_dialog import *

class JobBook(Gtk.Notebook):
   def __init__(self, parent, cx):
      Gtk.Notebook.__init__(self)
      self.parent = parent
      self.cx = cx
      
      self.jobs = Jobs(cx)
      
      self.treeview = Gtk.TreeView(self.jobs)
      self.treeview.set_grid_lines(Gtk.TreeViewGridLines.BOTH)
      self.treeview.connect("row-activated", self.query_callback)
      
      self.treeselection = self.treeview.get_selection()
      self.treeselection.set_mode(Gtk.SelectionMode.SINGLE)
      
      sw = Gtk.ScrolledWindow()
      sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
      sw.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
      sw.add(self.treeview)
     
      vbox = Gtk.VBox()
      vbox.set_name("test")
      vbox.pack_start(sw, True, True, 0)

      hbox = Gtk.HBox(False, 0)
      label = Gtk.Label("Jobs")
      hbox.pack_start(label, False, False, 0)
      hbox.show_all()
      
      self.insert_page(vbox, hbox, 0)
      
      for i in range(0, len(FIELD_NAMES)):
         renderer = Gtk.CellRendererText()
         column = Gtk.TreeViewColumn(FIELD_NAMES[i], renderer, text=i, foreground=len(FIELD_NAMES), background=len(FIELD_NAMES)+1)
         column.set_resizable(True)
         column.set_min_width(50)
         column.set_clickable(True)
         self.treeview.append_column(column)
      
      self.show_all()
      return

   def query_callback(self, widget, path, view_column):
      (model, path) = self.treeselection.get_selected_rows() # Get the selected row in the jobbook.
      job_id = self.jobs.get_value(model.get_iter(path[0]),0)
      
      if(self.jobs.get_current_job_by_id(job_id)["STATUS"] == "E" or self.jobs.get_current_job_by_id(job_id)["STATUS"] == "Q"):
         # Can't download data from a complete or queued job.
         return
         
      dialog = DownloadDialog(self.parent)
      response = dialog.run()
      if(response == Gtk.ResponseType.OK):
         user_details = dialog.get_sources()
         pattern = user_details["PATTERN"].get_text()
         dialog.destroy()
      else:
         dialog.destroy()
         return
         
      self.jobs.get_data(job_id, pattern)
      return      
      
