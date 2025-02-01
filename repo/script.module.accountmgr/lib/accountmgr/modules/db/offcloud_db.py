import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager Offcloud
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_oc_token = accountmgr.getSetting("offcloud.token")

###################### Connect to Database ######################
def create_conn(db_file):
    try:
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return conn
    except:
        xbmc.log('%s: Offcloud_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Offcloud #########################
def connect_oc(conn, setting):
    try:
        # Update settings database
        oc_enabled = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        oc_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(oc_enabled, setting)
        cur.execute(oc_token, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Offcloud_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#################### Auth Fen Light Offcloud ###################
def auth_fenlt_oc():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_oc(conn, ('true', 'oc.enabled'))
            connect_oc(conn, (your_oc_token, 'oc.token'))
    except:
        xbmc.log('%s: Offcloud_db Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass
