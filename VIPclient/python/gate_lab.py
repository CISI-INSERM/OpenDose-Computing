from gate import Gate

class GateLab(Gate):

	def __init__(self, config_path):
		Gate.__init__(self, config_path)
		print(self.config_path)
