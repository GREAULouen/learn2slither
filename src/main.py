# import pygame
# from pygame.locals import *

from environment import Environment
from agent import Agent
from vision import Vision
from interpreter import Interpreter

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

if __name__ == "__main__":
	# env = Environment(
	# 	size=10,
	# 	manual_initialization=True,
	# 	snake=[(1, 1), (0, 1), (0, 2)],
	# 	green_apples=[(1, 0), (1, 2)],
	# 	red_apples=[(2, 1)]
	# )

	agent = Agent(epsilon=0.05)
	agent.load('/Users/lgreau/goinfre/models/test.txt')

	for k in range(10000000):
		env = Environment()
		vision = Vision._get_vision(env)
		state = Interpreter._get_state(vision)
		restart = False
		while not restart:
			# print(env)
			# Vision._print_vision(vision)
			action = agent.act(vision)
			# print(action)
			reward = env.step(action)

			if reward == Interpreter._get_reward('GAME_OVER') \
				or len(env.snake) == 0:
				restart = True
				agent.update_game_over(state, action)
			else:
				if len(env.snake) > 9:
					print(f"length > 9")
					agent.save('/Users/lgreau/goinfre/models/test.txt')
					print(env)
					print(f"{k} games")
					exit(0)
				vision = Vision._get_vision(env)
				next_state = Interpreter._get_state(vision)
				agent.update(state, action, reward, next_state)
				state = next_state


		# print(f"states visited: {len(agent.q_table)}")
	agent.save('/Users/lgreau/goinfre/models/test.txt')


	# theApp = App()
	# theApp.on_execute()
