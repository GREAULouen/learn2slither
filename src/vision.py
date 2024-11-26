from environment import Environment


class Vision:
	@staticmethod
	def _get_vision(env: Environment):
		"""Computes the Agent's vision from its environment"""
		row, col = 'W', 'W'
		for c in range(env.size):
			row += env.board[(env.snake[0][0], c)]
		for r in range(env.size):
			col += env.board[(r, env.snake[0][1])]
		return ((env.snake[0][0] + 1, env.snake[0][1] + 1), row + 'W', col + 'W')

	@staticmethod
	def _print_vision(vision: tuple):
		# ANSI escape codes for colors
		GREEN = "\033[92m"
		RED = "\033[91m"
		BLUE = "\033[94m"
		DARK_BLUE = "\033[34m"
		RESET = "\033[0m"

		# Define the color mapping for the board elements
		color_map = {
			'G': GREEN,
			'R': RED,
			'S': BLUE,
			'H': DARK_BLUE,
			'0': '',
			'W': '',
		}

		repr = "\n"

		# Build the column above the Snake's Head row
		for row in range(vision[0][0]):
			row_repr = ""
			for col in range(vision[0][1]):
				row_repr += f" "
			repr += row_repr + f"{color_map.get(vision[2][row], '')}{vision[2][row]}{RESET}\n"

		row_repr = ""
		for col in range(len(vision[1])):
			row_repr += f"{color_map.get(vision[1][col])}{vision[1][col]}{RESET}"
		repr += row_repr + "\n"

		# Build the column under the Snake's Head row
		for row in range(vision[0][0] + 1, len(vision[1])):
			row_repr = ""
			for col in range(vision[0][1]):
				row_repr += " "
			repr += row_repr + f"{color_map.get(vision[2][row])}{vision[2][row]}{RESET}\n"

		return repr