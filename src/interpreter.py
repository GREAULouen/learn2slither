from math import floor


class Interpreter:
	@staticmethod
	def _get_state(vision):
		"""Converts the vision into a usable state"""
		def find_first_not_of(list, to_skip):
			"""Finds in the list the first occurence not in to_skip"""
			index = [
				i
				for i in range(len(list))
				if list[i] not in to_skip
			] + [len(list)]
			if not list[index[0]] in ['G', 'R']:
				index = [0]
			return list[:index[-1] + 1]

		state = (
			find_first_not_of(
							list=vision[2][vision[0][0] - 1::-1],
							to_skip=['0']
						),
			find_first_not_of(
							list=vision[1][vision[0][1] - 1::-1],
							to_skip=['0']
						),
			find_first_not_of(
							list=vision[2][vision[0][0] + 1:],
							to_skip=['0']
						),
			find_first_not_of(
							list=vision[1][vision[0][1] + 1:],
							to_skip=['0']
						)
		)

		return state

	@staticmethod
	def _get_reward(event):
		"""Define rewards for each game events"""
		rewards = {
			'G': 100,
			'R': -70,
			'W': -70,
			'S': -70,
			'DEFAULT': 0,
			'GAME_OVER': -100
		}
		return rewards.get(event, 0)

	# @staticmethod
	# def _compute_reward(state, action, grid_size):
	# 	"""Computes 'TOWARD_XX' rewards with a linear evolution from DEFAULT"""
	# 	action_order = {
	# 		'UP': 0,
	# 		'LEFT': 1,
	# 		'DOWN': 2,
	# 		'RIGHT': 3
	# 	}
	# 	dir_state = state[action_order[action]]
	# 	if dir_state[-1] == 'R':
	# 		return Interpreter._get_reward('TOWARD_RED_APPLE')(grid_size)
	# 	elif dir_state[-1] == 'G':
	# 		return Interpreter._get_reward('TOWARD_GREEN_APPLE')(grid_size)
	# 	return Interpreter._get_reward('DEFAULT')

