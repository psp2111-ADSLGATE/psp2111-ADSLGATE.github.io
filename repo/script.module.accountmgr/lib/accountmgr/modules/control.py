# -*- coding: utf-8 -*-
"""
	Account Manager
"""

import os.path
import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import datetime
from libs.common import var

addon = xbmcaddon.Addon
addonObject = addon('script.module.accountmgr')
addonInfo = addonObject.getAddonInfo
getLangString = xbmcaddon.Addon().getLocalizedString
condVisibility = xbmc.getCondVisibility
execute = xbmc.executebuiltin
monitor = xbmc.Monitor()
transPath = xbmcvfs.translatePath
joinPath = os.path.join
date = str(datetime.date.today())

accountmgr = xbmcaddon.Addon('script.module.accountmgr')
dialog = xbmcgui.Dialog()
window = xbmcgui.Window(10000)
progressDialog = xbmcgui.DialogProgress()

existsPath = xbmcvfs.exists
openFile = xbmcvfs.File
makeFile = xbmcvfs.mkdir

progress_line = '%s[CR]%s[CR]%s'

char_remov = ["'", ",", ")","("]

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
	
def getKodiVersion():
	return int(xbmc.getInfoLabel("System.BuildVersion")[:2])

def setting(id):
	return accountmgr.getSetting(id)

def setSetting(id, value):
	return accountmgr.setSetting(id, value)

def lang(language_id):
	text = getLangString(language_id)
	return text

def sleep(time):  # Modified `sleep` command that honors a user exit request
	while time > 0 and not monitor.abortRequested():
		xbmc.sleep(min(100, time))
		time = time - 100

def addonId():
	return addonInfo('id')

def addonName():
	return addonInfo('name')

def addonVersion():
	return addonInfo('version')

def addonIcon():
	return addonInfo('icon')

def addonPath():
	try: return transPath(addonInfo('path').decode('utf-8'))
	except: return transPath(addonInfo('path'))

def artPath():
	return os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons')

def openSettings(query=None, id=addonInfo('id')):
	try:
		idle()
		execute('Addon.OpenSettings(%s)' % id)
		if query is None: return
		c, f = query.split('.')
		execute('SetFocus(%i)' % (int(c) - 100))
		execute('SetFocus(%i)' % (int(f) - 80))
	except:
		return

def idle():
	if condVisibility('Window.IsActive(busydialognocancel)'):
		return execute('Dialog.Close(busydialognocancel)')

def fenlt_chk():
        if xbmcvfs.exists(var.synclist_file):
            fenlt = 'Fen Light'
            with open(var.synclist_file) as f:
                if fenlt in f.read():
                        if os.path.exists(os.path.join(var.fenlt_trakt_db)):
                                try:
                                        os.unlink(os.path.join(var.fenlt_trakt_db))
                                except OSError:
                                        pass
                else:
                    pass  
        else:
            pass
                                         
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

def notification_rd(title=None, message=None, icon=None, time=3000, sound=False):
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
	xbmc.sleep(3000)
	notification('Real-Debrid', 'Sync in progress, please wait!', icon=rd_icon)
	from accountmgr.modules.sync import debrid_rd
	debrid_rd.Auth().realdebrid_auth() #Sync all add-ons
	if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savedebrid_rd&name=all)') #Save Debrid data
                xbmc.sleep(3000)
                accountmgr.setSetting('rd_backup_date', date)
	notification('Real-Debrid', 'Sync Complete!', icon=rd_icon)
	
def notification_pm(title=None, message=None, icon=None, time=3000, sound=False):
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
	xbmc.sleep(3000)
	notification('Premiumize', 'Sync in progress, please wait!', icon=pm_icon)
	from accountmgr.modules.sync import debrid_pm
	debrid_pm.Auth().premiumize_auth() #Sync all add-ons
	if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savedebrid_pm&name=all)') #Save Debrid data
                xbmc.sleep(3000)
                accountmgr.setSetting('pm_backup_date', date)
	notification('Premiumize', 'Sync Complete!', icon=pm_icon)

