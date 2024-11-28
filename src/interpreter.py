

class Interpreter:
	@staticmethod
	def _get_state(vision):
		"""Converts the vision into a usable state"""
		return vision

	def _get_reward(state):
		"""Define rewards for each game events"""
		rewards = {
			'EAT_GREEN_APPLE': 10,
			'EAT_RED_APPLE': -10,
			'DEFAULT': -1,
			'GAME_OVER': -100
		}
		return rewards.get(state, 0)
