import xbmc, xbmcaddon
import xbmcvfs
import json
from pathlib import Path
from myaccts.modules import control

#Seren RD
def serenrd_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
       
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):
                
                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("rd.username", your_username)
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                enabled_rd = ("true")
                addon.setSetting("realdebrid.enabled", enabled_rd)

                enabled_pm = ("false")
                addon.setSetting("premiumize.enabled", enabled_pm)

                enabled_ad = ("false")
                addon.setSetting("alldebrid.enabled", enabled_ad)
                

#Ezra RD
def ezrard_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.ezra")
                addon.setSetting("rd.username", your_username)
                addon.setSetting("rd.token", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)


#Fen RD
def fenrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')   
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.fen")
                addon.setSetting("rd.account_id", your_username)
                addon.setSetting("rd.token", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)


#Umbrella RD
def umbrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')      
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):
                
                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                addon.setSetting("realdebridusername", your_username)
                addon.setSetting("realdebridtoken", your_token)
                addon.setSetting("realdebrid.clientid", your_client_id)
                addon.setSetting("realdebridrefresh", your_refresh)
                addon.setSetting("realdebridsecret", your_secret)


#Shadow RD
def shadowrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.shadow")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                rd_use = ("true")
                addon.setSetting("debrid_use_rd", rd_use)

                pm_use = ("false")
                addon.setSetting("debrid_use_pm", pm_use)

                ad_use = ("false")
                addon.setSetting("debrid_use_ad", ad_use)
                
#Ghost RD
def ghostrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                rd_use = ("true")
                addon.setSetting("debrid_use_rd", rd_use)

                pm_use = ("false")
                addon.setSetting("debrid_use_pm", pm_use)

                ad_use = ("false")
                addon.setSetting("debrid_use_ad", ad_use)


#Genocide RD
def genociderd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.Genocide/')      
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.Genocide/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.Genocide")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#Chains RD
def chainsrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')      
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.thechains")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#Moria RD
def moriard_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.moria")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#Base 19 RD
def baserd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.base19")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#Twisted RD
def twistedrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.twisted")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#Magic Dragon RD
def mdrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')
     
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#Asgard RD
def asgardrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.asgard")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#M.E.T.V RD
def metvrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.metv19")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#KodiVerse RD
def kverserd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.KodiVerse/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.KodiVerse/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.KodiVerse")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)


#4K RD
def fourkrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.4k/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.4k/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("plugin.video.4k")
                addon.setSetting("rd.auth", your_token)
                addon.setSetting("rd.client_id", your_client_id)
                addon.setSetting("rd.refresh", your_refresh)
                addon.setSetting("rd.secret", your_secret)

                d_select = ("0")
                addon.setSetting("debrid_select", d_select)
                

#ResolveURL RD
def rurlrd_auth():
        
        debrid_addon = xbmcvfs.translatePath('special://home/addons/script.module.resolveurl/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.resolveurl/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("script.module.resolveurl")
                addon.setSetting("RealDebridResolver_login", your_username)
                addon.setSetting("RealDebridResolver_token", your_token)
                addon.setSetting("RealDebridResolver_client_id", your_client_id)
                addon.setSetting("RealDebridResolver_refresh", your_refresh)
                addon.setSetting("RealDebridResolver_client_secret", your_secret)

                cache_only = ("true")
                addon.setSetting("RealDebridResolver_cached_only", cache_only)


#My Accounts RD
def myaccountsrd_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("realdebrid.username")
                your_token = myaccts.getSetting("realdebrid.token")
                your_client_id = myaccts.getSetting("realdebrid.client_id")
                your_refresh = myaccts.getSetting("realdebrid.refresh")
                your_secret = myaccts.getSetting("realdebrid.secret")
                
                addon = xbmcaddon.Addon("script.module.resolveurl")
                addon.setSetting("realdebrid.username", your_username)
                addon.setSetting("realdebrid.token", your_token)
                addon.setSetting("realdebrid.client_id", your_client_id)
                addon.setSetting("realdebrid.refresh", your_refresh)
                addon.setSetting("realdebrid.secret", your_secret)

#Realizer RD
realizer_path = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.realizerx/rdauth.json')
def realizer_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.realizerx/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.realizerx/rdauth.json')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                rdauth = {}
                myaccts = xbmcaddon.Addon('script.module.myaccts')
                rdauth = {'client_id': myaccts.getSetting('realdebrid.client_id'), 'client_secret': myaccts.getSetting('realdebrid.secret'), 'token': myaccts.getSetting('realdebrid.token'), 'refresh_token': myaccts.getSetting('realdebrid.refresh'), 'added': '202301010243'}

                with open(realizer_path, 'w') as debrid_write:
                        json.dump(rdauth, debrid_write)
                        
def debrid_auth_rd(): #Auth All Supported Addons

        #RealDebrid
        serenrd_auth()
        ezrard_auth()
        fenrd_auth()
        umbrd_auth()
        shadowrd_auth()
        ghostrd_auth()
        genociderd_auth()
        chainsrd_auth()
        moriard_auth()
        baserd_auth()
        twistedrd_auth()
        mdrd_auth()
        asgardrd_auth()
        metvrd_auth()
        kverserd_auth()
        fourkrd_auth()
        rurlrd_auth()
        myaccountsrd_auth()
        realizer_auth()
