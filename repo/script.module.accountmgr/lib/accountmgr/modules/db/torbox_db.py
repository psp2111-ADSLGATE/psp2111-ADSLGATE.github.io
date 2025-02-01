import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager TorBox
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_tb_token = accountmgr.getSetting("torbox.token")

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
        xbmc.log('%s: TorBox_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### TorBox #########################
def connect_tb(conn, setting):
    try:
        # Update settings database
        tb_enabled = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        tb_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(tb_enabled, setting)
        cur.execute(tb_token, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: TorBox_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#################### Auth Fen Light Offcloud ###################
def auth_fenlt_tb():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_tb(conn, ('true', 'tb.enabled'))
            connect_tb(conn, (your_tb_token, 'tb.token'))
    except:
        xbmc.log('%s: TorBox_db Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass
