import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from accountmgr.modules import control
from accountmgr.modules import var

#Seren AD
def serenad_auth():
        try:
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists
                        chk_auth_seren = xbmcaddon.Addon('plugin.video.seren').getSetting("alldebrid.apikey")
                        chk_auth_seren_rd = xbmcaddon.Addon('plugin.video.seren').getSetting("rd.auth")
                        chk_auth_seren_pm = xbmcaddon.Addon('plugin.video.seren').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_seren) or str(chk_auth_seren) == '': #Compare Account Mananger token to Add-on token. If they match authorization is skipped

                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                                
                                #Write debrid data to settings.xml
                                addon = xbmcaddon.Addon("plugin.video.seren")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.apikey", your_token)

                                premium_stat = ("Premium")
                                addon.setSetting("alldebrid.premiumstatus", premium_stat)
                                
                                #Set enabled for authorized debrid services
                                enabled_ad = ("true")
                                addon.setSetting("alldebrid.enabled", enabled_ad)

                                if str(chk_auth_seren_rd) != '': #Check if Real-Debrid is authorized
                                        enabled_rd = ("true")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_seren_pm) != '': #Check if Premiumize is authorized
                                        enabled_pm = ("true")
                                        addon.setSetting("premiumize.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("premiumize.enabled", enabled_pm)
        except:
                pass
        
#Ezra AD
def ezraad_auth():
        try:
                if xbmcvfs.exists(var.chk_ezra) and xbmcvfs.exists(var.chkset_ezra):
                        chk_auth_ezra = xbmcaddon.Addon('plugin.video.ezra').getSetting("ad.token")
                        chk_auth_ezra_rd = xbmcaddon.Addon('plugin.video.ezra').getSetting("rd.token")
                        chk_auth_ezra_pm = xbmcaddon.Addon('plugin.video.ezra').getSetting("pm.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_ezra) or str(chk_auth_ezra) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.ezra")
                                addon.setSetting("ad.account_id", your_username)
                                addon.setSetting("ad.token", your_token)

                                enabled_ad = ("true")
                                addon.setSetting("ad.enabled", enabled_ad)

                                if str(chk_auth_ezra_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)
                        
                                if str(chk_auth_ezra_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
        except:
                pass

#Fen AD
def fenad_auth():
        try:
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):
                        chk_auth_fen = xbmcaddon.Addon('plugin.video.fen').getSetting("ad.token")
                        chk_auth_fen_rd = xbmcaddon.Addon('plugin.video.fen').getSetting("rd.token")
                        chk_auth_fen_pm = xbmcaddon.Addon('plugin.video.fen').getSetting("pm.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_fen) or str(chk_auth_fen) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.fen")
                                addon.setSetting("ad.account_id", your_username)
                                addon.setSetting("ad.token", your_token)

                                enabled_ad = ("true")
                                addon.setSetting("ad.enabled", enabled_ad)

                                if str(chk_auth_fen_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)
                        
                                if str(chk_auth_fen_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
        except:
                pass

#POV AD
def povad_auth():
        try:
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):
                        chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("ad.token")
                        chk_auth_pov_rd = xbmcaddon.Addon('plugin.video.pov').getSetting("rd.token")
                        chk_auth_pov_pm = xbmcaddon.Addon('plugin.video.pov').getSetting("pm.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_pov) or str(chk_auth_pov) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.pov")
                                addon.setSetting("ad.account_id", your_username)
                                addon.setSetting("ad.token", your_token)

                                enabled_ad = ("true")
                                addon.setSetting("ad.enabled", enabled_ad)

                                if str(chk_auth_pov_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("rd.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("rd.enabled", enabled_rd)
                        
                                if str(chk_auth_pov_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("pm.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("pm.enabled", enabled_pm)
        except:
                pass                

#Umbrella AD
def umbad_auth():
        try:
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):
                        chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("alldebridtoken")
                        chk_auth_umb_rd = xbmcaddon.Addon('plugin.video.umbrella').getSetting("realdebridtoken")
                        chk_auth_umb_pm = xbmcaddon.Addon('plugin.video.umbrella').getSetting("premiumizetoken")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_umb) or str(chk_auth_umb) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                addon.setSetting("alldebridusername", your_username)
                                addon.setSetting("alldebridtoken", your_token)

                                enabled_ad = ("true")
                                addon.setSetting("alldebrid.enabled", enabled_ad)

                                if str(chk_auth_umb_rd) != '':
                                        enabled_rd = ("true")
                                        addon.setSetting("alldebrid.enabled", enabled_rd)
                                else:
                                        enabled_rd = ("false")
                                        addon.setSetting("realdebrid.enabled", enabled_rd)
                        
                                if str(chk_auth_umb_pm) != '':
                                        enabled_pm = ("true")
                                        addon.setSetting("premiumize.enabled", enabled_pm)
                                else:
                                        enabled_pm = ("false")
                                        addon.setSetting("premiumize.enabled", enabled_pm)
        except:
                pass

#Shadow AD
def shadowad_auth():
        try:
                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow):
                        chk_auth_shadow = xbmcaddon.Addon('plugin.video.shadow').getSetting("alldebrid.token")
                        chk_auth_shadow_rd = xbmcaddon.Addon('plugin.video.shadow').getSetting("rd.auth")
                        chk_auth_shadow_pm = xbmcaddon.Addon('plugin.video.shadow').getSetting("premiumize.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_shadow) or str(chk_auth_shadow) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.shadow")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                enabled_ad = ("true")
                                addon.setSetting("debrid_use_ad", enabled_ad)

                                if str(chk_auth_shadow_rd) != '':
                                        rd_use = ("true")
                                        addon.setSetting("debrid_use_rd", rd_use)
                                else:
                                        rd_use = ("false")
                                        addon.setSetting("debrid_use_rd", rd_use)
                        
                                if str(chk_auth_shadow_pm) != '':
                                        pm_use = ("true")
                                        addon.setSetting("debrid_use_pm", pm_use)
                                else:
                                        pm_use = ("false")
                                        addon.setSetting("debrid_use_pm", pm_use)
        except:
                pass
                
#Ghost AD
def ghostad_auth():
        try:
                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost):
                        chk_auth_ghost = xbmcaddon.Addon('plugin.video.ghost').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_ghost) or str(chk_auth_ghost) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                                
                                addon = xbmcaddon.Addon("plugin.video.ghost")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass
        
