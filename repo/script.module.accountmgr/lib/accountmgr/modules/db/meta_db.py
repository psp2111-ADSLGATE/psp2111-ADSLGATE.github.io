import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager Metadata
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_omdb_api = accountmgr.getSetting("omdb.api.key")
your_tmdb_api = accountmgr.getSetting("tmdb.api.key")

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
        xbmc.log('%s: Meta_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass

########################## Fen Light OMDb Metadata #########################
def connect_omdb_fenlt(conn, setting):
    try:
        # Update settings database
        omdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        
        cur = conn.cursor()
        cur.execute(omdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db OMDb Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass

########################## Fen Light TMDb Metadata #########################
def connect_tmdb_fenlt(conn, setting):
    try:
        # Update settings database
        tmdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        
        cur = conn.cursor()
        cur.execute(tmdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db TMDb Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
'''########################## Affenity Metadata #########################
def connect_meta_affen(conn, setting):
    try:
        # Update settings database
        omdb_api = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''

        cur = conn.cursor()
        cur.execute(omdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Meta_db Auth Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''

    
#################### Auth Fen Light OMDb Metadata ###################
def auth_fenlt_omdb():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_omdb_fenlt(conn, (your_omdb_api, 'omdb_api'))
    except:
        xbmc.log('%s: Meta_db OMDb Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#################### Auth Fen Light TMDb Metadata ###################
def auth_fenlt_tmdb():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_tmdb_fenlt(conn, (your_tmdb_api, 'tmdb_api'))
    except:
        xbmc.log('%s: Meta_db TMDb Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
        pass


'''#################### Auth afFENityt Metadata ###################
    def auth_affen_meta():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_meta_affen(conn, (your_omdb_api, 'omdb_api'))
    except:
        xbmc.log('%s: Meta_db afFENity Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''
