# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from cocoscrapers.modules.control import addonPath, addonVersion, joinPath
from cocoscrapers.windows.textviewer import TextViewerXML


def get(file):
	cocoscrapers_path = addonPath()
	cocoscrapers_version = addonVersion()
	helpFile = joinPath(cocoscrapers_path, 'lib', 'cocoscrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]CocoScrapers -  v%s - %s[/B]' % (cocoscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', cocoscrapers_path, heading=heading, text=text)
	windows.run()
	del windows