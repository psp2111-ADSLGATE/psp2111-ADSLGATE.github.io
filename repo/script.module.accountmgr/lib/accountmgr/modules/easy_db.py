import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager Easynews
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_easy_user = accountmgr.getSetting("easynews.username")
your_easy_pass = accountmgr.getSetting("easynews.password")

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
        xbmc.log('%s: Easy_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Easynews #########################
def connect_easy(conn, setting):
    try:
        # Update settings database
        easy_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        easy_user = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        easy_pass = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(easy_enable, setting)
        cur.execute(easy_user, setting)
        cur.execute(easy_pass, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Easy_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass


    
#################### Auth Fen Light Easynews ###################
def auth_fenlt_easy():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_easy(conn, ('true', 'provider_easynews'))
            connect_easy(conn, (your_easy_user, 'easynews_user'))
            connect_easy(conn, (your_easy_pass, 'easynews_password'))
    except:
        xbmc.log('%s: Easy_db Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass



################### Auth afFENity Easynews ##################
def auth_affen_easy():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_easy(conn, ('true', 'provider_easynews'))
            connect_easy(conn, (your_easy_user, 'easynews_user'))
            connect_easy(conn, (your_easy_pass, 'easynews_password'))
    except:
        xbmc.log('%s: Easy_db afFENity Failed!' % var.amgr, xbmc.LOGINFO)
        pass
