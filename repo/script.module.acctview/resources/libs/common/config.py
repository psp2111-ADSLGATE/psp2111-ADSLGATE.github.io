import xbmc
import xbmcaddon
import xbmcvfs
import os
import os.path
import vars
from pathlib import Path

joinPath = os.path.join
translatePath = xbmcvfs.translatePath
addon = xbmcaddon.Addon("script.module.accountmgr")
setting = addon.getSetting
backup_path = Path(translatePath(setting('backupfolder')))

addon_acctv = xbmcaddon.Addon
addon_acctvObject = addon_acctv('script.module.acctview')
addon_acctvInfo = addon_acctvObject.getAddonInfo
getLangString = xbmcaddon.Addon().getLocalizedString


class Config:
    def __init__(self):
        self.init_meta()
        self.init_vars()
        self.init_paths()
        self.init_settings()

    def init_meta(self):
        self.ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
        self.ADDON = xbmcaddon.Addon(self.ADDON_ID)
        self.ADDON_NAME = self.ADDON.getAddonInfo('name')
        self.ADDON_VERSION = self.ADDON.getAddonInfo('version')
        self.ADDON_PATH = self.ADDON.getAddonInfo('path')
        self.ADDON_ICON = self.ADDON.getAddonInfo('icon')
        self.ADDON_SEP_ICON = joinPath(os.path.join(xbmcaddon.Addon('script.module.acctview').getAddonInfo('path'), 'resources', 'icons'), 'separator.png')
        self.ADDON_FANART = self.ADDON.getAddonInfo('fanart')
        self.ICONDEBRID = self.ADDON.getAddonInfo('icon')
        self.ICONTRAKT = self.ADDON.getAddonInfo('icon')

    def init_vars(self):
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
        self.USERDATA = xbmcvfs.translatePath('special://profile/')
        self.DATABASE = xbmcvfs.translatePath('special://database/')
        self.THUMBNAILS = xbmcvfs.translatePath('special://thumbnails/')
        self.LOGPATH = xbmcvfs.translatePath('special://logpath/')

        # Constructed paths
        self.ADDONS = os.path.join(self.HOME, 'addons')
        self.KODIADDONS = os.path.join(self.XBMC, 'addons')
        self.PLUGIN = os.path.join(self.ADDONS, self.ADDON_ID)
        self.ADDON_DATA = os.path.join(self.USERDATA, 'addon_data')
        self.ADDON_DATA_TRAKT = os.path.join(self.USERDATA, 'addon_data')
        self.ADDON_DATA_DEBRID = os.path.join(self.USERDATA, 'addon_data')
        self.PLUGIN_DATA = os.path.join(self.ADDON_DATA, self.ADDON_ID)
        self.PLUGIN_DATA_BACKUP = os.path.join(backup_path)
        self.TRAKTFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'trakt')
        self.DEBRIDFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'debrid')
        self.DEBRIDFOLD_RD = os.path.join(self.PLUGIN_DATA_BACKUP, 'realdebrid')
        self.DEBRIDFOLD_PM = os.path.join(self.PLUGIN_DATA_BACKUP, 'premiumize')
        self.DEBRIDFOLD_AD = os.path.join(self.PLUGIN_DATA_BACKUP, 'alldebrid')
        self.TBFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'torbox')
        self.EDFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'easydebrid')
        self.OFFCFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'offcloud')
        self.EASYFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'easynews')
        self.FILEFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'filepursuit')
        self.METAFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'meta')
        self.EXTFOLD = os.path.join(self.PLUGIN_DATA_BACKUP, 'extproviders')
        self.LOGINFOLD = os.path.join(self.PLUGIN_DATA, 'login')
        
    def init_settings(self):
        # Logging variables
        self.DEBUGLEVEL = self.get_setting('debuglevel')
        self.KEEPOLDLOG = self.get_setting('oldlog') == 'true'
        self.KEEPCRASHLOG = self.get_setting('crashlog') == 'true'

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
            
CONFIG = Config()

