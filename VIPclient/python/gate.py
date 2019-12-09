import configparser

class Gate():
	def __init__(self, config_path):
		print(__name__)
		self.model = "AF"
		self.config_path = config_path

	def getConfigPath(self):
		return self.config_path

	def parseConfig(self):
		