import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

from pathlib import Path
from libs.common import var

#Account Manager OffCloud
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_username = accountmgr.getSetting("offcloud.user")
your_password = accountmgr.getSetting("offcloud.pass")
your_userid = accountmgr.getSetting("offcloud.userid")
your_token = accountmgr.getSetting("offcloud.token")
          
class Auth:
    def offcloud_auth(self):       
    #POV
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("oc.token")
                        if not str(var.chk_accountmgr_offc) == str(chk_auth_pov) or str(chk_auth_pov) == '':

                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("oc.account_id", your_username)
                                addon.setSetting("oc.token", your_token)
                                addon.setSetting("oc.enabled", "true")
        except:
                xbmc.log('%s: POV OffCloud Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
     #Dradis
        try:
                if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):
                        chk_auth_dradis = xbmcaddon.Addon('plugin.video.dradis').getSetting("realdebrid.token")
                        if not str(var.chk_accountmgr_offc) == str(chk_auth_dradis) or str(chk_auth_dradis) == '':

                                addon = xbmcaddon.Addon("plugin.video.dradis")
                                addon.setSetting("offcloud.username", your_username)
                                addon.setSetting("offcloud.token", your_token)
                                addon.setSetting("offcloud.enabled", "true")
        except:
                xbmc.log('%s: Dradis OffCloud Failed!' % var.amgr, xbmc.LOGINFO)
                pass
