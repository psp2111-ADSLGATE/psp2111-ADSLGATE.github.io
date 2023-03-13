# -*- coding: utf-8 -*-
"""
	My Accounts
"""

from myaccts.modules.control import addonPath, addonVersion, joinPath
from myaccts.windows.textviewer import TextViewerXML

def get(file):
	myaccts_path = addonPath()
	myaccts_version = addonVersion()
	helpFile = joinPath(myaccts_path, 'lib', 'myaccts', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]My Accounts -  v%s - %s[/B]' % (myaccts_version, file)
	windows = TextViewerXML('textviewer.xml', myaccts_path, heading=heading, text=text)
	windows.run()
	del windows