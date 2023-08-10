import xbmc, xbmcaddon, xbmcgui
import os
import xbmcvfs
from pathlib import Path
from accountmgr.modules import var

#Seren
def seren_trakt():
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists.
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("trakt.auth")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match, authorization is skipped
                
                                #Insert Account Mananger API keys into add-on
                                f = open(var.api_path_seren,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
                                f = open(var.api_path_seren,'w')
                                f.write(client)
                                f.close()

                                #Write trakt data to settings.xml
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.seren")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.auth", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.username", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)
                                
                                your_expires = accountmgr.getSetting("trakt.expires")
                                your_expires_float = float(your_expires)
                                your_expires_rnd = int(your_expires_float)
                                your_expires_str = str(your_expires_rnd)
                                addon.setSetting("trakt.expires", your_expires_str)
        except:
                pass
        
#Fen
def fen_trakt():
        try:
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                        chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_fen) or str(chk_auth_fen) == '':
                        
                                f = open(var.api_path_fen,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                                f = open(var.api_path_fen,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.fen")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)

                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched.indicators", '1')
        except:
                pass

#Ezra
def ezra_trakt():
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.ezra")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt_user", your_username)
                                
                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)
        except:
                pass
        
#POV
def pov_trakt():
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_pov) or str(chk_auth_pov) == '':

                                f = open(var.api_path_pov,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
                                f = open(var.api_path_pov,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.pov")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt_user", your_username)
                                
                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)

                                addon.setSetting("trakt.indicators_active", 'true')
                                addon.setSetting("watched.indicators", '1')              
        except:
                pass
        
