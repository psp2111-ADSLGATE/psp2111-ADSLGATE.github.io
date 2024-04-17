# -*- coding: utf-8 -*-
"""
	Account Manager
"""
import xbmcvfs
from accountmgr.modules.control import addonPath, addonVersion, joinPath
from accountmgr.windows.textviewer import TextViewerXML

supported_path = xbmcvfs.translatePath('special://home/addons/script.module.accountmgr/resources/skins/Default/media/common/')

def get():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(accountmgr_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - ChangeLog[/B]' % accountmgr_version
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_supported_trakt():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_trakt.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported Trakt Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_supported_simkl():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_simkl.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported Simkl Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_supported_debrid():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_debrid.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported Debrid Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
	
def get_supported_offcloud():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_offcloud.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported OffCloud Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_supported_easy():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_easy.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported Easynews Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
	
def get_supported_filepursuit():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_file.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported FilePursuit Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
	
def get_supported_meta():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	changelogfile = joinPath(supported_path, 'supported_meta.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager - Supported Metadata Add-ons[/B]'
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
