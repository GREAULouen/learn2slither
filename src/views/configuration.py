import pygame_menu

def init_configuration_view(app):
	menu = pygame_menu.Menu('Configuration', 1280, 720, theme=pygame_menu.themes.THEME_DARK)

	menu.add.button('Back', app.go_back)

	app.register_view("configuration", menu)
