import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager TorBox
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_ed_token = accountmgr.getSetting("easydebrid.token")

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
        xbmc.log('%s: Easydebrid_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Easy Debrid #########################
def connect_ed(conn, setting):
    try:
        # Update settings database
        ed_enabled = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        ed_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(ed_enabled, setting)
        cur.execute(ed_token, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Easydebrid_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#################### Auth Fen Light Easy Debrid ###################
def auth_fenlt_ed():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_ed(conn, ('true', 'ed.enabled'))
            connect_ed(conn, (your_ed_token, 'ed.token'))
    except:
        xbmc.log('%s: Easydebrid_db Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass
