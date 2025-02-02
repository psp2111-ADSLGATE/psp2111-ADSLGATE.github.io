# -*- coding: utf-8 -*-

'''
	Account Manager
'''

import sys
import os
import xbmcgui
import xbmcaddon
import xbmcvfs
from urllib.parse import parse_qsl
from accountmgr.modules import control
from libs.common import var

joinPath = os.path.join
dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon
addonObject = addon('script.module.accountmgr')
addonInfo = addonObject.getAddonInfo
accountmgr = xbmcaddon.Addon('script.module.accountmgr')

amgr_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'accountmgr.png')
rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')
trakt_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'trakt.png')
tmdb_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'tmdb.png')
torbox_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'torbox.png')
easyd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'easydebrid.png')
offcloud_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'offcloud.png')
easy_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'easynews.png')
file_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'filepursuit.png')

def notification(title=None, message=None, icon=None, time=3000, sound=False):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	if icon is None or icon == '' or icon == 'default': icon = addonIcon()
	elif icon == 'INFO': icon = xbmcgui.NOTIFICATION_INFO
	elif icon == 'WARNING': icon = xbmcgui.NOTIFICATION_WARNING
	elif icon == 'ERROR': icon = xbmcgui.NOTIFICATION_ERROR
	dialog.notification(heading, body, icon, time, sound=sound)

def addonIcon():
	return addonInfo('icon')

def addonName():
	return addonInfo('name')

control.set_active_monitor()

params = {}
for param in sys.argv[1:]:
	param = param.split('=')
	param_dict = dict([param])
	params = dict(params, **param_dict)

action = params.get('action')
query = params.get('query')
addon_id = params.get('addon_id')

if action and not any(i in action for i in ['Auth', 'Revoke']):
	control.release_active_monitor()

if action is None:
	control.openSettings(query, "script.module.accountmgr")
	
#Trakt
elif action == 'traktAcct':
	from accountmgr.modules.auth import trakt
	trakt.Trakt().account_info_to_dialog()

elif action == 'traktAuth':
        if xbmcvfs.exists(var.synclist_file):
                from accountmgr.modules.auth import trakt
                trakt.Trakt().auth()
                control.setSetting('sync.tk.service', 'true')
                xbmc.sleep(3000)
                xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                os._exit(1)
        else:
                msg = 'You have not created a list of add-ons to authorize![CR]Would you like to create your list now?'
                if control.yesnoDialog(msg):
                        from accountmgr.modules.sync import trakt_select
                        trakt_select.tk_list().create_list()
                        from accountmgr.modules.auth import trakt
                        trakt.Trakt().auth()
                        control.setSetting('sync.tk.service', 'true')
                        xbmc.sleep(3000)
                        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                        os._exit(1)
                                

elif action == 'traktReSync': #Sync Trakt with installed add-ons
        from accountmgr.modules.sync import trakt_sync
        notification('Account Manager', 'Sync in progress, please wait!', icon=trakt_icon)
        xbmc.sleep(3000)
        trakt_sync.Auth().trakt_auth()
        xbmc.sleep(1000)
        accountmgr.setSetting("api.service", "true") #Enable Trakt Service
        notification('Account Manager', 'Sync Complete!', icon=trakt_icon)
        xbmc.sleep(3000)
        xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
        os._exit(1)
        
elif action == 'traktRevoke':
	from accountmgr.modules.auth import trakt
	control.function_monitor(trakt.Trakt().revoke)

elif action == 'traktSyncList':
	from accountmgr.modules.sync import trakt_select
	control.function_monitor(trakt_select.tk_list().create_list)

elif action == 'traktReSyncList':
	from accountmgr.modules.sync import trakt_select
	trakt_select.tk_list().create_list()
	xbmc.sleep(1000)
	msg = 'Your list has been updated![CR]Would you like to sync your changes now?'
	if control.yesnoDialog(msg):
                from accountmgr.modules.sync import trakt_sync
                notification('Account Manager', 'Sync in progress, please wait!', icon=trakt_icon)
                xbmc.sleep(3000)
                trakt_sync.Auth().trakt_auth()
                xbmc.sleep(1000)
                accountmgr.setSetting("api.service", "true") #Enable Trakt Service
                notification('Account Manager', 'Sync Complete!', icon=trakt_icon)
                xbmc.sleep(3000)
                xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                os._exit(1)
	
#Real-Debrid
elif action == 'realdebridAcct':
	from accountmgr.modules.auth import realdebrid
	realdebrid.RealDebrid().account_info_to_dialog()

