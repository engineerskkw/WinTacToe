import ABC

class AbstractLogic:
	@abstractmethod
	def place_mark(self, x, y):
		pass

	@abstractmethod
	def gather_winnings(self):
		pass

	@abstractmethod
	def get_current_state(self):
		pass
		