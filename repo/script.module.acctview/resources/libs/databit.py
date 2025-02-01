import xbmc, xbmcaddon
import sqlite3
import xbmcvfs
import os
from resources.libs.common import var
from sqlite3 import Error

char_remov = ["'", ",", ")","("]

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
        xbmc.log('%s: Databit_db Connect Failed!' % var.amgr, xbmc.LOGINFO)
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
        xbmc.log('%s: Databit_db RD Failed!' % var.amgr, xbmc.LOGINFO)
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
        xbmc.log('%s: Databit_db PM Failed!' % var.amgr, xbmc.LOGINFO)
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
        xbmc.log('%s: Databit_db AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass


######################### Fen Light Trakt #########################
def connect_trakt_fenlt(conn, setting):
    try:
        # Update settings database
        trakt_client = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        trakt_secret = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
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
        cur.execute(trakt_client, setting)
        cur.execute(trakt_secret, setting)
        cur.execute(trakt_token, setting)
        cur.execute(trakt_user, setting)
        cur.execute(trakt_refresh, setting)
        cur.execute(trakt_expires, setting)
        cur.execute(trakt_watched_indicators, setting)
        cur.execute(trakt_watched_indicators_name, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Databit_db Fen Light Trakt Failed!' % var.amgr, xbmc.LOGINFO)
        pass

    
'''######################### Affenity Trakt #########################
def connect_trakt_affen(conn, setting):
    try:
        # Update settings database
        trakt_token = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''
        trakt_user = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''
        trakt_refresh = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''
        trakt_expires = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''
        trakt_watched_indicators = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''
        trakt_watched_indicators_name = '''''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?''''''

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
        xbmc.log('%s: Databit_db Affenity Trakt Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''

######################### Torbox #########################
def connect_tb(conn, setting):
    try:
        # Update settings database
        tb_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        tb_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(tb_enable, setting)
        cur.execute(tb_token, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Databit_db TorBox Failed!' % var.amgr, xbmc.LOGINFO)

######################### Easy Debrid #########################
def connect_ed(conn, setting):
    try:
        # Update settings database
        ed_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        ed_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(ed_enable, setting)
        cur.execute(ed_token, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Databit_db Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)

######################### Offcloud #########################
def connect_oc(conn, setting):
    try:
        # Update settings database
        oc_enable = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        oc_token = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(oc_enable, setting)
        cur.execute(oc_token, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Databit_db Offcloud Failed!' % var.amgr, xbmc.LOGINFO)
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
        xbmc.log('%s: Databit_db Easynews Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Fen Light Metadata #########################
def connect_meta_fenlt(conn, setting):
    try:
        # Update settings database
        omdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''
        tmdb_api = ''' UPDATE settings
                  SET setting_value = ?
                  WHERE setting_id = ?'''

        cur = conn.cursor()
        cur.execute(omdb_api, setting)
        cur.execute(tmdb_api, setting)
        conn.commit()
        cur.close()
    except:
        xbmc.log('%s: Databit_db Fen Light Metadata Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
'''######################### Affenity Metadata #########################
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
        xbmc.log('%s: Databit_db Affenity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
        pass'''

    
######################### External Providers #########################
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


########################################################################
########################################################################
############################ Fen Light RD ##############################
    
######################### Restore Fen Light RD #########################
def restore_fenlt_rd():
    try:
        conn_p = create_conn(var.rd_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.enabled',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'rd.enabled',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'rd.token',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.account_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'rd.account_id',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.client_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'rd.client_id',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.refresh',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'rd.refresh',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.secret',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'rd.secret',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke Fen Light RD #########################
def revoke_fenlt_rd():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_rd(conn, ('empty_setting', 'rd.enabled'))
            connect_rd(conn, ('empty_setting', 'rd.token'))
            connect_rd(conn, ('empty_setting', 'rd.account_id'))
            connect_rd(conn, ('empty_setting', 'rd.client_id'))
            connect_rd(conn, ('empty_setting', 'rd.refresh'))
            connect_rd(conn, ('empty_setting', 'rd.secret'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Backup Fen Light RD #########################
def backup_fenlt_rd():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.rd_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.rd_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light RD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete Fen Light RD Backup #####################
#def delete_fenlt_rd():
#    if os.path.exists(os.path.join(var.rd_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.rd_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light RD Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



########################################################################
########################################################################
############################ Fen Light PM ##############################

######################### Restore Fen Light PM #########################
def restore_fenlt_pm():
    try:
        conn_p = create_conn(var.pm_backup_affen)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.enabled',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'pm.enabled',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'pm.token',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.account_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'pm.account_id',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke Fen Light PM #########################
def revoke_fenlt_pm():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_pm(conn, ('empty_setting', 'pm.enabled'))
            connect_pm(conn, ('empty_setting', 'pm.token'))
            connect_pm(conn, ('empty_setting', 'pm.account_id'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Backup Fen Light PM #########################
def backup_fenlt_pm():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.pm_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.pm_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light PM Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete Fen Light PM Backup #####################
#def delete_fenlt_pm():
#    if os.path.exists(os.path.join(var.pm_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.pm_backup_fenlt))
#        except OSError:
#           xbmc.log('%s: Databit_db Delete Fen Light PM Failed!' % var.amgr, xbmc.LOGINFO)
#           pass

######################### Restore Fen Light AD #########################
def restore_fenlt_ad():
    try:
        conn_p = create_conn(var.ad_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ad.enabled',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'ad.enabled',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ad.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'ad.token',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ad.account_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'ad.account_id',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke Fen Light AD #########################
def revoke_fenlt_ad():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_ad(conn, ('empty_setting', 'ad.enabled'))
            connect_ad(conn, ('empty_setting', 'ad.token'))
            connect_ad(conn, ('empty_setting', 'ad.account_id'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Backup Fen Light AD #########################
def backup_fenlt_ad():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.ad_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.ad_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light AD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete Fen Light AD Backup #####################
#def delete_fenlt_ad():
#    if os.path.exists(os.path.join(var.ad_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.ad_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light AD Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



'''#######################################################################
#######################################################################
############################# AfFENity RD #############################

######################### Restore afFENity RD #########################
def restore_affen_rd():
    try:
        conn_p = create_conn(var.rd_backup_affen)
        conn_t = create_conn(var.affen_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('rd.enabled',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'rd.enabled',))

        conn_t.commit()
        
        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('rd.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'rd.token',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('rd.account_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'rd.account_id',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('rd.client_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'rd.client_id',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('rd.refresh',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'rd.refresh',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('rd.secret',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'rd.secret',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore afFENity RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke afFENity RD #########################
def revoke_affen_rd():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_rd(conn, ('empty_setting', 'rd.enabled'))
            connect_rd(conn, ('empty_setting', 'rd.token'))
            connect_rd(conn, ('empty_setting', 'rd.account_id'))
            connect_rd(conn, ('empty_setting', 'rd.client_id'))
            connect_rd(conn, ('empty_setting', 'rd.refresh'))
            connect_rd(conn, ('empty_setting', 'rd.secret'))
    except:
        xbmc.log('%s: Databit_db Revoke afFENity RD Failed!' % var.amgr, xbmc.LOGINFO)
        pass

######################### Backup afFENity RD #########################
def backup_affen_rd():
    if os.path.exists(os.path.join(var.affen_settings_db)) and os.path.exists(os.path.join(var.rd_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.affen_settings_db), os.path.join(var.rd_backup_affen))
        except:
            xbmc.log('%s: Databit_db Backup afFENity RD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete afFENity RD Backup #####################
#def delete_affen_rd():
#    if os.path.exists(os.path.join(var.rd_backup_affen)):
#        try:
#            os.unlink(os.path.join(var.rd_backup_affen))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete afFENity RD Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



#######################################################################
#######################################################################
############################# AfFENity PM #############################
  
######################### Restore afFENity PM #########################
def restore_affen_pm():
    try:
        conn_p = create_conn(var.pm_backup_affen)
        conn_t = create_conn(var.affen_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('pm.enabled',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'pm.enabled',))

        conn_t.commit()
        
        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('pm.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'pm.token',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('pm.account_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'pm.account_id',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore afFENity PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke afFENity PM #########################
def revoke_affen_pm():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_pm(conn, ('empty_setting', 'pm.enabled'))
            connect_pm(conn, ('empty_setting', 'pm.token'))
            connect_pm(conn, ('empty_setting', 'pm.account_id'))
    except:
        xbmc.log('%s: Databit_db Revoke afFENity PM Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Backup afFENity PM #########################
def backup_affen_pm():
    if os.path.exists(os.path.join(var.affen_settings_db)) and os.path.exists(os.path.join(var.pm_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.affen_settings_db), os.path.join(var.pm_backup_affen))
        except:
            xbmc.log('%s: Databit_db Backup afFENity PM Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete afFENity PM Backup #####################
#def delete_affen_pm():
#    if os.path.exists(os.path.join(var.pm_backup_affen)):
#        try:
#            os.unlink(os.path.join(var.pm_backup_affen))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete afFENity PM Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



#######################################################################
#######################################################################
############################## AfFENity AD ############################

######################### Restore afFENity AD #########################
def restore_affen_ad():
    try:
        conn_p = create_conn(var.ad_backup_affen)
        conn_t = create_conn(var.affen_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('ad.enabled',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'ad.enabled',))

        conn_t.commit()
        
        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('ad.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'ad.token',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('ad.account_id',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'ad.account_id',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore afFENity AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke afFENity AD #########################
def revoke_affen_ad():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_ad(conn, ('empty_setting', 'ad.enabled'))
            connect_ad(conn, ('empty_setting', 'ad.token'))
            connect_ad(conn, ('empty_setting', 'ad.account_id'))
    except:
        xbmc.log('%s: Databit_db Revoke afFENity AD Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Backup afFENity AD #########################
def backup_affen_ad():
    if os.path.exists(os.path.join(var.affen_settings_db)) and os.path.exists(os.path.join(var.ad_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.affen_settings_db), os.path.join(var.ad_backup_affen))
        except:
            xbmc.log('%s: Databit_db Backup afFENity AD Failed!' % var.amgr, xbmc.LOGINFO)
            pass

##################### Delete afFENity AD Backup #####################
#def delete_affen_ad():
#    if os.path.exists(os.path.join(var.ad_backup_affen)):
#        try:
#            os.unlink(os.path.join(var.ad_backup_affen))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete afFENity AD Failed!' % var.amgr, xbmc.LOGINFO)
#            pass'''


    
##########################################################################
##########################################################################
############################# Fen Light Trakt ############################
    
######################### Restore Fen Light Trakt #########################
        
def restore_fenlt_trakt():
    try:
        conn_p = create_conn(var.trakt_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.client',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'trakt.client',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.secret',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'trakt.secret',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'trakt.token',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.user',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'trakt.user',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.refresh',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'trakt.refresh',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.expires',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'trakt.expires',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('watched_indicators',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'watched_indicators',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('watched_indicators_name',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'watched_indicators_name',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light Trakt Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
#Revoke Trakt
def revoke_fenlt_trakt():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_trakt_fenlt(conn, (var.fenlt_client, 'trakt.client'))
            connect_trakt_fenlt(conn, (var.fenlt_secret, 'trakt.secret'))
            connect_trakt_fenlt(conn, ('empty_setting', 'trakt.token'))
            connect_trakt_fenlt(conn, ('empty_setting', 'trakt.user'))
            connect_trakt_fenlt(conn, ('empty_setting', 'trakt.refresh'))
            connect_trakt_fenlt(conn, ('empty_setting', 'trakt.expires'))
            connect_trakt_fenlt(conn, (0, 'watched_indicators'))
            connect_trakt_fenlt(conn, ('Fen Light', 'watched_indicators_name'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light Trakt Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
#Backup Trakt
def backup_fenlt_trakt():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.trakt_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.trakt_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light Trakt Failed!' % var.amgr, xbmc.LOGINFO)
            pass

#Delete Trakt Backup
#def delete_fenlt_trakt():
#    if os.path.exists(os.path.join(var.trakt_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.trakt_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light Trakt Failed!' % var.amgr, xbmc.LOGINFO)
#            pass
        


'''##########################################################################
##########################################################################
############################# afFENity Trakt #############################
    
######################### Restore afFENity Trakt #########################
        
def restore_affen_trakt():
    try:
        conn_p = create_conn(var.trakt_backup_affen)
        conn_t = create_conn(var.affen_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('trakt.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'trakt.token',))

        conn_t.commit()
        
        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('trakt.user',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'trakt.user',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('trakt.refresh',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'trakt.refresh',))

        conn_t.commit()
        
        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('trakt.expires',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'trakt.expires',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('watched_indicators',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'watched_indicators',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('watched_indicators_name',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'watched_indicators_name',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore afFENity Trakt Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
#Revoke Trakt
def revoke_affen_trakt():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_trakt_affen(conn, ('empty_setting', 'trakt.token'))
            connect_trakt_affen(conn, ('empty_setting', 'trakt.user'))
            connect_trakt_affen(conn, ('empty_setting', 'trakt.refresh'))
            connect_trakt_affen(conn, ('empty_setting', 'trakt.expires'))
            connect_trakt_affen(conn, (0, 'watched_indicators'))
            connect_trakt_affen(conn, ('afFENity', 'watched_indicators_name'))
    except:
        xbmc.log('%s: Databit_db Revoke afFENity Trakt Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
#Backup Trakt
def backup_affen_trakt():
    if os.path.exists(os.path.join(var.affen_settings_db)) and os.path.exists(os.path.join(var.trakt_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.affen_settings_db), os.path.join(var.trakt_backup_affen))
        except:
            xbmc.log('%s: Databit_db Backup afFENity Trakt Failed!' % var.amgr, xbmc.LOGINFO)
            pass

#Delete Trakt Backup
#def delete_affen_trakt():
#    if os.path.exists(os.path.join(var.trakt_backup_affen)):
#        try:
#            os.unlink(os.path.join(var.trakt_backup_affen))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete afFENity Trakt Failed!' % var.amgr, xbmc.LOGINFO)
#            pass'''



##########################################################################
##########################################################################
########################### Fen Light TorBox ###########################
    
############################ Restore TorBox ############################
def restore_fenlt_tb():
    try:
        conn_p = create_conn(var.tb_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('tb.enable',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'tb.enable',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('tb.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'tb.token',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light TorBox Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke TorBox ############################
def revoke_fenlt_tb():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_tb(conn, ('false', 'tb.enabled'))
            connect_tb(conn, ('empty_setting', 'tb.token'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light TorBox Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup TorBox ############################
def backup_fenlt_tb():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.tb_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.tb_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light TorBox Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete TorBox Backup ############################
#def delete_fenlt_tb():
#    if os.path.exists(os.path.join(var.tb_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.tb_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light TorBox Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



#############################################################################
#############################################################################
########################### Fen Light Easy Debrid ###########################
    
############################ Restore Easy Debrid ############################
def restore_fenlt_ed():
    try:
        conn_p = create_conn(var.ed_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ed.enable',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'ed.enable',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ed.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'ed.token',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke Easy Debrid ############################
def revoke_fenlt_ed():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_ed(conn, ('false', 'ed.enabled'))
            connect_ed(conn, ('empty_setting', 'ed.token'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup Easy Debrid ############################
def backup_fenlt_ed():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.ed_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.ed_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete Easy Debrid ############################
#def delete_fenlt_ed():
#    if os.path.exists(os.path.join(var.ed_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.ed_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light Easy Debrid Failed!' % var.amgr, xbmc.LOGINFO)
#            pass


##########################################################################
##########################################################################
########################### Fen Light Offcloud ###########################
    
############################ Restore Offcloud ############################
def restore_fenlt_oc():
    try:
        conn_p = create_conn(var.offc_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('oc.enable',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'oc.enable',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('oc.token',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'oc.token',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light Offcloud Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke Offcloud ############################
def revoke_fenlt_oc():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_oc(conn, ('false', 'oc.enabled'))
            connect_oc(conn, ('empty_setting', 'oc.token'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light Offcloud Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup Offcloud ############################
def backup_fenlt_oc():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.offc_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.offc_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light Offcloud Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete Offcloud Backup ############################
#def delete_fenlt_oc():
#    if os.path.exists(os.path.join(var.offc_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.offc_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light Offcloud Failed!' % var.amgr, xbmc.LOGINFO)
#            pass




##########################################################################
##########################################################################
########################### Fen Light Easynews ###########################
    
############################ Restore Easynews ############################
def restore_fenlt_easy():
    try:
        conn_p = create_conn(var.easy_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('provider.easynews',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'provider.easynews',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('easynews_user',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'easynews_user',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('easynews_password',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'easynews_password',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light Easynews Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke Easynews ############################
def revoke_fenlt_easy():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_easy(conn, ('false', 'provider.easynews'))
            connect_easy(conn, ('empty_setting', 'easynews_user'))
            connect_easy(conn, ('empty_setting', 'easynews_password'))
    except:
        xbmc.log('%s: Databit_db Revoke Fen Light Easynews Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup Easynews ############################
def backup_fenlt_easy():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.easy_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.easy_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light Easynews Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete Easynews Backup ############################
#def delete_fenlt_easy():
#    if os.path.exists(os.path.join(var.easy_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.easy_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light Easynews Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



'''##########################################################################
##########################################################################
########################### afFENity Easynews ############################
    
############################ Restore Easynews ############################
def restore_affen_easy():
    try:
        conn_p = create_conn(var.easy_backup_affen)
        conn_t = create_conn(var.affen_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('provider.easynews',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'provider.easynews',))

        conn_t.commit()
        
        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('easynews_user',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'easynews_user',))

        conn_t.commit()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('easynews_password',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'easynews_password',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore afFENity Easynews Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke Easynews ############################
def revoke_affen_easy():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_easy(conn, ('empty_setting', 'provider.easynews'))
            connect_easy(conn, ('empty_setting', 'easynews_user'))
            connect_easy(conn, ('empty_setting', 'easynews_password'))
    except:
        xbmc.log('%s: Databit_db Revoke afFENity Easynews Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup Easynews ############################
def backup_affen_easy():
    if os.path.exists(os.path.join(var.affen_settings_db)) and os.path.exists(os.path.join(var.easy_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.affen_settings_db), os.path.join(var.easy_backup_affen))
        except:
            xbmc.log('%s: Databit_db Backup afFENity Easynews Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete Easynews Backup ############################
#def delete_affen_easy():
#    if os.path.exists(os.path.join(var.easy_backup_affen)):
#        try:
#            os.unlink(os.path.join(var.easy_backup_affen))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete afFENity Easynews Failed!' % var.amgr, xbmc.LOGINFO)
#            pass'''



        

##########################################################################
##########################################################################
########################### Fen Light Metadata ############################
    
############################ Restore Metadata ############################
def restore_fenlt_meta():
    try:
        conn_p = create_conn(var.meta_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('omdb_api',))
        data_omdb = cur_p.fetchone()
        data_set_omdb = str(data_omdb)
        
        for char in char_remov:
            data_set_omdb = data_set_omdb.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set_omdb, 'omdb_api',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('tmdb_api',))
        data_tmdb = cur_p.fetchone()
        data_set_tmdb = str(data_tmdb)

        for char in char_remov:
            data_set_tmdb = data_set_tmdb.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set_tmdb, 'tmdb_api',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Metadata Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke Metadata ############################
def revoke_fenlt_meta():
    try:
        # Create database connection
        conn = create_conn(var.fenlt_settings_db)
        with conn:
            connect_meta_fenlt(conn, ('empty_setting', 'omdb_api'))
            connect_meta_fenlt(conn, (var.fenlt_tmdb, 'tmdb_api'))
    except:
        xbmc.log('%s: Databit_db Revoke Metadata Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup Metadata ############################
def backup_fenlt_meta():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.meta_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.meta_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Metadata Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete Metadata ############################
#def delete_fenlt_meta():
#    if os.path.exists(os.path.join(var.meta_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.meta_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Metadata Failed!' % var.amgr, xbmc.LOGINFO)
#            pass



'''##########################################################################
##########################################################################
########################### afFENity Metadata ############################
    
############################ Restore Metadata ############################
def restore_affen_meta():
    try:
        conn_p = create_conn(var.meta_backup_affen)
        conn_t = create_conn(var.affen_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('omdb_api',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute(''''''UPDATE settings SET setting_value = ? WHERE setting_id = ?'''''', (data_set, 'omdb_api',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore afFENity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Revoke Metadata ############################
def revoke_affen_meta():
    try:
        # Create database connection
        conn = create_conn(var.affen_settings_db)
        with conn:
            connect_meta(conn, ('empty_setting', 'omdb_api'))
    except:
        xbmc.log('%s: Databit_db Revoke afFENity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
############################ Backup Metadata ############################
def backup_affen_meta():
    if os.path.exists(os.path.join(var.affen_settings_db)) and os.path.exists(os.path.join(var.meta_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.affen_settings_db), os.path.join(var.meta_backup_affen))
        except:
            xbmc.log('%s: Databit_db Backup afFENity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete Metadata ############################
#def delete_affen_meta():
#    if os.path.exists(os.path.join(var.meta_backup_affen)):
#        try:
#            os.unlink(os.path.join(var.meta_backup_affen))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete afFENity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
#            pass'''



#######################################################################################
#######################################################################################
########################### Fen Light External Providers ##############################
    
############################ Restore External Providers ###############################
def restore_fenlt_ext():
    try:
        conn_p = create_conn(var.ext_backup_fenlt)
        conn_t = create_conn(var.fenlt_settings_db)

        cur_p = conn_p.cursor()
        cur_t = conn_t.cursor()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('provider.external',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'provider.external',))

        conn_t.commit()
        
        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('external_scraper.name',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'external_scraper.name',))

        conn_t.commit()

        cur_p.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('external_scraper.module',))
        data = cur_p.fetchone()
        data_set = str(data)
        
        for char in char_remov:
            data_set = data_set.replace(char, "")
            cur_t.execute('''UPDATE settings SET setting_value = ? WHERE setting_id = ?''', (data_set, 'external_scraper.module',))

        conn_t.commit()
        cur_t.close()
        cur_p.close()
    except:
        xbmc.log('%s: Databit_db Restore Fen Light Ext Providers Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
######################### Revoke Fen Light External Provider ###########################
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
    
############################ Backup External Providers ##################################
def backup_fenlt_ext():
    if os.path.exists(os.path.join(var.fenlt_settings_db)) and os.path.exists(os.path.join(var.ext_backup)):
        try:
            xbmcvfs.copy(os.path.join(var.fenlt_settings_db), os.path.join(var.ext_backup_fenlt))
        except:
            xbmc.log('%s: Databit_db Backup Fen Light Ext Providers Failed!' % var.amgr, xbmc.LOGINFO)
            pass

############################ Delete External Providers Backup ############################
#def delete_fenlt_ext():
#    if os.path.exists(os.path.join(var.ext_backup_fenlt)):
#        try:
#            os.unlink(os.path.join(var.ext_backup_fenlt))
#        except OSError:
#            xbmc.log('%s: Databit_db Delete Fen Light Ext Providers Failed!' % var.amgr, xbmc.LOGINFO)
#            pass

