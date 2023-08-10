# -*- coding: utf-8 -*-
"""
	CocoScrapers Module  Modified 01-02-23 UD
"""

from json import dumps as jsdumps, loads as jsloads
import os.path
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
from xml.dom.minidom import parse as mdParse
#import xml.etree.ElementTree as ET #python 3.11 bug screws element tree. everything changed was left commented out.

addon = xbmcaddon.Addon
addonObject = addon('script.module.cocoscrapers')
addonInfo = addonObject.getAddonInfo
getLangString = addonObject.getLocalizedString
condVisibility = xbmc.getCondVisibility
infoLabel = xbmc.getInfoLabel
execute = xbmc.executebuiltin
jsonrpc = xbmc.executeJSONRPC
monitor_class = xbmc.Monitor
monitor = xbmc.Monitor()

dialog = xbmcgui.Dialog()
homeWindow = xbmcgui.Window(10000)
progressDialog = xbmcgui.DialogProgress()
progress_line = '%s[CR]%s[CR]%s'

deleteFile = xbmcvfs.delete
existsPath = xbmcvfs.exists
openFile = xbmcvfs.File
makeFile = xbmcvfs.mkdir
makeDirs = xbmcvfs.mkdirs
renameFile = xbmcvfs.rename
transPath = xbmcvfs.translatePath
joinPath = os.path.join

SETTINGS_PATH = transPath(joinPath(addonInfo('path'), 'resources', 'settings.xml'))
dataPath = transPath(addonInfo('profile'))
cacheFile = joinPath(dataPath, 'cache.db')
undesirablescacheFile = joinPath(dataPath, 'undesirables.db')
plexSharesFile = joinPath(dataPath, 'plexshares.db')
settingsFile = joinPath(dataPath, 'settings.xml')

def getKodiVersion(full=False):
	if full: return xbmc.getInfoLabel("System.BuildVersion")
	else: return int(xbmc.getInfoLabel("System.BuildVersion")[:2])

def setting(id, fallback=None):
	try: settings_dict = jsloads(homeWindow.getProperty('cocoscrapers_settings'))
	except: settings_dict = make_settings_dict()
	if settings_dict is None: settings_dict = settings_fallback(id)
	value = settings_dict.get(id, '')
	if fallback is None: return value
	if value == '': return fallback
	return value

def settings_fallback(id):
	return {id: addonObject.getSetting(id)}

def setSetting(id, value):
	return addonObject.setSetting(id, value)

def make_settings_dict(): # service runs upon a setting change
	try:
		#root = ET.parse(settingsFile).getroot()
		root = mdParse(settingsFile) #minidom instead of element tree
		curSettings = root.getElementsByTagName("setting") #minidom instead of element tree
		settings_dict = {}
		for item in curSettings:
			dict_item = {}
			#setting_id = item.get('id')
			setting_id = item.getAttribute('id') #minidom instead of element tree
			#setting_value = item.text
			try:
				setting_value = item.firstChild.data #minidom instead of element tree
			except:
				setting_value = None
			if setting_value is None: setting_value = ''
			dict_item = {setting_id: setting_value}
			settings_dict.update(dict_item)
		homeWindow.setProperty('cocoscrapers_settings', jsdumps(settings_dict))
		return settings_dict
	except:
		return None

def refresh_debugReversed(): # called from service "onSettingsChanged" to clear cocoscrapers.log if setting to reverse has been changed
	if homeWindow.getProperty('cocoscrapers.debug.reversed') != setting('debug.reversed'):
		homeWindow.setProperty('cocoscrapers.debug.reversed', setting('debug.reversed'))
		execute('RunPlugin(plugin://script.module.cocoscrapers/?action=tools_clearLogFile)')

def lang(language_id):
	return getLangString(language_id)

def sleep(time):  # Modified `sleep` command that honors a user exit request
	while time > 0 and not monitor.abortRequested():
		xbmc.sleep(min(100, time))
		time = time - 100

def isVersionUpdate():
	versionFile = joinPath(dataPath, 'installed.version')
	try:
		if not xbmcvfs.exists(versionFile):
			f = open(versionFile, 'w')
			f.close()
	except:
		LOGINFO = 1 # (LOGNOTICE(2) deprecated in 19, use LOGINFO(1))
		xbmc.log('CocoScrapers Addon Data Path Does not Exist. Creating Folder....', LOGINFO)
		addon_folder = transPath('special://profile/addon_data/script.module.cocoscrapers')
		xbmcvfs.mkdirs(addon_folder)
	try:
		with open(versionFile, 'r') as fh: oldVersion = fh.read()
	except: oldVersion = '0'
	try:
		curVersion = addon('script.module.cocoscrapers').getAddonInfo('version')
		if oldVersion != curVersion:
			with open(versionFile, 'w') as fh: fh.write(curVersion)
			return True
		else: return False
	except:
		from cocoscrapers.modules import log_utils
		log_utils.error()
		return False

