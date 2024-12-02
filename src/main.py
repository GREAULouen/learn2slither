#!venv/bin/python
from environment import Environment
from agent import Agent
from vision import Vision
from interpreter import Interpreter
from cl_args import parse_arguments
from utils import print_progress_bar

# import pygame
# from pygame.locals import *
# class App:
# 	"""
# 	Main Application class, containing:
# 	  - main loop
# 	  - window management
# 	"""

# 	def __init__(self):
# 		self._running = True
# 		self._display_surf = None
# 		self.size = self.width, self.height = 1280, 720
# 		self.margin = self.top_margin, self.left_margin = 10, 10
# 		self.sq_size = min(self.width - 2*self.left_margin, self.height - 2*self.top_margin) // 10
# 		self.board = [
# 			pygame.Rect(
# 				self.left_margin + (col * self.sq_size),
# 				self.top_margin  + (row * self.sq_size),
# 				self.sq_size,
# 				self.sq_size
# 			)
# 			for row in range(10)
# 			for col in range(10)
# 		]
# 		self.FPS = pygame.time.Clock()

# 	def on_init(self):
# 		pygame.init()
# 		pygame.display.set_caption("learn2slither")
# 		self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
# 		self._running = True
# 		self.FPS.tick(60)

# 	def on_event(self, event):
# 		if event.type == pygame.QUIT:
# 			self._running = False
# 	def on_loop(self):
# 		self._display_surf.fill(pygame.Color(0, 0, 0))
# 	def on_render(self):
# 		self.on_render_board()
# 		pygame.display.flip()
# 	def on_cleanup(self):
# 		pygame.quit()

# 	def on_render_board(self):
# 		for cell in self.board:
# 			pygame.draw.rect(self._display_surf,
# 					color=pygame.Color(0, 0, 255),
# 					rect=cell,
# 					width=1)


# 	def on_execute(self):
# 		if self.on_init() == False:
# 			self._running = False

# 		while( self._running ):
# 			for event in pygame.event.get():
# 				self.on_event(event)
# 			self.on_loop()
# 			self.on_render()
# 		self.on_cleanup()

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
		epsilon_decay_rate=decay_rate
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

	for session in range(args.sessions):
		env = Environment(size=args.grid_size)
		vision = Vision._get_vision(env)
		state = Interpreter._get_state(vision)
		game_over = False

		while not game_over:
			if args.visual == 'on':
				print(env)
				Vision._print_vision(vision)
			# If step-by-step mode, wait for user input
			if args.step_by_step:
				input("Press Enter to perform the next step...")

			action = agent.act(vision)
			if args.visual == 'on':
				print(action)
			reward = env.step(action)

			if reward == Interpreter._get_reward("GAME_OVER") or len(env.snake) == 0:
				game_over = True
				if not args.test_mode:  # Update agent in learning mode
					agent.update_game_over(state, action)
			else:
				if reward == Interpreter._get_reward('DEFAULT'):
					reward = Interpreter._compute_reward(state, action)
				vision = Vision._get_vision(env)
				next_state = Interpreter._get_state(vision)
				if not args.test_mode:  # Update agent in learning mode
					agent.update(state, action, reward, next_state)
				state = next_state

		# Track maximum length and update
		if len(env.snake) > max_length:
			max_length = len(env.snake)
			max_length_session = session + 1

		# Print the progress bar if enabled
		if args.progress_bar:
			print_progress_bar(session, args.sessions, max_length, max_length_session, args)

	# Final print for progress bar
	if args.progress_bar:
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
