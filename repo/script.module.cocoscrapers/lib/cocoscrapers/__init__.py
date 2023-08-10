# -*- coding: UTF-8 -*-

from os.path import join as osPath_join, dirname as osPath_dirname
from os import walk as osWalk
from pkgutil import walk_packages
from cocoscrapers.modules.control import setting as getSetting

debug = getSetting('debug.enabled') == 'true'
sourceFolder = 'sources_cocoscrapers'

def sources(specified_folders=None, ret_all=False):
	try:
		sourceDict = []
		append = sourceDict.append
		sourceFolderLocation = osPath_join(osPath_dirname(__file__), sourceFolder)
		sourceSubFolders = [x[1] for x in osWalk(sourceFolderLocation)][0]
		if specified_folders: sourceSubFolders = specified_folders
		for i in sourceSubFolders:
			for loader, module_name, is_pkg in walk_packages([osPath_join(sourceFolderLocation, i)]):
				if is_pkg: continue
				if ret_all or enabledCheck(module_name):
					try:
						module = loader.find_module(module_name).load_module(module_name)
						append((module_name, module.source))
					except Exception as e:
						if debug:
							from cocoscrapers.modules import log_utils
							log_utils.log('Error: Loading module: "%s": %s' % (module_name, e), level=log_utils.LOGWARNING)
		return sourceDict
	except:
		from cocoscrapers.modules import log_utils
		log_utils.error()
		return []

def enabledCheck(module_name):
	try:
		if getSetting('provider.' + module_name) == 'true': return True
		else: return False
	except:
		from cocoscrapers.modules import log_utils
		log_utils.error()
		return True

def pack_sources(sourceSubFolder='torrents'):
	try:
		sourceList = []
		sourceList_append = sourceList.append
		sourceFolderLocation = osPath_join(osPath_dirname(__file__), sourceFolder)
		for loader, module_name, is_pkg in walk_packages([osPath_join(sourceFolderLocation, sourceSubFolder)]):
			if is_pkg: continue
			module = loader.find_module(module_name).load_module(module_name)
			if module.source.pack_capable: sourceList_append(module_name)
		return sourceList
	except:
		from cocoscrapers.modules import log_utils
		log_utils.error()