# -*- coding: utf-8 -*-
"""
	Account Manager
"""

import re
import requests
import os.path
import xbmc
import xbmcaddon
import xbmcgui
from libs.common import var
from requests.adapters import HTTPAdapter
from accountmgr.modules import control

addon_id = 'script.module.accountmgr'
addon = xbmcaddon.Addon(addon_id)
joinPath = os.path.join
session = requests.Session()
session.mount('https://offcloud.com/api', HTTPAdapter(max_retries=1, pool_maxsize=100))
apikey = control.setting('offcloud.token')
username = control.setting('offcloud.user')
password = control.setting('offcloud.pass')
offcloud_icon = joinPath(os.path.join(addon.getAddonInfo('path'), 'resources', 'icons'), 'offcloud.png')

class Offcloud:               

        def auth(self):
                #Get USERID
                data = {'username': username, 'password': password}
                r = session.request('post', 'https://offcloud.com/api/login', data=data)
                try:
                        r = r.json()
                except:
                        r = {}
                user_id = r.get('userId')
                
                if not user_id:
                        control.notification(message="OffCloud Authorization Failed", icon=offcloud_icon)
                else:
                        control.setSetting('offcloud.userid', user_id)

                #Get API Key
                if apikey:
                        control.notification(message="OffCloud is already authorized!", icon=offcloud_icon)
                        quit()
                        
                api_path = 'https://offcloud.com/api/key'
                r = session.request('post', 'https://offcloud.com/api/key', user_id, timeout=3)
                try:
                        r = r.json()
                except:
                        r = {}
                api_key = r.get('apiKey')

                if not api_key:
                        control.notification(message="OffCloud Authorization Failed", icon=offcloud_icon)
                else:
                        control.setSetting('offcloud.token', api_key)
                control.notification_offcloud(title='OffCloud', message='OffCloud Successfully Authorized', icon=offcloud_icon) #Authorization complete. Start sync process

        def revoke(self):
                if not control.okDialog():
                        return
                control.setSetting('offcloud.user', '')
                control.setSetting('offcloud.pass','')
                control.setSetting('offcloud.token', '')
                control.setSetting('offcloud.userid', '')
                control.notification(message="OffCloud Authorization Revoked", icon=offcloud_icon)
