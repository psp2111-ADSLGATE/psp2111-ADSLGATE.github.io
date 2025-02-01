# -*- coding: utf-8 -*-
"""
	Account Manager
"""

import os.path
import xbmc
import xbmcaddon
import xbmcgui
from accountmgr.modules import control

addon_id = 'script.module.accountmgr'
addon = xbmcaddon.Addon(addon_id)
joinPath = os.path.join
file_icon = joinPath(os.path.join(addon.getAddonInfo('path'), 'resources', 'icons'), 'filepursuit.png')

class Filepursuit:

        def auth(self):
                api = xbmcgui.Dialog().input('Enter FilePursuit API Key:')
                control.setSetting('filepursuit.api.key', api)
                control.notification_filepursuit(title='FilePursuit', message='FilePursuit Successfully Authorized', icon=file_icon) #Authorization complete. Start sync process


