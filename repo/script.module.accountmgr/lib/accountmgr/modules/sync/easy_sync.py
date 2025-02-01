import xbmc, xbmcaddon
import xbmcvfs
import os

from pathlib import Path
from accountmgr.modules import control
from libs.common import var

char_remov = ["'", ",", ")","("]

#Account Manager Easynews
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_easy_user = accountmgr.getSetting("easynews.username")
your_easy_pass = accountmgr.getSetting("easynews.password")

class Auth:
        def easy_auth(self):

        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen): #Check that the addon is installed and settings.xml exists
                                
                                #Get add-on setting to compare
                                chk_easy = xbmcaddon.Addon('plugin.video.fen').getSetting("easynews_password")
                                enable_easy = ("true")
                                
                                #Write data to settings.xml
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '': #Compare Account Mananger data to Add-on data. If they match authorization is skipped
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        xbmc.log('%s: Fen Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
 
        #Fen Light
                try:
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt): #Check that the addon is installed and settings.db exists
                            
                            #Create database connection
                            from accountmgr.modules.db import easy_db
                            conn = easy_db.create_conn(var.fenlt_settings_db)
                            
                            #Get add-on settings to compare
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('easynews_user',))
                                auth_easy = cursor.fetchone()
                                chk_auth_fenlt = str(auth_easy)
                                cursor.close()
                                
                                #Clean up database results
                                for char in char_remov:
                                    chk_auth_fenlt = chk_auth_fenlt.replace(char, "")
                                    
                                if not str(var.chk_accountmgr_easy) == chk_auth_fenlt: #Compare Account Mananger data to Add-on data. If they match, authorization is skipped
                                    
                                    #Write settings to database
                                    from accountmgr.modules.db import easy_db
                                    easy_db.auth_fenlt_easy()
                                    var.remake_settings()
                except:
                        xbmc.log('%s: Fen Light Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #afFENity
                '''try:
                        if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen): #Check that the addon is installed and settings.db exists
                            
                            from accountmgr.modules.db import easy_db
                            conn = easy_db.create_conn(var.affen_settings_db)
                            
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('easynews_user',))
                                auth_easy = cursor.fetchone()
                                chk_auth_affen = str(auth_easy)
                                cursor.close()
                                
                                for char in char_remov:
                                    chk_auth_affen = chk_auth_affen.replace(char, "")
                                    
                                if not str(var.chk_accountmgr_easy) == chk_auth_affen: #Compare Account Mananger data to Add-on data. If they match, authorization is skipped
                                    
                                    from accountmgr.modules.db import easy_db
                                    easy_db.auth_affen_easy()
                                    var.remake_settings()
                except:
                        xbmc.log('%s: afFENity Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass'''

        #Coalition
                try:
                        if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):

                                chk_easy = xbmcaddon.Addon('plugin.video.coalition').getSetting("easynews_password")
                                enable_easy = ("true")
                         
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        xbmc.log('%s: Coalition Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #POV
                try:
                        if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov) and accountmgr.getSetting("easynews.password") != '':

                                chk_easy = xbmcaddon.Addon('plugin.video.pov').getSetting("easynews_password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("provider.easynews", enable_easy)
                                        addon.setSetting("easynews_user", your_easy_user)
                                        addon.setSetting("easynews_password", your_easy_pass)
                except:
                        xbmc.log('%s: POV Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):

                                chk_easy = xbmcaddon.Addon('plugin.video.umbrella').getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("easynews.enable", enable_easy)
                                        addon.setSetting("easynews.user", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        xbmc.log('%s: Umbrella Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Infinity
                try:
                        if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity):

                                chk_easy = xbmcaddon.Addon('plugin.video.infinity').getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("easynews.enable", enable_easy)
                                        addon.setSetting("easynews.user", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        xbmc.log('%s: Infinity Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Dradis
                try:
                        if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):

                                chk_easy = xbmcaddon.Addon('plugin.video.dradis').getSetting("easynews.password")
                                enable_easy = ("true")
                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("easynews.username", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        xbmc.log('%s: Dradis Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #The Crew
                try:
                        if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.crew_ud):
                                os.mkdir(var.crew_ud)
                                xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))
                                
                        if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.chkset_crew):
                                xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))

                        if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                                chk_easy = xbmcaddon.Addon('plugin.video.thecrew').getSetting("easynews.password")

                                     
                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("easynews.user", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        xbmc.log('%s: The Crew Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #All Accounts
                try:
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.allaccounts_ud):
                                os.mkdir(var.allaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                                
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.chkset_allaccounts):
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))

                        if xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts):

                                chk_easy = xbmcaddon.Addon('script.module.allaccounts').getSetting("easynews.password")

                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("easynews.username", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        xbmc.log('%s: All Accounts Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.myaccounts_ud):
                                os.mkdir(var.myaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                                
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.chkset_myaccounts):
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))

                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):

                                chk_easy = xbmcaddon.Addon('script.module.myaccounts').getSetting("easynews.password")

                                if not str(var.chk_accountmgr_easy) == str(chk_easy) or str(chk_easy) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("easynews.username", your_easy_user)
                                        addon.setSetting("easynews.password", your_easy_pass)
                except:
                        xbmc.log('%s: My Accounts Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
