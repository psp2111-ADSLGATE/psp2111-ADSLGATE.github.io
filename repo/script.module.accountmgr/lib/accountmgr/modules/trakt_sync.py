import xbmc, xbmcaddon, xbmcgui
import xbmcvfs
import os

from pathlib import Path
from libs.common import var

char_remov = ["'", ",", ")","("]

#Account Manager Trakt
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_token = accountmgr.getSetting("trakt.token")
your_username = accountmgr.getSetting("trakt.username")           
your_refresh = accountmgr.getSetting("trakt.refresh")
your_expires = accountmgr.getSetting("trakt.expires")

class Auth:
    def trakt_auth(self):
    #Seren
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren) and (var.setting('traktuserkey.enabled') == 'true' or var.setting('devuserkey.enabled') == 'true'): #Check that the addon is installed and settings.xml exists.
                        
                        #Get add-on setting to compare
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("trakt.auth")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match, authorization is skipped
                
                                #Insert Account Mananger API keys
                                with open(var.path_seren,'r') as f:
                                    data = f.read()

                                client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)

                                with open(var.path_seren,'w') as f:
                                    f.write(client)

                                #Write data to settings.xml
                                addon = xbmcaddon.Addon("plugin.video.seren")
                                addon.setSetting("trakt.auth", your_token)
                                addon.setSetting("trakt.username", your_username)
                                addon.setSetting("trakt.refresh", your_refresh)
                                
                                your_expires_float = float(your_expires)
                                your_expires_rnd = int(your_expires_float)
                                your_expires_str = str(your_expires_rnd)
                                addon.setSetting("trakt.expires", your_expires_str)
        except:
                xbmc.log('%s: Seren Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Fen
        try:
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                        chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_fen) or str(chk_auth_fen) == '':
                        
                                    with open(var.path_fen,'r') as f:
                                        data = f.read()

                                    client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)

                                    with open(var.path_fen,'w') as f:
                                        f.write(client) 

                                    addon = xbmcaddon.Addon("plugin.video.fen")
                                    addon.setSetting("trakt.token", your_token)
                                    addon.setSetting("trakt.user", your_username)
                                    addon.setSetting("trakt.refresh", your_refresh)
                                    addon.setSetting("trakt.expires", your_expires)
                                    addon.setSetting("trakt.indicators_active", 'true')
                                    addon.setSetting("watched_indicators", '1')
        except:
                xbmc.log('%s: Fen Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Fen Light
        try:
                if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt): #Check that the addon is installed and settings.db exists
                        
                    #Create database connection
                    from accountmgr.modules import trakt_db
                    conn = trakt_db.create_conn(var.fenlt_settings_db)
                    
                    #Get add-on settings to compare
                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.token',))
                        auth_trakt = cursor.fetchone()
                        chk_auth_fenlt = str(auth_trakt)
                        
                        #Clean up database results
                        for char in char_remov:
                            chk_auth_fenlt = chk_auth_fenlt.replace(char, "")
                            
                        if not str(var.chk_accountmgr_tk) == chk_auth_fenlt: #Compare Account Mananger token to Add-on token. If they match, authorization is skipped
                            
                            #Write settings to database
                            from accountmgr.modules import trakt_db
                            trakt_db.auth_fenlt_trakt()
                            accountmgr.setSetting("rm_traktcache", 'true')
                        cursor.close()
        except:
                xbmc.log('%s: Fen Light Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #afFENity
        try:
                if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                    with open(var.path_affen,'r') as f:
                        data = f.read()

                    client = data.replace(var.affen_client,var.client_am).replace(var.affen_secret,var.secret_am)

                    with open(var.path_affen,'w') as f:
                        f.write(client)

                    from accountmgr.modules import trakt_db
                    conn = trakt_db.create_conn(var.affen_settings_db)

                    with conn:
                        cursor = conn.cursor()
                        cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('trakt.token',))
                        auth_trakt = cursor.fetchone()
                        chk_auth_affen = str(auth_trakt)

                        for char in char_remov:
                            chk_auth_affen = chk_auth_affen.replace(char, "")
                            
                        if not str(var.chk_accountmgr_tk) == chk_auth_affen:

                            from accountmgr.modules import trakt_db
                            trakt_db.auth_affen_trakt()
                            accountmgr.setSetting("rm_traktcache", 'true')
                        cursor.close()
        except:
                xbmc.log('%s: afFENity Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Ezra
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':

                                addon = xbmcaddon.Addon("plugin.video.ezra")
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt_user", your_username)
                                addon.setSetting("trakt.expires", your_expires)
                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched_indicators", '1')
        except:
                xbmc.log('%s: Ezra Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

     #Coalition
        try:
                if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):
                        chk_auth_coal = xbmcaddon.Addon('plugin.video.coalition').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_coal) or str(chk_auth_coal) == '':
                        
                                    with open(var.path_coal,'r') as f:
                                        data = f.read()

                                    client = data.replace(var.coal_client,var.client_am).replace(var.coal_secret,var.secret_am)

                                    with open(var.path_coal,'w') as f:
                                        f.write(client)

                                    addon = xbmcaddon.Addon("plugin.video.coalition")
                                    addon.setSetting("trakt.token", your_token)
                                    addon.setSetting("trakt_user", your_username)
                                    addon.setSetting("trakt.refresh", your_refresh)
                                    addon.setSetting("trakt.expires", your_expires)
                                    addon.setSetting("trakt.indicators_active", 'true')
                                    addon.setSetting("watched_indicators", '1')
        except:
                xbmc.log('%s: Coalition Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #POV
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_pov) or str(chk_auth_pov) == '':

                                with open(var.path_pov,'r') as f:
                                    data = f.read()

                                client = data.replace(var.pov_client,var.client_am).replace(var.pov_secret,var.secret_am)

                                with open(var.path_pov,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt_user", your_username)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.expires", your_expires)
                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched.indicators", '1')              
        except:
                xbmc.log('%s: POV Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Umbrella
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("trakt.user.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_umb) or str(chk_auth_umb) == '':

                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("trakt.user.name", your_username)
                                addon.setSetting("trakt.user.token", your_token)
                                addon.setSetting("trakt.refreshtoken", your_refresh)
                                addon.setSetting("trakt.token.expires", your_expires)
                                addon.setSetting("traktuserkey.customenabled", 'true')
                                addon.setSetting("trakt.clientid", var.client_am)
                                addon.setSetting("trakt.clientsecret", var.secret_am)
                                addon.setSetting("trakt.scrobble", 'true')
                                addon.setSetting("resume.source", '1')  
        except:
                xbmc.log('%s: Umbrella Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #OneMoar
        try:
                if xbmcvfs.exists(var.chk_onem) and xbmcvfs.exists(var.chkset_onem):
                        chk_auth_onem = xbmcaddon.Addon('plugin.video.onemoar').getSetting("trakt.user.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_onem) or str(chk_auth_onem) == '':

                                addon = xbmcaddon.Addon("plugin.video.onemoar")
                                addon.setSetting("trakt.user.name", your_username)
                                addon.setSetting("trakt.user.token", your_token)
                                addon.setSetting("trakt.refreshtoken", your_refresh)
                                addon.setSetting("trakt.token.expires", your_expires)
                                addon.setSetting("traktuserkey.customenabled", 'true')
                                addon.setSetting("trakt.clientid", var.client_am)
                                addon.setSetting("trakt.clientsecret", var.secret_am)
                                addon.setSetting("trakt.scrobble", 'true')
                                addon.setSetting("resume.source", '1')  
        except:
                xbmc.log('%s: OneMoar Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Dradis
        try:
                if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):
                        chk_auth_dradis = xbmcaddon.Addon('plugin.video.dradis').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_dradis) or str(chk_auth_dradis) == '':

                                with open(var.path_dradis,'r') as f:
                                    data = f.read()

                                client = data.replace(var.dradis_client,var.client_am).replace(var.dradis_secret,var.secret_am)

                                with open(var.path_dradis,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.dradis")
                                addon.setSetting("trakt.username", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.expires", your_expires)
                                addon.setSetting("trakt.isauthed", 'true')
                                accountmgr.setSetting("dradis_traktsync", 'true')
        except:
                xbmc.log('%s: Dradis Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Taz19
        try:
                if xbmcvfs.exists(var.chk_taz) and xbmcvfs.exists(var.chkset_taz):
                        chk_auth_taz = xbmcaddon.Addon('plugin.video.taz19').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_taz) or str(chk_auth_taz) == '':

                                with open(var.path_taz,'r') as f:
                                    data = f.read()

                                client = data.replace(var.taz_client,var.client_am)

                                with open(var.path_taz,'w') as f:
                                    f.write(client)
                                
                                addon = xbmcaddon.Addon("plugin.video.taz19")
                                addon.setSetting("trakt_user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.expires", your_expires)
                                addon.setSetting("trakt_indicators_active", 'true')
                                addon.setSetting("watched_indicators", '1')
        except:
                xbmc.log('%s: Taz Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Shadow
        try:
                if xbmcvfs.exists(var.chk_shadow) and not xbmcvfs.exists(var.shadow_ud):
                        os.mkdir(var.shadow_ud)
                        xbmcvfs.copy(os.path.join(var.shadow), os.path.join(var.chkset_shadow))
                        
                if xbmcvfs.exists(var.chk_shadow) and not xbmcvfs.exists(var.chkset_shadow):
                        xbmcvfs.copy(os.path.join(var.shadow), os.path.join(var.chkset_shadow))

                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':
                                
                                with open(var.path_shadow,'r') as f:
                                    data = f.read()

                                client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)

                                with open(var.path_shadow,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.shadow")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Shadow Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Ghost
        try:
                if xbmcvfs.exists(var.chk_ghost) and not xbmcvfs.exists(var.ghost_ud):
                        os.mkdir(var.ghost_ud)
                        xbmcvfs.copy(os.path.join(var.ghost), os.path.join(var.chkset_ghost))
                        
                if xbmcvfs.exists(var.chk_ghost) and not xbmcvfs.exists(var.chkset_ghost):
                        xbmcvfs.copy(os.path.join(var.ghost), os.path.join(var.chkset_ghost))

                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                with open(var.path_ghost,'r') as f:
                                    data = f.read()

                                client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)

                                with open(var.path_ghost,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.ghost")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Ghost Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Base
        try:
                if xbmcvfs.exists(var.chk_base) and not xbmcvfs.exists(var.base_ud):
                        os.mkdir(var.base_ud)
                        xbmcvfs.copy(os.path.join(var.base), os.path.join(var.chkset_base))
                        
                if xbmcvfs.exists(var.chk_base) and not xbmcvfs.exists(var.chkset_base):
                        xbmcvfs.copy(os.path.join(var.base), os.path.join(var.chkset_base))

                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base):
                        chk_auth_base = xbmcaddon.Addon('plugin.video.base').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_base) or str(chk_auth_base) == '':
                                
                                with open(var.path_base,'r') as f:
                                    data = f.read()

                                client = data.replace(var.base_client,var.client_am).replace(var.base_secret,var.secret_am)

                                with open(var.path_base,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.base")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Base Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Unleashed
        try:
                if xbmcvfs.exists(var.chk_unleashed) and not xbmcvfs.exists(var.unleashed_ud):
                        os.mkdir(var.unleashed_ud)
                        xbmcvfs.copy(os.path.join(var.unleashed), os.path.join(var.chkset_unleashed))
                        
                if xbmcvfs.exists(var.chk_unleashed) and not xbmcvfs.exists(var.chkset_unleashed):
                        xbmcvfs.copy(os.path.join(var.unleashed), os.path.join(var.chkset_unleashed))

                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                with open(var.path_unleashed,'r') as f:
                                    data = f.read()

                                client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)

                                with open(var.path_unleashed,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.unleashed")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Unleashed Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Chain Reaction
        try:
                if xbmcvfs.exists(var.chk_chains) and not xbmcvfs.exists(var.chains_ud):
                        os.mkdir(var.chains_ud)
                        xbmcvfs.copy(os.path.join(var.chains), os.path.join(var.chkset_chains))
                        
                if xbmcvfs.exists(var.chk_chains) and not xbmcvfs.exists(var.chkset_chains):
                        xbmcvfs.copy(os.path.join(var.chains), os.path.join(var.chkset_chains))

                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_chains = xbmcaddon.Addon('plugin.video.thechains').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_chains) or str(chk_auth_chains) == '':
                                
                                with open(var.path_chains,'r') as f:
                                    data = f.read()

                                client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)

                                with open(var.path_chains,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.thechains")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Chain Reaction Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
           
    #Magic Dragon
        try:
                if xbmcvfs.exists(var.chk_md) and not xbmcvfs.exists(var.md_ud):
                        os.mkdir(var.md_ud)
                        xbmcvfs.copy(os.path.join(var.md), os.path.join(var.chkset_md))
                        
                if xbmcvfs.exists(var.chk_md) and not xbmcvfs.exists(var.chkset_md):
                        xbmcvfs.copy(os.path.join(var.md), os.path.join(var.chkset_md))

                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_md) or str(chk_auth_md) == '':
                               
                                with open(var.path_md,'r') as f:
                                    data = f.read()

                                client = data.replace(var.md_client,var.client_am).replace(var.md_secret,var.secret_am)

                                with open(var.path_md,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Magic Dragon Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Asgard
        try:
                if xbmcvfs.exists(var.chk_asgard) and not xbmcvfs.exists(var.asgard_ud):
                        os.mkdir(var.asgard_ud)
                        xbmcvfs.copy(os.path.join(var.asgard), os.path.join(var.chkset_asgard))
                        
                if xbmcvfs.exists(var.chk_asgard) and not xbmcvfs.exists(var.chkset_asgard):
                        xbmcvfs.copy(os.path.join(var.asgard), os.path.join(var.chkset_asgard))

                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                                
                                with open(var.path_asgard,'r') as f:
                                    data = f.read()

                                client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)

                                with open(var.path_asgard,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.asgard")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Asgard Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Patriot
        try:
                if xbmcvfs.exists(var.chk_patriot) and not xbmcvfs.exists(var.patriot_ud):
                        os.mkdir(var.patriot_ud)
                        xbmcvfs.copy(os.path.join(var.patriot), os.path.join(var.chkset_patriot))
                        
                if xbmcvfs.exists(var.chk_patriot) and not xbmcvfs.exists(var.chkset_patriot):
                        xbmcvfs.copy(os.path.join(var.patriot), os.path.join(var.chkset_patriot))

                if xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot):
                        chk_auth_patriot = xbmcaddon.Addon('plugin.video.patriot').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_patriot) or str(chk_auth_patriot) == '':
                                
                                with open(var.path_patriot,'r') as f:
                                    data = f.read()

                                client = data.replace(var.patriot_client,var.client_am).replace(var.patriot_secret,var.secret_am)

                                with open(var.path_patriot,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.patriot")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Patriot Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Black Lightning
        try:
                if xbmcvfs.exists(var.chk_blackl) and not xbmcvfs.exists(var.blackl_ud):
                        os.mkdir(var.blackl_ud)
                        xbmcvfs.copy(os.path.join(var.blackl), os.path.join(var.chkset_blackl))
                        
                if xbmcvfs.exists(var.chk_blackl) and not xbmcvfs.exists(var.chkset_blackl):
                        xbmcvfs.copy(os.path.join(var.blackl), os.path.join(var.chkset_blackl))

                if xbmcvfs.exists(var.chk_blackl) and xbmcvfs.exists(var.chkset_blackl):
                        chk_auth_blackl = xbmcaddon.Addon('plugin.video.blacklightning').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_blackl) or str(chk_auth_blackl) == '':
                                
                                with open(var.path_blackl,'r') as f:
                                    data = f.read()

                                client = data.replace(var.blackl_client,var.client_am).replace(var.blackl_secret,var.secret_am)

                                with open(var.path_blackl,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.blacklightning")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Black Lightning Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Aliunde
        try:
                if xbmcvfs.exists(var.chk_aliunde) and not xbmcvfs.exists(var.aliunde_ud):
                        os.mkdir(var.aliunde_ud)
                        xbmcvfs.copy(os.path.join(var.aliunde), os.path.join(var.chkset_aliunde))
                        
                if xbmcvfs.exists(var.chk_aliunde) and not xbmcvfs.exists(var.chkset_aliunde):
                        xbmcvfs.copy(os.path.join(var.aliunde), os.path.join(var.chkset_aliunde))

                if xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde):
                        chk_auth_aliunde = xbmcaddon.Addon('plugin.video.aliundek19').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_aliunde) or str(chk_auth_aliunde) == '':
                                
                                with open(var.path_aliunde,'r') as f:
                                    data = f.read()

                                client = data.replace(var.aliunde_client,var.client_am).replace(var.aliunde_secret,var.secret_am)

                                with open(var.path_aliunde,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.aliundek19")
                                addon.setSetting("trakt_access_token", your_token)
                                addon.setSetting("trakt_refresh_token", your_refresh)
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                xbmc.log('%s: Aliunde Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Homelander
        try:
                if xbmcvfs.exists(var.chk_home) and not xbmcvfs.exists(var.home_ud):
                        os.mkdir(var.home_ud)
                        xbmcvfs.copy(os.path.join(var.home), os.path.join(var.chkset_home))
                        
                if xbmcvfs.exists(var.chk_home) and not xbmcvfs.exists(var.chkset_home):
                        xbmcvfs.copy(os.path.join(var.home), os.path.join(var.chkset_home))

                if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
                        chk_auth_home = xbmcaddon.Addon('plugin.video.homelander').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_home) or str(chk_auth_home) == '':

                                addon = xbmcaddon.Addon("plugin.video.homelander")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Homelander Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Quicksilver
        try:
                if xbmcvfs.exists(var.chk_quick) and not xbmcvfs.exists(var.quick_ud):
                        os.mkdir(var.quick_ud)
                        xbmcvfs.copy(os.path.join(var.quick), os.path.join(var.chkset_quick))
                        
                if xbmcvfs.exists(var.chk_quick) and not xbmcvfs.exists(var.chkset_quick):
                        xbmcvfs.copy(os.path.join(var.quick), os.path.join(var.chkset_quick))

                if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                        chk_auth_quick = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_quick) or str(chk_auth_quick) == '':

                                addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Quicksilver Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Chains Genocide
        try:
                if xbmcvfs.exists(var.chk_genocide) and not xbmcvfs.exists(var.genocide_ud):
                        os.mkdir(var.genocide_ud)
                        xbmcvfs.copy(os.path.join(var.genocide), os.path.join(var.chkset_genocide))
                        
                if xbmcvfs.exists(var.chk_genocide) and not xbmcvfs.exists(var.chkset_genocide):
                        xbmcvfs.copy(os.path.join(var.genocide), os.path.join(var.chkset_genocide))

                if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                        chk_auth_genocide = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_genocide) or str(chk_auth_genocide) == '':

                                addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Chains Genocide Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Absolution
        try:
                if xbmcvfs.exists(var.chk_absol) and not xbmcvfs.exists(var.absol_ud):
                        os.mkdir(var.absol_ud)
                        xbmcvfs.copy(os.path.join(var.absol), os.path.join(var.chkset_absol))
                        
                if xbmcvfs.exists(var.chk_absol) and not xbmcvfs.exists(var.chkset_absol):
                        xbmcvfs.copy(os.path.join(var.absol), os.path.join(var.chkset_absol))

                if xbmcvfs.exists(var.chk_absol) and xbmcvfs.exists(var.chkset_absol):
                        chk_auth_absol = xbmcaddon.Addon('plugin.video.absolution').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_absol) or str(chk_auth_absol) == '':

                                addon = xbmcaddon.Addon("plugin.video.absolution")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Absolution Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Shazam
        try:
                if xbmcvfs.exists(var.chk_shazam) and not xbmcvfs.exists(var.shazam_ud):
                        os.mkdir(var.shazam_ud)
                        xbmcvfs.copy(os.path.join(var.shazam), os.path.join(var.chkset_shazam))
                        
                if xbmcvfs.exists(var.chk_shazam) and not xbmcvfs.exists(var.chkset_shazam):
                        xbmcvfs.copy(os.path.join(var.shazam), os.path.join(var.chkset_shazam))

                if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):
                        chk_auth_shazam = xbmcaddon.Addon('plugin.video.shazam').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_shazam) or str(chk_auth_shazam) == '':

                                addon = xbmcaddon.Addon("plugin.video.shazam")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Shazam Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #The Crew
        try:
                if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.crew_ud):
                        os.mkdir(var.crew_ud)
                        xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))
                        
                if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.chkset_crew):
                        xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))
                        
                if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                        chk_auth_crew = xbmcaddon.Addon('plugin.video.thecrew').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_crew) or str(chk_auth_crew) == '':

                                with open(var.path_crew,'r') as f:
                                    data = f.read()

                                client = data.replace(var.crew_client,var.client_am).replace(var.crew_secret,var.secret_am)

                                with open(var.path_crew,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.thecrew")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
        except:
                xbmc.log('%s: The Crew Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
    #Nightwing
        try:
                if xbmcvfs.exists(var.chk_night) and not xbmcvfs.exists(var.night_ud):
                        os.mkdir(var.night_ud)
                        xbmcvfs.copy(os.path.join(var.night), os.path.join(var.chkset_night))
                        
                if xbmcvfs.exists(var.chk_night) and not xbmcvfs.exists(var.chkset_night):
                        xbmcvfs.copy(os.path.join(var.night), os.path.join(var.chkset_night))

                if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night):
                        chk_auth_night = xbmcaddon.Addon('plugin.video.nightwing').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_night) or str(chk_auth_night) == '':
                                
                                addon = xbmcaddon.Addon("plugin.video.nightwing")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Nightwing Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #TheLab
        try:
                if xbmcvfs.exists(var.chk_lab) and not xbmcvfs.exists(var.lab_ud):
                        os.mkdir(var.lab_ud)
                        xbmcvfs.copy(os.path.join(var.lab), os.path.join(var.chkset_lab))
                        
                if xbmcvfs.exists(var.chk_lab) and not xbmcvfs.exists(var.chkset_lab):
                        xbmcvfs.copy(os.path.join(var.lab), os.path.join(var.chkset_lab))

                if xbmcvfs.exists(var.chk_lab) and xbmcvfs.exists(var.chkset_lab):
                        chk_auth_lab = xbmcaddon.Addon('plugin.video.thelab').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_lab) or str(chk_auth_lab) == '':

                                addon = xbmcaddon.Addon("plugin.video.thelab")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: TheLab Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Alvin
        try:
                if xbmcvfs.exists(var.chk_alvin) and not xbmcvfs.exists(var.alvin_ud):
                        os.mkdir(var.alvin_ud)
                        xbmcvfs.copy(os.path.join(var.alvin), os.path.join(var.chkset_alvin))
                        
                if xbmcvfs.exists(var.chk_alvin) and not xbmcvfs.exists(var.chkset_alvin):
                        xbmcvfs.copy(os.path.join(var.alvin), os.path.join(var.chkset_alvin))

                if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):
                        chk_auth_alvin = xbmcaddon.Addon('plugin.video.alvin').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_alvin) or str(chk_auth_alvin) == '':

                                addon = xbmcaddon.Addon("plugin.video.alvin")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Alvin Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Moria
        try:
                if xbmcvfs.exists(var.chk_moria) and not xbmcvfs.exists(var.moria_ud):
                        os.mkdir(var.moria_ud)
                        xbmcvfs.copy(os.path.join(var.moria), os.path.join(var.chkset_moria))
                        
                if xbmcvfs.exists(var.chk_moria) and not xbmcvfs.exists(var.chkset_moria):
                        xbmcvfs.copy(os.path.join(var.moria), os.path.join(var.chkset_moria))

                if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):
                        chk_auth_moria = xbmcaddon.Addon('plugin.video.moria').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_moria) or str(chk_auth_moria) == '':

                                addon = xbmcaddon.Addon("plugin.video.moria")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Moria Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Nine Lives
        try:
                if xbmcvfs.exists(var.chk_nine) and not xbmcvfs.exists(var.nine_ud):
                        os.mkdir(var.nine_ud)
                        xbmcvfs.copy(os.path.join(var.nine), os.path.join(var.chkset_nine))
                        
                if xbmcvfs.exists(var.chk_nine) and not xbmcvfs.exists(var.chkset_nine):
                        xbmcvfs.copy(os.path.join(var.nine), os.path.join(var.chkset_nine))

                if xbmcvfs.exists(var.chk_nine) and xbmcvfs.exists(var.chkset_nine):
                        chk_auth_nine = xbmcaddon.Addon('plugin.video.nine').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_nine) or str(chk_auth_nine) == '':

                                addon = xbmcaddon.Addon("plugin.video.nine")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
                                addon.setSetting("trakt.client_id", var.client_am)
                                addon.setSetting("trakt.client_secret", var.secret_am)
        except:
                xbmc.log('%s: Nine Lives Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #Scrubs V2
        try:
                if xbmcvfs.exists(var.chk_scrubs) and not xbmcvfs.exists(var.scrubs_ud):
                        os.mkdir(var.scrubs_ud)
                        xbmcvfs.copy(os.path.join(var.scrubs), os.path.join(var.chkset_scrubs))
                        
                if xbmcvfs.exists(var.chk_scrubs) and not xbmcvfs.exists(var.chkset_scrubs):
                        xbmcvfs.copy(os.path.join(var.scrubs), os.path.join(var.chkset_scrubs))

                if xbmcvfs.exists(var.chk_scrubs) and xbmcvfs.exists(var.chkset_scrubs):
                        chk_auth_scrubs = xbmcaddon.Addon('plugin.video.scrubsv2').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_scrubs) or str(chk_auth_scrubs) == '':

                                with open(var.path_scrubs,'r') as f:
                                    data = f.read()

                                client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)

                                with open(var.path_scrubs,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.scrubsv2")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
        except:
                xbmc.log('%s: Scrubs V2 Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #TheLabjr
        try:
                if xbmcvfs.exists(var.chk_labjr) and not xbmcvfs.exists(var.labjr_ud):
                        os.mkdir(var.labjr_ud)
                        xbmcvfs.copy(os.path.join(var.labjr), os.path.join(var.chkset_labjr))
                        
                if xbmcvfs.exists(var.chk_labjr) and not xbmcvfs.exists(var.chkset_labjr):
                        xbmcvfs.copy(os.path.join(var.labjr), os.path.join(var.chkset_labjr))

                if xbmcvfs.exists(var.chk_labjr) and xbmcvfs.exists(var.chkset_labjr):
                        chk_auth_labjr = xbmcaddon.Addon('plugin.video.thelabjr').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_labjr) or str(chk_auth_labjr) == '':

                                with open(var.path_labjr,'r') as f:
                                    data = f.read()

                                client = data.replace(var.labjr_client,var.client_am).replace(var.labjr_secret,var.secret_am)

                                with open(var.path_labjr,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("plugin.video.thelabjr")
                                addon.setSetting("trakt.user", your_username)
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.authed", 'yes')
        except:
                xbmc.log('%s: TheLabjr Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #TMDB Helper
        try:
                if xbmcvfs.exists(var.chk_tmdbh) and not xbmcvfs.exists(var.tmdbh_ud):
                        os.mkdir(var.tmdbh_ud)
                        xbmcvfs.copy(os.path.join(var.tmdbh), os.path.join(var.chkset_tmdbh))
                        
                if xbmcvfs.exists(var.chk_tmdbh) and not xbmcvfs.exists(var.chkset_tmdbh):
                        xbmcvfs.copy(os.path.join(var.tmdbh), os.path.join(var.chkset_tmdbh))

                if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh):

                        chk_auth_tmdbh = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("trakt_token")
                        
                        if str(your_token) in str(chk_auth_tmdbh):
                            pass
                                
                        else:                           
                            with open(var.path_tmdbh,'r') as f:
                                data = f.read()

                            client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)

                            with open(var.path_tmdbh,'w') as f:
                                f.write(client)
                                    
                            addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                            your_expires_float = float(your_expires)
                            your_expires_rnd = int(your_expires_float)
                            token = '{"access_token":"'
                            refresh = f'","token_type":"bearer","expires_in":7776000,"refresh_token":"'
                            expires = f'","scope":"public","created_at":'
                            tmdbh_data = '%s%s%s%s%s%s}' %(token, your_token, refresh, your_refresh, expires, your_expires_rnd)
                            addon.setSettingString("trakt_token", tmdbh_data)
                            addon.setSetting("startup_notifications", 'false')
        except:
                xbmc.log('%s: TMDBh Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #Trakt Addon
        try:
                if xbmcvfs.exists(var.chk_trakt) and not xbmcvfs.exists(var.trakt_ud):
                        os.mkdir(var.trakt_ud)
                        xbmcvfs.copy(os.path.join(var.trakt), os.path.join(var.chkset_trakt))
                        
                if xbmcvfs.exists(var.chk_trakt) and not xbmcvfs.exists(var.chkset_trakt):
                        xbmcvfs.copy(os.path.join(var.trakt), os.path.join(var.chkset_trakt))
                
                if xbmcvfs.exists(var.chk_trakt) and xbmcvfs.exists(var.chkset_trakt):
                        
                        chk_auth_trakt = xbmcaddon.Addon('script.trakt').getSetting("trakt_token")
                        
                        if str(your_token) in str(chk_auth_trakt):
                            pass
                                
                        else:
                            with open(var.path_trakt,'r') as f:
                                data = f.read()

                            client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)

                            with open(var.path_trakt,'w') as f:
                                f.write(client)
                            
                            addon = xbmcaddon.Addon("script.trakt")
                            addon.setSetting("user", your_username)
                            your_expires_float = float(your_expires)
                            your_expires_rnd = int(your_expires_float)
                            token = '{"access_token": "'
                            refresh = f'","token_type": "bearer", "expires_in": 7776000, "refresh_token": "'
                            expires = f'", "scope": "public", "created_at": '
                            trakt_data = '%s%s%s%s%s%s}' %(token, your_token, refresh, your_refresh, expires, your_expires_rnd)
                            addon.setSetting("authorization", trakt_data)
        except:
                xbmc.log('%s: Trakt Addon Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass

    #All Accounts
        try:
                if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.allaccounts_ud):
                        os.mkdir(var.allaccounts_ud)
                        xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                        
                if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.chkset_allaccounts):
                        xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                        
                if xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts):
                        chk_auth_allaccounts = xbmcaddon.Addon('script.module.allaccounts').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_allaccounts) or str(chk_auth_allaccounts) == '':

                                with open(var.path_allaccounts,'r') as f:
                                    data = f.read()

                                client = data.replace(var.allacts_client,var.client_am).replace(var.allacts_secret,var.secret_am)

                                with open(var.path_allaccounts,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("script.module.allaccounts")
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.username", your_username)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.expires", your_expires)
        except:
                xbmc.log('%s: All Accounts Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            
    #My Accounts
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.myaccounts_ud):
                        os.mkdir(var.myaccounts_ud)
                        xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.chkset_myaccounts):
                        xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':

                                with open(var.path_myaccounts,'r') as f:
                                    data = f.read()

                                client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)

                                with open(var.path_myaccounts,'w') as f:
                                    f.write(client)

                                addon = xbmcaddon.Addon("script.module.myaccounts")
                                addon.setSetting("trakt.token", your_token)
                                addon.setSetting("trakt.username", your_username)
                                addon.setSetting("trakt.refresh", your_refresh)
                                addon.setSetting("trakt.expires", your_expires)
        except:
                xbmc.log('%s: My Accounts Trakt Failed!' % var.amgr, xbmc.LOGINFO)
                pass
