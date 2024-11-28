import numpy as np
from math import exp
from interpreter import Interpreter


class Agent:
	def __init__(self,
			learning_rate=0.1,
			discount_factor=0.9,
			epsilon=1.0,
			q_function='time_difference',
			epsilon_decay_method='None',
			epsilon_decay_rate=0.0):
		self.q_table = {}
		self.learning_rate = learning_rate
		self.gamma = discount_factor
		self.epsilon = epsilon
		self.q_function = q_function
		self.epsilon_decay_method = epsilon_decay_method
		self.epsilon_decay_rate = epsilon_decay_rate
		if not self.epsilon_decay_method == 'None':
			self.epsilon = 1.0

	def act(self, state):
		"""Choose an action using epsilon-greedy policy."""
		if np.random.rand() < self.epsilon \
			or state not in self.q_table:
			return np.random.choice(['UP', 'LEFT', 'DOWN', 'RIGHT'])
		max_action = ('UP', self.q_table[state]['UP'])
		for action in ['LEFT', 'DOWN', 'RIGHT']:
			if self.q_table[state][action] > max_action[1]:
				max_action = (action, self.q_table[state][action])
		return max_action[0]

	def update(self, state, action, reward, next_state):
		if self.q_function == 'time-difference':
			self._time_difference(state, action, reward, next_state)
		elif self.q_function == 'bellman':
			self._bellman_equation(state, action, reward, next_state)
		else:
			raise ValueError(f"Unknown q_function: {self.q_function}")

	def update_game_over(self, state, action):
		"""Update the Q-value of the state/action pair that led to death"""
		if not state in self.q_table:
			self.q_table[state] = {
				'UP': 0,
				'LEFT': 0,
				'DOWN': 0,
				'RIGHT': 0
			}
		self.q_table[state][action] = -1.0

	def update_epsilon(self, current_session):
		"""Updates agent's epsilon for epsilon-greedy policy"""
		if self.epsilon_decay_method == 'None':
			pass
		elif self.epsilon_decay_method == 'linear':
			self._linear_epsilon_decay(current_session)
		elif self.epsilon_decay_method == 'exponential':
			self._exponential_epsilon_decay(current_session)
		else:
			raise ValueError(f"Unknown epsilon decay method: {self.epsilon_decay_method}")

	def save(self, filepath):
		"""Save the Q-table to a file."""
		with open(filepath, 'w') as f:
			f.write(f"{self.q_table}")

	def load(self, filepath):
		"""Load the Q-table from a file."""
		with open(filepath, 'r') as f:
			self.q_table = eval(f.read())

	# Argument selected methods #

	def _time_difference(self, state, action, reward, next_state):
		"""Update Q-values using the Time-Difference Q-learning formula."""
		# Q(s, a) += alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))
		if not state in self.q_table:
			self.q_table[state] = {
				'UP': 0,
				'LEFT': 0,
				'DOWN': 0,
				'RIGHT': 0
			}
		current_q = self.q_table.get(state, {}).get(action, 0)
		max_future_q = max(self.q_table.get(next_state, {}).values(), default=0)
		self.q_table[state][action] = current_q + self.learning_rate * \
			(reward + self.gamma * max_future_q - current_q)

	def _bellman_equation(self, state, action, reward, next_state):
		"""Update Q-values using the Bellman's Equation Q-learning formula."""
		# Q(s, a) = reward + gamma * max(Q(s', a'))
		if not state in self.q_table:
			self.q_table[state] = {
				'UP': 0,
				'LEFT': 0,
				'DOWN': 0,
				'RIGHT': 0
			}
		max_next_q = max([
				self.q_table.get((next_state, a), 0)
				for a in ["UP", "DOWN", "LEFT", "RIGHT"]
			])
		self.q_table[state][action] = reward + self.gamma * max_next_q

	def _linear_epsilon_decay(self, current_session):
		"""Update epsilon using a linear decay rate"""
		self.epsilon = max(
			self.epsilon,
			1.0 - self.epsilon_decay_rate * current_session
		)

	def _exponential_epsilon_decay(self, current_session):
		"""Update epsilon using an exponential decay rate"""
		self.epsilon = max(
			self.epsilon,
			exp(-self.epsilon_decay_rate * current_session)
		)
