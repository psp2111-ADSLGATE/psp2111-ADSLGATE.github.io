import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

from pathlib import Path
from libs.common import var

char_remov = ["'", ",", ")","("]

#Account Manager Easy Debrid
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_token = accountmgr.getSetting("easydebrid.token")
your_acct_id = accountmgr.getSetting("easydebrid.acct_id")
          
class Auth:
    def easydebrid_auth(self):
    #Fen Light
        try:
                if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt): #Check that the addon is installed and settings.db exists
                    
                    #Create database connection
                    from accountmgr.modules.db import easydebrid_db
                    conn = easydebrid_db.create_conn(var.fenlt_settings_db)
                    
                    #Get add-on settings to compare
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ed.token',))
                        auth_ed = cursor.fetchone()
                        chk_auth_fenlt = str(auth_ed)
                        cursor.close()
                        
                        #Clean up database results
                        for char in char_remov:
                            chk_auth_fenlt = chk_auth_fenlt.replace(char, "")
                            
                        if not str(var.chk_accountmgr_ed) == chk_auth_fenlt: #Compare Account Mananger data to Add-on data. If they match, authorization is skipped
                            
                            #Write settings to database
                            from accountmgr.modules.db import easydebrid_db
                            easydebrid_db.auth_fenlt_ed()
                            var.remake_settings()
        except:
                xbmc.log('%s: Fen Light Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass


    #Umbrella
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("easydebridtoken")
                        if not str(var.chk_accountmgr_ed) == str(chk_auth_umb) or str(chk_auth_umb) == '':
                        
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("easydebridtoken", your_token)
                                addon.setSetting("easydebrid.enable", 'true')

        except:
                xbmc.log('%s: Umbrella Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass


    #POV
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("ed.token")
                        if not str(var.chk_accountmgr_ed) == str(chk_auth_pov) or str(chk_auth_pov) == '':

                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("ed.token", your_token)
                                addon.setSetting("ed.account_id", your_acct_id)
                                addon.setSetting("ed.enabled", 'true')

        except:
                xbmc.log('%s: POV Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Infinity
        try:
                if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity):
                        chk_auth_infinity = xbmcaddon.Addon('plugin.video.infinity').getSetting("easydebridtoken")
                        if not str(var.chk_accountmgr_ed) == str(chk_auth_infinity) or str(chk_auth_infinity) == '':

                                addon = xbmcaddon.Addon("plugin.video.infinity")
                                addon.setSetting("easydebridtoken", your_token)
                                addon.setSetting("easydebrid.username", your_acct_id)
                                addon.setSetting("easydebrid.enable", 'true')
                                addon.setSetting("easydebrid.expirynotice", '0')

        except:
                xbmc.log('%s: Infinity Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Dradis
        try:
                if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):
                        chk_auth_dradis = xbmcaddon.Addon('plugin.video.dradis').getSetting("easydebrid.token")
                        if not str(var.chk_accountmgr_ed) == str(chk_auth_dradis) or str(chk_auth_dradis) == '':

                                addon = xbmcaddon.Addon("plugin.video.dradis")
                                addon.setSetting("easydebrid.token", your_token)
                                addon.setSetting("easydebrid.username", your_acct_id)
                                addon.setSetting("easydebrid.enable", 'true')
                                addon.setSetting("easydebrid.expires", '0')

        except:
                xbmc.log('%s: Dradis Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass

