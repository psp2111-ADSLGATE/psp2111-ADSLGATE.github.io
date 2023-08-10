# -*- coding: utf-8 -*-

'''
	Account Manager
'''

import sys
import os
import xbmcgui
import xbmcaddon
from urllib.parse import parse_qsl
from accountmgr.modules import control
from accountmgr.modules import var

joinPath = os.path.join
dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon
addonObject = addon('script.module.accountmgr')
addonInfo = addonObject.getAddonInfo

rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')
trakt_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'trakt.png')


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

elif action == 'traktAcct':
	from accountmgr.modules import trakt
	trakt.Trakt().account_info_to_dialog()

elif action == 'traktAuth':
	from accountmgr.modules import trakt
	control.function_monitor(trakt.Trakt().auth)

elif action == 'traktReSync': #Sync additional add-ons after Account Manager is already authoorized
	if str(var.chk_accountmgr_tk) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import trakt_sync
                trakt_sync.sync_all()
                xbmc.sleep(1000)
                notification('Account Manager', 'تم مزامنة Trakt بنجاح!', icon=trakt_icon)
                xbmc.sleep(3000)
                xbmcgui.Dialog().ok('Account Manager', 'لحفظ التغييرات يجب إغلاق التطبيق, اضغط على "موافق" لإجبار Kodi على الإغلاق')
                os._exit(1)
	if str(var.chk_accountmgr_tk) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Trakt غير مفعل!', icon=trakt_icon)
        
elif action == 'traktRevoke':
	from accountmgr.modules import trakt
	control.function_monitor(trakt.Trakt().revoke)

elif action == 'alldebridAcct':
	from accountmgr.modules import alldebrid
	alldebrid.AllDebrid().account_info_to_dialog()

elif action == 'alldebridAuth':
	from accountmgr.modules import alldebrid
	control.function_monitor(alldebrid.AllDebrid().auth)

elif action == 'alldebridReSync': #Sync additional add-ons after Account Manager is already authoorized
	if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import debrid_ad
                debrid_ad.debrid_auth_ad()
                notification('Account Manager', 'تمت المزامنة بنجاح!', icon=ad_icon)
	if str(var.chk_accountmgr_tk_ad) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'All-Debrid غير مفعل!', icon=ad_icon)

elif action == 'alldebridRevoke':
	from accountmgr.modules import alldebrid
	control.function_monitor(alldebrid.AllDebrid().revoke)

elif action == 'premiumizeAcct':
	from accountmgr.modules import premiumize
	premiumize.Premiumize().account_info_to_dialog()

elif action == 'premiumizeAuth':
	from accountmgr.modules import premiumize
	control.function_monitor(premiumize.Premiumize().auth)

elif action == 'premiumizeReSync': #Sync additional add-ons after Account Manager is already authoorized
	if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import debrid_pm
                debrid_pm.debrid_auth_pm()
                notification('Account Manager', 'تمت المزامنة بنجاح!', icon=pm_icon)
	if str(var.chk_accountmgr_tk_pm) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Premiumize غير مفعل!', icon=pm_icon)
	
elif action == 'premiumizeRevoke':
	from accountmgr.modules import premiumize
	control.function_monitor(premiumize.Premiumize().revoke)

elif action == 'realdebridAcct':
	from accountmgr.modules import realdebrid
	realdebrid.RealDebrid().account_info_to_dialog()

elif action == 'realdebridAuth':
	from accountmgr.modules import realdebrid
	control.function_monitor(realdebrid.RealDebrid().auth)

elif action == 'realdebridReSync': #Sync additional add-ons after Account Manager is already authoorized
	if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import debrid_rd
                debrid_rd.debrid_auth_rd()
                notification('Account Manager', 'تمت المزامنة بنجاح!', icon=rd_icon)
	if str(var.chk_accountmgr_tk_rd) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Real-Debrid غير مفعل!', icon=rd_icon)
                
elif action == 'realdebridRevoke':
	from accountmgr.modules import realdebrid
	control.function_monitor(realdebrid.RealDebrid().revoke)

elif action == 'tmdbAuth':
	from accountmgr.modules import tmdb
	control.function_monitor(tmdb.Auth().create_session_id)

elif action == 'tmdbRevoke':
	from accountmgr.modules import tmdb
	control.function_monitor(tmdb.Auth().revoke_session_id)

elif action == 'ShowChangelog':
	from accountmgr.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from accountmgr.help import help
	help.get(params.get('name'))

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

elif action == 'ReSyncAll': #Sync additional add-ons for all services after Account Manager is already authorized
        #Real-Debrid
	if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import debrid_rd
                debrid_rd.debrid_auth_rd()
                notification('Account Manager', 'Real-Debrid تمت المزامنة بنجاح!', icon=rd_icon)
	if str(var.chk_accountmgr_tk_rd) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Real-Debrid غير مفعل!', icon=rd_icon)

        #Premiumize
	if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import debrid_pm
                debrid_pm.debrid_auth_pm()
                notification('Account Manager', 'Premiumize تمت المزامنة بنجاح!', icon=pm_icon)
	if str(var.chk_accountmgr_tk_pm) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Premiumize غير مفعل!', icon=pm_icon)

        #All-Debrid
	if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import debrid_ad
                debrid_ad.debrid_auth_ad()
                notification('Account Manager', 'All-Debrid تمت المزامنة بنجاح!', icon=ad_icon)
	if str(var.chk_accountmgr_tk_ad) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'All-Debrid غير مفعل!', icon=ad_icon)

        #Trakt
	if str(var.chk_accountmgr_tk) != '': #Skip sync if Account Mananger is not authorized
                from accountmgr.modules import trakt_sync
                trakt_sync.sync_all()
                xbmc.sleep(1000)
                notification('Account Manager', 'تم مزامنة Trakt بنجاح!', icon=trakt_icon)
                xbmc.sleep(3000)
                xbmcgui.Dialog().ok('Account Manager', 'لحفظ التغييرات يجب إغلاق التطبيق, اضغط على "موافق" لإجبار Kodi على الإغلاق')
                os._exit(1)
	if str(var.chk_accountmgr_tk) == '': #If Account Mananger is not Authorized notify user
                notification('Account Manager', 'Trakt غير مفعل!', icon=trakt_icon)
