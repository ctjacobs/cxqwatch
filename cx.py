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

import sys
import paramiko
from contextlib import closing
from scpclient import *
import re
import logging

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

      self.temp_dir = "/tmp/tmp_%s" % (username)
      logging.info("Connected successfully.")
      return True

   def login_disconnect(self):
      logging.info("Disconnecting from login node...")
      try:
         self.shell.close()
      except paramiko.SSHException as e:
         logging.error(str(e))
         return False
      except AttributeError as e:
         logging.error("Cannot disconnect - no connection exists!")
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
      logging.info("Cleaning temp directory (%s)" % self.temp_dir)
      self.send_command("rm -rf %s; mkdir %s" % (self.temp_dir, self.temp_dir))
      return

   def ls_on_node(self, job_id, node):
      logging.info("Listing files on node %s..." % node)
      response = self.send_command("ssh %s \"ls /tmp/pbs.%s/\"" % (node, job_id))
      return response

   def get_data_from_node(self, job_id, node, pattern):
      logging.info("Getting data from node %s..." % node)
      self.send_command("scp -r %s:/tmp/pbs.%s/*%s* %s" % (node, job_id, pattern, self.temp_dir))
      return
   
   def get_data_from_cx(self, pattern):
      logging.info("Downloading data from CX1...")
      with closing(ReadDir(self.shell.get_transport(), '%s' % self.temp_dir)) as scp:
         scp.receive_dir('.', preserve_times=True)

      return
