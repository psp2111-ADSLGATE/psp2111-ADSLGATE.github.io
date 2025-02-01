# -*- coding: utf-8 -*-
"""
	Account Manager
"""

import os.path
import xbmc
import xbmcaddon
import xbmcgui
from libs.common import var
from accountmgr.modules import control

addon_id = 'script.module.accountmgr'
addon = xbmcaddon.Addon(addon_id)
joinPath = os.path.join
api_key = control.setting('torbox.token')
torbox_icon = joinPath(os.path.join(addon.getAddonInfo('path'), 'resources', 'icons'), 'torbox.png')

class Torbox:

        def auth(self):
                api = xbmcgui.Dialog().input('Enter TorBox API Key:')
                if api == '':
                        control.notification(message="TorBox authorization failed!", icon=torbox_icon)
                        quit()
                else:
                        control.setSetting('torbox.token', api)
                        control.setSetting('torbox.acct_id', api)
                        control.notification_torbox(title='TorBox', message='TorBox Successfully Authorized', icon=torbox_icon) #Authorization complete. Start sync process

                '''def auth(self):
                if api_key:
                        control.notification(message="TorBox is already authorized!", icon=torbox_icon)
                        quit()
                else:
                        api = xbmcgui.Dialog().input('Enter TorBox API Key:')
                        control.setSetting('torbox.token', api)
                        control.setSetting('torbox.acct_id', api)
                        control.notification_torbox(title='TorBox', message='TorBox Successfully Authorized', icon=torbox_icon) #Authorization complete. Start sync process'''

        def revoke(self):
                if not control.okDialog():
                        return
                control.setSetting('torbox.token', '')
                control.notification(message="TorBox Authorization Revoked", icon=torbox_icon)