elif action == 'realdebridAuth':
	from accountmgr.modules.auth import realdebrid
	control.function_monitor(realdebrid.RealDebrid().auth)
	control.setSetting('sync.rd.service', 'true')

elif action == 'realdebridReSync': #Sync Real-Debrid with installed add-ons
        notification('Account Manager', 'Sync in progress, please wait!', icon=rd_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import debrid_rd
        control.function_monitor(debrid_rd.Auth().realdebrid_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=rd_icon)
                
elif action == 'realdebridRevoke':
	from accountmgr.modules.auth import realdebrid
	control.function_monitor(realdebrid.RealDebrid().revoke)

#Premiumize
elif action == 'premiumizeAcct':
	from accountmgr.modules.auth import premiumize
	premiumize.Premiumize().account_info_to_dialog()

elif action == 'premiumizeAuth':
	from accountmgr.modules.auth import premiumize
	control.function_monitor(premiumize.Premiumize().auth)
	control.setSetting('sync.pm.service', 'true')

elif action == 'premiumizeReSync': #Sync Premiumize with installed add-ons
        notification('Account Manager', 'Sync in progress, please wait!', icon=pm_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import debrid_pm
        control.function_monitor(debrid_pm.Auth().premiumize_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=pm_icon)
	
elif action == 'premiumizeRevoke':
	from accountmgr.modules.auth import premiumize
	control.function_monitor(premiumize.Premiumize().revoke)

#All-Debrid
elif action == 'alldebridAcct':
	from accountmgr.modules.auth import alldebrid
	alldebrid.AllDebrid().account_info_to_dialog()

elif action == 'alldebridAuth':
	from accountmgr.modules.auth import alldebrid
	control.function_monitor(alldebrid.AllDebrid().auth)
	control.setSetting('sync.ad.service', 'true')

elif action == 'alldebridReSync': #Sync All-Debrid with installed add-ons
        notification('Account Manager', 'Sync in progress, please wait!', icon=rd_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import debrid_ad
        control.function_monitor(debrid_ad.Auth().alldebrid_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=ad_icon)

elif action == 'alldebridRevoke':
	from accountmgr.modules.auth import alldebrid
	control.function_monitor(alldebrid.AllDebrid().revoke)

#TorBox
elif action == 'torboxAuth':
	from accountmgr.modules.auth import torbox
	control.function_monitor(torbox.Torbox().auth)
	control.setSetting('sync.torbox.service', 'true')
elif action == 'torboxRevoke':
	from accountmgr.modules.auth import torbox
	control.function_monitor(torbox.Torbox().revoke)
elif action == 'torboxReSync':
        notification('Account Manager', 'Sync in progress, please wait!', icon=torbox_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import torbox_sync
        control.function_monitor(torbox_sync.Auth().torbox_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=torbox_icon)

#Easy Debrid
elif action == 'easydebridAuth':
	from accountmgr.modules.auth import easydebrid
	control.function_monitor(easydebrid.Easydebrid().auth)
	control.setSetting('sync.easyd.service', 'true')
elif action == 'easydebridRevoke':
	from accountmgr.modules.auth import easydebrid
	control.function_monitor(easydebrid.Easydebrid().revoke)
elif action == 'easydebridReSync':
        notification('Account Manager', 'Sync in progress, please wait!', icon=easyd_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import easydebrid_sync
        control.function_monitor(easydebrid_sync.Auth().easydebrid_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=easyd_icon)
                
#Offcloud
elif action == 'offcloudAuth':
	from accountmgr.modules.auth import offcloud
	control.function_monitor(offcloud.Offcloud().auth)
	control.setSetting('sync.offc.service', 'true')
elif action == 'offcloudRevoke':
	from accountmgr.modules.auth import offcloud
	control.function_monitor(offcloud.Offcloud().revoke)
elif action == 'offcloudReSync':
        notification('Account Manager', 'Sync in progress, please wait!', icon=offcloud_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import offcloud_sync
        control.function_monitor(offcloud_sync.Auth().offcloud_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=offcloud_icon)

#Easynews
elif action == 'easynewsAuth':
	from accountmgr.modules.auth import easynews
	control.function_monitor(easynews.Easynews().auth)
	control.setSetting('sync.easy.service', 'true')
elif action == 'easynewsReSync':                              
        notification('Account Manager', 'Sync in progress, please wait!', icon=easy_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import easy_sync
        control.function_monitor(easy_sync.Auth().easy_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=easy_icon)

#Filepursuit
elif action == 'filepursuitAuth':
	from accountmgr.modules.auth import filepursuit
	control.function_monitor(filepursuit.Filepursuit().auth)
	control.setSetting('sync.filep.service', 'true')
elif action == 'filepursuitReSync':
        notification('Account Manager', 'Sync in progress, please wait!', icon=file_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import filepursuit_sync
        control.function_monitor(filepursuit_sync.Auth().file_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=file_icon)

#Sync Meta Accounts
elif action == 'tmdbAuth':
	from accountmgr.modules.auth import tmdb
	control.function_monitor(tmdb.Auth().create_session_id)

elif action == 'tmdbRevoke':
	from accountmgr.modules.auth import tmdb
	control.function_monitor(tmdb.Auth().revoke_session_id)

elif action == 'metaAuth':
	if str(var.chk_accountmgr_fanart) != '' or str(var.chk_accountmgr_omdb) != '' or str(var.chk_accountmgr_mdb) != '' or str(var.chk_accountmgr_imdb) != '' or str(var.chk_accountmgr_tmdb) != '' or str(var.chk_accountmgr_tmdb_user) != '' or str(var.chk_accountmgr_tvdb) != '': #Skip sync if no meta account data in Account Manager
                notification('Account Manager', 'Sync in progress, please wait!', icon=amgr_icon)
                from accountmgr.modules.sync import meta_sync
                meta_sync.Auth().meta_auth()
                control.setSetting('sync.meta.service', 'true')
                if var.setting('backupenable') == 'true': #Check if backup service is enabled
                        xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savemeta&name=all)') #Save Metadata               
                        xbmc.sleep(3000)
                xbmc.sleep(2000)
                notification('Account Manager', 'Sync Complete!', icon=amgr_icon)
                xbmc.sleep(2000)
                xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                os._exit(1)
	else: #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'No Meta Data to Sync!', icon=amgr_icon)
                
elif action == 'metaReSync':
	if str(var.chk_accountmgr_fanart) != '' or str(var.chk_accountmgr_omdb) != '' or str(var.chk_accountmgr_mdb) != '' or str(var.chk_accountmgr_imdb) != '' or str(var.chk_accountmgr_tmdb) != '' or str(var.chk_accountmgr_tmdb_user) != '' or str(var.chk_accountmgr_tvdb) != '': #Skip sync if no meta account data in Account Manager
                notification('Account Manager', 'Sync in progress, please wait!', icon=amgr_icon)
                from accountmgr.modules.sync import meta_sync
                meta_sync.Auth().meta_auth()
                xbmc.sleep(2000)
                notification('Account Manager', 'Sync Complete!', icon=amgr_icon)
                xbmc.sleep(2000)
                xbmcgui.Dialog().ok('Account Manager', 'To save changes, please close Kodi, Press OK to force close Kodi')
                os._exit(1)

#External Providers
elif action == 'extAuth': #Sync external providers with installed add-ons
        if not os.path.exists(var.chk_coco):
                xbmcgui.Dialog().ok('Account Manager', 'No external scrapers are installed! Please install a supported scraper package and re-sync.')
                xbmc.executebuiltin('Dialog.CLose(all,true)')
                xbmc.executebuiltin("Addon.openSettings(script.module.accountmgr)")
                quit()
        else:
                from accountmgr.modules.sync import ext_sync
                accountmgr.setSetting("ext.provider", "CocoScrapers")
                notification('Account Manager', 'Sync in progress, please wait!', icon=amgr_icon)
                xbmc.sleep(3000)
                control.function_monitor(ext_sync.Auth().ext_auth)
                control.setSetting('sync.ext.service', 'true')
                xbmc.sleep(1000)
                notification('Account Manager', 'Sync Complete!', icon=amgr_icon)
elif action == 'extReSync':                              
        notification('Account Manager', 'Sync in progress, please wait!', icon=amgr_icon)
        xbmc.sleep(3000)
        from accountmgr.modules.sync import ext_sync
        control.function_monitor(ext_sync.Auth().ext_auth)
        xbmc.sleep(1000)
        notification('Account Manager', 'Sync Complete!', icon=amgr_icon)
        
#Sync Multiple Debrid Accounts
elif action == 'ReSyncAll': #Sync RD/PM/AD with installed add-ons
        #Real-Debrid
	if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules.sync import debrid_rd
                control.function_monitor(debrid_rd.Auth().realdebrid_auth)
                xbmc.sleep(1000)
                notification('Account Manager', 'Real-Debrid Sync Complete!', icon=rd_icon)
	if str(var.chk_accountmgr_tk_rd) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Real-Debrid NOT Authorized!', icon=rd_icon)

        #Premiumize
	if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules.sync import debrid_pm
                control.function_monitor(debrid_pm.Auth().premiumize_auth)
                xbmc.sleep(1000)
                notification('Account Manager', 'Premiumize Sync Complete!', icon=pm_icon)
	if str(var.chk_accountmgr_tk_pm) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Premiumize NOT Authorized!', icon=pm_icon)

        #All-Debrid
	if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules.sync import debrid_ad
                control.function_monitor(debrid_ad.Auth().alldebrid_auth)
                xbmc.sleep(1000)
                notification('Account Manager', 'All-Debrid Sync Complete!', icon=ad_icon)
	if str(var.chk_accountmgr_tk_ad) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'All-Debrid NOT Authorized!', icon=ad_icon)

#View Supported Add-ons              
elif action == 'ShowSupported_Trakt':
	from accountmgr.modules import changelog
	changelog.get_supported_trakt()

elif action == 'ShowSupported_Debrid':
	from accountmgr.modules import changelog
	changelog.get_supported_debrid()

elif action == 'ShowSupported_Torbox':
	from accountmgr.modules import changelog
	changelog.get_supported_torbox()

elif action == 'ShowSupported_Easydebrid':
	from accountmgr.modules import changelog
	changelog.get_supported_easydebrid()
	
elif action == 'ShowSupported_Offcloud':
	from accountmgr.modules import changelog
	changelog.get_supported_offcloud()
	
elif action == 'ShowSupported_Easy':
	from accountmgr.modules import changelog
	changelog.get_supported_easy()

elif action == 'ShowSupported_File':
	from accountmgr.modules import changelog
	changelog.get_supported_filepursuit()

elif action == 'ShowSupported_Meta':
	from accountmgr.modules import changelog
	changelog.get_supported_meta()

elif action == 'ShowSupported_Ext':
	from accountmgr.modules import changelog
	changelog.get_supported_ext()

elif action == 'ShowSupported_Ext_Addons':
	from accountmgr.modules import changelog
	changelog.get_supported_ext_addons()

#View Changelog	
elif action == 'ShowChangelog':
	from accountmgr.modules import changelog
	changelog.get()

#Other
elif action == 'ShowHelp':
	from accountmgr.help import help
	help.get(params.get('name'))

elif action == 'ShowHelpTMDb':
	from accountmgr.help import help
	help.get_tmdb()

elif action == 'ShowHelpMeta':
	from accountmgr.help import help
	help.get_meta()

elif action == 'ShowHelpNonDebrid':
	from accountmgr.help import help
	help.get_nondebrid()

elif action == 'ShowHelpServiceSync':
	from accountmgr.help import help
	help.get_service_sync()
	
elif action == 'ShowHelpCustom':
	from accountmgr.help import help
	help.get_custom()

elif action == 'ShowHelpRestore':
	from accountmgr.help import help
	help.get_restore()

elif action == 'ShowHelpReadme':
	from accountmgr.help import help
	help.get_readme()
	
elif action == 'ShowHelpIssues':
	from accountmgr.help import help
	help.get_issues()
	
elif action == 'ShowOKDialog':
	control.okDialog(params.get('title', 'default'), int(params.get('message', '')))

elif action == 'tools_clearLogFile':
	from accountmgr.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='My Accounts Log File Successfully Cleared')
	else: control.notification(message='Error clearing My Accounts Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from accountmgr.modules import log_utils
	log_utils.view_LogFile(params.get('name'))

elif action == 'tools_uploadLogFile':
	from accountmgr.modules import log_utils
	log_utils.upload_LogFile()

elif action == 'SetBackupFolder':
	from accountmgr.modules import control
	control.set_backup_folder()

elif action == 'ResetBackupFolder':
	from accountmgr.modules import control
	control.reset_backup_folder()
             
elif action == 'resetSettings':
        yes = dialog.yesno('Account Manager', 'WARNING! This will completely wipe all your saved data and remove all settings applied to add-ons via Account Manager. Click proceed to continue or cancel to quit.', 'Cancel', 'Proceed') # Ask user for permission
        if yes:
                control.setSetting("api.service", "false") #Disable Trakt service
                control.setSetting('reset_settings', 'true') #Enable reset at startup
                xbmcgui.Dialog().ok('Account Manager', 'Press OK to force close Kodi. You will be prompted at next startup to begin removal.')
                os._exit(1) #Force close Kodi

