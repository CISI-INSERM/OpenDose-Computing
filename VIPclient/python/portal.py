import os
import argparse
import configparser

from gate import Gate
from gate_lab import GateLab
from gate_CL import GateCL

class Portal():
	def __init__(self):
		pass

	def parseParams(self):
		print("Portal :: parse params")
		parser = argparse.ArgumentParser()
		parser.add_argument("--config", "-C", help="path to the configuration file in cfg format", type=str)
		return parser.parse_args()

		# get init values from config file
	def parseConfig(self, config_path):
		cfgparser = configparser.RawConfigParser()	
		cfgparser.read(config_path)
		config = {}
		config['apiKey'] = cfgparser.get('application', 'apikey')
		config['gaterelease'] = cfgparser.get('application', 'gaterelease')
		config['application'] = cfgparser.get('application', 'name')
		config['CPUparam'] = cfgparser.get('application', 'CPUparam')
		config['gateinput'] = cfgparser.get('inputs', 'input')
		config['macfile'] = cfgparser.get('inputs', 'macfile')
		config['outputdir'] = cfgparser.get('inputs', 'outputdir')
		config['maxExecsNb'] = int(cfgparser.get('jobs', 'maxjobs')) 
		config['jobfile'] = os.environ['OPENDOSE_PATH'] + "/" + cfgparser.get('jobs', 'jobfile')
		return config

	def launchGate(self):
		if config['application'] == "GateLab":
			batch = GateLab(config)
		elif args.type == "GateCL":
			batch = GateCL(config)


if __name__ == "__main__":
	print("OPENDOSE_PATH: ", os.environ['OPENDOSE_PATH'])
	portal = Portal()
	args = portal.parseParams()
	config = portal.parseConfig(args.config)
	portal.launchGate()