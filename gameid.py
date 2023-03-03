import codes

class gameid:
	def __init__(self, id):
		self.id = id
		if len(self.id) == 6:
			self.system = self.id[0]
			self.title = self.id[1:3]
			self.region = self.id[3]
			self.publisher = self.id[3:3]