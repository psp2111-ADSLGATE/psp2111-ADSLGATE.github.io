# -*- coding: utf-8 -*-
import re
from windows import content_settings
from windows.base_window import BaseDialog, translate_path, open_file, notification, addon_skins_folder
# from modules.kodi_utils import logger

settings_contents = ['menu_settings', 'content_settings']

class SettingsManager(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, *args)
		self.settings_file = translate_path(addon_skins_folder + 'settings_manager.xml')
		self.original_content = ''
	
	def insert_content(self):
		try:
			with open_file(self.settings_file) as f: content = f.read()
			self.original_content = str(content)
		except: pass
		if not self.original_content:
			notification('Error Opening Settings')
			return self.close()
		for item in settings_contents: content = re.sub(r'<!-- %s -->' % item, getattr(content_settings, item), content)
		with open_file(self.settings_file, 'w') as f: f.write(content)
	
	def reset_content(self):
		with open_file(self.settings_file, 'w') as f: f.write(self.original_content)

	def run(self):
		self.insert_content()
		if self.original_content: self.doModal()
		self.reset_content()
		self.clearProperties()

class SettingsManagerFolders(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, *args)

	def run(self):
		self.doModal()
		self.clearProperties()
