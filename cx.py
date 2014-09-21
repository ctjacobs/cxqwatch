import sys
import paramiko
from contextlib import closing
from scpclient import *
import re
import logging

TEMP_DIR = "/tmp/ctjacobs"

class CX:

   def __init__(self, shell=None):
      self.shell = shell
      return

   def login_connect(self, username, password):
      """ Connect to the CX1 login node. """
      
      logging.info("Connecting to login node...")
      try:
         self.shell = paramiko.SSHClient()
         self.shell.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         self.shell.connect("login.cx1.hpc.ic.ac.uk", username=username, password=password)
      except paramiko.SSHException, e:
         logging.exception(str(e))
         return False

      logging.info("Connected successfully.")
      return True

   def login_disconnect(self):
      logging.info("Disconnecting from login node...")
      try:
         self.shell.close()
      except paramiko.SSHException, e:
         logging.exception(str(e))
         return False
      logging.info("Disconnected successfully.")
      return True
      
   def send_command(self, command):
      stdin, stdout, stderr = self.shell.exec_command(command)
      stdin.close()
      response = stdout.readlines()
      return response
      
   def get_jobs_list(self):
      response = self.send_command("qstat -a")
      # Ignore header lines
      response = response[5:]
      
      jobs = []
      number_of_jobs = len(response)
      for i in range(number_of_jobs):
         if(response[i] != ""):
            response[i] = response[i].replace("\n", "")
            jobs.append(response[i])
         
      return jobs
      
   def get_nodes_list(self, job_id):
      response = self.send_command("qstat -an")
      
      for i in range(len(response)):
         if(job_id in response[i]):
            break
      
      # Handle the case where the nodes list is split over multiple lines.
      s = ""
      for j in range(i+1, len(response)):
         if(not ".cx1b" in response[j]):
            s += response[j]
         else:
            break
      
      # Remove whitespace.
      s = s.replace("\n", "")
      s = s.replace("\r", "")
      s = s.replace(" ", "")
      
      # Extract the nodes
      nodes = []
      pattern = re.compile("((cx1-\d+-\d+-\d+)/\d+\*\d+\+*)")
      for match in re.findall(pattern, s):
         nodes.append(match[1])
      
      return nodes
      
   def clean_temp(self):
      logging.info("Cleaning temp directory (%s)" % TEMP_DIR)
      self.send_command("rm -rf %s; mkdir %s" % (TEMP_DIR, TEMP_DIR))
      return
      
   def get_data_from_node(self, job_id, node, pattern):
      logging.info("Getting data from node %s..." % node)
      self.send_command("scp -r %s:/tmp/pbs.%s/*%s* %s" % (node, job_id, pattern, TEMP_DIR))
      return
   
   def get_data_from_cx(self, pattern):
      logging.info("Downloading data from CX1...")
      with closing(ReadDir(self.shell.get_transport(), '%s' % TEMP_DIR)) as scp:
         scp.receive_dir('.', preserve_times=True)

      return
