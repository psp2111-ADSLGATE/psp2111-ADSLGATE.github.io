import xbmc
import xbmcgui
import xbmcvfs
import os
import re
import time
import _strptime
from resources.libs.common import tools
from resources.libs.common.config import CONFIG
try:  # Python 3
    from urllib.parse import urlencode
    from urllib.request import FancyURLopener
except ImportError:  # Python 2
    from urllib import urlencode
    from urllib import FancyURLopener


URL = 'https://paste.ubuntu.com/'
EXPIRATION = 2592000
REPLACES = (('//.+?:.+?@', '//USER:PASSWORD@'), ('<user>.+?</user>', '<user>USER</user>'), ('<pass>.+?</pass>',
                                                                                            '<pass>PASSWORD</pass>'),)


def log(msg, level=xbmc.LOGDEBUG):
    if CONFIG.DEBUGLEVEL == '0':  # No Logging
        return False
    if CONFIG.DEBUGLEVEL == '1':  # Normal Logging
        pass
    if CONFIG.DEBUGLEVEL == '2':  # Full Logging
        level = xbmc.LOGINFO
    
    xbmc.log('{0}: {1}'.format(CONFIG.ADDONTITLE, msg), level)
    if CONFIG.ENABLEWIZLOG == 'true':
        if not os.path.exists(CONFIG.WIZLOG):
            with open(CONFIG.WIZLOG, 'w+') as f:
                f.close()

        lastcheck = CONFIG.NEXTCLEANDATE if not CONFIG.NEXTCLEANDATE == 0 else tools.get_date()
        if CONFIG.CLEANWIZLOG == 'true' and time.mktime(time.strptime(lastcheck, "%Y-%m-%d %H:%M:%S")) <= tools.get_date():
            check_log()

        line = "[{0}] {1}".format(tools.get_date(formatted=True), msg)
        line = line.rstrip('\r\n') + '\n'
        tools.write_to_file(CONFIG.WIZLOG, line, mode='a')


def log_notify(title, message, times=2000, icon=CONFIG.ADDON_ICON, sound=False):
    dialog = xbmcgui.Dialog()
    dialog.notification(title, message, icon, int(times), sound)


def show_result(message, url=None):
    from resources.libs.gui import window

    dialog = xbmcgui.Dialog()

    if url:
        try:
            from resources.libs import qr
            
            fn = url.split('/')[-2]
            imagefile = qr.generate_code(url, fn)
            window.show_qr_code("loguploader.xml", imagefile, message)
            try:
                os.remove(imagefile)
            except:
                pass
        except Exception as e:
            log(str(e), xbmc.LOGINFO)
            confirm = dialog.ok(CONFIG.ADDONTITLE, "[COLOR %s]%s[/COLOR]" % (CONFIG.COLOR2, message))
    else:
        confirm = dialog.ok(CONFIG.ADDONTITLE, "[COLOR %s]%s[/COLOR]" % (CONFIG.COLOR2, message))

