

class Interpreter:
	@staticmethod
	def get_state(vision):
		"""Converts the vision into a usable state"""
		state = {
			'vision': vision,
			'UP': vision[2][vision[0][0] - 1],
			'LEFT': vision[1][vision[0][1] - 1],
			'DOWN': vision[2][vision[0][0] + 1],
			'RIGHT': vision[1][vision[0][1] + 1],
		}
		return state

	def get_reward(state):
		"""Define rewards for each game events"""
		rewards = {
			'EAT_GREEN_APPLE': 10,
			'EAT_RED_APPLE': -10,
			'EAT_NOTHING': -1,
			'GAME_OVER': -100
		}
		return rewards.get(state, 0)
