import random
import numpy as np

# Board possible states:
#   - O: Empty cell
#   - W: Wall (first layer outside the board)
#   - H: snake's Head
#   - S: snake's Body part
#   - G: Green apple
#   - R: Red apple


class Environment:
	def __init__(self, size=10, manual_initialization=False, snake=[], green_apples=[], red_apples=[]):
		self.size = size
		self.board = np.zeros((size, size), dtype=str)
		self.board.fill('0')
		self.snake = snake
		self.green_apples = green_apples
		self.red_apples = red_apples
		self._update_board()
		self.actions = {
			'UP' : (-1, 0),
			'LEFT' : (0, -1),
			'DOWN' : (1, 0),
			'RIGHT' : (0, 1)
		}
		if not manual_initialization:
			self.reset()
		else:
			self._update_board()

	def reset(self):
		"""Initializes the Environment"""
		self.board.fill('0')
		self.snake = self._initialize_snake()
		self.green_apples = [
			self._random_empty_cell(new_value='G')
			for k in range(2)
		]
		self.red_apples = [self._random_empty_cell(new_value='R')]

	def step(self, action):
		"""Modify the environment according to the action taken"""
		new_head = self._compute_new_head(action)
		collision = self._check_collision(new_head)
		if collision in ['W', 'S']:
			return 'GAME_OVER'
		old_tail = self.snake[-1]
		reward = 0
		if collision == '0':
			self._move_snake(new_head)
		else:
			reward = self._handle_apples(new_head, old_tail)
		return reward

	# Utility functions #

	def _update_cell(self, cell, new_value):
		"""Updates the cell w/ its new value"""
		if not new_value in ['0', 'W', 'H', 'S', 'G', 'R']:
			raise ValueError(f"Trying to update a cell with an unknown value: {new_value}")
		self.board[cell] = new_value

	def _update_board(self):
		"""Updates the entire board w/ the valeus set in snake/green/red apples"""
		# Clear the board
		self.board = np.zeros((self.size, self.size), dtype=str)
		self.board.fill('0')

		# Place the snake
		for i, (x, y) in enumerate(self.snake):
			self.board[x][y] = 'H' if i == 0 else 'S'

		# Place green apples
		for x, y in self.green_apples:
			self.board[x][y] = 'G'

		# Place red apples
		for x, y in self.red_apples:
			self.board[x][y] = 'R'

	def _random_empty_cell(self, new_value):
		"""Find a random empty cell on the board."""
		empty_cells = [
			(x, y)
			for x in range(self.size)
			for y in range(self.size)
			if self.board[(x, y)] == '0'
		]
		if not empty_cells:
			raise ValueError("No empty cells available on the board.")
		random_cell = random.choice(empty_cells)
		self._update_cell(random_cell, new_value)
		return random_cell

	def _initialize_snake(self):
		"""Initializes the Snake w/ 1 Head and 2 Body parts"""
		snake = []
		empty_cells = [
			(x, y) for x in range(self.size) for y in range(self.size)
			if self.board[x][y] == '0'
		]
		if not empty_cells:
			raise ValueError("No empty cells available on the board.")
		random_cell = random.choice(empty_cells)
		snake.append(random_cell)
		self.board[random_cell] = 'H'

		for _ in range(2):
			empty_cells = [
				(random_cell[0] + (x - 1), random_cell[1] + (y - 1))
				for x in range(2)
				for y in range(2)
				if (x == 1 or y == 1) \
					and random_cell[0] + (x - 1) >= 0 \
					and random_cell[0] + (x - 1) < self.size \
					and random_cell[1] + (y - 1) >= 0 \
					and random_cell[1] + (y - 1) < self.size \
					and self.board[random_cell[0] + (x - 1)][random_cell[1] + (y - 1)] == '0'
			]
			if not empty_cells:
				self.reset()
			random_cell = random.choice(empty_cells)
			snake.append(random_cell)
			self.board[random_cell] = 'S'
		return snake

	def _move_snake(self, new_head):
		"""Move the Snake's Body according to its new head cell"""
		old_snake = self.snake.copy()
		self.snake = [new_head] + [
			old_snake[i - 1]
			for i in range(1, len(old_snake))
		]

	def _compute_new_head(self, action):
		"""Move the Snake's Head according to the given action"""
		if not action in self.actions:
			raise ValueError(f"Unknow action: {action}")
		new_head = (
			self.snake[0][0] + self.actions[action][0],
			self.snake[0][1] + self.actions[action][1]
		)
		return new_head

	def _check_collision(self, new_head):
		"""Compute collision between the updated Snake's Head & walls/body"""
		if  new_head[0] < 0 or \
			new_head[0] >= self.size or \
			new_head[1] < 0 or \
			new_head[1] >= self.size:
			return 'W'
		return self.board[new_head]

	def _handle_apples(self, new_head, old_tail):
		"""Modify the Snake according to the effect of the apple taken & Computes a reward score"""
		if self.board[new_head] == 'R':
			self._move_snake(new_head)
			self.snake = self.snake[:-1]
			self.red_apples = [self._random_empty_cell('R')]
			self._update_board()
			return -1
		self.green_apples.remove(new_head)
		self._move_snake(new_head)
		self.snake.append(old_tail)
		self._update_board()
		self.green_apples.append(self._random_empty_cell('G'))
		return 1


	def __repr__(self):
		"""Return a string representation of the board with colors."""
		# ANSI escape codes for colors
		GREEN = "\033[92m"
		RED = "\033[91m"
		BLUE = "\033[94m"
		DARK_BLUE = "\033[34m"
		RESET = "\033[0m"

		# Generate the board representation
		repr_lines = []
		first_row = "   | "
		for k in range(self.size):
			first_row += (f" {k}")
		repr_lines.append(first_row)
		repr_lines.append("---+---------------------")
		for x in range(self.size):
			row = [f" {x} | "]
			for y in range(self.size):
				cell = self.board[(x,y)]
				if cell == 'G':  # Green apple
					row.append(f"{GREEN}G{RESET}")
				elif cell == 'R':  # Red apple
					row.append(f"{RED}R{RESET}")
				elif (x, y) == self.snake[0]:  # Snake's head
					row.append(f"{DARK_BLUE}H{RESET}")
				elif (x, y) in self.snake[1:]:  # Snake's body
					row.append(f"{BLUE}S{RESET}")
				else:  # Empty space
					row.append("0")
			repr_lines.append(" ".join(row))
		return "\n".join(repr_lines)
