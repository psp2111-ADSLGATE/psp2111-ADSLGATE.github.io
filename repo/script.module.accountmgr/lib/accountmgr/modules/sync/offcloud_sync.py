import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

from pathlib import Path
from libs.common import var

char_remov = ["'", ",", ")","("]

#Account Manager OffCloud
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_username = accountmgr.getSetting("offcloud.user")
your_password = accountmgr.getSetting("offcloud.pass")
your_userid = accountmgr.getSetting("offcloud.userid")
your_token = accountmgr.getSetting("offcloud.token")
          
class Auth:
    def offcloud_auth(self):
        #Fen Light
        try:
                if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt): #Check that the addon is installed and settings.db exists
                    
                    #Create database connection
                    from accountmgr.modules.db import offcloud_db
                    conn = offcloud_db.create_conn(var.fenlt_settings_db)
                    
                    #Get add-on settings to compare
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('oc.token',))
                        auth_oc = cursor.fetchone()
                        chk_auth_fenlt = str(auth_oc)
                        cursor.close()
                        
                        #Clean up database results
                        for char in char_remov:
                            chk_auth_fenlt = chk_auth_fenlt.replace(char, "")
                            
                        if not str(var.chk_accountmgr_offc) == chk_auth_fenlt: #Compare Account Mananger data to Add-on data. If they match, authorization is skipped
                            
                            #Write settings to database
                            from accountmgr.modules.db import offcloud_db
                            offcloud_db.auth_fenlt_oc()
                            var.remake_settings()
        except:
                xbmc.log('%s: Fen Light Offcloud Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Umbrella
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("offcloudtoken")
                        if not str(var.chk_accountmgr_offc) == str(chk_auth_umb) or str(chk_auth_umb) == '':

                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("offcloud.username", your_username)
                                addon.setSetting("offcloudtoken", your_token)
                                addon.setSetting("offcloud.enable", "true")
        except:
                xbmc.log('%s: Umbrella OffCloud Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
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

    #Infinity
        try:
                if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity):
                        chk_auth_infinity = xbmcaddon.Addon('plugin.video.infinity').getSetting("offcloudtoken")
                        if not str(var.chk_accountmgr_offc) == str(chk_auth_pov) or str(chk_auth_infinity) == '':

                                addon = xbmcaddon.Addon("plugin.video.infinity")
                                addon.setSetting("offcloud.username", your_username)
                                addon.setSetting("offcloudtoken", your_token)
                                addon.setSetting("offcloud.enable", "true")
        except:
                xbmc.log('%s: Infinity OffCloud Failed!' % var.amgr, xbmc.LOGINFO)
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
