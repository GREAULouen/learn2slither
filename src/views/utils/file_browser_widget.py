import os
import pygame

class FileBrowserWidget:
	def __init__(self, x, y, width, height, initial_path=os.getcwd(), font_size=30, callback=None):
		self.rect = pygame.Rect(x, y, width, height)
		self.path = initial_path
		self.font = pygame.font.Font(None, font_size)
		self.callback = callback

		self.entries = []
		self.selected_index = 0
		self.scroll_offset = 0
		self.entry_height = font_size + 10

		self.refresh()

	def refresh(self):
		try:
			entries = os.listdir(self.path)
			entries.sort()
			self.entries = ['..'] + entries
		except Exception:
			self.entries = ['..']
		self.selected_index = 0
		self.scroll_offset = 0

	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.selected_index = max(0, self.selected_index - 1)
			elif event.key == pygame.K_DOWN:
				self.selected_index = min(len(self.entries) - 1, self.selected_index + 1)
			elif event.key == pygame.K_RETURN:
				selected_name = self.entries[self.selected_index]
				selected_path = os.path.join(self.path, selected_name)
				if selected_name == '..':
					self.path = os.path.dirname(self.path)
					self.refresh()
				elif os.path.isdir(selected_path):
					self.path = selected_path
					self.refresh()
				else:
					if self.callback:
						self.callback(selected_path)

	def draw(self, surface):
		pygame.draw.rect(surface, (40, 40, 40), self.rect)
		visible_entries = self.rect.height // self.entry_height
		start_index = self.scroll_offset
		end_index = min(len(self.entries), start_index + visible_entries)

		for i in range(start_index, end_index):
			entry = self.entries[i]
			entry_path = os.path.join(self.path, entry)
			label = entry + ('/' if os.path.isdir(entry_path) else '')
			color = (255, 255, 255)
			if i == self.selected_index:
				color = (0, 255, 0)
			text_surf = self.font.render(label, True, color)
			surface.blit(text_surf, (self.rect.x + 5, self.rect.y + (i - start_index) * self.entry_height))