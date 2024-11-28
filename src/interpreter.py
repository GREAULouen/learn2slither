

class Interpreter:
	@staticmethod
	def _get_state(vision):
		"""Converts the vision into a usable state"""
		return vision

	@staticmethod
	def _get_reward(state):
		"""Define rewards for each game events"""
		rewards = {
			'EAT_GREEN_APPLE': 10,
			'EAT_RED_APPLE': -10,
			'DEFAULT': -1,
			'GAME_OVER': -100
		}
		return rewards.get(state, 0)

	@staticmethod
	def _compute_reward(state, action):
		"""Computes the imediate reward for the pair state/action"""
		collision = {
			'UP': state[2][state[0][0] - 1],
			'LEFT': state[1][state[0][1] - 1],
			'DOWN': state[2][state[0][0] + 1],
			'RIGHT': state[1][state[0][1] + 1]
		}
		rewards = {
			'W': 'GAME_OVER',
			'S': 'GAME_OVER',
			\
			'0': 'DEFAULT',
			\
			'G': 'EAT_GREEN_APPLE',
			\
			'R': 'EAT_RED_APPLE'
		}
		return Interpreter._get_reward(rewards[collision[action]])