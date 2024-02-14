import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager Trakt
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_token = accountmgr.getSetting("trakt.token")
your_username = accountmgr.getSetting("trakt.username")           
your_refresh = accountmgr.getSetting("trakt.refresh")
your_expires = accountmgr.getSetting("trakt.expires")

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
        xbmc.log('%s: Trakt_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Trakt #########################
def connect_trakt(conn, setting):
    try:
        # Update settings database
        trakt_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        trakt_user = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        trakt_refresh = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        trakt_expires = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        trakt_watched_indicators = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        trakt_watched_indicators_name = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(trakt_token, setting)
        cur.execute(trakt_user, setting)
        cur.execute(trakt_refresh, setting)
        cur.execute(trakt_expires, setting)
        cur.execute(trakt_watched_indicators, setting)
        cur.execute(trakt_watched_indicators_name, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Trakt_db Failed!' % var.amgr, xbmc.LOGINFO)
        pass


    
#################### Auth Fen Light Trakt ###################
def auth_fenlt_trakt():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_trakt(conn, (your_token, 'trakt.token'))
            connect_trakt(conn, (your_username, 'trakt.user'))
            connect_trakt(conn, (your_refresh, 'trakt.refresh'))
            connect_trakt(conn, (your_expires, 'trakt.expires'))
            connect_trakt(conn, (1, 'watched_indicators'))
            connect_trakt(conn, ('Trakt', 'watched_indicators_name'))
    except:
        xbmc.log('%s: Trakt_db Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass



#################### Auth afFENity Trakt ###################
def auth_affen_trakt():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_trakt(conn, (your_token, 'trakt.token'))
            connect_trakt(conn, (your_username, 'trakt.user'))
            connect_trakt(conn, (your_refresh, 'trakt.refresh'))
            connect_trakt(conn, (your_expires, 'trakt.expires'))
            connect_trakt(conn, (1, 'watched_indicators'))
            connect_trakt(conn, ('Trakt', 'watched_indicators_name'))
    except:
        xbmc.log('%s: Trakt_db afFENity Failed!' % var.amgr, xbmc.LOGINFO)
        pass
