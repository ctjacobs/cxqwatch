from gi.repository import Gtk, GObject
import logging

FIELD_NAMES = ["JOB_ID", "USER", "QUEUE", "NAME", "SESSION_ID", "NODES", "PROCS", "MEMORY", "TIME", "STATUS"]

class Jobs(Gtk.ListStore):

   def __init__(self, cx):
   
      self.cx = cx
   
      data_types = [str]*(len(FIELD_NAMES) + 2)
      Gtk.ListStore.__init__(self, *data_types)

      self.jobs_current = []
      self.jobs_finished = []
      
      return
      
   def create_job(self, *args):
      job = {}
      for i in range(len(FIELD_NAMES)):
         job[FIELD_NAMES[i]] = args[0][i]
      return job
      
   def get_current_job_by_id(self, job_id):
      for job in self.jobs_current:
         if(job["JOB_ID"] == job_id):
            return job
      return None
      
   def populate(self):
      jobs_list = self.cx.get_jobs_list()
      for j in jobs_list:
         j = self.create_job(j.split())
         self.jobs_current.append(j)
      self.refresh()
      return
      
   def refresh(self):
      logging.debug("Refreshing jobs list...")
      
      self.clear()
      
      jobs_new = []
      
      # Get the most recent list of jobs from CX1.
      jobs_list = self.cx.get_jobs_list()
      for j in jobs_list:
         j = self.create_job(j.split())
         jobs_new.append(j)
    
      for job in jobs_new:
         liststore_entry = []
         for k in FIELD_NAMES:
            liststore_entry.append(job[k])
            
         # Job already exists in the current list of jobs
         if(job in self.jobs_current):
            i = self.jobs_current.index(job)
            # The status has changed (maybe from "Q" to "R"?)
            if(job["STATUS"] != self.jobs_current[i]["STATUS"]):
               if(job["STATUS"] == "R"):
                  liststore_entry.append("#000000")
                  liststore_entry.append("#A6D785")
               else:
                  liststore_entry.append("#000000")
                  liststore_entry.append("#FFFFFF")
               self.jobs_current[i]["STATUS"] = job["STATUS"]
            else:
               if(job["STATUS"] == "R"):
                  liststore_entry.append("#000000")
                  liststore_entry.append("#A6D785")
               else:
                  liststore_entry.append("#000000")
                  liststore_entry.append("#FFFFFF")
         else:
            self.jobs_current.append(job)
            if(job["STATUS"] == "R"):
               liststore_entry.append("#000000")
               liststore_entry.append("#A6D785")
            else:
               liststore_entry.append("#000000")
               liststore_entry.append("#FFFFFF")
         self.append(liststore_entry)
         
      # Check to see if a current job is no longer in the list of jobs from CX1.
      for job in self.jobs_current:
         if(not job in jobs_new):
            self.jobs_current.remove(job)
            job["STATUS"] = "E"
            self.jobs_finished.append(job)
            
      # Add the finished/old jobs.
      for job in self.jobs_finished:
         liststore_entry = []
         for k in FIELD_NAMES:
            liststore_entry.append(job[k])
         liststore_entry.append("#000000")
         liststore_entry.append("#FF0000")
         self.append(liststore_entry)
         
      return True
     
      
   def get_data(self, job_id, pattern):

      nodes = self.cx.get_nodes_list(job_id)
      
      # List all files on the first compute node
      print self.cx.ls_on_node(job_id, nodes[0])
      
      self.cx.clean_temp()
      
      for node in nodes:
         self.cx.get_data_from_node(job_id, node, pattern)
      self.cx.get_data_from_cx(pattern)         
      
      return
