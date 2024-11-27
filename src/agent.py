import numpy as np


class Agent:
	def __init__(self,
		learning_rate=0.1,
		discount_factor=0.9,
		epsilon=1.0):
		self.q_table = {}
		self.learning_rate = learning_rate
		self.gamma = discount_factor
		self.epsilon = epsilon

	def act(self, state):
		"""Choose an action using epsilon-greedy policy."""
		if np.random.rand() < self.epsilon:
			return np.random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
		return max(self.q_table.get(state, {}), key=self.q_table.get, default='UP')

	def update(self, state, action, reward, next_state):
		"""Update Q-values using the Q-learning formula."""
		current_q = self.q_table.get(state, {}).get(action, 0)
		max_future_q = max(self.q_table.get(next_state, {}).values(), default=0)
		self.q_table[state][action] = current_q + self.lr * (reward + self.gamma * max_future_q - current_q)

	def save(self, filepath):
		"""Save the Q-table to a file."""
		with open(filepath, 'w') as f:
			f.write(f"{self.q_table}")

	def load(self, filepath):
		"""Load the Q-table from a file."""
		with open(filepath, 'r') as f:
			self.q_table = eval(f.read())