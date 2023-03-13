# -*- coding: utf-8 -*-
"""
	My Accounts
"""

from myaccts.modules.control import addonPath, addonVersion, joinPath
from myaccts.windows.textviewer import TextViewerXML


def get():
	myaccts_path = addonPath()
	myaccts_version = addonVersion()
	changelogfile = joinPath(myaccts_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]My Accounts -  v%s - ChangeLog[/B]' % myaccts_version
	windows = TextViewerXML('textviewer.xml', myaccts_path, heading=heading, text=text)
	windows.run()
	del windows