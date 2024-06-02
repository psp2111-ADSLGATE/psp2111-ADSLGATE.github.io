import xbmc, xbmcaddon
import xbmcvfs
import os

from pathlib import Path
from accountmgr.modules import control
from libs.common import var

char_remov = ["'", ",", ")","("]

#Account Manager Premiumize
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_pm_username = accountmgr.getSetting("premiumize.username")
your_pm_token = accountmgr.getSetting("premiumize.token")

class Auth:
    def premiumize_auth(self):
    #Seren PM
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists
                        
                        #Get add-on setting to compare
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("premiumize.token")
                        chk_auth_seren_rd = xbmcaddon.Addon('plugin.video.seren').getSetting("rd.auth")
                        chk_auth_seren_ad = xbmcaddon.Addon('plugin.video.seren').getSetting("alldebrid.apikey")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match authorization is skipped
                                
                                #Write data to settings.xml
                                addon = xbmcaddon.Addon("plugin.video.seren")
                                addon.setSetting("premiumize.username", your_pm_username)
                                addon.setSetting("premiumize.token", your_pm_token)

                                premium_stat = ("Premium")
                                addon.setSetting("premiumize.premiumstatus", premium_stat)
                                
                                #Enable authorized debrid services
                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enabled", enabled_pm)

                                if str(chk_auth_seren_rd) != '': #Check if Real-Debrid is authorized
                                        enabled_rd = ("true")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_seren_ad) != '': #Check if Premiumize is authorized
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enabled", enabled_ad)
        except:
                xbmc.log('%s: Seren Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Fen PM
        try:
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                        chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("pm.token")
                        chk_auth_fen_rd = xbmcaddon.Addon('plugin.video.fen').getSetting("rd.token")
                        chk_auth_fen_ad = xbmcaddon.Addon('plugin.video.fen').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_fen) or str(chk_auth_fen) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.fen")
                                addon.setSetting("pm.account_id", your_pm_username)
                                addon.setSetting("pm.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_fen_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_fen_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                xbmc.log('%s: Fen Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass


    #Fen Light PM        
        try:
                if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt):
                        
                        from accountmgr.modules import debrid_db
                        conn = debrid_db.create_conn(var.fenlt_settings_db)
                        
                        with conn:
                            cursor = conn.cursor()
                            cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.token',))
                            auth_pm = cursor.fetchone()
                            chk_auth_fenlt = str(auth_pm)

                            cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.token',))
                            auth_rd = cursor.fetchone()
                            chk_auth_fenlt_rd = str(auth_pm)

                            cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ad.token',))
                            auth_ad = cursor.fetchone()
                            chk_auth_fenlt_ad = str(auth_ad)
                            
                            for char in char_remov:
                                chk_auth_fenlt = chk_auth_fenlt.replace(char, "")
                                
                            if not str(var.chk_accountmgr_tk_pm) == chk_auth_fenlt:
                                
                                from accountmgr.modules import debrid_db
                                debrid_db.auth_fenlt_pm()
                                
                                for char in char_remov:
                                    chk_auth_fenlt_rd = chk_auth_fenlt_rd.replace(char, "")
                                
                                if chk_auth_fenlt_rd != 'empty_setting' or chk_auth_fenlt_rd != '' or chk_auth_fenlt_rd != None:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.enable_fenlt_rd()
                                else:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.disable_fenlt_rd()
                                    
                                for char in char_remov:
                                    chk_auth_fenlt_ad = chk_auth_fenlt_ad.replace(char, "")

                                if chk_auth_fenlt_ad != 'empty_setting' or chk_auth_fenlt_ad != '' or chk_auth_fenlt_ad != None:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.enable_fenlt_ad()
                                else:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.disable_fenlt_ad()
                            cursor.close()
        except:
                xbmc.log('%s: Fen Light Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #afFENity PM        
        try:
                if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen): #Check that the addon is installed and settings.db exists
                        
                        #Create database connection
                        from accountmgr.modules import debrid_db
                        conn = debrid_db.create_conn(var.affen_settings_db)
                        
                        #Get add-on settings to compare
                        with conn:
                            cursor = conn.cursor()
                            cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.token',))
                            auth_pm = cursor.fetchone()
                            chk_auth_affen = str(auth_pm)

                            cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('rd.token',))
                            auth_rd = cursor.fetchone()
                            chk_auth_affen_rd = str(auth_pm)

                            cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ad.token',))
                            auth_ad = cursor.fetchone()
                            chk_auth_affen_ad = str(auth_ad)
                            
                            #Clean up database results
                            for char in char_remov:
                                chk_auth_affen = chk_auth_affen.replace(char, "")
                                
                            if not str(var.chk_accountmgr_tk_pm) == chk_auth_affen: #Compare Account Mananger token to Add-on token. If they match, authorization is skipped
                                
                                #Write settings to database
                                from accountmgr.modules import debrid_db
                                debrid_db.auth_affen_pm()
                                
                                #Enable authorized debrid services
                                for char in char_remov:
                                    chk_auth_affen_rd = chk_auth_affen_rd.replace(char, "")
                                
                                if chk_auth_affen_rd != 'empty_setting' or chk_auth_affen_rd != '' or chk_auth_affen_rd != None:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.enable_affen_rd()
                                else:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.disable_affen_rd()
                                    
                                for char in char_remov:
                                    chk_auth_affen_ad = chk_auth_affen_ad.replace(char, "")

                                if chk_auth_affen_ad != 'empty_setting' or chk_auth_affen_ad != '' or chk_auth_affen_ad != None:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.enable_affen_ad()
                                else:
                                    from accountmgr.modules import debrid_db
                                    debrid_db.disable_affen_ad()
                            cursor.close()
        except:
                xbmc.log('%s: afFENity Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Ezra PM
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("pm.token")
                        chk_auth_ezra_rd = xbmcaddon.Addon('plugin.video.ezra').getSetting("rd.token")
                        chk_auth_ezra_ad = xbmcaddon.Addon('plugin.video.ezra').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':

                                addon = xbmcaddon.Addon("plugin.video.ezra")
                                addon.setSetting("pm.account_id", your_pm_username)
                                addon.setSetting("pm.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_ezra_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_ezra_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                xbmc.log('%s: Ezra Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Coalition PM
        try:
                if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):
                        chk_auth_coal = xbmcaddon.Addon('plugin.video.coalition').getSetting("pm.token")
                        chk_auth_coal_rd = xbmcaddon.Addon('plugin.video.coalition').getSetting("rd.token")
                        chk_auth_coal_ad = xbmcaddon.Addon('plugin.video.coalition').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_coal) or str(chk_auth_coal) == '':

                                addon = xbmcaddon.Addon("plugin.video.coalition")
                                addon.setSetting("pm.account_id", your_pm_username)
                                addon.setSetting("pm.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_coal_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_coal_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                xbmc.log('%s: Coalition Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #POV PM
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("pm.token")
                        chk_auth_pov_rd = xbmcaddon.Addon('plugin.video.pov').getSetting("rd.token")
                        chk_auth_pov_ad = xbmcaddon.Addon('plugin.video.pov').getSetting("ad.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_pov) or str(chk_auth_pov) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("pm.account_id", your_pm_username)
                                addon.setSetting("pm.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)

                                if str(chk_auth_pov_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)

                                if str(chk_auth_pov_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("ad.enabled", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("ad.enabled", enabled_ad)
        except:
                xbmc.log('%s: POV Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass                

    #Umbrella PM
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("premiumizetoken")
                        chk_auth_umb_rd = xbmcaddon.Addon('plugin.video.umbrella').getSetting("realdebridtoken")
                        chk_auth_umb_ad = xbmcaddon.Addon('plugin.video.umbrella').getSetting("alldebridtoken")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_umb) or str(chk_auth_umb) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("premiumizeusername", your_pm_username)
                                addon.setSetting("premiumizetoken", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enable", enabled_pm)

                                if str(chk_auth_umb_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("alldebrid.enable", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enable", enabled_rd)

                                if str(chk_auth_umb_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enable", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enable", enabled_ad)
        except:
                xbmc.log('%s: Umbrella Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #OneMoar PM
        try:
                if xbmcvfs.exists(var.chk_onem) and xbmcvfs.exists(var.chkset_onem):
                        chk_auth_onem = xbmcaddon.Addon('plugin.video.onemoar').getSetting("premiumizetoken")
                        chk_auth_onem_rd = xbmcaddon.Addon('plugin.video.onemoar').getSetting("realdebridtoken")
                        chk_auth_onem_ad = xbmcaddon.Addon('plugin.video.onemoar').getSetting("alldebridtoken")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_onem) or str(chk_auth_onem) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.onemoar")
                                addon.setSetting("premiumizeusername", your_pm_username)
                                addon.setSetting("premiumizetoken", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enable", enabled_pm)

                                if str(chk_auth_onem_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("alldebrid.enable", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enable", enabled_rd)

                                if str(chk_auth_onem_ad) != '':
                                        enabled_ad = ("true")
                                        addon.setSetting("alldebrid.enable", enabled_ad)
                                else:
                                        enabled_ad = ("false")
                                        addon.setSetting("alldebrid.enable", enabled_ad)
        except:
                xbmc.log('%s: OneMoar Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
     #Dradis PM
        try:
                if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):
                        chk_auth_dradis = xbmcaddon.Addon('plugin.video.dradis').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_dradis) or str(chk_auth_dradis) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.dradis")
                                addon.setSetting("premiumize.username", your_pm_username)
                                addon.setSetting("premiumize.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enable", enabled_pm)
        except:
                xbmc.log('%s: Dradis Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

     #Taz19 PM
        try:
                if xbmcvfs.exists(var.chk_taz) and xbmcvfs.exists(var.chkset_taz):
                        chk_auth_taz = xbmcaddon.Addon('plugin.video.taz19').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_taz) or str(chk_auth_taz) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.taz19")
                                addon.setSetting("pm.account_id", your_pm_username)
                                addon.setSetting("pm.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("pm.enabled", enabled_pm)
        except:
                xbmc.log('%s: Taz Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Shadow PM
        try:
                if xbmcvfs.exists(var.chk_shadow) and not xbmcvfs.exists(var.shadow_ud):
                        os.mkdir(var.shadow_ud)
                        xbmcvfs.copy(os.path.join(var.shadow), os.path.join(var.chkset_shadow))
                        
                if xbmcvfs.exists(var.chk_shadow) and not xbmcvfs.exists(var.chkset_shadow):
                        xbmcvfs.copy(os.path.join(var.shadow), os.path.join(var.chkset_shadow))

                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("premiumize.token")
                        chk_auth_shadow_rd = xbmcaddon.Addon('plugin.video.shadow').getSetting("rd.auth")
                        chk_auth_shadow_ad = xbmcaddon.Addon('plugin.video.shadow').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':

                                addon = xbmcaddon.Addon("plugin.video.shadow")
                                addon.setSetting("premiumize.token", your_pm_token)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                if str(chk_auth_shadow_rd) != '':
                                        rd_use = ("true")
                                        addon.setSetting("debrid_use_rd", rd_use)
                                else:
                                        rd_use = ("false")
                                        addon.setSetting("debrid_use_rd", rd_use)
                        
                                if str(chk_auth_shadow_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                xbmc.log('%s: Shadow Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Ghost PM
        try:
                if xbmcvfs.exists(var.chk_ghost) and not xbmcvfs.exists(var.ghost_ud):
                        os.mkdir(var.ghost_ud)
                        xbmcvfs.copy(os.path.join(var.ghost), os.path.join(var.chkset_ghost))
                        
                if xbmcvfs.exists(var.chk_ghost) and not xbmcvfs.exists(var.chkset_ghost):
                        xbmcvfs.copy(os.path.join(var.ghost), os.path.join(var.chkset_ghost))

                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.ghost")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Ghost Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Base PM
        try:
                if xbmcvfs.exists(var.chk_base) and not xbmcvfs.exists(var.base_ud):
                        os.mkdir(var.base_ud)
                        xbmcvfs.copy(os.path.join(var.base), os.path.join(var.chkset_base))
                        
                if xbmcvfs.exists(var.chk_base) and not xbmcvfs.exists(var.chkset_base):
                        xbmcvfs.copy(os.path.join(var.base), os.path.join(var.chkset_base))

                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base):
                        chk_auth_base = xbmcaddon.Addon('plugin.video.base').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_base) or str(chk_auth_base) == '':
                        
                                addon = xbmcaddon.Addon("plugin.video.base")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Base Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Unleashed PM
        try:
                if xbmcvfs.exists(var.chk_unleashed) and not xbmcvfs.exists(var.unleashed_ud):
                        os.mkdir(var.unleashed_ud)
                        xbmcvfs.copy(os.path.join(var.unleashed), os.path.join(var.chkset_unleashed))
                        
                if xbmcvfs.exists(var.chk_unleashed) and not xbmcvfs.exists(var.chkset_unleashed):
                        xbmcvfs.copy(os.path.join(var.unleashed), os.path.join(var.chkset_unleashed))

                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.unleashed")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Unleashed Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Chains PM
        try:
                if xbmcvfs.exists(var.chk_chains) and not xbmcvfs.exists(var.chains_ud):
                        os.mkdir(var.chains_ud)
                        xbmcvfs.copy(os.path.join(var.chains), os.path.join(var.chkset_chains))
                        
                if xbmcvfs.exists(var.chk_chains) and not xbmcvfs.exists(var.chkset_chains):
                        xbmcvfs.copy(os.path.join(var.chains), os.path.join(var.chkset_chains))

                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_chains = xbmcaddon.Addon('plugin.video.thechains').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_chains) or str(chk_auth_chains) == '':

                                addon = xbmcaddon.Addon("plugin.video.thechains")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Chains Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Twisted PM
        try:
                if xbmcvfs.exists(var.chk_twisted) and not xbmcvfs.exists(var.twisted_ud):
                        os.mkdir(var.twisted_ud)
                        xbmcvfs.copy(os.path.join(var.twisted), os.path.join(var.chkset_twisted))
                        
                if xbmcvfs.exists(var.chk_twisted) and not xbmcvfs.exists(var.chkset_twisted):
                        xbmcvfs.copy(os.path.join(var.twisted), os.path.join(var.chkset_twisted))

                if xbmcvfs.exists(var.chk_twisted) and xbmcvfs.exists(var.chkset_twisted):
                        chk_auth_twisted = xbmcaddon.Addon('plugin.video.twisted').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_twisted) or str(chk_auth_twisted) == '':
                        
                                addon = xbmcaddon.Addon("plugin.video.twisted")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Twisted Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Magic Dragon PM
        try:
                if xbmcvfs.exists(var.chk_md) and not xbmcvfs.exists(var.md_ud):
                        os.mkdir(var.md_ud)
                        xbmcvfs.copy(os.path.join(var.md), os.path.join(var.chkset_md))
                        
                if xbmcvfs.exists(var.chk_md) and not xbmcvfs.exists(var.chkset_md):
                        xbmcvfs.copy(os.path.join(var.md), os.path.join(var.chkset_md))

                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_md) or str(chk_auth_md) == '':
                        
                                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Magic Dragon Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Asgard PM
        try:
                if xbmcvfs.exists(var.chk_asgard) and not xbmcvfs.exists(var.asgard_ud):
                        os.mkdir(var.asgard_ud)
                        xbmcvfs.copy(os.path.join(var.asgard), os.path.join(var.chkset_asgard))
                        
                if xbmcvfs.exists(var.chk_asgard) and not xbmcvfs.exists(var.chkset_asgard):
                        xbmcvfs.copy(os.path.join(var.asgard), os.path.join(var.chkset_asgard))

                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                        
                                addon = xbmcaddon.Addon("plugin.video.asgard")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Asgard Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Patriot PM
        try:
                if xbmcvfs.exists(var.chk_patriot) and not xbmcvfs.exists(var.patriot_ud):
                        os.mkdir(var.patriot_ud)
                        xbmcvfs.copy(os.path.join(var.patriot), os.path.join(var.chkset_patriot))
                        
                if xbmcvfs.exists(var.chk_patriot) and not xbmcvfs.exists(var.chkset_patriot):
                        xbmcvfs.copy(os.path.join(var.patriot), os.path.join(var.chkset_patriot))

                if xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot):
                        chk_auth_patriot = xbmcaddon.Addon('plugin.video.patriot').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_patriot) or str(chk_auth_patriot) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.patriot")
                                addon.setSetting("premiumize.token", your_pm_token)

                                rd_use = ("false")
                                addon.setSetting("debrid_use_rd", rd_use)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                ad_use = ("false")
                                addon.setSetting("debrid_use_ad", ad_use)

                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: Patriot Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Black Lightning PM
        try:
                if xbmcvfs.exists(var.chk_blackl) and not xbmcvfs.exists(var.blackl_ud):
                        os.mkdir(var.blackl_ud)
                        xbmcvfs.copy(os.path.join(var.blackl), os.path.join(var.chkset_blackl))
                        
                if xbmcvfs.exists(var.chk_blackl) and not xbmcvfs.exists(var.chkset_blackl):
                        xbmcvfs.copy(os.path.join(var.blackl), os.path.join(var.chkset_blackl))

                if xbmcvfs.exists(var.chk_blackl) and xbmcvfs.exists(var.chkset_blackl):
                        chk_auth_blackl = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("premiumize.token")
                        chk_auth_blackl_rd = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("rd.auth")
                        chk_auth_blackl_ad = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_blackl) or str(chk_auth_blackl) == '':

                                addon = xbmcaddon.Addon("plugin.video.blacklightning")
                                addon.setSetting("premiumize.token", your_pm_token)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                if str(chk_auth_blackl_rd) != '':
                                        rd_use = ("true")
                                        addon.setSetting("debrid_use_rd", rd_use)
                                else:
                                        rd_use = ("false")
                                        addon.setSetting("debrid_use_rd", rd_use)
                        
                                if str(chk_auth_blackl_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                xbmc.log('%s: Black Lightning Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #M.E.T.V PM
        try:
                if xbmcvfs.exists(var.chk_metv) and not xbmcvfs.exists(var.metv_ud):
                        os.mkdir(var.metv_ud)
                        xbmcvfs.copy(os.path.join(var.metv), os.path.join(var.chkset_metv))
                        
                if xbmcvfs.exists(var.chk_metv) and not xbmcvfs.exists(var.chkset_metv):
                        xbmcvfs.copy(os.path.join(var.metv), os.path.join(var.chkset_metv))

                if xbmcvfs.exists(var.chk_metv) and xbmcvfs.exists(var.chkset_metv):
                        chk_auth_metv = xbmcaddon.Addon('plugin.video.metv19').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_metv) or str(chk_auth_metv) == '':
                        
                                addon = xbmcaddon.Addon("plugin.video.metv19")
                                addon.setSetting("premiumize.token", your_pm_token)

                                d_use = ("true")
                                addon.setSetting("debrid_use", d_use)
                                
                                d_select = ("1")
                                addon.setSetting("debrid_select", d_select)
        except:
                xbmc.log('%s: METV Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Aliunde PM
        try:
                if xbmcvfs.exists(var.chk_aliunde) and not xbmcvfs.exists(var.aliunde_ud):
                        os.mkdir(var.aliunde_ud)
                        xbmcvfs.copy(os.path.join(var.aliunde), os.path.join(var.chkset_aliunde))
                        
                if xbmcvfs.exists(var.chk_aliunde) and not xbmcvfs.exists(var.chkset_aliunde):
                        xbmcvfs.copy(os.path.join(var.aliunde), os.path.join(var.chkset_aliunde))

                if xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde):
                        chk_auth_aliunde = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("premiumize.token")
                        chk_auth_aliunde_rd = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("rd.auth")
                        chk_auth_aliunde_ad = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_aliunde) or str(chk_auth_aliunde) == '':

                                addon = xbmcaddon.Addon("plugin.video.aliundek19")
                                addon.setSetting("premiumize.token", your_pm_token)

                                pm_use = ("true")
                                addon.setSetting("debrid_use_pm", pm_use)

                                if str(chk_auth_aliunde_rd) != '':
                                        rd_use = ("true")
                                        addon.setSetting("debrid_use_rd", rd_use)
                                else:
                                        rd_use = ("false")
                                        addon.setSetting("debrid_use_rd", rd_use)
                        
                                if str(chk_auth_aliunde_ad) != '':
                                        ad_use = ("true")
                                        addon.setSetting("debrid_use_ad", ad_use)
                                else:
                                        ad_use = ("false")
                                        addon.setSetting("debrid_use_ad", ad_use)
        except:
                xbmc.log('%s: Aliunde Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

     #Otaku PM
        try:
                if xbmcvfs.exists(var.chk_otaku) and not xbmcvfs.exists(var.otaku_ud):
                        os.mkdir(var.otaku_ud)
                        xbmcvfs.copy(os.path.join(var.otaku), os.path.join(var.chkset_otaku))
                        
                if xbmcvfs.exists(var.chk_otaku) and not xbmcvfs.exists(var.chkset_otaku):
                        xbmcvfs.copy(os.path.join(var.otaku), os.path.join(var.chkset_otaku))

                if xbmcvfs.exists(var.chk_otaku) and xbmcvfs.exists(var.chkset_otaku):
                        chk_auth_otaku = xbmcaddon.Addon('plugin.video.otaku').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_otaku) or str(chk_auth_otaku) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.otaku")
                                addon.setSetting("premiumize.username", your_pm_username)
                                addon.setSetting("premiumize.token", your_pm_token)

                                enabled_pm = ("true")
                                addon.setSetting("premiumize.enabled", enabled_pm)
        except:
                xbmc.log('%s: Otaku Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass

     #Premiumizer PM
        try:
                if xbmcvfs.exists(var.chk_premx) and not xbmcvfs.exists(var.premx_ud):
                        os.mkdir(var.premx_ud)
                        xbmcvfs.copy(os.path.join(var.premx), os.path.join(var.chkset_premx))
                        
                if xbmcvfs.exists(var.chk_premx) and not xbmcvfs.exists(var.chkset_premx):
                        xbmcvfs.copy(os.path.join(var.premx), os.path.join(var.chkset_premx))

                if xbmcvfs.exists(var.chk_premx) and xbmcvfs.exists(var.chkset_premx):
                        chk_auth_premx = xbmcaddon.Addon('plugin.video.premiumizerx').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_premx) or str(chk_auth_premx) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.premiumizerx")
                                addon.setSetting("premiumize.status", 'Authorized')
                                addon.setSetting("premiumize.token", your_pm_token)
                                addon.setSetting("premiumize.refresh", '315360000')
        except:
                xbmc.log('%s: Premiumizer Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #All Accounts PM
        try:
                if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.allaccounts_ud):
                        os.mkdir(var.allaccounts_ud)
                        xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                        
                if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.chkset_allaccounts):
                        xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                        
                if xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts):
                        chk_auth_allaccounts = xbmcaddon.Addon('script.module.allaccounts').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_allaccounts) or str(chk_auth_allaccounts) == '':
                        
                                addon = xbmcaddon.Addon("script.module.allaccounts")
                                addon.setSetting("premiumize.username", your_pm_username)
                                addon.setSetting("premiumize.token", your_pm_token)
        except:
                xbmc.log('%s: All Accounts Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #My Accounts PM
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.myaccounts_ud):
                        os.mkdir(var.myaccounts_ud)
                        xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.chkset_myaccounts):
                        xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':
                        
                                addon = xbmcaddon.Addon("script.module.myaccounts")
                                addon.setSetting("premiumize.username", your_pm_username)
                                addon.setSetting("premiumize.token", your_pm_token)
        except:
                xbmc.log('%s: My Accounts Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #ResolveURL PM
        try:
                if xbmcvfs.exists(var.chk_rurl) and not xbmcvfs.exists(var.rurl_ud):
                        os.mkdir(var.rurl_ud)
                        xbmcvfs.copy(os.path.join(var.rurl), os.path.join(var.chkset_rurl))
                        
                if xbmcvfs.exists(var.chk_rurl) and not xbmcvfs.exists(var.chkset_rurl):
                        xbmcvfs.copy(os.path.join(var.rurl), os.path.join(var.chkset_rurl))
                        
                if xbmcvfs.exists(var.chk_rurl) and xbmcvfs.exists(var.chkset_rurl):
                        chk_auth_rurl = xbmcaddon.Addon('script.module.resolveurl').getSetting("PremiumizeMeResolver_token")
                        if not str(var.chk_accountmgr_tk_pm) == str(chk_auth_rurl) or str(chk_auth_rurl) == '':
                        
                                addon = xbmcaddon.Addon("script.module.resolveurl")
                                addon.setSetting("PremiumizeMeResolver_token", your_pm_token)

                                cache_only = ("true")
                                addon.setSetting("PremiumizeMeResolver_cached_only", cache_only)
        except:
                xbmc.log('%s: ResolveURL Premiumize Failed!' % var.amgr, xbmc.LOGINFO)
                pass
