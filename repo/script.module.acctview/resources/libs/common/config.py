import xbmc
import xbmcaddon
import xbmcvfs
import os
import vars
from pathlib import Path

translatePath = xbmcvfs.translatePath
addon = xbmcaddon.Addon("script.module.accountmgr")
setting = addon.getSetting
backup_path = Path(translatePath(setting('backupfolder')))

class Config:
    def __init__(self):
        self.init_meta()
        self.init_varss()
        self.init_paths()
        self.init_settings()

    def init_meta(self):
        self.ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
        self.ADDON = xbmcaddon.Addon(self.ADDON_ID)
        self.ADDON_NAME = self.ADDON.getAddonInfo('name')
        self.ADDON_VERSION = self.ADDON.getAddonInfo('version')
        self.ADDON_PATH = self.ADDON.getAddonInfo('path')
        self.ADDON_ICON = self.ADDON.getAddonInfo('icon')
        self.ADDON_FANART = self.ADDON.getAddonInfo('fanart')
        self.KODIV = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
        self.RAM = int(xbmc.getInfoLabel("System.Memory(total)")[:-2])

    def init_varss(self):
        # User Edit Variables
        self.ADDONTITLE = vars.ADDONTITLE

        # Themeing Menu Items
        self.HIDESPACERS = vars.HIDESPACERS
        self.SPACER = vars.SPACER
        self.COLOR1 = vars.COLOR1
        self.COLOR2 = vars.COLOR2
        self.THEME2 = vars.THEME2
        self.THEME3 = vars.THEME3
        

    def init_paths(self):

        # Default special paths
        self.XBMC = xbmcvfs.translatePath('special://xbmc/')
        self.HOME = xbmcvfs.translatePath('special://home/')
        self.TEMP = xbmcvfs.translatePath('special://temp/')
        self.MASTERPROFILE = xbmcvfs.translatePath('special://masterprofile/')
        self.PROFILE = xbmcvfs.translatePath('special://profile/')
        self.USERDATA = xbmcvfs.translatePath('special://userdata/')
        self.DATABASE = xbmcvfs.translatePath('special://database/')
        self.THUMBNAILS = xbmcvfs.translatePath('special://thumbnails/')
        self.SKIN = xbmcvfs.translatePath('special://skin/')
        self.LOGPATH = xbmcvfs.translatePath('special://logpath/')

        # Constructed paths
        self.ADDONS = os.path.join(self.HOME, 'addons')
        self.KODIADDONS = os.path.join(self.XBMC, 'addons')
        self.PLUGIN = os.path.join(self.ADDONS, self.ADDON_ID)
        self.ADDON_DATA = os.path.join(self.USERDATA, 'addon_data')
        self.ADDON_DATA_TRAKT = os.path.join(self.USERDATA, 'addon_data')
        self.ADDON_DATA_DEBRID = os.path.join(self.USERDATA, 'addon_data')
        self.PLUGIN_DATA = os.path.join(self.ADDON_DATA, self.ADDON_ID)
        self.PLUGIN_DATA_TRAKT = os.path.join(backup_path)
        self.PLUGIN_DATA_DEBRID = os.path.join(backup_path)
        self.DEBRIDFOLD = os.path.join(self.PLUGIN_DATA_DEBRID, 'debrid')
        self.TRAKTFOLD = os.path.join(self.PLUGIN_DATA_TRAKT, 'trakt')
        self.LOGINFOLD = os.path.join(self.PLUGIN_DATA, 'login')

        
    def init_settings(self):
        

        # Logging variables
        self.DEBUGLEVEL = self.get_setting('debuglevel')
        self.ENABLEWIZLOG = self.get_setting('wizardlog')
        self.CLEANWIZLOG = self.get_setting('autocleanwiz')
        self.CLEANWIZLOGBY = self.get_setting('wizlogcleanby')
        self.CLEANDAYS = self.get_setting('wizlogcleandays')
        self.CLEANSIZE = self.get_setting('wizlogcleansize')
        self.CLEANLINES = self.get_setting('wizlogcleanlines')
        self.MAXWIZSIZE = [100, 200, 300, 400, 500, 1000]
        self.MAXWIZLINES = [100, 200, 300, 400, 500]
        self.MAXWIZDATES = [1, 2, 3, 7]
        self.KEEPOLDLOG = self.get_setting('oldlog') == 'true'
        self.KEEPWIZLOG = self.get_setting('wizlog') == 'true'
        self.KEEPCRASHLOG = self.get_setting('crashlog') == 'true'
        self.LOGEMAIL = self.get_setting('email')
        self.NEXTCLEANDATE = self.get_setting('nextwizcleandate')

    def get_setting(self, key, id=xbmcaddon.Addon().getAddonInfo('id')):
        try:
            return xbmcaddon.Addon(id).getSetting(key)
        except:
            return False

    def set_setting(self, key, value, id=xbmcaddon.Addon().getAddonInfo('id')):
        try:
            return xbmcaddon.Addon(id).setSetting(key, value)
        except:
            return False

    def open_settings(self, id=None, cat=None, set=None, activate=False):
        offset = [(100,  200), (-100, -80)]
        if not id:
            id = self.ADDON_ID

        try:
            xbmcaddon.Addon(id).openSettings()
        except:
            import logging
            logging.log('Cannot open settings for {}'.format(id), level=xbmc.LOGERROR)
        
        if int(self.KODIV) < 18:
            use = 0
        else:
            use = 1

        if cat is not None:
            category_id = cat + offset[use][0]
            xbmc.executebuiltin('SetFocus({})'.format(category_id))
            if set is not None:
                setting_id = set + offset[use][1]
                xbmc.executebuiltin('SetFocus({})'.format(setting_id))
                
                if activate:
                    xbmc.executebuiltin('SendClick({})'.format(setting_id))
            

    def clear_setting(self, type):
        build = {'buildname': '', 'buildversion': '', 'buildtheme': '',
                 'latestversion': '', 'nextbuildcheck': '2019-01-01 00:00:00'}
        install = {'extract': '', 'errors': '', 'installed': ''}
        default = {'defaultskinignore': 'false', 'defaultskin': '',
                   'defaultskinname': ''}
        lookfeel = ['default.enablerssfeeds', 'default.font', 'default.rssedit',
                    'default.skincolors', 'default.skintheme',
                    'default.skinzoom', 'default.soundskin',
                    'default.startupwindow', 'default.stereostrength']
        if type == 'build':
            for element in build:
                self.set_setting(element, build[element])
            for element in install:
                self.set_setting(element, install[element])
            for element in default:
                self.set_setting(element, default[element])
            for element in lookfeel:
                self.set_setting(element, '')
        elif type == 'default':
            for element in default:
                self.set_setting(element, default[element])
            for element in lookfeel:
                self.set_setting(element, '')
        elif type == 'install':
            for element in install:
                self.set_setting(element, install[element])
        elif type == 'lookfeel':
            for element in lookfeel:
                self.set_setting(element, '')
        else:
            self.set_setting(type, '')


CONFIG = Config()

