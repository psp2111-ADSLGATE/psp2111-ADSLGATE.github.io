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
        xbmc.log('%s: Ext_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### External Provider #########################
def connect_ext(conn, setting):
    try:
        # Update settings database
        ext_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        ext_user = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        ext_pass = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(ext_enable, setting)
        cur.execute(ext_user, setting)
        cur.execute(ext_pass, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Ext_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass


    
#################### Auth Fen Light External Provider ###################
def auth_fenlt_ext():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_ext(conn, ('true', 'provider.external'))
            connect_ext(conn, ('CocoScrapers Module', 'external_scraper.name'))
            connect_ext(conn, ('script.module.cocoscrapers', 'external_scraper.module'))
    except:
        xbmc.log('%s: Easy_db Fen Light Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Revoke Fen Light External Provider #########################
def revoke_fenlt_ext():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_ext(conn, ('false', 'provider.external'))
            connect_ext(conn, ('empty_setting', 'external_scraper.name'))
            connect_ext(conn, ('empty_setting', 'external_scraper.module'))
    except:
        xbmc.log('%s: Ext_db Revoke Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass
