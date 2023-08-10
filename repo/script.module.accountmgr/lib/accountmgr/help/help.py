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
	heading = '[B]My Accounts -  v%s - %s[/B]' % (accountmgr_version, file)
	windows = TextViewerXML('textviewer.xml', accountmgr_path, heading=heading, text=text)
	windows.run()
	del windows
