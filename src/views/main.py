import pygame_menu
import pygame_menu.events

def init_main_view(app):
	menu = pygame_menu.Menu('learn2slither', 1280, 720, theme=pygame_menu.themes.THEME_DARK)

	menu.add.button('Configuration', lambda: app.set_view("configuration"))
	menu.add.button('Exit', pygame_menu.events.EXIT)

	app.register_view("main", menu)