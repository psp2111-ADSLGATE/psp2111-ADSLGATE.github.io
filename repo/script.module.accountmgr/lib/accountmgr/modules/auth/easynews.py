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
easy_icon = joinPath(os.path.join(addon.getAddonInfo('path'), 'resources', 'icons'), 'easynews.png')

class Easynews:

        def auth(self):
                username = xbmcgui.Dialog().input('Enter Easynews Username:')
                password = xbmcgui.Dialog().input('Enter Easynews Password:')
                if username == '' or password == '':
                        control.notification(message="Easynews authorization failed!", icon=easy_icon)
                        quit()
                else:
                        control.setSetting('easynews.username', username)
                        control.setSetting('easynews.password', password)
                        control.notification_easynews(title='Easynews', message='Easynews Successfully Authorized', icon=easy_icon) #Authorization complete. Start sync process


