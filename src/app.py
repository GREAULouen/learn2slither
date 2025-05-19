#!venv/bin/python
import pygame

from views.main import init_main_view
from views.configuration import init_configuration_view

class App:
	def __init__(self, args):
		pygame.init()
		self.surface = pygame.display.set_mode((1280, 720))
		pygame.display.set_caption("learn2slither")
		self.clock = pygame.time.Clock()

		self.views = {}
		self.current_view = None
		self.view_history = []
		self.args = args

		init_main_view(self)
		init_configuration_view(self)

		self.set_view("main")
		self.start_loop()

	def register_view(self, name, menu):
		self.views[name] = menu

	def set_view(self, name):
		if self.current_view is not None:
			self.view_history.append(self.current_view)
		self.current_view = name

	def go_back(self):
		if self.view_history:
			self.current_view = self.view_history.pop()

	def display_current_menu(self):
		if self.current_view in self.views:
			self.views[self.current_view].draw(self.surface)

	def start_loop(self):
		self.main_loop()

	def main_loop(self):
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					return

			self.surface.fill((0, 0, 0))

			if self.current_view in self.views:
				menu = self.views[self.current_view]
				menu.update(events)   # ← IMPORTANT: Update the menu with events
				menu.draw(self.surface)

			pygame.display.flip()
			self.clock.tick(60)
