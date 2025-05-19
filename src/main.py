#!venv/bin/python
from environment import Environment
from agent import Agent
from vision import Vision
from interpreter import Interpreter
from cl_args import parse_arguments
from utils import print_progress_bar

import time
import numpy as np

def configure_agent(args):
	"""Configure the agent based on command-line arguments."""
	decay_rate = 0.0
	if not args.epsilon_decay == 'None':
		decay_rate = (1.0 - args.agent_epsilon) / args.sessions
	agent = Agent(
		epsilon=args.agent_epsilon,
		learning_rate=args.agent_learning_rate,
		discount_factor=args.agent_discount_factor,
		q_function=args.q_function,
		epsilon_decay_method=args.epsilon_decay,
		epsilon_decay_rate=decay_rate,
		grid_size=args.grid_size
	)
	if args.load:
		try:
			agent.load(args.load)
			print(f"Loaded model from {args.load}.")
		except FileNotFoundError:
			print(f"Error: Model file '{args.load}' not found.")
			exit(1)
	return agent

def train_or_test_session(agent, args):
	"""Run a training or testing session."""
	max_length = 0
	max_length_session = 0
	max_length_grid_size = 0
	objective = args.objective

	# Track the number of lines printed by previous visuals
	previous_lines = 0

	for session in range(args.sessions):
		if args.progressive_grid_size:
			method, start_size, end_size = args.progressive_grid_size
			start_size, end_size = int(start_size), int(end_size)

			def get_grid_size(session_idx, total_sessions):
				if method == "logarithmic":
					progress = np.log10(1 + (session_idx))
					progress /= np.log10(1 + (total_sessions - 1))
					return int(start_size + (end_size + 1 - start_size) * progress)
				elif method == "random":
					return np.random.randint(
						low=int(2 * start_size / 3), high=int(5 * end_size / 3)
					)
				else:
					return start_size  # Fallback

			grid_size = get_grid_size(session_idx=session, total_sessions=args.sessions)
			env = Environment(size=grid_size)
			objective = max(3, int(grid_size**2 * args.objective / args.grid_size**2))
			objective = min(objective, grid_size**2 - 6)
		else:
			env = Environment(size=args.grid_size)

		vision = Vision._get_vision(env)
		state = Interpreter._get_state(vision)
		game_over = False
		previous_lines = 0

		while not game_over:
			if args.visual in ['terminal-only']:
				# Clear the previous printed lines
				print("\033[F\033[K" * previous_lines, end='')

				# Print environment
				env_repr = repr(env)
				print(env_repr)

				# Print vision
				vision_repr = Vision._get_vision_representation(vision)
				print(vision_repr)

			# If step-by-step mode, wait for user input
			if args.step_by_step:
				input("Press Enter to perform the next step...")

			action = agent.act(state)
			if args.visual in ['terminal-only']:
				# Print action
				print(action)

				# Update the line count for next clearing
				previous_lines = env_repr.count("\n") + vision_repr.count("\n") + 1 + 3

				# Add a delay for readability
				if args.visual_speed > 0.0:
					time.sleep(args.visual_speed)

			reward = env.step(action)

			if reward == Interpreter._get_reward("GAME_OVER") or len(env.snake) == 0:
				game_over = True
				if not args.test_mode:  # Update agent in learning mode
					agent.update_game_over(state, action)
			else:
				# if reward == Interpreter._get_reward('DEFAULT'):
				# 	reward = Interpreter._compute_reward(state, action, args.grid_size)
				vision = Vision._get_vision(env)
				next_state = Interpreter._get_state(vision)
				if not args.test_mode:  # Update agent in learning mode
					agent.update(state, action, reward, next_state)
				state = next_state
				if len(env.snake) >= objective:
					game_over = True

		if args.visual in ['terminal-only'] and session != args.sessions - 1:
			# Clear the previous printed lines
			print("\033[F\033[K" * previous_lines, end='')

		# Track maximum length and update
		if len(env.snake) > max_length:
			max_length = len(env.snake)
			max_length_session = session + 1
			max_length_grid_size = env.size

		# Print the progress bar if enabled
		if args.progress_bar and not args.visual in ['terminal-only']:
			print_progress_bar(session, args.sessions, max_length, max_length_session, max_length_grid_size, args)

	# Final print for progress bar
	if args.progress_bar and not args.visual in ['terminal-only']:
		print("\n")

	# Save the model after training (if applicable)
	if args.save and not args.test_mode:
		agent.save(args.save)
		print(f"Model saved to {args.save}.")

if __name__ == "__main__":
	args = parse_arguments()
	print("Starting Snake AI...")

	# Configure the agent
	agent = configure_agent(args)

	# Run the training or testing sessions
	train_or_test_session(agent, args)
