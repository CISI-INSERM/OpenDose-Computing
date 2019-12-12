import argparse

from gate import Gate
from gate_lab import GateLab
from gate_CL import GateCL

class Portal():
	def __init__(self):
		print("init portal")

	def parseParams(self):
		print("parse params")
		# Prend 3 params en entrée : fichier config, fichier csv, LAB / CL
		parser = argparse.ArgumentParser()
		parser.add_argument("--config", "-C", help="path to the configuration file in cfg format", type=str)
		parser.add_argument("--jobs", "-J", help="path to the list of jobs in csv format", type=str)
		parser.add_argument("--type", "-T", help="type of batch : LAB for high energy particles, CL for low energy particles", type=str)
		return parser.parse_args()

	def launchGate(self, args):
		print("launch gate class")
		if args.type == "CL":
			batch = GateCL(args)
		elif args.type == "LAB":
			batch = GateLab(args)


if __name__ == "__main__":
	portal = Portal()
	args = portal.parseParams()
	portal.launchGate(args)