def notification_ad(title=None, message=None, icon=None, time=3000, sound=False):
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
	xbmc.sleep(3000)
	notification('All-Debrid', 'Sync in progress, please wait!', icon=ad_icon)
	from accountmgr.modules.sync import debrid_ad
	debrid_ad.Auth().alldebrid_auth() #Sync all add-ons
	if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savedebrid_ad&name=all)') #Save Debrid data
                xbmc.sleep(3000)
                accountmgr.setSetting('ad_backup_date', date)
	notification('All-Debrid', 'Sync Complete!', icon=ad_icon)

def notification_trakt(title=None, message=None, icon=None, time=3000, sound=False):
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
        xbmc.sleep(3000)
        notification('Trakt', 'Sync in progress, please wait!', icon=trakt_icon)
        from accountmgr.modules.sync import trakt_sync
        trakt_sync.Auth().trakt_auth() #Sync all add-ons
        xbmc.sleep(1000)
        if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savetrakt&name=all)') #Save Trakt data
                xbmc.sleep(4000)
                accountmgr.setSetting('tk_backup_date', date)
        notification('Trakt', 'Sync Complete!', icon=trakt_icon)
        accountmgr.setSetting("api.service", "true") #Enable Trakt Service
        if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):
                chk_auth_dradis = xbmcaddon.Addon('plugin.video.dradis').getSetting("trakt.token")
                if not str(var.chk_accountmgr_tk) == str(chk_auth_dradis) or str(chk_auth_dradis) == '':
                        pass
                else:
                        accountmgr.setSetting("dradis_traktsync", 'true')
        if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                chk_auth_genocide = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("trakt.token")
                if not str(var.chk_accountmgr_tk) == str(chk_auth_genocide) or str(chk_auth_genocide) == '':
                        pass
                else:
                        accountmgr.setSetting("genocide_traktsync", 'true')


def notification_torbox(title=None, message=None, icon=None, time=3000, sound=False):
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
        xbmc.sleep(3000)
        notification('TorBox', 'Sync in progress, please wait!', icon=torbox_icon)
        from accountmgr.modules.sync import torbox_sync
        torbox_sync.Auth().torbox_auth() #Sync all add-ons
        if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savetorbox&name=all)') #Save OffCloud data
                xbmc.sleep(3000)
                accountmgr.setSetting('tb_backup_date', date)
        notification('TorBox', 'Sync Complete!', icon=torbox_icon)

def notification_easydebrid(title=None, message=None, icon=None, time=3000, sound=False):
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
        xbmc.sleep(3000)
        notification('Easy Debrid', 'Sync in progress, please wait!', icon=easyd_icon)
        from accountmgr.modules.sync import easydebrid_sync
        easydebrid_sync.Auth().easydebrid_auth() #Sync all add-ons
        if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=saveeasydebrid&name=all)') #Save OffCloud data
                xbmc.sleep(3000)
                accountmgr.setSetting('ed_backup_date', date)
        notification('Easy Debrid', 'Sync Complete!', icon=easyd_icon)
        
def notification_offcloud(title=None, message=None, icon=None, time=3000, sound=False):
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
        xbmc.sleep(3000)
        notification('OffCloud', 'Sync in progress, please wait!', icon=offcloud_icon)
        from accountmgr.modules.sync import offcloud_sync
        offcloud_sync.Auth().offcloud_auth() #Sync all add-ons
        if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=saveoffcloud&name=all)') #Save OffCloud data
                xbmc.sleep(3000)
                accountmgr.setSetting('oc_backup_date', date)
        notification('OffCloud', 'Sync Complete!', icon=offcloud_icon)