#Umbrella
def umb_trakt():
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("trakt.user.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_umb) or str(chk_auth_umb) == '':

                                f = open(var.api_path_umb,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.umb_client,var.client_am).replace(var.umb_secret,var.secret_am)
                                f = open(var.api_path_umb,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.umbrella")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user.name", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.user.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refreshtoken", your_refresh)

                                your_secret = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.token.expires", your_secret)
        except:
                pass
        
#Homelander
def home_trakt():
        try:
                if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):
                        chk_auth_home = xbmcaddon.Addon('plugin.video.homelander').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_home) or str(chk_auth_home) == '':

                                f = open(var.api_path_home,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                f = open(var.api_path_home,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.homelander")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#Quicksilver
def quick_trakt():
        try:
                if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                        chk_auth_quick = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_quick) or str(chk_auth_quick) == '':

                                f = open(var.api_path_quick,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                f = open(var.api_path_quick,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.quicksilver")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#Chains Genocide
def genocide_trakt():
        try:
                if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):
                        chk_auth_genocide = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_genocide) or str(chk_auth_genocide) == '':

                                f = open(var.api_path_genocide,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                f = open(var.api_path_genocide,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.chainsgenocide")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#The Crew
def crew_trakt():
        try:
                if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):
                        chk_auth_crew = xbmcaddon.Addon('plugin.video.thecrew').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_crew) or str(chk_auth_crew) == '':

                                f = open(var.api_path_crew,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
                                f = open(var.api_path_crew,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.thecrew")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)
        except:
                pass
        
#Shazam
def shazam_trakt():
        try:
                if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):
                        chk_auth_shazam = xbmcaddon.Addon('plugin.video.shazam').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_shazam) or str(chk_auth_shazam) == '':

                                f = open(var.api_path_shazam,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                f = open(var.api_path_shazam,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.shazam")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#Nightwing
def night_trakt():
        try:
                if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night):
                        chk_auth_night = xbmcaddon.Addon('plugin.video.nightwing').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_night) or str(chk_auth_night) == '':

                                f = open(var.api_path_night,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.night_client,var.std_client_am).replace(var.night_secret,var.std_secret_am)
                                f = open(var.api_path_night,'w')
                                f.write(client)
                                f.close()
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.nightwing")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#The Promise
def promise_trakt():
        try:
                if xbmcvfs.exists(var.chk_promise) and xbmcvfs.exists(var.chkset_promise):
                        chk_auth_promise = xbmcaddon.Addon('plugin.video.thepromise').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_promise) or str(chk_auth_promise) == '':

                                f = open(var.api_path_promise,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                f = open(var.api_path_promise,'w')
                                f.write(client)
                                f.close()
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.thepromise")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#Scrubs V2
def scrubs_trakt():
        try:
                if xbmcvfs.exists(var.chk_scrubs) and xbmcvfs.exists(var.chkset_scrubs):
                        chk_auth_scrubs = xbmcaddon.Addon('plugin.video.scrubsv2').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_scrubs) or str(chk_auth_scrubs) == '':

                                f = open(var.api_path_scrubs,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
                                f = open(var.api_path_scrubs,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.scrubsv2")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#Alvin
def alvin_trakt():
        try:
                if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):
                        chk_auth_alvin = xbmcaddon.Addon('plugin.video.alvin').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_alvin) or str(chk_auth_alvin) == '':

                                f = open(var.api_path_alvin,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                f = open(var.api_path_alvin,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.alvin")

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.user", your_username)

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_refresh)

                                addon.setSetting("trakt.authed", 'yes')
        except:
                pass
        
#Shadow
def shadow_trakt():
        try:
                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':
                                
                                f = open(var.api_path_shadow,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
                                f = open(var.api_path_shadow,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.shadow")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
#Ghost
def ghost_trakt():
        try:
                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                f = open(var.api_path_ghost,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
                                f = open(var.api_path_ghost,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.ghost")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
#Unleashed
def unleashed_trakt():
        try:
                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                f = open(var.api_path_unleashed,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
                                f = open(var.api_path_unleashed,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.unleashed")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
#Chain Reaction
def chains_trakt():
        try:
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_chains = xbmcaddon.Addon('plugin.video.thechains').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_chains) or str(chk_auth_chains) == '':
                                
                                f = open(var.api_path_chains,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
                                f = open(var.api_path_chains,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.thechains")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
#Magic Dragon
def md_trakt():
        try:
                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_md) or str(chk_auth_md) == '':
                               
                                f = open(var.api_path_md,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
                                f = open(var.api_path_md,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.magicdragon")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
#Asgard
def asgard_trakt():
        try:
                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("trakt_access_token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                                
                                f = open(var.api_path_asgard,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
                                f = open(var.api_path_asgard,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("plugin.video.asgard")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt_access_token", your_token)

                                your_refresh = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt_refresh_token", your_refresh)

                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt_expires_at", your_expires)
        except:
                pass
        
#My Accounts
def myacts_trakt():
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("trakt.token")
                        if not str(var.chk_accountmgr_tk) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':

                                f = open(var.api_path_myaccounts,'r')
                                data = f.read()
                                f.close()
                                client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
                                f = open(var.api_path_myaccounts,'w')
                                f.write(client)
                                f.close()

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                addon = xbmcaddon.Addon("script.module.myaccounts")

                                your_token = accountmgr.getSetting("trakt.token")
                                addon.setSetting("trakt.token", your_token)

                                your_username = accountmgr.getSetting("trakt.username")
                                addon.setSetting("trakt.username", your_username)

                                your_expires = accountmgr.getSetting("trakt.refresh")
                                addon.setSetting("trakt.refresh", your_expires)
                                
                                your_expires = accountmgr.getSetting("trakt.expires")
                                addon.setSetting("trakt.expires", your_expires)
        except:
                pass
        
#TMDB Helper
def tmdbh_trakt():
        try:
                if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh):
                        
                        f = open(var.api_path_tmdbh,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
                        f = open(var.api_path_tmdbh,'w')
                        f.write(client)
                        f.close()

                        accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")

                        your_token = accountmgr.getSetting("trakt.token")
                        your_refresh = accountmgr.getSetting("trakt.refresh")
                        your_expires = accountmgr.getSetting("trakt.expires")
                        your_expires_float = float(your_expires)
                        your_expires_rnd = int(your_expires_float)

                        token = '{"access_token":"'
                        refresh = f'","token_type":"bearer","expires_in":7776000,"refresh_token":"'
                        expires = f'","scope":"public","created_at":'
                        tmdbh_data = '%s%s%s%s%s%s}' %(token,your_token,refresh,your_refresh,expires,your_expires_rnd)
                        addon.setSettingString("Trakt_token", tmdbh_data)
        except:
                pass

#Trakt Addon
def trakt_trakt():
        try:
                if xbmcvfs.exists(var.chk_trakt) and xbmcvfs.exists(var.chkset_trakt):
                        
                        f = open(var.api_path_trakt,'r')
                        data = f.read()
                        f.close()
                        client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
                        f = open(var.api_path_trakt,'w')
                        f.write(client)
                        f.close()
                        
                        accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                        addon = xbmcaddon.Addon("script.trakt")

                        your_username = accountmgr.getSetting("trakt.username")
                        addon.setSetting("user", your_username)
                        
                        your_token = accountmgr.getSetting("trakt.token")
                        your_refresh = accountmgr.getSetting("trakt.refresh")
                        your_expires = accountmgr.getSetting("trakt.expires")
                        your_expires_float = float(your_expires)
                        your_expires_rnd = int(your_expires_float)
                        
                        token = '{"access_token": "'
                        refresh = f'","token_type": "bearer", "expires_in": 7776000, "refresh_token": "'
                        expires = f'", "scope": "public", "created_at": '
                        trakt_data = '%s%s%s%s%s%s}' %(token, your_token, refresh, your_refresh, expires, your_expires_rnd)
                        addon.setSetting("authorization", trakt_data)
        except:
                pass

def sync_all(): #Sync all add-ons
                seren_trakt()
                fen_trakt()
                pov_trakt()
                ezra_trakt()
                umb_trakt()
                home_trakt()
                quick_trakt()
                genocide_trakt()
                crew_trakt()
                shazam_trakt()
                night_trakt()
                promise_trakt()
                scrubs_trakt()
                alvin_trakt()
                shadow_trakt()
                ghost_trakt()
                unleashed_trakt()
                chains_trakt()
                md_trakt()
                asgard_trakt()
                myacts_trakt()
                tmdbh_trakt()
                trakt_trakt()

