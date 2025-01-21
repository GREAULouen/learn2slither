import numpy as np
from math import exp, floor
from interpreter import Interpreter


class Agent:
	def __init__(self,
			learning_rate=0.1,
			discount_factor=0.9,
			epsilon=1.0,
			q_function='time_difference',
			epsilon_decay_method='None',
			epsilon_decay_rate=0.0,
			grid_size=10):
		self.q_table = {}
		self.learning_rate = learning_rate
		self.gamma = discount_factor
		self.epsilon = epsilon
		self.q_function = q_function
		self.epsilon_decay_method = epsilon_decay_method
		self.epsilon_decay_rate = epsilon_decay_rate
		if not self.epsilon_decay_method == 'None':
			self.epsilon = 1.0
		self.grid_size = grid_size
		self.action_order = {
			'UP': 0,
			'LEFT': 1,
			'DOWN': 2,
			'RIGHT': 3
		}

	def act(self, state):
		"""Choose an action using epsilon-greedy policy."""

		for states in state:
			if not states in self.q_table:
				self.q_table[states] = self._initialize_q_value(states)
		dir_states = [self.q_table[states]
				for states in state]

		if np.random.rand() < self.epsilon:
			non_suicidal_actions = [
				key
				for key in self.action_order
				if not dir_states[self.action_order[key]] == -100.0
			]
			if len(non_suicidal_actions) > 0:
				return np.random.choice(non_suicidal_actions)
			return np.random.choice(['UP', 'LEFT', 'DOWN', 'RIGHT'])

		max_action = [(0, dir_states[0])]
		for k in range(1, 4):
			if dir_states[k] > max_action[1]:
				max_action = [(k, dir_states[k])]
			elif dir_states[k] == max_action[1]:
				max_action.append((k, dir_states[k]))
		return np.random.choice([
			['UP', 'LEFT', 'DOWN', 'RIGHT'][i]
			for (i, value) in max_action
		])
		# return ['UP', 'LEFT', 'DOWN', 'RIGHT'][max_action[0]]

	def update(self, state, action, reward, next_state):
		if self.q_function == 'time-difference':
			self._time_difference(state, action, reward, next_state)
		elif self.q_function == 'bellman':
			self._bellman_equation(state, action, reward, next_state)
		else:
			raise ValueError(f"Unknown q_function: {self.q_function}")

	def update_game_over(self, state, action):
		"""Update the Q-value of the state/action pair that led to death"""
		dir_state = state[self.action_order[action]]
		self.q_table[dir_state] = -100.0

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
		dir_state = state[self.action_order[action]]
		if not dir_state in self.q_table:
			self.q_table[dir_state] = self._initialize_q_value(dir_state)
		if dir_state == '0':
			return
		for states in next_state:
			if not states in self.q_table:
				self.q_table[states] = self._initialize_q_value(states)
		current_q = self.q_table.get(dir_state, 0)
		max_future_q = max([
				self.q_table[states]
				for states in next_state
			])
		self.q_table[dir_state] = current_q + self.learning_rate * \
			(reward + self.gamma * max_future_q - current_q)

	def _bellman_equation(self, state, action, reward, next_state):
		"""Update Q-values using the Bellman's Equation Q-learning formula."""
		# Q(s, a) = reward + gamma * max_a'(Q(s', a'))
		dir_state = state[self.action_order[action]]
		if not dir_state in self.q_table:
			self.q_table[dir_state] = self._initialize_q_value(dir_state)
		if dir_state == '0':
			return
		for states in next_state:
			if not states in self.q_table:
				self.q_table[states] = self._initialize_q_value(states)
		max_next_q = max([
				self.q_table[states]
				for states in next_state
			])
		self.q_table[dir_state] = reward + self.gamma * max_next_q

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

	def _initialize_q_value(self, state):
		"""Computes the initial q_value of the state based on its potential"""
		rewards = [
			Interpreter._get_reward(state[i]) * (len(state) + 1 - i) / (len(state) + 1)
			for i in range(len(state))
			if state[i] in ['G', 'R', 'S', 'W']
		]
		total = 0
		for r in rewards:
			total += r
		# if total != 0:
		# 	print(f"Initializing {state} to {total}")
		return total

		# if not state[-1] in ['G', 'R']:
		# 	return 0
		# if state[-1] == 'R':
		# 	print(f"new state: {state} => {Interpreter._get_reward('EAT_RED_APPLE')}")
		# 	return Interpreter._get_reward('EAT_RED_APPLE')
		# else:
		# 	return Interpreter._get_reward('EAT_GREEN_APPLE')
