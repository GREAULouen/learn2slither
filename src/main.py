# import pygame
# from pygame.locals import *

from environment import Environment

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
	env = Environment(
		size=10,
		manual_initialization=True,
		snake=[(1, 1), (0, 1), (0, 2)],
		green_apples=[(1, 0), (1, 2)],
		red_apples=[(2, 1)]
	)

	print(env)
	print(env.step(action='RIGHT'))
	print(env)

	# theApp = App()
	# theApp.on_execute()
