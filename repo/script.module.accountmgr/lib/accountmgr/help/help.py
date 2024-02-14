# -*- coding: utf-8 -*-
"""
	Account Manager
"""

from accountmgr.modules.control import addonPath, addonVersion, joinPath
from accountmgr.windows.textviewer import TextViewerXML

def get(file):
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - %s[/B]' % (accountmgr_version, file)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_tmdb():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'tmdbUser.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - TMDb Login Help[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_meta():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'metaAuth.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - Metadata API[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_nondebrid():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'nonDebrid.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - Furk/Easynews/FilePursuit[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_custom():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'custom_keys.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - Custom Trakt API Keys[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_restore():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'restore.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - Restore to Default[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_readme():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'readme.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - Readme[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows

def get_issues():
	accountmgr_path = addonPath()
	accountmgr_version = addonVersion()
	helpFile = joinPath(accountmgr_path, 'lib', 'accountmgr', 'help', 'issues.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]Account Manager -  v%s - Reporting Issues[/B]' % (accountmgr_version)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
