import vip
import time
import pandas as pd
import numpy as np
import signal

class Gate():

	exit_message = ""

	def __init__(self, args):
		# Interruption signal handler
		signal.signal(signal.SIGINT, self.handler)
		# Arguments
		self.config = args
		self.jobfile = self.config['jobfile']
		self.maxExecsNb = self.config['maxExecsNb']
		# A joblist is linked to a specific csv file so we can make it global
		# in the context of this execution
		# Start
		self.readJobList()
		self.initVIP()

	def initVIP(self):
		print("Gate :: apiKey : ", self.config['apiKey'])
		vip.setApiKey(self.config['apiKey'])

	def readJobList(self):
		self.joblist = pd.read_csv(self.jobfile) # , dtype={'submitted': int}
		print("joblist type: ", type(self.joblist))

	def handleExecutions(self):
	    pass

	def startJobIfNecessary(self, joblist, jobfile):
		pass

	def handler(self, signum, frame):
		pass

	def exitApplication(self):
		print(exit_message)