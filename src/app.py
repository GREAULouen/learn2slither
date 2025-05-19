#!venv/bin/python
import pygame

from views.main import init_main_view
from views.configuration import init_configuration_view

class App:
	def __init__(self, config):
		pygame.init()
		self.surface = pygame.display.set_mode((1280, 720))
		pygame.display.set_caption("learn2slither")
		self.clock = pygame.time.Clock()

		self.views = {}
		self.current_view = None
		self.view_history = []
		self.config = config

		self.additional_widgets = {}  # NEW: optional extra widgets per view

		init_main_view(self)
		init_configuration_view(self)

		self.set_view("main")
		self.start_loop()

	def register_view(self, name, menu, widgets=None):
		self.views[name] = menu
		if widgets:
			self.additional_widgets[name] = widgets

	def set_view(self, name):
		if self.current_view is not None:
			self.view_history.append(self.current_view)
		self.current_view = name

	def go_back(self):
		if self.view_history:
			self.current_view = self.view_history.pop()

	def main_loop(self):
		while True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					return

			self.surface.fill((0, 0, 0))

			# Menu logic
			if self.current_view in self.views:
				menu = self.views[self.current_view]
				menu.update(events)
				menu.draw(self.surface)

			# Handle additional widgets (like file browsers)
			widgets = self.additional_widgets.get(self.current_view, [])
			for widget in widgets:
				widget.handle_event(events)
				widget.draw(self.surface)

			pygame.display.flip()
			self.clock.tick(60)
