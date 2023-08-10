# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from cocoscrapers.modules.control import addonPath, addonVersion, joinPath
from cocoscrapers.windows.textviewer import TextViewerXML


def get():
	cocoscrapers_path = addonPath()
	cocoscrapers_version = addonVersion()
	changelogfile = joinPath(cocoscrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]CocoScrapers -  v%s - ChangeLog[/B]' % cocoscrapers_version
	windows = TextViewerXML('textviewer.xml', cocoscrapers_path, heading=heading, text=text)
	windows.run()
	del windows