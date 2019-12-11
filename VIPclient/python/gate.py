import configparser
import vip
import time
import random
import sched
import configparser
import pandas as pd
import math
import re

class Gate():
	# apiKey, gaterelease, application, CPUparam, gateinput, macfile, outputdir, jobfile = ["",]

	def __init__(self, args):
		self.type = args.type
		self.config_path = args.config
		self.jobs_path = args.jobs
		self.parseConfig()
		self.initVIP()

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
		self.jobfile = config.get('jobs', 'jobfile')

	def initVIP(self):
		print("apiKey : %s" % self.apiKey)
		%vip.setApiKey(self.apiKey)
		self.maxExecsNb = 2 # should be from the config file no ?
