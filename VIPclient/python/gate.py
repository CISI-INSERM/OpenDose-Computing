import os
import configparser
import vip
import time
import pandas as pd

class Gate():


	def __init__(self, args):
		self.type = args.type
		self.config_path = args.config
		self.jobs_path = args.jobs
		self.parseConfig()
		self.initVIP()
		joblist = self.readJobList()
		self.handleExecutions(joblist, self.jobfile)

	# get init values from config file
	def parseConfig(self):
		config = configparser.RawConfigParser()	
		config.read(self.config_path)
		self.apiKey = config.get('application', 'apikey')
		self.gaterelease = config.get('application', 'gaterelease')
		self.application = config.get('application', 'application')
		self.CPUparam = config.get('application', 'CPUparam')
		self.gateinput = config.get('inputs', 'input')
		self.macfile = config.get('inputs', 'macfile')
		self.outputdir = config.get('inputs', 'outputdir')
		self.maxExecsNb = int(config.get('jobs', 'maxjobs')) # should be from the config file no ? YES
		self.jobfile = self.jobs_path #config.get('jobs', 'jobfile')

	def initVIP(self):
		print("apiKey : %s" % self.apiKey)
		if os.environ['DEBUG_VIP'] != "1" : 
			vip.setApiKey(self.apiKey)

	def readJobList(self):
	    joblist = pd.read_csv(self.jobfile)
	    return joblist

	def handleExecutions(self, joblist, jobfile):
	    pass

	def startJobIfNecessary(self, joblist, jobfile):
		pass