def notification_easynews(title=None, message=None, icon=None, time=3000, sound=False):
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
        xbmc.sleep(3000)
        notification('Easynews', 'Sync in progress, please wait!', icon=easy_icon)
        from accountmgr.modules.sync import easy_sync
        easy_sync.Auth().easy_auth() #Sync all add-ons
        if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=saveeasy&name=all)') #Save Easynews data
                xbmc.sleep(3000)
                accountmgr.setSetting('en_backup_date', date)
        notification('Easynews', 'Sync Complete!', icon=easy_icon)

def notification_filepursuit(title=None, message=None, icon=None, time=3000, sound=False):
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
        xbmc.sleep(3000)
        notification('FilePursuit', 'Sync in progress, please wait!', icon=file_icon)
        from accountmgr.modules.sync import filepursuit_sync
        filepursuit_sync.Auth().file_auth() #Sync all add-ons
        if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savefile&name=all)') #Save FilePursuit data
                xbmc.sleep(3000)
                accountmgr.setSetting('fp_backup_date', date)
        notification('FilePursuit', 'Sync Complete!', icon=file_icon)

def notification_tmdb(title=None, message=None, icon=None, time=3000, sound=False):
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
	xbmc.sleep(3000)
	notification('TMDb', 'Sync in progress, please wait!', icon=tmdb_icon)
	from accountmgr.modules.sync import meta_sync
	meta_sync.Auth().meta_auth() #Sync all add-ons
	if var.setting('backupenable') == 'true': #Check if backup service is enabled
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=savemeta&name=all)') #Save Metadata
                xbmc.sleep(3000)
                accountmgr.setSetting('md_backup_date', date)
	notification('TMDb', 'Sync Complete!', icon=tmdb_icon)

def yesnoDialog(line, heading=addonInfo('name'), nolabel='', yeslabel=''):
	return dialog.yesno(heading, line, nolabel, yeslabel)

def selectDialog(list, heading=addonInfo('name')):
	return dialog.select(heading, list)

def okDialog(title=None, message=None):
	if title == 'default' or title is None: title = addonName()
	if isinstance(title, int): heading = lang(title)
	else: heading = str(title)
	if isinstance(message, int): body = lang(message)
	else: body = str(message)
	return dialog.ok(heading, body)

def closeAll():
	return execute('Dialog.Close(all, true)')

def jsondate_to_datetime(jsondate_object, resformat, remove_time=False):
	import _strptime  # fix bug in python import
	from datetime import datetime
	import time
	if remove_time:
		try: datetime_object = datetime.strptime(jsondate_object, resformat).date()
		except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6])).date()
	else:
		try: datetime_object = datetime.strptime(jsondate_object, resformat)
		except TypeError: datetime_object = datetime(*(time.strptime(jsondate_object, resformat)[0:6]))
	return datetime_object

def set_active_monitor():
	window.setProperty('accountmgr.active', 'true')

def release_active_monitor():
	window.clearProperty('accountmgr.active')

def function_monitor(func, query='0.0'):
	func()
	sleep(100)
	openSettings(query)
	while not condVisibility('Window.IsVisible(addonsettings)'):
		sleep(250)
	sleep(100)
	release_active_monitor()

def refresh_debugReversed(): # called from service "onSettingsChanged" to clear accountmgr.log if setting to reverse has been changed
	if window.getProperty('accountmgr.debug.reversed') != setting('debug.reversed'):
		window.setProperty('accountmgr.debug.reversed', setting('debug.reversed'))
		execute('RunScript(script.module.accountmgr, action=tools_clearLogFile)')

def set_backup_folder(): #Set backup directory
        dialog = xbmcgui.Dialog()
        backup_location = dialog.browseSingle(0, 'Kodi', 'local', '', False, False)
        setSetting('backupfolder', backup_location)
        xbmcgui.Dialog().ok('Configure Backup', 'Backup Location Set')

def reset_backup_folder(): #Re-set backup directory
        setSetting('backupfolder', 'special://userdata/addon_data/script.module.accountmgr')
        xbmcgui.Dialog().ok('Configure Backup', 'Backup Location Set to Default')
