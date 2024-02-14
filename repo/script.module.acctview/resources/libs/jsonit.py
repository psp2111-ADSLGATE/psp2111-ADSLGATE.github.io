import xbmc, xbmcaddon
import xbmcvfs
import json
import os
from resources.libs.common import var

########################################################################
########################################################################
############################ Realizer RD ##############################

###################### Restore Realizer RD ######################
def realizer_rst():
    if os.path.exists(os.path.join(var.rd_backup_realx)) and os.path.exists(os.path.join(var.realx_path)):
        try:
            xbmcvfs.copy(os.path.join(var.rd_backup_realx), os.path.join(var.realx_json_path))
        except:
            xbmc.log('%s: Jsonit_db Restore Realizer RD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

###################### Revoke Realizer RD ######################
def realizer_rvk():
    if os.path.exists(os.path.join(var.realx_json_path)):
        try:
            os.unlink(os.path.join(var.realx_json_path))
            xbmcvfs.copy(os.path.join(var.realx_json), os.path.join(var.realx_json_path))
        except:
            xbmc.log('%s: Jsonit_db Revoke Realizer RD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

###################### Backup Realizer RD ######################
def realizer_bk():
    if os.path.exists(os.path.join(var.realx_json_path)) and os.path.exists(os.path.join(var.rd_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.realx_json_path), os.path.join(var.rd_backup_realx))
        except:
            xbmc.log('%s: Jsonit_db Backup Realizer RD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete Realizer RD Backup #####################
#def realizer_rm():
#    if os.path.exists(os.path.join(var.rd_backup_realx)):
#        try:
#            os.unlink(os.path.join(var.rd_backup_realx))
#        except OSError:
#            xbmc.log('%s: Jsonit_db Delete Realizer RD Failed!' % var.amgr, xbmc.LOGINFO)
#            pass