def clean_settings():
	def _make_content(dict_object):
		content = '<settings version="2">'
		for item in dict_object:
			if item['id'] in active_settings:
				if 'default' in item and 'value' in item: content += '\n    <setting id="%s" default="%s">%s</setting>' % (item['id'], item['default'], item['value'])
				elif 'default' in item: content += '\n    <setting id="%s" default="%s"></setting>' % (item['id'], item['default'])
				elif 'value' in item: content += '\n    <setting id="%s">%s</setting>' % (item['id'], item['value'])
				else: content += '\n    <setting id="%s"></setting>'
			else: removed_settings.append(item)
		content += '\n</settings>'
		return content
	addon_id = 'script.module.cocoscrapers'
	try:
		removed_settings = []
		active_settings = []
		current_user_settings = []
		addon = xbmcaddon.Addon(id=addon_id)
		addon_name = addon.getAddonInfo('name')
		addon_dir = transPath(addon.getAddonInfo('path'))
		profile_dir = transPath(addon.getAddonInfo('profile'))
		active_settings_xml = joinPath(addon_dir, 'resources', 'settings.xml')
		#root = ET.parse(active_settings_xml).getroot()
		#for item in root.findall(r'./section/category/group/setting'):
		root = mdParse(active_settings_xml) #minidom instead of element tree
		root = root.getElementsByTagName("setting") #minidom instead of element tree
		for item in root:
			#setting_id = item.get('id')
			setting_id = item.getAttribute('id') #minidom instead of element tree
			if setting_id:
				active_settings.append(setting_id)
		settings_xml = joinPath(profile_dir, 'settings.xml')
		#root = ET.parse(settings_xml).getroot()
		root = mdParse(settings_xml) #minidom instead of element tree
		root = root.getElementsByTagName("setting") #minidom instead of element tree 
		for item in root:
			dict_item = {}
			#setting_id = item.get('id')
			#setting_default = item.get('default')
			#setting_value = item.text
			setting_id = item.getAttribute('id') #minidom instead of element tree
			setting_default = item.getAttribute('default') #minidom instead of element tree
			try:
				setting_value = item.firstChild.data #minidom instead of element tree
			except:
				setting_value = None
			dict_item['id'] = setting_id
			if setting_value:
				dict_item['value'] = setting_value
			if setting_default:
				dict_item['default'] = setting_default
			current_user_settings.append(dict_item)
		new_content = _make_content(current_user_settings)
		nfo_file = xbmcvfs.File(settings_xml, 'w')
		nfo_file.write(new_content)
		nfo_file.close()
		sleep(200)
		notification(title=addon_name, message=lang(32042).format(str(len(removed_settings))))
	except:
		from cocoscrapers.modules import log_utils
		log_utils.error()
		notification(title=addon_name, message=32043)

def addonId():
	return addonInfo('id')

def addonName():
	return addonInfo('name')

def addonVersion():
	return addonInfo('version')

def addonIcon():
	return addonInfo('icon')

def addonPath():
	return transPath(addonInfo('path'))

def addonEnabled(addon_id):
	return condVisibility('System.AddonIsEnabled(%s)' % addon_id)

def addonInstalled(addon_id):
	return condVisibility('System.HasAddon(%s)' % addon_id)

def openSettings(query=None, id=addonInfo('id')):
	try:
		hide()
		execute('Addon.OpenSettings(%s)' % id)
		if not query: return
		c, f = query.split('.')
		execute('SetFocus(%i)' % (int(c) - 100))
		execute('SetFocus(%i)' % (int(f) - 80))
	except:
		return

def getProviderDefaults():
	provider_defaults = {}
	try:
		for item in mdParse(SETTINGS_PATH).getElementsByTagName("setting"): #holy shit look at that.
			setting_id = item.getAttribute('id') #minidom instead of element tree
			if not setting_id.startswith('provider.'): continue
			try: defaulttext = item.getElementsByTagName('default')[0].firstChild.data
			except: defaulttext = 'false'
			provider_defaults[setting_id] = defaulttext or 'false'
	except: pass
	return provider_defaults

def setProviderDefaults(provider_defaults=None):
	try:
		if provider_defaults is None: provider_defaults = getProviderDefaults()
		for k, v in provider_defaults.items(): setSetting(k, v)
	except: return

def hide():
	execute('Dialog.Close(busydialog)')
	execute('Dialog.Close(busydialognocancel)')


####################################################
# --- Dialogs
####################################################
def notification(title=None, message=None, icon=None, time=3000, sound=False):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	if icon is None or icon == '' or icon == 'default': icon = addonIcon()
	elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
	elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
	elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
	dialog.notification(heading, body, icon, time, sound=sound)

def yesnoDialog(line, heading=addonInfo('name'), nolabel='', yeslabel=''):
	return dialog.yesno(heading, line, nolabel, yeslabel)

def selectDialog(list, heading=addonInfo('name')):
	return dialog.select(heading, list)

def multiselectDialog(list, preselect=[], heading=addonInfo('name')):
	return dialog.multiselect(heading, list, preselect=preselect)

def okDialog(title=None, message=None):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	return dialog.ok(heading, body)
####################################################
