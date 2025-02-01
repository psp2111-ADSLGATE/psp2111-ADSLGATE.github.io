import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

#Account Manager FilePursuit
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_file_api = accountmgr.getSetting("filepursuit.api.key")

class Auth:
        def file_auth(self):
               
        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb): #Check that the addon is installed and settings.xml exists
                                
                                #Get add-on setting to compare
                                chk_file = xbmcaddon.Addon('plugin.video.umbrella').getSetting("filepursuit.api")
                                enable_file = ("true")
                                
                                #Write data to settings.xml
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '': #Compare Account Mananger data to Add-on data. If they match authorization is skipped
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("filepursuit.enable", enable_file)
                                        addon.setSetting("filepursuit.api", your_file_api)
                except:
                        xbmc.log('%s: Umbrella FilePursuit Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Infinity
                try:
                        if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity):
                                
                                chk_file = xbmcaddon.Addon('plugin.video.infinity').getSetting("filepursuit.api")
                                enable_file = ("true")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("filepursuit.enable", enable_file)
                                        addon.setSetting("filepursuit.api", your_file_api)
                except:
                        xbmc.log('%s: Infinity FilePursuit Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Dradis
                try:
                        if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):
                                
                                chk_file = xbmcaddon.Addon('plugin.video.dradis').getSetting("filepursuit.api")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("filepursuit.api", your_file_api)
                except:
                        xbmc.log('%s: Dradis FilePursuit Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #All Accounts
                try:
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.allaccounts_ud):
                                os.mkdir(var.allaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                                
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.chkset_allaccounts):
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                        
                        if xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts):
                                
                                chk_file = xbmcaddon.Addon('script.module.allaccounts').getSetting("filepursuit.api.key")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("filepursuit.api.key", your_file_api)
                except:
                        xbmc.log('%s: All Accounts FilePursuit Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.myaccounts_ud):
                                os.mkdir(var.myaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                                
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.chkset_myaccounts):
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                                
                                chk_file = xbmcaddon.Addon('script.module.myaccounts').getSetting("filepursuit.api.key")
                                
                                if not str(var.chk_accountmgr_file) == str(chk_file) or str(chk_file) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("filepursuit.api.key", your_file_api)
                except:
                        xbmc.log('%s: My Accounts FilePursuit Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
