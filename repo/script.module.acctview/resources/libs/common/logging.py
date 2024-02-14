import xbmc
import xbmcgui
import xbmcvfs
import os
import re
import time
import _strptime
from resources.libs.common import tools
from resources.libs.common.config import CONFIG

def log(msg, level=xbmc.LOGDEBUG):
    if CONFIG.DEBUGLEVEL == '0':  # No Logging
        return False
    if CONFIG.DEBUGLEVEL == '1':  # Normal Logging
        pass
    if CONFIG.DEBUGLEVEL == '2':  # Full Logging
        level = xbmc.LOGINFO
    
    xbmc.log('{0}: {1}'.format(CONFIG.ADDONTITLE, msg), level)

def log_notify(title, message, times=2000, icon=CONFIG.ADDON_ICON, sound=False):
    dialog = xbmcgui.Dialog()
    dialog.notification(title, message, icon, int(times), sound)