#Unleashed AD
def unleashedad_auth():
        try:
                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed):
                        chk_auth_unleashed = xbmcaddon.Addon('plugin.video.unleashed').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_unleashed) or str(chk_auth_unleashed) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.unleashed")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#Chains AD
def chainsad_auth():
        try:
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains):
                        chk_auth_thechains = xbmcaddon.Addon('plugin.video.thechains').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_chains) or str(chk_auth_chains) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.thechains")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#Moria AD
def moriaad_auth():
        try:
                if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):
                        chk_auth_moria = xbmcaddon.Addon('plugin.video.moria').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_moria) or str(chk_auth_moria) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.moria")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#Base 19 AD
def basead_auth():
        try:
                if xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base):
                        chk_auth_base = xbmcaddon.Addon('plugin.video.base19').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_base) or str(chk_auth_base) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.base19")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#Twisted AD
def twistedad_auth():
        try:
                if xbmcvfs.exists(var.chk_twisted) and xbmcvfs.exists(var.chkset_twisted):
                        chk_auth_twisted = xbmcaddon.Addon('plugin.video.twisted').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_twisted) or str(chk_auth_twisted) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.twisted")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#Magic Dragon AD
def mdad_auth():
        try:
                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md):
                        chk_auth_md = xbmcaddon.Addon('plugin.video.magicdragon').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_md) or str(chk_auth_md) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#Asgard AD
def asgardad_auth():
        try:
                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard):
                        chk_auth_asgard = xbmcaddon.Addon('plugin.video.asgard').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_asgard) or str(chk_auth_asgard) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.asgard")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#M.E.T.V AD
def metvad_auth():
        try:
                if xbmcvfs.exists(var.chk_metv) and xbmcvfs.exists(var.chkset_metv):
                        chk_auth_metv = xbmcaddon.Addon('plugin.video.metv19').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_metv) or str(chk_auth_metv) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("plugin.video.metv19")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)

                                d_select = ("2")
                                addon.setSetting("debrid_select", d_select)
        except:
                pass

#ResolveURL AD
def rurlad_auth():
        try:
                if xbmcvfs.exists(var.chk_rurl) and xbmcvfs.exists(var.chkset_rurl):
                        chk_auth_rurl = xbmcaddon.Addon('script.module.resolveurl').getSetting("AllDebridResolver_token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_rurl) or str(chk_auth_rurl) == '':
                                
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("script.module.resolveurl")
                                addon.setSetting("AllDebridResolver_client_id", your_username)
                                addon.setSetting("AllDebridResolver_token", your_token)

                                cache_only = ("true")
                                addon.setSetting("AllDebridResolver_cached_only", cache_only)
        except:
                pass

#My Accounts AD
def myaccountsad_auth():
        try:
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):
                        chk_auth_myaccounts = xbmcaddon.Addon('script.module.myaccounts').getSetting("alldebrid.token")
                        if not str(var.chk_accountmgr_tk_ad) == str(chk_auth_myaccounts) or str(chk_auth_myaccounts) == '':
                        
                                accountmgr = xbmcaddon.Addon("script.module.accountmgr")
                                your_username = accountmgr.getSetting("alldebrid.username")
                                your_token = accountmgr.getSetting("alldebrid.token")
                        
                                addon = xbmcaddon.Addon("script.module.myaccounts")
                                addon.setSetting("alldebrid.username", your_username)
                                addon.setSetting("alldebrid.token", your_token)
        except:
                pass

def debrid_auth_ad(): #Sync all add-ons
                serenad_auth()
                ezraad_auth()
                fenad_auth()
                povad_auth()
                umbad_auth()
                shadowad_auth()
                ghostad_auth()
                unleashedad_auth()
                chainsad_auth()
                moriaad_auth()
                basead_auth()
                twistedad_auth()
                mdad_auth()
                asgardad_auth()
                metvad_auth()
                rurlad_auth()
                myaccountsad_auth()
