import pygame_menu
from pygame_menu.locals import ALIGN_LEFT, INPUT_TEXT
import pygame_menu.locals
from pygame_menu.widgets import Frame, Label, RangeSlider, Selector, ToggleSwitch, Table

from .utils.file_browser_widget import FileBrowserWidget


def init_configuration_view(app):
	config = app.config
	menu = pygame_menu.Menu('Configuration', 1280, 720, theme=pygame_menu.themes.THEME_DARK)

	frame = Frame(width=800, height=600, orientation=pygame_menu.locals.ORIENTATION_VERTICAL)
	table = Table()

	def row(label, widget):
		label_widget = Label(label) #, align=ALIGN_LEFT, font_size=30)
		table.add_row(label_widget, widget)

	def make_range_slider(label, attr, range_vals, step=1):
		row(label, RangeSlider(
			'', default_value=getattr(config, attr), range_values=range_vals, increment=step,
			onchange=lambda val: setattr(config, attr, int(val) if step == 1 else round(val, 2)),
			width=400
		))

	# Sliders
	make_range_slider('Grid Size:', 'grid_size', (3, 101), 1)
	make_range_slider('Objective Length:', 'objective', (4, 100), 1)
	make_range_slider('Epsilon:', 'agent_epsilon', (0.0, 1.0), 0.01)
	make_range_slider('Learning Rate:', 'agent_learning_rate', (0.0, 1.0), 0.01)
	make_range_slider('Discount Factor:', 'agent_discount_factor', (0.0, 1.0), 0.01)
	make_range_slider('Visual Speed (s):', 'visual_speed', (0.0, 2.0), 0.1)

	# Selectors
	q_options = [('Time Difference', 'time-difference'), ('Bellman', 'bellman')]
	q_index = 0 if config.q_function == 'time-difference' else 1
	row('Q Function:', Selector(
		'', q_options, default=q_index,
		onchange=lambda _, val: setattr(config, 'q_function', val)
	))

	visual_options = ['all', 'terminal-only', 'graphical-interface-only', 'off']
	visual_index = visual_options.index(config.visual) if config.visual in visual_options else 1
	row('Visual:', Selector(
		'', [(v, v) for v in visual_options], default=visual_index,
		onchange=lambda _, val: setattr(config, 'visual', val)
	))

	# Toggles
	row('Step-by-step:', ToggleSwitch('', config.step_by_step,
		onchange=lambda val: setattr(config, 'step_by_step', val)))
	row('Test Mode:', ToggleSwitch('', config.test_mode,
		onchange=lambda val: setattr(config, 'test_mode', val)))
	row('Progress Bar:', ToggleSwitch('', config.progress_bar,
		onchange=lambda val: setattr(config, 'progress_bar', val)))

	# --- File Browsers outside the frame ---
	def on_load_selected(path):
		print(f"Selected load model: {path}")
		config.load = path

	def on_save_selected(path):
		print(f"Selected save path: {path}")
		config.save = path

	load_browser = FileBrowserWidget(x=820, y=150, width=400, height=250, callback=on_load_selected)
	save_browser = FileBrowserWidget(x=820, y=450, width=400, height=250, callback=on_save_selected)

	# Add main frame & button to menu
	frame.pack(table)
	menu.add.generic_widget(frame)
	menu.add.button('Back', app.go_back)

	# Register both menu and extra widgets
	app.register_view("configuration", menu, widgets=[load_browser, save_browser])
