import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from myaccts.modules import control


#Seren AD
def serenad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")

                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                enabled_rd = ("false")
                addon.setSetting("realdebrid.enabled", enabled_rd)

                enabled_pm = ("false")
                addon.setSetting("premiumize.enabled", enabled_pm)

                enabled_ad = ("true")
                addon.setSetting("alldebrid.enabled", enabled_ad)

#Ezra AD
def ezraad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.ezra")
                addon.setSetting("ad.account_id", your_username)
                addon.setSetting("ad.token", your_token)


#Fen AD
def fenad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.fen")
                addon.setSetting("ad.account_id", your_username)
                addon.setSetting("ad.token", your_token)


#Umbrella AD
def umbad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                addon.setSetting("alldebridusername", your_username)
                addon.setSetting("alldebridtoken", your_token)


#Shadow AD
def shadowad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.shadow")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                rd_use = ("false")
                addon.setSetting("debrid_use_rd", rd_use)

                pm_use = ("false")
                addon.setSetting("debrid_use_pm", pm_use)

                ad_use = ("true")
                addon.setSetting("debrid_use_ad", ad_use)

                
#Ghost AD
def ghostad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                rd_use = ("false")
                addon.setSetting("debrid_use_rd", rd_use)

                pm_use = ("false")
                addon.setSetting("debrid_use_pm", pm_use)

                ad_use = ("true")
                addon.setSetting("debrid_use_ad", ad_use)


#Genocide AD
def genocidead_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.Genocide/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.Genocide/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.Genocide")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Chains AD
def chainsad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.thechains")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Moria AD
def moriaad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.moria")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Base 19 AD
def basead_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.base19")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Twisted AD
def twistedad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.twisted")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Magic Dragon AD
def mdad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#Asgard AD
def asgardad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.asgard")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#M.E.T.V AD
def metvad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.metv19")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#KodiVerse AD
def kversead_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.KodiVerse/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.KodiVerse/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.KodiVerse")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)


#4K AD
def fourkad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.4k/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.4k/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.4k")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)

                d_select = ("2")
                addon.setSetting("debrid_select", d_select)
                

#ResolveURL AD
def rurlad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/script.module.resolveurl/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("AllDebridResolver_client_id", your_username)
                addon.setSetting("AllDebridResolver_token", your_token)

                cache_only = ("true")
                addon.setSetting("AllDebridResolver_cached_only", cache_only)


#My Accounts AD
def myaccountsad_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("alldebrid.username")
                your_token = myaccts.getSetting("alldebrid.token")
                
                addon = xbmcaddon.Addon("script.module.myaccounts")
                addon.setSetting("alldebrid.username", your_username)
                addon.setSetting("alldebrid.token", your_token)


def debrid_auth_ad(): #Auth All Supported Addons

        #AllDebrid
        serenad_auth()
        ezraad_auth()
        fenad_auth()
        umbad_auth()
        shadowad_auth()
        ghostad_auth()
        genocidead_auth()
        chainsad_auth()
        moriaad_auth()
        basead_auth()
        twistedad_auth()
        mdad_auth()
        asgardad_auth()
        metvad_auth()
        kversead_auth()
        fourkad_auth()
        rurlad_auth()
        myaccountsad_auth()
