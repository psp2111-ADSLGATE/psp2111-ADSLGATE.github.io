import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from accountmgr.modules import control
from libs.common import var

#Account Manager Furk
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_furk_user = accountmgr.getSetting("furk.username")
your_furk_pass = accountmgr.getSetting("furk.password")
your_furk_api = accountmgr.getSetting("furk.api.key")

class Auth:
        def furk_auth(self):

        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen): #Check that the addon is installed and settings.xml exists
                                
                                #Get add-on setting to compare
                                chk_furk = xbmcaddon.Addon('plugin.video.fen').getSetting("furk_password")
                                enable_furk = ("true")
                                
                                #Write data to settings.xml
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '': #Compare Account Mananger data to Add-on data. If they match authorization is skipped
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        xbmc.log('%s: Fen Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Ezra
                try:
                        if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.ezra').getSetting("furk_password")
                                enable_furk = ("true")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.ezra")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        xbmc.log('%s: Ezra Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Coalition
                try:
                        if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):

                                chk_furk = xbmcaddon.Addon('plugin.video.coalition').getSetting("furk_password")
                                enable_furk = ("true")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        xbmc.log('%s: Coalition Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #POV
                try:
                        if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.pov').getSetting("furk_password")
                                enable_furk = ("true")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("provider.furk", enable_furk)
                                        addon.setSetting("furk_login", your_furk_user)
                                        addon.setSetting("furk_password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        xbmc.log('%s: POV Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):

                                chk_furk = xbmcaddon.Addon('plugin.video.umbrella').getSetting("furk.user_pass")
                                enable_furk = ("true")
                                
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("furk.enable", enable_furk)
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Umbrella Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Dradis
                try:
                        if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):

                                chk_furk = xbmcaddon.Addon('plugin.video.dradis').getSetting("furk.user_pass")
                                
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("furk.username", your_furk_user)
                                        addon.setSetting("furk.password", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Dradis Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Taz19
                try:
                        if xbmcvfs.exists(var.chk_taz) and xbmcvfs.exists(var.chkset_taz):

                                chk_furk = xbmcaddon.Addon('plugin.video.taz19').getSetting("furk.password")
                                
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.taz19")
                                        addon.setSetting("furk.login", your_furk_user)
                                        addon.setSetting("furk.password", your_furk_pass)
                                        addon.setSetting("furk_api_key", your_furk_api)
                except:
                        xbmc.log('%s: Taz Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #The Crew
                try:
                        if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.crew_ud):
                                os.mkdir(var.crew_ud)
                                xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))
                                
                        if not xbmcvfs.exists(var.chkset_crew):
                                xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))
                        
                        if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.thecrew').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: The Crew Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Homelander
                try:
                        if xbmcvfs.exists(var.chk_homelander) and not xbmcvfs.exists(var.homelander_ud):
                                os.mkdir(var.homelander_ud)
                                xbmcvfs.copy(os.path.join(var.homelander), os.path.join(var.chkset_homelander))
                                
                        if not xbmcvfs.exists(var.chkset_homelander):
                                xbmcvfs.copy(os.path.join(var.homelander), os.path.join(var.chkset_homelander))
                        
                        if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.homelander').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Homelander Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Quicksilver
                try:
                        if xbmcvfs.exists(var.chk_quick) and not xbmcvfs.exists(var.quick_ud):
                                os.mkdir(var.quick_ud)
                                xbmcvfs.copy(os.path.join(var.quick), os.path.join(var.chkset_quick))
                                
                        if not xbmcvfs.exists(var.chkset_quick):
                                xbmcvfs.copy(os.path.join(var.quick), os.path.join(var.chkset_quick))
                        
                        if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Quicksilver Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Chains Genocide
                try:
                        if xbmcvfs.exists(var.chk_genocide) and not xbmcvfs.exists(var.genocide_ud):
                                os.mkdir(var.genocide_ud)
                                xbmcvfs.copy(os.path.join(var.genocide), os.path.join(var.chkset_genocide))
                                
                        if not xbmcvfs.exists(var.chkset_genocide):
                                xbmcvfs.copy(os.path.join(var.genocide), os.path.join(var.chkset_genocide))
                        
                        if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Chains Genocide Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Absolution
                try:
                        if xbmcvfs.exists(var.chk_absol) and not xbmcvfs.exists(var.absol_ud):
                                os.mkdir(var.absol_ud)
                                xbmcvfs.copy(os.path.join(var.absol), os.path.join(var.chkset_absol))
                                
                        if not xbmcvfs.exists(var.chkset_absol):
                                xbmcvfs.copy(os.path.join(var.absol), os.path.join(var.chkset_absol))
                        
                        if xbmcvfs.exists(var.chk_absol) and xbmcvfs.exists(var.chkset_absol):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.absolution').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Absolution Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                    
        #Shazam
                try:
                        if xbmcvfs.exists(var.chk_shazam) and not xbmcvfs.exists(var.shazam_ud):
                                os.mkdir(var.shazam_ud)
                                xbmcvfs.copy(os.path.join(var.shazam), os.path.join(var.chkset_shazam))
                                
                        if not xbmcvfs.exists(var.chkset_shazam):
                                xbmcvfs.copy(os.path.join(var.shazam), os.path.join(var.chkset_shazam))
                        
                        if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.shazam').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Shazam Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Nightwing
                try:
                        if xbmcvfs.exists(var.chk_night) and not xbmcvfs.exists(var.night_ud):
                                os.mkdir(var.night_ud)
                                xbmcvfs.copy(os.path.join(var.night), os.path.join(var.chkset_night))
                                
                        if not xbmcvfs.exists(var.chkset_night):
                                xbmcvfs.copy(os.path.join(var.night), os.path.join(var.chkset_night))
                        
                        if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.nightwing').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nightwing")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Nightwing Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #TheLab
                try:
                        if xbmcvfs.exists(var.chk_lab) and not xbmcvfs.exists(var.lab_ud):
                                os.mkdir(var.lab_ud)
                                xbmcvfs.copy(os.path.join(var.lab), os.path.join(var.chkset_lab))
                                
                        if not xbmcvfs.exists(var.chkset_lab):
                                xbmcvfs.copy(os.path.join(var.lab), os.path.join(var.chkset_lab))
                        
                        if xbmcvfs.exists(var.chk_lab) and xbmcvfs.exists(var.chkset_lab):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.thelab').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thelab")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: TheLab Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Alvin
                try:
                        if xbmcvfs.exists(var.chk_alvin) and not xbmcvfs.exists(var.alvin_ud):
                                os.mkdir(var.alvin_ud)
                                xbmcvfs.copy(os.path.join(var.alvin), os.path.join(var.chkset_alvin))
                                
                        if not xbmcvfs.exists(var.chkset_alvin):
                                xbmcvfs.copy(os.path.join(var.alvin), os.path.join(var.chkset_alvin))
                        
                        if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.alvin').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Alvin Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Moria
                try:
                        if xbmcvfs.exists(var.chk_moria) and not xbmcvfs.exists(var.moria_ud):
                                os.mkdir(var.moria_ud)
                                xbmcvfs.copy(os.path.join(var.moria), os.path.join(var.chkset_moria))
                                
                        if not xbmcvfs.exists(var.chkset_moria):
                                xbmcvfs.copy(os.path.join(var.moria), os.path.join(var.chkset_moria))
                        
                        if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.moria').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Moria Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Nine Lives
                try:
                        if xbmcvfs.exists(var.chk_nine) and not xbmcvfs.exists(var.nine_ud):
                                os.mkdir(var.nine_ud)
                                xbmcvfs.copy(os.path.join(var.nine), os.path.join(var.chkset_nine))
                                
                        if not xbmcvfs.exists(var.chkset_nine):
                                xbmcvfs.copy(os.path.join(var.nine), os.path.join(var.chkset_nine))
                        
                        if xbmcvfs.exists(var.chk_nine) and xbmcvfs.exists(var.chkset_nine):
                                
                                chk_furk = xbmcaddon.Addon('plugin.video.nine').getSetting("furk.user_pass")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("furk.user_name", your_furk_user)
                                        addon.setSetting("furk.user_pass", your_furk_pass)
                                        addon.setSetting("furk.api", your_furk_api)
                except:
                        xbmc.log('%s: Nine Lives Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #All Accounts
                try:
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.allaccounts_ud):
                                os.mkdir(var.allaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                                
                        if not xbmcvfs.exists(var.chkset_allaccounts):
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                        
                        if xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts):
                                
                                chk_furk = xbmcaddon.Addon('script.module.allaccounts').getSetting("furk.password")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("furk.username", your_furk_user)
                                        addon.setSetting("furk.password", your_furk_pass)
                                        addon.setSetting("furk.api.key", your_furk_api)
                except:
                        xbmc.log('%s: All Accounts Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.myaccounts_ud):
                                os.mkdir(var.myaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                                
                        if not xbmcvfs.exists(var.chkset_myaccounts):
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                                
                                chk_furk = xbmcaddon.Addon('script.module.myaccounts').getSetting("furk.password")
                        
                                if not str(var.chk_accountmgr_furk) == str(chk_furk) or str(chk_furk) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("furk.username", your_furk_user)
                                        addon.setSetting("furk.password", your_furk_pass)
                                        addon.setSetting("furk.api.key", your_furk_api)
                except:
                        xbmc.log('%s: My Accounts Furk Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
