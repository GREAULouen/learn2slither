import pygame
from pygame.locals import *

import pygame_menu as pm
from utils import Slider, Checkbox, FileSelector
# from settings_page import SettingsPage  # (to be created)
# from start_page import StartPage  # (to be created)
# from game_screen import GameScreen  # (to be created)

class App:
	def __init__(self):
		self.running = True
		self.display = None
		self.size = self.width, self.height = 1280, 720
		self.current_screen = None

	def on_init(self):
		pygame.init()
		pygame.display.set_caption("Learn2Slither")
		self.display = pygame.display.set_mode(self.size)
		self.current_screen = StartPage(self.display, self.set_screen)
		self.running = True

	def set_screen(self, new_screen):
		"""Switch between screens."""
		self.current_screen = new_screen

	def on_event(self, event):
		if event.type == pygame.QUIT:
			self.running = False
		# else:
		# 	self.current_screen.handle_event(event)

	def on_loop(self):
		self.current_screen.update()

	def on_render(self):
		self.current_screen.render()
		pygame.display.flip()

	def on_execute(self):
		self.on_init()
		while self.running:
			for event in pygame.event.get():
				self.on_event(event)
			self.on_loop()
			self.on_render()
		pygame.quit()


class StartPage:
	def __init__(self, display, change_screen):
		self.display = display
		self.change_screen = change_screen
		self.main_menu = pm.Menu(
			title="Learn2Slither",
			width=1280,
			height=720,
			theme=pm.themes.THEME_GREEN
		)
		self.define_menu()
		self.font = pygame.font.SysFont(None, 36)

	def settings_action(self):
		print(f"Clicked on Settings button")
		self.change_screen(SettingsPage(self.display, self.change_screen, config_type="sessions"))

	def define_menu(self):
		self.main_menu.add.button(
			title="Settings",
			action=self.settings_action,
			font_color=(255, 255, 255),
			background_color=(0, 255, 0)
		)
		self.main_menu.add.button(
			title="Exit",
			action=pm.events.EXIT,
			font_color=(0, 0, 0),
			background_color=(255, 0, 0)
		)

	def update(self):
		pass

	def render(self):
		self.main_menu.mainloop(self.display)
		# self.display.fill((30, 30, 30))  # Background color
		# for label, rect in self.buttons.items():
		# 	pygame.draw.rect(self.display, (70, 130, 180), rect)
		# 	text = self.font.render(label, True, (255, 255, 255))
		# 	self.display.blit(text, (rect.x + 10, rect.y + 10))


class SettingsPage:
	def __init__(self, display, change_screen, config_type="general"):
		self.display = display
		self.change_screen = change_screen
		self.sliders = [
			Slider(100, 100, 300, 0.1, 1.0, 0.5),
		]
		self.checkboxes = [
			Checkbox(100, 200, "Enable Visuals", checked=True),
		]
		self.file_selector = FileSelector(100, 300, 200)

	def handle_event(self, event):
		for slider in self.sliders:
			slider.handle_event(event)
		for checkbox in self.checkboxes:
			checkbox.handle_event(event)
		self.file_selector.handle_event(event)

	def update(self):
		pass

	def render(self):
		self.display.fill((30, 30, 30))
		for slider in self.sliders:
			slider.draw(self.display)
		for checkbox in self.checkboxes:
			checkbox.draw(self.display)
		self.file_selector.draw(self.display)
