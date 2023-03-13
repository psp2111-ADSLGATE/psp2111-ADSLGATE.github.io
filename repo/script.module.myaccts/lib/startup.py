import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path

joinPath = os.path.join
dialog = xbmcgui.Dialog()
addon = xbmcaddon.Addon
addonObject = addon('script.module.myaccts')
addonInfo = addonObject.getAddonInfo
rd_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'realdebrid.png')
pm_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'premiumize.png')
ad_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.myaccts').getAddonInfo('path'), 'resources', 'icons'), 'alldebrid.png')

second_check = None

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

def tmdbh():

        trakt_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.themoviedb.helper/')
        trakt_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.themoviedb.helper/settings.xml')        

        if xbmcvfs.exists(trakt_addon) and xbmcvfs.exists(trakt_file):
                
                first_check = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.709wiz/trakt/tmdbhelper_trakt')
                second_check = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("trakt_token")
                backup_file_save = xbmcvfs.translatePath('special://userdata/addon_data/plugin.program.709wiz/trakt/tmdbhelper_trakt')
                check = str(second_check)
  
                if xbmcvfs.exists(first_check) and str(check) != '':
                        quit()
             
                if not xbmcvfs.exists(backup_file_save) and second_check:
                        xbmc.sleep(15000)
                        xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=save_tmdbh&name=all)')

              
                if xbmcvfs.exists(backup_file_save):
                        
                        third_check = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("trakt_token")
                        
                        if not third_check:
                                xbmc.sleep(15000)
                                xbmc.executebuiltin('PlayMedia(plugin://script.module.myauth/?mode=restore_tmdbh&name=all)')


tmdbh()
