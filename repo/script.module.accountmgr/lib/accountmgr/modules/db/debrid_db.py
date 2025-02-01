import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from libs.common import var
from sqlite3 import Error

#Account Manager Real-Debrid
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_rd_username = accountmgr.getSetting("realdebrid.username")
your_rd_token = accountmgr.getSetting("realdebrid.token")
your_rd_client_id = accountmgr.getSetting("realdebrid.client_id")
your_rd_refresh = accountmgr.getSetting("realdebrid.refresh")
your_rd_secret = accountmgr.getSetting("realdebrid.secret")
your_rd_expiry = accountmgr.getSetting("realdebrid.expiry.notice")

#Account Manager Premiumize
your_pm_username = accountmgr.getSetting("premiumize.username")
your_pm_token = accountmgr.getSetting("premiumize.token")

#Account Manager All-Debrid
your_ad_username = accountmgr.getSetting("alldebrid.username")
your_ad_token = accountmgr.getSetting("alldebrid.token")

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
        xbmc.log('%s: Debrid_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Real-Debrid #########################
def connect_rd(conn, setting):
    try:
        # Update settings database
        rd_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        rd_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        rd_account_id = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        rd_client_id = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        rd_refresh = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        rd_secret = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(rd_enable, setting)
        cur.execute(rd_token, setting)
        cur.execute(rd_account_id, setting)
        cur.execute(rd_client_id, setting)
        cur.execute(rd_refresh, setting)
        cur.execute(rd_secret, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Auth RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#Enable RD
def enable_rd(conn, setting):
    try:
        # Update settings database
        rd_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(rd_enable, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Enable RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#Disable RD
def disable_rd(conn, setting):
    try:
        # Update settings database
        rd_disable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(rd_disable, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Disable RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass



######################### Premiumize #########################
def connect_pm(conn, setting):
    try:
        # Update settings database
        pm_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        pm_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        pm_account_id = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(pm_enable, setting)
        cur.execute(pm_token, setting)
        cur.execute(pm_account_id, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Auth PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#Enable PM
def enable_pm(conn, setting):
    try:
        # Update settings database
        pm_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(pm_enable, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Enable PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#Disable PM
def disable_pm(conn, setting):
    try:
        # Update settings database
        pm_disable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(pm_disable, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Disable PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass



######################### All-Debrid #########################
def connect_ad(conn, setting):
    try:
        # Update settings database
        ad_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        ad_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        ad_account_id = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(ad_enable, setting)
        cur.execute(ad_token, setting)
        cur.execute(ad_account_id, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Auth AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#Enable AD
def enable_ad(conn, setting):
    try:
        # Update settings database
        ad_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(ad_enable, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Enable AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass

#Disable AD
def disable_ad(conn, setting):
    try:
        # Update settings database
        ad_disable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(ad_disable, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Debrid_db Disable AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass


    
######################################################################
######################################################################    
######################################################################
########################## Auth Fen Light RD #########################
def auth_fenlt_rd():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_rd(conn, ('true', 'rd.enabled'))
            connect_rd(conn, (your_rd_token, 'rd.token'))
            connect_rd(conn, (your_rd_username, 'rd.account_id'))
            connect_rd(conn, (your_rd_client_id, 'rd.client_id'))
            connect_rd(conn, (your_rd_refresh, 'rd.refresh'))
            connect_rd(conn, (your_rd_secret, 'rd.secret'))
    except:
        xbmc.log('%s: Debrid_db Fen Light RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def enable_fenlt_rd():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            enable_rd(conn, ('true', 'rd.enabled'))
    except:
        xbmc.log('%s: Debrid_db Fen Light Enable RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
   
def disable_fenlt_rd():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            disable_rd(conn, ('false', 'rd.enabled'))
    except:
        xbmc.log('%s: Debrid_db Fen Light Disable RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass



#####################################################################
#####################################################################   
#####################################################################
######################### Auth Fen Light PM #########################
def auth_fenlt_pm():
    try:
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_pm(conn, ('true', 'pm.enabled'))
            connect_pm(conn, (your_pm_token, 'pm.token'))
            connect_pm(conn, (your_pm_username, 'pm.account_id'))
    except:
        xbmc.log('%s: Debrid_db Fen Light PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def enable_fenlt_pm():
    try:
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            enable_pm(conn, ('true', 'pm.enabled'))
    except:
        xbmc.log('%s: Debrid_db Fen Light Enable PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    

    
def disable_fenlt_pm():
    try:
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            disable_pm(conn, ('false', 'pm.enabled'))
    except:
        xbmc.log('%s: Debrid_db Fen Light Disable PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass


    
#####################################################################
#####################################################################    
#####################################################################    
######################### Auth Fen Light AD #########################
def auth_fenlt_ad():
    try:
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_ad(conn, ('true', 'ad.enabled'))
            connect_ad(conn, (your_ad_token, 'ad.token'))
            connect_ad(conn, (your_ad_username, 'ad.account_id'))
    except:
        xbmc.log('%s: Debrid_db Fen Light AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def enable_fenlt_ad():
    try:
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            enable_ad(conn, ('true', 'ad.enabled'))
    except:
        xbmc.log('%s: Debrid_db Fen Light Enable AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
       
def disable_fenlt_ad():
    try:
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            disable_ad(conn, ('false', 'ad.enabled'))
    except:
        xbmc.log('%s: Debrid_db Fen Light Disable AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass


    
'''####################################################################
####################################################################   
####################################################################
######################### Auth afFENity RD #########################
def auth_affen_rd():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_rd(conn, ('true', 'rd.enabled'))
            connect_rd(conn, (your_rd_token, 'rd.token'))
            connect_rd(conn, (your_rd_username, 'rd.account_id'))
            connect_rd(conn, (your_rd_client_id, 'rd.client_id'))
            connect_rd(conn, (your_rd_refresh, 'rd.refresh'))
            connect_rd(conn, (your_rd_secret, 'rd.secret'))
    except:
        xbmc.log('%s: Debrid_db afFENity RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def enable_affen_rd():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            enable_rd(conn, ('true', 'rd.enabled'))
    except:
        xbmc.log('%s: Debrid_db afFENity Enable RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def disable_affen_rd():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            disable_rd(conn, ('false', 'rd.enabled'))
    except:
        xbmc.log('%s: Debrid_db afFENity Disable RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass



####################################################################
####################################################################    
####################################################################    
######################### Auth afFENity PM #########################
def auth_affen_pm():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_pm(conn, ('true', 'pm.enabled'))
            connect_pm(conn, (your_pm_token, 'pm.token'))
            connect_pm(conn, (your_pm_username, 'pm.account_id'))
    except:
        xbmc.log('%s: Debrid_db afFENity PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def enable_affen_pm():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            enable_pm(conn, ('true', 'pm.enabled'))
    except:
        xbmc.log('%s: Debrid_db afFENity Enable PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
   
def disable_affen_pm():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            disable_pm(conn, ('false', 'pm.enabled'))
    except:
        xbmc.log('%s: Debrid_db afFENity Disable PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    


####################################################################
####################################################################    
####################################################################
######################### Auth afFENity AD #########################
def auth_affen_ad():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_ad(conn, ('true', 'ad.enabled'))
            connect_ad(conn, (your_ad_token, 'ad.token'))
            connect_ad(conn, (your_ad_username, 'ad.account_id'))
    except:
        xbmc.log('%s: Debrid_db afFENity AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def enable_affen_ad():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            enable_ad(conn, ('true', 'ad.enabled'))
    except:
        xbmc.log('%s: Debrid_db afFENity Enable AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
       
def disable_affen_ad():
    try:
        conn = create_conn(var.affen_settings_db)
        with conn:
            disable_ad(conn, ('false', 'ad.enabled'))
    except:
        xbmc.log('%s: Debrid_db afFENity Disable AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''
