

class Interpreter:
	@staticmethod
	def _get_state(vision):
		"""Converts the vision into a usable state"""
		return vision

	@staticmethod
	def _get_reward(state):
		"""Define rewards for each game events"""
		rewards = {
			'EAT_GREEN_APPLE': 15,
			'EAT_RED_APPLE': -15,
			'TOWARD_GREEN_APPLE': 2,
			'TOWARD_RED_APPLE': -2,
			'DEFAULT': -1,
			'GAME_OVER': -100
		}
		return rewards.get(state, 0)

	@staticmethod
	def _compute_reward(state, action):
		"""Computes 'TOWARD_XX' rewards with a linear evolution from DEFAULT"""
		distance = {
			'UP': 	[(i, state[2][state[0][0] - i])
					for i in range(1, state[0][0])
					if state[2][state[0][0] - i] in ['G', 'R']],
					\
			'LEFT': [(i, state[1][state[0][1] - i])
					for i in range(1, state[0][1])
					if state[1][state[0][1] - i] in ['G', 'R']],
					\
			'DOWN': [(i - state[0][0], state[2][i])
					for i in range(state[0][0], len(state[2]))
					if state[2][i] in ['G', 'R']],
					\
			'RIGHT': [(i - state[0][1], state[1][i])
					for i in range(state[0][1], len(state[1]))
					if state[1][i] in ['G', 'R']]
		}
		if len(distance[action]) == 0:
			return Interpreter._get_reward('DEFAULT')
		if distance[action][0][1] == 'G':
			return (
				Interpreter._get_reward('EAT_GREEN_APPLE') - \
				distance[action][0][0] * Interpreter._get_reward('TOWARD_GREEN_APPLE')
			)
		elif distance[action][0][1] == 'R':
			return (
				Interpreter._get_reward('EAT_RED_APPLE') - \
				distance[action][0][0] * Interpreter._get_reward('TOWARD_RED_APPLE')
			)
		else:
			raise ValueError(f"Unhandled distance calculation: {distance[action][0][1]}")

