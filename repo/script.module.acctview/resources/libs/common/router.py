import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import os.path
import sys
from datetime import datetime
try:  # Python 3
    from urllib.parse import parse_qsl
except ImportError:  # Python 2
    from urlparse import parse_qsl
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common import var
from resources.libs.gui import menu

accountmgr = xbmcaddon.Addon("script.module.accountmgr")
addon = xbmcaddon.Addon
addonObject = addon('script.module.acctview')
addonInfo = addonObject.getAddonInfo
getLangString = xbmcaddon.Addon().getLocalizedString
condVisibility = xbmc.getCondVisibility
execute = xbmc.executebuiltin
monitor = xbmc.Monitor()
joinPath = os.path.join
dialog = xbmcgui.Dialog()
date_time = datetime.now()
date = date_time.strftime('Date: %Y-%m-%d  Time: %H:%M')

amgr_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'accountmgr.png')
rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')
trakt_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'trakt.png')
torbox_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'torbox.png')
easyd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'easydebrid.png')
offcloud_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'offcloud.png')
easy_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'easynews.png')
file_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'filepursuit.png')
                      
class Router:
    def __init__(self):
        self.route = None
        self.params = {}

    def _log_params(self, paramstring):
        _url = sys.argv[0]

        self.params = dict(parse_qsl(paramstring))

        logstring = '{0}: '.format(_url)
        for param in self.params:
            logstring += '[ {0}: {1} ] '.format(param, self.params[param])

        logging.log(logstring, level=xbmc.LOGDEBUG)

        return self.params

    def dispatch(self, handle, paramstring):
        self._log_params(paramstring)

        mode = self.params['mode'] if 'mode' in self.params else None
        url = self.params['url'] if 'url' in self.params else None
        name = self.params['name'] if 'name' in self.params else None
        action = self.params['action'] if 'action' in self.params else None
        
        from resources.libs import traktit, debridit_rd, debridit_pm, debridit_ad, tbit, edit, offit, easyit, fileit, extit, metait_all, databit, jsonit
        
        # MAIN MENU
        if mode is None:
            self._finish(handle)
                 
        elif mode == 'trakt':  # Trakt Account Viewer
            menu.trakt_menu()
            self._finish(handle)
            
        elif mode == 'realdebrid':  # Real-Debrid Account Viewer
            menu.debrid_menu()
            self._finish(handle)

        elif mode == 'premiumize':  # Premiumize Account Viewer
            menu.premiumize_menu()
            self._finish(handle)

        elif mode == 'alldebrid':  # All-Debird Account Viewer
            menu.alldebrid_menu()
            self._finish(handle)

        elif mode == 'torbox':  # TorBox Account Viewer
            menu.torbox_menu()
            self._finish(handle)

        elif mode == 'easydebrid':  # Easy Debrid Account Viewer
            menu.easydebrid_menu()
            self._finish(handle)
            
        elif mode == 'offcloud':  # OffCloud Account Viewer
            menu.offcloud_menu()
            self._finish(handle)

        elif mode == 'easynews':  # Easynews Account Viewer
            menu.easynews_menu()
            self._finish(handle)
            
        elif mode == 'filepursuit':  # Filepursuit Account Viewer
            menu.filepursuit_menu()
            self._finish(handle)

        elif mode == 'extproviders':  # External Providers Account Viewer
            menu.ext_menu()
            self._finish(handle)

        elif mode == 'metadata':  # Metadata Account Viewer
            menu.meta_accounts_menu()
            self._finish(handle)

        elif mode == 'allaccts':  # All Account Viewer
            menu.all_accounts_menu()
            self._finish(handle)

        # OPEN ADDON SETTINGS
        elif mode == 'opensettings_tk':  # Trakt
            from resources.libs import traktit
            traktit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')
            
        elif mode == 'opensettings_rd':  # Real Debrid
            from resources.libs import debridit_rd
            debridit_rd.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_pm':  # Premiumize
            from resources.libs import debridit_pm
            debridit_pm.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_ad':  # All-Debrid
            from resources.libs import debridit_ad
            debridit_ad.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_all':  # Debrid All
            from resources.libs import debridit_all
            debridit_all.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_tb':  # TorBox
            from resources.libs import tbit
            tbit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_ed':  # Easy Debrid
            from resources.libs import edit
            edit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_oc':  # OffCloud
            from resources.libs import offit
            offit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_en':  # Easynews
            from resources.libs import easyit
            easyit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_fp':  # Filepursuit
            from resources.libs import fileit
            fileit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_md':  # Metadata
            from resources.libs import metait_all
            metait_all.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_ext':  # External Providers
            from resources.libs import extit
            extit.open_settings(name)
            xbmc.executebuiltin('Container.Refresh()')

        elif mode == 'opensettings_fenlt':  # Open Fen Light settings
            var.open_settings_fenlt()
            xbmc.executebuiltin('Container.Refresh()')
            
        # TRAKT MANAGER
        elif mode == 'savetrakt':  # Save Trakt Data
            traktit.trakt_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_trakt()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_trakt()
        elif mode == 'savetrakt_acctmgr':  # Save Trakt Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_tk) != '':
                    traktit.trakt_it('update', name)
                    var.backup_synclist()
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_trakt()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_trakt()
                    accountmgr.setSetting('tk_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'Trakt Backup Complete!', trakt_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Backup!', trakt_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoretrakt':  # Recover All Saved Trakt Data
            try:
                if xbmcvfs.exists(var.trakt_backup): # Skip restore if no trakt folder present in backup folder
                    path = os.listdir(var.trakt_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        var.restore_synclist()
                        traktit.trakt_it_restore('restore', name)
                        accountmgr.setSetting("trakt.synclist", 'true')
                        accountmgr.setSetting("sync.tk.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) or xbmcvfs.exists(var.chk_dradis) or xbmcvfs.exists(var.chk_genocide):
                            fenlt = 'Fen Light'
                            dradis = 'Dradis'
                            genocide = 'Chains Genocide'
                            with open(var.synclist_file) as f:
                                if fenlt in f.read():
                                    databit.restore_fenlt_trakt()
                                    xbmc.executebuiltin('Dialog.Close(all,true)')
                                    xbmc.sleep(1000)
                                    var.remake_settings()
                                else:
                                    pass
                                if dradis in f.read():
                                    accountmgr.setSetting("dradis_traktsync", 'true')
                                else:
                                    pass
                                if genocide in f.read():
                                    accountmgr.setSetting("genocide_traktsync", 'true')
                                else:
                                    pass    
                        else:
                            pass                       
                        accountmgr.setSetting("api.service", "true") #Enable API Check Service
                        xbmcgui.Dialog().notification('Account Manager', 'Trakt Data Restored!', trakt_icon, 3000)
                        xbmc.sleep(3000)
                        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                        os._exit(1)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Restore!', trakt_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Restore!', trakt_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addontrakt':  # Clear All Addon Trakt Data
            #Revoke Account Manager/Custom API keys for all add-ons
            if var.chk_accountmgr_tk != '':
                pass
            else:
                accountmgr.setSetting("api.service", "false") #Disable API Check Service
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_trakt()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_trakt()
                #var.remake_settings() #Refresh settings database
            if xbmcvfs.exists(var.chk_seren) and (var.setting('traktuserkey.enabled') == 'true' or var.setting('devuserkey.enabled') == 'true'): #Check if add-on is installed
                try:
                    with open(var.path_seren,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.seren_client).replace(var.secret_am,var.seren_secret)

                    with open(var.path_seren,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Seren Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_fen):
                try:
                    with open(var.path_fen,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.fen_client).replace(var.secret_am,var.fen_secret)

                    with open(var.path_fen,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Fen Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_coal):
                try:
                    with open(var.path_coal,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.coal_client).replace(var.secret_am,var.coal_secret)

                    with open(var.path_coal,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Coalition Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_pov):
                try:
                    addon = xbmcaddon.Addon("plugin.video.pov")
                    addon.setSetting("trakt.client_id", var.pov_client)
                    addon.setSetting("trakt.client_secret", var.pov_secret)
                except:
                    xbmc.log('%s: Traktit.py Revoke API POV Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_dradis):
                try:
                    addon = xbmcaddon.Addon("plugin.video.dradis")
                    addon.setSetting("trakt.client_id", var.client_am)
                    addon.setSetting("trakt.client_secret", var.secret_am)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Dradis Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_shadow):
                try:
                    with open(var.path_shadow,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.shadow_client).replace(var.secret_am,var.shadow_secret)

                    with open(var.path_shadow,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Shadow Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_ghost):
                try:
                    with open(var.path_ghost,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.ghost_client).replace(var.secret_am,var.ghost_secret)

                    with open(var.path_ghost,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Ghost Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_base):
                try:
                    with open(var.path_base,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.base_client).replace(var.secret_am,var.base_secret)

                    with open(var.path_base,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Base Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_chains):
                try:
                    with open(var.path_chains,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.chains_client).replace(var.secret_am,var.chains_secret)

                    with open(var.path_chains,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Chain Reaction Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_asgard):
                try:
                    with open(var.path_asgard,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.asgard_client).replace(var.secret_am,var.asgard_secret)

                    with open(var.path_asgard,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Asgard Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_patriot):
                try:
                    with open(var.path_patriot,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.patriot_client).replace(var.secret_am,var.patriot_secret)

                    with open(var.path_patriot,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Patriot Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_blackl):
                try:
                    with open(var.path_blackl,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.blackl_client).replace(var.secret_am,var.blackl_secret)

                    with open(var.path_blackl,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Black Lightning Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_aliunde):
                try:
                    with open(var.path_aliunde,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.aliunde_client).replace(var.secret_am,var.aliunde_secret)

                    with open(var.path_aliunde,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Aliunde Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_night):
                try:
                    with open(var.path_night,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.night_client).replace(var.secret_am,var.night_secret)

                    with open(var.path_night,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Nightwing Lite Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_genocide):
                try:
                    with open(var.path_genocide,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.genocide_client).replace(var.secret_am,var.genocide_secret)

                    with open(var.path_genocide,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Chains Genocide Failed!' % var.amgr, xbmc.LOGINFO)
                    pass
                
            if xbmcvfs.exists(var.chk_crew):
                try:
                    with open(var.path_crew,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.crew_client).replace(var.secret_am,var.crew_secret)

                    with open(var.path_crew,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API The Crew Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_scrubs):
                try:
                    with open(var.path_scrubs,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.scrubs_client).replace(var.secret_am,var.scrubs_secret)

                    with open(var.path_scrubs,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Scrubs V2 Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_tmdbh):
                try:
                    with open(var.path_tmdbh,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.tmdbh_client).replace(var.secret_am,var.tmdbh_secret)

                    with open(var.path_tmdbh,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API TMDbH Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_trakt):
                try:
                    with open(var.path_trakt,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.trakt_client).replace(var.secret_am,var.trakt_secret)

                    with open(var.path_trakt,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API Trakt Addon Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_allaccounts):
                try:
                    with open(var.path_allaccounts,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.allacts_client).replace(var.secret_am,var.allacts_secret)

                    with open(var.path_allaccounts,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API All Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                    pass

            if xbmcvfs.exists(var.chk_myaccounts):
                try:
                    with open(var.path_myaccounts,'r') as f:
                        data = f.read()

                    client = data.replace(var.client_am,var.myacts_client).replace(var.secret_am,var.myacts_secret)

                    with open(var.path_myaccounts,'w') as f:
                        f.write(client)
                except:
                    xbmc.log('%s: Traktit.py Revoke API My Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                    pass
                
            traktit.trakt_it_revoke('clearaddon', name)
            var.delete_synclist()
            accountmgr.setSetting("trakt.synclist", 'false')
            accountmgr.setSetting("sync.tk.service", "false")
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', trakt_icon, 3000)
            xbmc.sleep(3000)
            xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
            os._exit(1)
        elif mode == 'cleartrakt':  # Clear All Saved Trakt Data
            try:
                if xbmcvfs.exists(var.trakt_backup): # Skip clearing data if no Trakt folder present in backup folder
                    path = os.listdir(var.trakt_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('tk_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.trakt_backup)
                        for file in data:
                                files = os.path.join(var.trakt_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Trakt Data Cleared!', trakt_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Clear!', trakt_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Trakt Data to Clear!', trakt_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'opentraktsettings':  # Authorize Trakt
            traktit.open_settings_trakt(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatetrakt':  # Update Saved Trakt Data
            traktit.auto_update('all')
            
        # DEBRID MANAGER RD
        elif mode == 'savedebrid_rd':  # Save Debrid Data
            debridit_rd.debrid_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_rd()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_rd()
            jsonit.realizer_bk()
        elif mode == 'savedebrid_acctmgr_rd':  # Save Debrid Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_tk_rd) != '':
                    debridit_rd.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_rd()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_rd()
                    jsonit.realizer_bk()
                    accountmgr.setSetting('rd_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'RealDebrid Backup Complete!', rd_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No RealDebrid Data to Backup!', rd_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoredebrid_rd':  # Recover All Saved Debrid Data
            try:
                if xbmcvfs.exists(var.rd_backup): # Skip restore if no debrid folder present in backup folder
                    path = os.listdir(var.rd_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        debridit_rd.debrid_it('restore', name)
                        accountmgr.setSetting("sync.rd.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_rd()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            #databit.restore_affen_rd()
                            #var.remake_settings() #Refresh settings database
                        jsonit.realizer_rst()
                        xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Restored!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Restore!', rd_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Restore!', rd_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore RD Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addondebrid_rd':  # Clear All Addon Debrid Data
            debridit_rd.debrid_it('wipeaddon', name)
            accountmgr.setSetting("sync.rd.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_rd()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_rd()
                #var.remake_settings() #Refresh settings database
            jsonit.realizer_rvk()
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', rd_icon, 3000)           
        elif mode == 'cleardebrid_rd':  # Clear All Saved Debrid Data
            try:
                if xbmcvfs.exists(var.rd_backup): # Skip clearing data if no debrid folder present in backup folder
                    path = os.listdir(var.rd_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('rd_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.rd_backup)
                        for file in data:
                                files = os.path.join(var.rd_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Cleared!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear RD Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'opendebridsettings_rd':  # Authorize Debrid
            debridit_rd.open_settings_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid_rd':  # Update Saved Debrid Data
            debridit_rd.auto_update('all')

        # DEBRID MANAGER PM
        elif mode == 'savedebrid_pm':  # Save Debrid Data
            debridit_pm.debrid_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_pm()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_pm()
        elif mode == 'savedebrid_acctmgr_pm':  # Save Debrid Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_tk_pm) != '':
                    debridit_pm.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_pm()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_pm()
                    accountmgr.setSetting('pm_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'Premiumize Backup Complete!', pm_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Backup!', pm_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoredebrid_pm':  # Recover All Saved Debrid Data
            try:
                if xbmcvfs.exists(var.pm_backup): # Skip restore if no debrid folder present in backup folder
                    path = os.listdir(var.pm_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        debridit_pm.debrid_it('restore', name)
                        accountmgr.setSetting("sync.pm.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_pm()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            #databit.restore_affen_pm()
                            #var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Restored!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Restore!', pm_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Restore!', pm_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore PM Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addondebrid_pm':  # Clear All Addon Debrid Data
            debridit_pm.debrid_it('wipeaddon', name)
            accountmgr.setSetting("sync.pm.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_pm()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_pm()
                #var.remake_settings() #Refresh settings database
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', pm_icon, 3000)
        elif mode == 'cleardebrid_pm':  # Clear All Saved Debrid Data
            try:
                if xbmcvfs.exists(var.pm_backup): # Skip clearing data if no debrid folder present in backup folder
                    path = os.listdir(var.pm_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('pm_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.pm_backup)
                        for file in data:
                                files = os.path.join(var.pm_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Cleared!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', pm_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', pm_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear PM Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'opendebridsettings_pm':  # Authorize Debrid
            debridit_pm.open_settings_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid_pm':  # Update Saved Debrid Data
            debridit_pm.auto_update('all')

        # DEBRID MANAGER AD
        elif mode == 'savedebrid_ad':  # Save Debrid Data
            debridit_ad.debrid_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_ad()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_ad()
        elif mode == 'savedebrid_acctmgr_ad':  # Save Debrid Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_tk_ad) != '':
                    debridit_ad.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_ad()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_ad()
                    accountmgr.setSetting('ad_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'AllDebrid Backup Complete!', ad_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No AllDebrid Data to Backup!', ad_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoredebrid_ad':  # Recover All Saved Debrid Data
            try:
                if xbmcvfs.exists(var.ad_backup): # Skip restore if no debrid folder present in backup folder
                    path = os.listdir(var.ad_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        debridit_ad.debrid_it('restore', name)
                        accountmgr.setSetting("sync.ad.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_ad()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            #databit.restore_affen_ad()
                            #var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Restored!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Restore!', ad_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Restore!', ad_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore AD Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addondebrid_ad':  # Clear All Addon Debrid Data
            debridit_ad.debrid_it('wipeaddon', name)
            accountmgr.setSetting("sync.ad.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_ad()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_ad()
                #var.remake_settings() #Refresh settings database
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', ad_icon, 3000)
        elif mode == 'cleardebrid_ad':  # Clear All Saved Debrid Data
            try:
                if xbmcvfs.exists(var.ad_backup): # Skip clearing data if no debrid folder present in backup folder
                    path = os.listdir(var.ad_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('ad_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.ad_backup)
                        for file in data:
                                files = os.path.join(var.ad_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Cleared!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', ad_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', ad_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear AD Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'opendebridsettings_ad':  # Authorize Debrid
            debridit_ad.open_settings_debrid(name)
            xbmc.executebuiltin('Container.Refresh()')
        elif mode == 'updatedebrid_ad':  # Update Saved Debrid Data
            debridit_ad.auto_update('all')

        # TORBOX MANAGER
        elif mode == 'savetorbox':  # Save Data
            tbit.tb_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_tb()
        elif mode == 'save_tb_acctmgr':  # Save Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_tb) != '':
                    tbit.tb_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_tb()
                    accountmgr.setSetting('tb_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'TorBox Backup Complete!', torbox_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No TorBox Data to Backup!', torbox_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoretb':  # Recover All Saved Data
            try:
                if xbmcvfs.exists(var.tb_backup): # Skip restore if no TorBox folder present in backup folder
                    path = os.listdir(var.tb_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        tbit.tb_it('restore', name)
                        accountmgr.setSetting("sync.torbox.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_tb()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'TorBox Data Restored!', torbox_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No TorBox Data to Restore!', torbox_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No TorBox Data to Restore!', torbox_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore TorBox Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addontb':  # Clear All Addon OffCloud Data
            tbit.tb_it('wipeaddon', name)
            accountmgr.setSetting("sync.torbox.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_tb()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', torbox_icon, 3000)
        elif mode == 'cleartb':  # Clear All Saved Data
            try:
                if xbmcvfs.exists(var.tb_backup): # Skip clearing data if no nondebrid folder present in backup folder
                    path = os.listdir(var.tb_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('tb_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.tb_backup)
                        for file in data:
                                files = os.path.join(var.tb_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'TorBox Data Cleared!', torbox_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No TorBox Data to Clear!', torbox_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No TorBox Data to Clear!', torbox_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear TorBox Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updatetb':  # Update Saved Data
            tbit.auto_update('all')

        # EASY DEBRID MANAGER
        elif mode == 'saveeasydebrid':  # Save Data
            edit.ed_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_ed()
        elif mode == 'save_ed_acctmgr':  # Save Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_ed) != '':
                    edit.ed_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_ed()
                    accountmgr.setSetting('ed_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'Easy Debrid Backup Complete!', easyd_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Easy Debrid  Data to Backup!', easyd_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoreed':  # Recover All Saved Data
            try:
                if xbmcvfs.exists(var.ed_backup): # Skip restore if no Easy Debrid folder present in backup folder
                    path = os.listdir(var.ed_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        edit.ed_it('restore', name)
                        accountmgr.setSetting("sync.easyd.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_ed()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'Easy Debrid  Data Restored!', easyd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Easy Debrid  Data to Restore!', easyd_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Easy Debrid  Data to Restore!', easyd_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addoned':  # Clear All Addon OffCloud Data
            edit.ed_it('wipeaddon', name)
            accountmgr.setSetting("sync.eastd.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_ed()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', easyd_icon, 3000)
        elif mode == 'cleared':  # Clear All Saved Data
            try:
                if xbmcvfs.exists(var.ed_backup): # Skip clearing data if no nondebrid folder present in backup folder
                    path = os.listdir(var.ed_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('ed_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.ed_backup)
                        for file in data:
                                files = os.path.join(var.ed_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Easy Debrid  Data Cleared!', easyd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Easy Debrid Data to Clear!', easyd_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Easy Debrid Data to Clear!', easyd_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updateed':  # Update Saved Data
            edit.auto_update('all')
            
        # OFFCLOUD MANAGER
        elif mode == 'saveoffcloud':  # Save Data
            offit.offc_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_oc()
        elif mode == 'save_offc_acctmgr':  # Save Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_offc) != '':
                    offit.offc_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_oc()
                    accountmgr.setSetting('oc_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'OffCloud Backup Complete!', offcloud_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No OffCloud Data to Backup!', offcloud_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoreoffc':  # Recover All Saved Data
            try:
                if xbmcvfs.exists(var.offc_backup): # Skip restore if no offcloud folder present in backup folder
                    path = os.listdir(var.offc_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        offit.offc_it('restore', name)
                        accountmgr.setSetting("sync.offc.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_oc()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'OffCloud Data Restored!', offcloud_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No OffCloud Data to Restore!', offcloud_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No OffCloud Data to Restore!', offcloud_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore OffCloud Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addonoffc':  # Clear All Addon OffCloud Data
            offit.offc_it('wipeaddon', name)
            accountmgr.setSetting("sync.offc.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_oc()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', offcloud_icon, 3000)
        elif mode == 'clearoffc':  # Clear All Saved Data
            try:
                if xbmcvfs.exists(var.offc_backup): # Skip clearing data if no nondebrid folder present in backup folder
                    path = os.listdir(var.offc_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('oc_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.offc_backup)
                        for file in data:
                                files = os.path.join(var.offc_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'OffCloud Data Cleared!', offcloud_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No OffCloud Data to Clear!', offcloud_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No OffCloud Data to Clear!', offcloud_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear OffCloud Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updateoffc':  # Update Saved Data
            offit.auto_update('all')
            
        # EASYNEWS MANAGER
        elif mode == 'saveeasy':  # Save Data
            easyit.easy_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_easy()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_easy()
        elif mode == 'save_easy_acctmgr':  # Save Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_easy) != '':
                    easyit.easy_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_easy()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_easy()
                    accountmgr.setSetting('en_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'Easynews Backup Complete!', easy_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Easynews Data to Backup!', easy_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoreeasy':  # Recover All Saved Data
            try:
                if xbmcvfs.exists(var.easy_backup): # Skip restore if no easynews folder present in backup folder
                    path = os.listdir(var.easy_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        easyit.easy_it('restore', name)
                        accountmgr.setSetting("sync.easy.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_easy()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            #databit.restore_affen_easy()
                            #var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'Easynews Data Restored!', easy_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Easynews Data to Restore!', easy_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Easynews  Data to Restore!', easy_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addoneasy':  # Clear All Addon Easynews Data
            easyit.easy_it('wipeaddon', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_easy()
                accountmgr.setSetting("sync.easy.service", "false")
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_easy()
                #var.remake_settings() #Refresh settings database
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', easy_icon, 3000)
        elif mode == 'cleareasy':  # Clear All Saved Data
            try:
                if xbmcvfs.exists(var.easy_backup): # Skip clearing data if no easynews folder present in backup folder
                    path = os.listdir(var.easy_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('en_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.easy_backup)
                        for file in data:
                                files = os.path.join(var.easy_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Easynews Data Cleared!', easy_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Easynews Data to Clear!', easy_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Easynews Data to Clear!', easy_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear Easynews Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updateeasy':  # Update Saved Data
            easyit.auto_update('all')

        # FILEPURSUIT MANAGER
        elif mode == 'savefile':  # Save Data
            fileit.filep_it('update', name)
        elif mode == 'save_file_acctmgr':  # Save Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_file) != '':
                    fileit.filep_it('update', name)
                    accountmgr.setSetting('fp_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'Filepursuit Backup Complete!', file_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Filepursuit Data to Backup!', file_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restorefile':  # Recover All Saved Data
            try:
                if xbmcvfs.exists(var.file_backup): # Skip restore if no fileloud folder present in backup folder
                    path = os.listdir(var.file_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        fileit.filep_it('restore', name)
                        accountmgr.setSetting("sync.filep.service", "true")
                        xbmcgui.Dialog().notification('Account Manager', 'Filepursuit Data Restored!', file_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Filepursuit Data to Restore!', file_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Filepursuit Data to Restore!', file_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore Filepursuit Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addonfile':  # Clear All Addon Filepursuit Data
            fileit.filep_it('wipeaddon', name)
            accountmgr.setSetting("sync.filep.service", "false")
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', file_icon, 3000)
        elif mode == 'clearfile':  # Clear All Saved Data
            try:
                if xbmcvfs.exists(var.file_backup): # Skip clearing data if no nondebrid folder present in backup folder
                    path = os.listdir(var.file_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('fp_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.file_backup)
                        for file in data:
                                files = os.path.join(var.file_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Filepursuit Data Cleared!', file_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Filepursuit Data to Clear!', file_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Filepursuit Data to Clear!', file_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear Filepursuit Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updatefile':  # Update Saved Data
            fileit.auto_update('all')

        #EXTERNAL PROVIDERS MANAGER
        elif mode == 'saveext':  # Save Data
            extit.ext_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_ext()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_ext()
        elif mode == 'save_ext_acctmgr':  # Save Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_ext) != '':
                    extit.ext_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_ext()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_ext()
                    accountmgr.setSetting('ext_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'External Providers Backup Complete!', amgr_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No External Providers Data to Backup!', amgr_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoreext':  # Recover All Saved Data
            try:
                if xbmcvfs.exists(var.ext_backup): # Skip restore if no extprovider folder present in backup folder
                    path = os.listdir(var.ext_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        extit.ext_it('restore', name)
                        accountmgr.setSetting("sync.ext.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_ext()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            #databit.restore_affen_ext()
                            #var.remake_settings() #Refresh settings database
                        accountmgr.setSetting("ext.provider", 'CocoScrapers')
                        xbmcgui.Dialog().notification('Account Manager', 'External Providers Data Restored!', amgr_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No External Providers Data to Restore!', amgr_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No External Providers  Data to Restore!', amgr_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.lLose(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore External Providers Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addonext':  # Clear All Addon External Providers Data
            extit.ext_it('wipeaddon', name)
            accountmgr.setSetting("sync.ext.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_ext()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_ext()
                #var.remake_settings() #Refresh settings database
            accountmgr.setSetting("ext.provider", '')
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', amgr_icon, 3000)
        elif mode == 'clearext':  # Clear All Saved Data
            try:
                if xbmcvfs.exists(var.ext_backup): # Skip clearing data if no extprovider folder present in backup folder
                    path = os.listdir(var.ext_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('ext_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.ext_backup)
                        for file in data:
                                files = os.path.join(var.ext_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'External Providers Data Cleared!', amgr_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No External Providers Data to Clear!', amgr_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No External Providers Data to Clear!', amgr_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear External Providers Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updateext':  # Update Saved Data
            extit.auto_update('all')
            
        #META DATA MANAGER
        elif mode == 'savemeta':  # Save Meta Data
            metait_all.debrid_it('update', name)
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.backup_fenlt_meta()
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.backup_affen_meta()
        elif mode == 'savemeta_acctmgr':  # Save Meta Data via Account Manager settings menu
            if not var.backup_path:
                xbmcgui.Dialog().ok('Account Manager', 'No backup path set! Please set a backup path in Account Manager settings.')
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
            else:
                if str(var.chk_accountmgr_fanart) != '' or str(var.chk_accountmgr_omdb) != '' or str(var.chk_accountmgr_mdb) != '' or str(var.chk_accountmgr_imdb) != '' or str(var.chk_accountmgr_tmdb) != '' or str(var.chk_accountmgr_tmdb_user) != '' or str(var.chk_accountmgr_tvdb) != '':
                    metait_all.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_meta()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_meta()
                    accountmgr.setSetting('md_backup_date', date)
                    xbmcgui.Dialog().notification('Account Manager', 'Metadata Backup Complete!', amgr_icon, 3000)
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Backup!', amgr_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
        elif mode == 'restoremeta':  # Recover All Saved Meta Data
            try:
                if xbmcvfs.exists(var.meta_backup): # Skip restore if no meta folder present in backup folder
                    path = os.listdir(var.meta_backup)
                    if len(path) != 0: # Skip restore if no saved data in backup folder
                        metait_all.debrid_it('restore', name)
                        accountmgr.setSetting("sync.meta.service", "true")
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                            databit.restore_fenlt_meta()
                            xbmc.executebuiltin('Dialog.Close(all,true)')
                            xbmc.sleep(1000)
                            var.remake_settings() #Refresh settings database
                        #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            #databit.restore_affen_meta()
                            #var.remake_settings() #Refresh settings database
                        xbmcgui.Dialog().notification('Account Manager', 'Metadata Restored!', amgr_icon, 3000)
                        xbmc.sleep(3000)
                        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                        os._exit(1)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Restore!', amgr_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Restore!', amgr_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Restore Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'addonmeta':  # Clear All Addon Meta Data
            metait_all.debrid_it('wipeaddon', name)
            accountmgr.setSetting("sync.meta.service", "false")
            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                databit.revoke_fenlt_meta()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                #databit.revoke_affen_meta()
                #var.remake_settings() #Refresh settings database
            xbmc.executebuiltin("Skin.Reset(mdblist_api_key)")
            xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', amgr_icon, 3000)
            xbmc.sleep(3000)
            xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
            os._exit(1)
        elif mode == 'clearmeta':  # Clear All Saved Meta Data
            try:
                if xbmcvfs.exists(var.meta_backup): # Skip clearing data if no meta folder present in backup folder
                    path = os.listdir(var.meta_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        accountmgr.setSetting('md_backup_date', 'Date: 0000-00-00   Time: 00:00')
                        data = os.listdir(var.meta_backup)
                        for file in data:
                                files = os.path.join(var.meta_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        xbmcgui.Dialog().notification('Account Manager', 'Metadata Cleared!', amgr_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Clear!', amgr_icon, 3000)
                        xbmc.sleep(3000)
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                else:
                    xbmcgui.Dialog().notification('Account Manager', 'No Metadata to Clear!', amgr_icon, 3000)
                    xbmc.sleep(3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
            except:
                xbmc.log('%s: Router.py Clear Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif mode == 'updatemeta':  # Update Saved Meta Data
            metait_all.auto_update('all')
            
        #REVOKE ALL DEBRID ACCOUNTS
        elif mode == 'revokeall':  # Clear Addon Data for all Debrid services
            if str(var.chk_accountmgr_tk_rd) == '' and str(var.chk_accountmgr_tk_pm) == '' and str(var.chk_accountmgr_tk_ad) == '': # If no accounts are authorized notify user
                xbmcgui.Dialog().notification('Account Manager', 'No Active Debrid Accounts!', amgr_icon, 3000) # If Accounts authorized notify user
            else:
                if not str(var.chk_accountmgr_tk_rd) == '':
                    debridit_rd.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.rd.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_rd()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_rd()
                    jsonit.realizer_rvk()
                    
                if not str(var.chk_accountmgr_tk_pm) == '':
                    debridit_pm.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.pm.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_pm()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_pm()
                    
                if not str(var.chk_accountmgr_tk_ad) == '':
                    debridit_ad.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.ad.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_ad()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_ad()
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database     
                xbmcgui.Dialog().notification('Account Manager', 'All Add-ons Revoked!', amgr_icon, 3000)
                
        #BACKUP ALL DEBRID ACCOUNTS
        elif mode == 'backupall':  # Save Debrid Data for all Debrid services
            if str(var.chk_accountmgr_tk_rd) == '' and str(var.chk_accountmgr_tk_pm) == '' and str(var.chk_accountmgr_tk_ad) != '': # If no accounts are authorized notify user
                xbmcgui.Dialog().notification('Account Manager', 'No Active Debrid Accounts!', amgr_icon, 3000)
            else:
                if not str(var.chk_accountmgr_tk_rd) == '': # Skip backup if Debrid account not authorized
                    #Real-Debrid
                    debridit_rd.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_rd()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_rd()
                    jsonit.realizer_bk()
                    accountmgr.setSetting('rd_backup_date', date)
                    
                if not str(var.chk_accountmgr_tk_pm) == '':
                    #Premiumize
                    debridit_pm.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_pm()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_pm()
                    accountmgr.setSetting('pm_backup_date', date)

                if not str(var.chk_accountmgr_tk_ad) == '':
                    #All-Debrid
                    debridit_ad.debrid_it('update', name)
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.backup_fenlt_ad()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.backup_affen_ad()
                    accountmgr.setSetting('ad_backup_date', date)
                        
                xbmcgui.Dialog().notification('Account Manager', 'Backup Complete!', amgr_icon, 3000)
            
        #RESTORE ALL DEBRID ACCOUNTS
        elif mode == 'restoreall':  # Recover All Saved Debrid Data for all Accounts
            if xbmcvfs.exists(var.rd_backup) or xbmcvfs.exists(var.pm_backup) or xbmcvfs.exists(var.ad_backup): # Skip restore if no debrid folder present in backup folder
                try:
                    if xbmcvfs.exists(var.rd_backup): # Skip restore if no backup folder exists or it's empty
                        path_rd = os.listdir(var.rd_backup)
                        if len(path_rd) != 0: # Skip if backup directory is empty
                            debridit_rd.debrid_it('restore', name)
                            accountmgr.setSetting("sync.rd.service", "true")
                            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                                databit.restore_fenlt_rd()
                            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                                #databit.restore_affen_rd()
                            jsonit.realizer_rst()
                            xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Restored!', rd_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data Found!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data Found!', rd_icon, 3000)
                    if xbmcvfs.exists(var.pm_backup): # Skip restore if no backup folder exists or it's empty
                        path_pm = os.listdir(var.pm_backup)
                        if len(path_pm) != 0: # Skip if backup directory is empty
                            debridit_pm.debrid_it('restore', name)
                            accountmgr.setSetting("sync.pm.service", "true")
                            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                                databit.restore_fenlt_pm()
                            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                                #databit.restore_affen_pm()
                            xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Restored!', pm_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data Found!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data Found!', pm_icon, 3000)
                    if xbmcvfs.exists(var.ad_backup): # Skip restore if no backup folder exists or it's empty
                        path_ad = os.listdir(var.ad_backup)
                        if len(path_ad) != 0: # Skip if backup directory is empty
                            debridit_ad.debrid_it('restore', name)
                            accountmgr.setSetting("sync.ad.service", "true")
                            if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                                databit.restore_fenlt_ad()
                            #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                                #databit.restore_affen_ad()
                            xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Restored!', ad_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data Found!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data Found!', ad_icon, 3000)
                    xbmc.executebuiltin('Dialog.Close(all,true)')
                    xbmc.sleep(1000)
                    var.remake_settings() #Refresh settings database
                except:
                    xbmc.log('%s: Router.py Restore All Debrid Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'Restore Failed! No Saved Data Found!', amgr_icon, 3000)
                xbmc.sleep(3000)
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                 
        #CLEAR ALL SAVED DATA FOR DEBRID ACCOUNTS
        elif mode == 'clearall':  # Clear All Saved Debrid Data
            if xbmcvfs.exists(var.rd_backup) or xbmcvfs.exists(var.pm_backup) or xbmcvfs.exists(var.ad_backup): # Skip clearing data if no debrid folder present in backup folder
                try:
                    #Clear Real-Debrid Saved Data
                    if xbmcvfs.exists(var.rd_backup): # Skip clearing data if no folder present in backup folder
                        path = os.listdir(var.rd_backup)
                        if len(path) != 0: # Skip clearing data if no saved data in backup folder
                            data = os.listdir(var.rd_backup)
                            for file in data:
                                    files = os.path.join(var.rd_backup, file)
                                    if os.path.isfile(files):
                                            os.remove(files) 
                            xbmcgui.Dialog().notification('Account Manager', 'Real-Debrid Data Cleared!', rd_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Real-Debrid Data to Clear!', rd_icon, 3000)
                    
                    #Clear Premiumize Saved Data
                    if xbmcvfs.exists(var.pm_backup): # Skip clearing data if no folder present in backup folder
                        path = os.listdir(var.pm_backup)
                        if len(path) != 0: # Skip clearing data if no saved data in backup folder
                            data = os.listdir(var.pm_backup)
                            for file in data:
                                    files = os.path.join(var.pm_backup, file)
                                    if os.path.isfile(files):
                                            os.remove(files)
                            xbmcgui.Dialog().notification('Account Manager', 'Premiumize Data Cleared!', pm_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', pm_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No Premiumize Data to Clear!', pm_icon, 3000)
                        
                    #Clear All-Debrid Saved Data
                    if xbmcvfs.exists(var.ad_backup): # Skip clearing data if no folder present in backup folder
                        path = os.listdir(var.ad_backup)
                        if len(path) != 0: # Skip clearing data if no saved data in backup folder
                            data = os.listdir(var.ad_backup)
                            for file in data:
                                    files = os.path.join(var.ad_backup, file)
                                    if os.path.isfile(files):
                                            os.remove(files)
                            xbmcgui.Dialog().notification('Account Manager', 'All-Debrid Data Cleared!', ad_icon, 3000)
                        else:
                            xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', ad_icon, 3000)
                    else:
                        xbmcgui.Dialog().notification('Account Manager', 'No All-Debrid Data to Clear!', ad_icon, 3000)
                except:
                    xbmc.log('%s: Router.py Clear All Debrid Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                    pass
            else:
                xbmcgui.Dialog().notification('Account Manager', 'No Data to Clear!', amgr_icon, 3000)
                xbmc.sleep(3000)
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.executebuiltin('Addon.OpenSettings(script.module.accountmgr)')
                 
        # REVOKE/WIPE/CLEAN ALL ADD-ONS
        elif mode == 'wipeclean':  # Revoke all Add-ons, Clear all saved data, and restore stock API Keys for all add-ons
            xbmcgui.Dialog().notification('Account Manager', 'Restoring default settings, please wait!', amgr_icon, 3000)
            try:
                #Revoke Trakt
                if not str(var.chk_accountmgr_tk) == '':
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_trakt()
                        xbmc.executebuiltin('Dialog.Close(all,true)')
                        xbmc.sleep(1000)
                        var.remake_settings()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_trakt()
                    #Revoke Account Manager/Custom API keys for all add-ons
                    if xbmcvfs.exists(var.chk_seren) and (var.setting('traktuserkey.enabled') == 'true' or var.setting('devuserkey.enabled') == 'true'): #Check if add-on is installed
                        try:
                            with open(var.path_seren,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.seren_client).replace(var.secret_am,var.seren_secret)

                            with open(var.path_seren,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Seren Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_fen):
                        try:
                            with open(var.path_fen,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.fen_client).replace(var.secret_am,var.fen_secret)

                            with open(var.path_fen,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Fen Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_fenlt):
                        try:
                            with open(var.path_fenlt,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.fenlt_client).replace(var.secret_am,var.fenlt_secret)

                            with open(var.path_fenlt,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_coal):
                        try:
                            with open(var.path_coal,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.coal_client).replace(var.secret_am,var.coal_secret)

                            with open(var.path_coal,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Coalition Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_pov):
                        try:
                            addon = xbmcaddon.Addon("plugin.video.pov")
                            addon.setSetting("trakt.client_id", var.pov_client)
                            addon.setSetting("trakt.client_secret", var.pov_secret)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API POV Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_dradis):
                        try:
                            addon.setSetting("trakt.client_id", var.dradis_client)
                            addon.setSetting("trakt.client_secret", var.dradis_secret)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Dradis Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_shadow):
                        try:
                            with open(var.path_shadow,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.shadow_client).replace(var.secret_am,var.shadow_secret)

                            with open(var.path_shadow,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Shadow Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_ghost):
                        try:
                            with open(var.path_ghost,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.ghost_client).replace(var.secret_am,var.ghost_secret)

                            with open(var.path_ghost,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Ghost Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_base):
                        try:
                            with open(var.path_base,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.base_client).replace(var.secret_am,var.base_secret)

                            with open(var.path_base,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Base Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_chains):
                        try:
                            with open(var.path_chains,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.chains_client).replace(var.secret_am,var.chains_secret)

                            with open(var.path_chains,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Chain Reaction Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_asgard):
                        try:
                            with open(var.path_asgard,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.asgard_client).replace(var.secret_am,var.asgard_secret)

                            with open(var.path_asgard,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Asgard Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_patriot):
                        try:
                            with open(var.path_patriot,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.patriot_client).replace(var.secret_am,var.patriot_secret)

                            with open(var.path_patriot,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Patriot Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_blackl):
                        try:
                            with open(var.path_blackl,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.blackl_client).replace(var.secret_am,var.blackl_secret)

                            with open(var.path_blackl,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Black Lightning Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_aliunde):
                        try:
                            with open(var.path_aliunde,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.aliunde_client).replace(var.secret_am,var.aliunde_secret)

                            with open(var.path_aliunde,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Aliunde Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_night):
                        try:
                            with open(var.path_night,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.night_client).replace(var.secret_am,var.night_secret)

                            with open(var.path_night,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Nightwing Lite Failed!' % var.amgr, xbmc.LOGINFO)
                            pass
                        
                    if xbmcvfs.exists(var.chk_crew):
                        try:
                            with open(var.path_crew,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.crew_client).replace(var.secret_am,var.crew_secret)

                            with open(var.path_crew,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API The Crew Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_scrubs):
                        try:
                            with open(var.path_scrubs,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.scrubs_client).replace(var.secret_am,var.scrubs_secret)

                            with open(var.path_scrubs,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Scrubs V2 Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_tmdbh):
                        try:
                            with open(var.path_tmdbh,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.tmdbh_client).replace(var.secret_am,var.tmdbh_secret)

                            with open(var.path_tmdbh,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API TMDbH Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_trakt):
                        try:
                            with open(var.path_trakt,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.trakt_client).replace(var.secret_am,var.trakt_secret)

                            with open(var.path_trakt,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API Trakt Addon Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_allaccounts):
                        try:
                            with open(var.path_allaccounts,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.allacts_client).replace(var.secret_am,var.allacts_secret)

                            with open(var.path_allaccounts,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API All Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                            pass

                    if xbmcvfs.exists(var.chk_myaccounts):
                        try:
                            with open(var.path_myaccounts,'r') as f:
                                data = f.read()

                            client = data.replace(var.client_am,var.myacts_client).replace(var.secret_am,var.myacts_secret)

                            with open(var.path_myaccounts,'w') as f:
                                f.write(client)
                        except:
                            xbmc.log('%s: Traktit.py Revoke API My Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                            pass
                        
                    traktit.trakt_it_revoke('wipeaddon', name)
                    accountmgr.setSetting("sync.tk.service", "false")
                    
                #Revoke Real-Debrid
                if not str(var.chk_accountmgr_tk_rd) == '':
                    debridit_rd.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.rd.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_rd()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_rd()
                    jsonit.realizer_rvk()
                
                #Revoke Premiumize
                if not str(var.chk_accountmgr_tk_pm) == '':
                    debridit_pm.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.pm.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_pm()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_pm()
                
                #Revoke All-Debrid
                if not str(var.chk_accountmgr_tk_ad) == '':
                    debridit_ad.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.ad.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_ad()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_ad()
                        
                #Revoke TorBox
                if not str(var.setting('torbox.token')) == '':
                    tbit.tb_it('wipeaddon', name)
                    accountmgr.setSetting("sync.torbox.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_tb()
                    accountmgr.setSetting("torbox.enabled", 'false')

                #Revoke Easy Debrid
                if not str(var.setting('easydebrid.token')) == '':
                    edit.ed_it('wipeaddon', name)
                    accountmgr.setSetting("sync.easyd.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_ed()
                    accountmgr.setSetting("easydebrid.enabled", 'false')
                    
                #Revoke OffCloud
                if not str(var.setting('offcloud.token')) == '':
                    offit.offc_it('wipeaddon', name)
                    accountmgr.setSetting("sync.offc.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_oc()
                    accountmgr.setSetting("offcloud.enabled", 'false')
                    
                #Revoke Easynews
                if not str(var.setting('easynews.password')) == '':
                    easyit.easy_it('wipeaddon', name)
                    accountmgr.setSetting("sync.easy.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_easy()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_easy()
                    accountmgr.setSetting("easynews.enabled", 'false')

                #Revoke Filepursuit
                if not str(var.setting('filepursuit.api.key')) == '':
                    fileit.filep_it('wipeaddon', name)
                    accountmgr.setSetting("sync.filep.service", "false")
                    accountmgr.setSetting("filepursuit.enabled", 'false')

                #Revoke External Providers
                if not str(var.setting('ext.provider')) == '':
                    extit.ext_it('wipeaddon', name)
                    accountmgr.setSetting("sync.ext.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_ext()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_ext()
                    accountmgr.setSetting("ext.provider", '')

                #Revoke Metadata
                if str(var.setting('fanart.tv.api.key')) != '' or str(var.setting('omdb.api.key')) != '' or str(var.setting('mdb.api.key')) != '' or str(var.setting('imdb.user')) != '' or str(var.setting('tvdb.api.key')) != '' or str(var.setting('tmdb.api.key')) != '' or str(var.setting('tmdb.username')) != '' or str(var.setting('tmdb.password')) != '' or str(var.setting('tmdb.session_id')) != '':
                    metait_all.debrid_it('wipeaddon', name)
                    accountmgr.setSetting("sync.meta.service", "false")
                    if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        databit.revoke_fenlt_meta()
                    #if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                        #databit.revoke_affen_meta()
                    xbmc.executebuiltin("Skin.Reset(mdblist_api_key)")
                    accountmgr.setSetting("meta.enabled", 'false')
                    
                
                #Clear Trakt Saved Data
                if xbmcvfs.exists(var.trakt_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.trakt_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.trakt_backup)
                        for file in data:
                                files = os.path.join(var.trakt_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                
                #Clear Real-Debrid Saved Data
                if xbmcvfs.exists(var.rd_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.rd_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.rd_backup)
                        for file in data:
                                files = os.path.join(var.rd_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                        
                #Clear Premiumize Saved Data
                if xbmcvfs.exists(var.pm_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.pm_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.pm_backup)
                        for file in data:
                                files = os.path.join(var.pm_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                    
                #Clear All-Debrid Saved Data
                if xbmcvfs.exists(var.ad_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.ad_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.ad_backup)
                        for file in data:
                                files = os.path.join(var.ad_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                                        
                #Clear TorBox Saved Data
                if xbmcvfs.exists(var.tb_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.tb_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.tb_backup)
                        for file in data:
                                files = os.path.join(var.tb_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)

                #Clear Easy Debrid Saved Data
                if xbmcvfs.exists(var.ed_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.ed_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.ed_backup)
                        for file in data:
                                files = os.path.join(var.ed_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)

                #Clear OffCloud Saved Data
                if xbmcvfs.exists(var.offc_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.offc_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.offc_backup)
                        for file in data:
                                files = os.path.join(var.offc_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)

                #Clear Easynews Saved Data
                if xbmcvfs.exists(var.easy_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.easy_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.easy_backup)
                        for file in data:
                                files = os.path.join(var.easy_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)

                #Clear Filepursuit Saved Data
                if xbmcvfs.exists(var.file_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.file_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.file_backup)
                        for file in data:
                                files = os.path.join(var.file_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)

                #Clear External Providers Saved Data
                if xbmcvfs.exists(var.ext_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.ext_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.ext_backup)
                        for file in data:
                                files = os.path.join(var.ext_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                                        
                #Clear Metadata Saved Data
                if xbmcvfs.exists(var.meta_backup): # Skip clearing data if no folder present in backup folder
                    path = os.listdir(var.meta_backup)
                    if len(path) != 0: # Skip clearing data if no saved data in backup folder
                        data = os.listdir(var.meta_backup)
                        for file in data:
                                files = os.path.join(var.meta_backup, file)
                                if os.path.isfile(files):
                                        os.remove(files)
                xbmc.executebuiltin('Dialog.Close(all,true)')
                xbmc.sleep(1000)
                var.remake_settings() #Refresh settings database
                
            except:
                xbmc.log('%s: Router.py Revoke/Wipe/Clean Account Manager Failed!' % var.amgr, xbmc.LOGINFO)
                pass

            xbmcgui.Dialog().ok('Account Manager', 'All settings have been restored to default.')
                    
    def _finish(self, handle):
        from resources.libs.common import directory
        
        directory.set_view()
        
        xbmcplugin.setContent(handle, 'files')
        xbmcplugin.endOfDirectory(handle)
