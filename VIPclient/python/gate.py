import vip
import time
import pandas as pd
import numpy as np
import signal
import fcntl, os
import atexit
import os.path
from os import path

class Gate():

	exit_message = ""

	def __init__(self, args):
		# Interruption signal handler
		signal.signal(signal.SIGINT, self.handler)
		# Exit program handling
		atexit.register(self.atExit)
		# Arguments
		self.config = args
		self.jobfile = self.config['jobfile']
		self.maxExecsNb = self.config['maxExecsNb']
		# Condition to start, false if another process is already running
		self.go = True
		# A joblist is linked to a specific csv file so we can make it global
		# in the context of this execution
		# Start
		self.readJobList()
		self.initVIP()

	def initVIP(self):
		print("Gate :: apiKey : ", self.config['apiKey'])
		vip.setApiKey(self.config['apiKey'])

	def readJobList(self):
		# # Add a lock
		self.lock_file = self.jobfile + ".lock"
		if not path.exists(self.lock_file):
			f = open(self.lock_file, 'w+')
			# Panda converts the cvs to data frame
			self.joblist = pd.read_csv(self.jobfile) # , dtype={'submitted': int}
		else:
			self.go = False

	def handleExecutions(self):
	    pass

	def startJobIfNecessary(self, joblist, jobfile):
		pass

	def handler(self, signum, frame):
		pass

	def exitMessage(self, msg=exit_message):
		print(msg)

	def atExit(self):
		pass