import xbmc, xbmcaddon
import xbmcvfs
from pathlib import Path
from myaccts.modules import control


#Seren PM
def serenpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.seren/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.seren/settings.xml')
       
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):
                
                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")

                addon = xbmcaddon.Addon("plugin.video.seren")
                addon.setSetting("premiumize.username", your_username)
                addon.setSetting("premiumize.token", your_token)

                enabled_rd = ("false")
                addon.setSetting("realdebrid.enabled", enabled_rd)

                enabled_pm = ("true")
                addon.setSetting("premiumize.enabled", enabled_pm)

                enabled_ad = ("false")
                addon.setSetting("alldebrid.enabled", enabled_ad)


#Ezra PM
def ezrapm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ezra/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ezra/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.ezra")
                addon.setSetting("pm.account_id", your_username)
                addon.setSetting("pm.token", your_token)


#Fen PM
def fenpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.fen/')   
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.fen/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.fen")
                addon.setSetting("pm.account_id", your_username)
                addon.setSetting("pm.token", your_token)


#Umbrella PM
def umbpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.umbrella/')      
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.umbrella/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.umbrella")
                addon.setSetting("premiumizeusername", your_username)
                addon.setSetting("premiumizetoken", your_token)


#Shadow PM
def shadowpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.shadow/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.shadow/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.shadow")
                addon.setSetting("premiumize.token", your_token)

                rd_use = ("false")
                addon.setSetting("debrid_use_rd", rd_use)

                pm_use = ("true")
                addon.setSetting("debrid_use_pm", pm_use)

                ad_use = ("false")
                addon.setSetting("debrid_use_ad", ad_use)

                
#Ghost PM
def ghostpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.ghost/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.ghost/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.ghost")
                addon.setSetting("premiumize.token", your_token)

                rd_use = ("false")
                addon.setSetting("debrid_use_rd", rd_use)

                pm_use = ("true")
                addon.setSetting("debrid_use_pm", pm_use)

                ad_use = ("false")
                addon.setSetting("debrid_use_ad", ad_use)


#Genocide PM
def genocidepm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.Genocide/')      
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.Genocide/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.Genocide")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Chains PM
def chainspm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.thechains/')      
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.thechains/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.thechains")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Moria PM
def moriapm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.moria/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.moria/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.moria")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Base19 PM
def basepm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.base19/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.base19/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.base19")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Twisted PM
def twistedpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.twisted/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.twisted/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.twisted")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Magic Dragon PM
def mdpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.magicdragon/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.magicdragon/settings.xml')
     
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.magicdragon")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#Asgard PM
def asgardpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.asgard/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.asgard/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.asgard")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#M.E.T.V PM
def metvpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.metv19/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.metv19/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.metv19")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#KodiVerse PM
def kversepm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.KodiVerse/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.KodiVerse/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.KodiVerse")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)


#4K PM
def fourkpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.4k/')       
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.4k/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.4k")
                addon.setSetting("premiumize.token", your_token)

                d_select = ("1")
                addon.setSetting("debrid_select", d_select)
                

#ResolveURL PM
def rurlpm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/script.module.resolveurl/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.resolveurl/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("script.module.resolveurl")
                addon.setSetting("PremiumizeMeResolver_token", your_token)

                cache_only = ("true")
                addon.setSetting("PremiumizeMeResolver_cached_only", cache_only)


#My Accounts PM
def myaccountspm_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/script.module.myaccounts/')
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/script.module.myaccounts/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("script.module.myaccounts")
                addon.setSetting("premiumize.username", your_username)

                your_token = myaccts.getSetting("premiumize.token")
                addon.setSetting("premiumize.token", your_token)


#Premiumizer PM
def premiumizer_auth():

        debrid_addon = xbmcvfs.translatePath('special://home/addons/plugin.video.premiumizer/')        
        debrid_file = xbmcvfs.translatePath('special://userdata/addon_data/plugin.video.premiumizer/settings.xml')
        
        if xbmcvfs.exists(debrid_addon) and xbmcvfs.exists(debrid_file):

                myaccts = xbmcaddon.Addon("script.module.myaccts")
                your_username = myaccts.getSetting("premiumize.username")
                your_token = myaccts.getSetting("premiumize.token")
                
                addon = xbmcaddon.Addon("plugin.video.premiumizer")
                addon.setSetting("premiumize.token", your_token)


def debrid_auth_pm(): #Auth All Supported Addons

        #Premiumize       
        serenpm_auth()
        ezrapm_auth()
        fenpm_auth()
        umbpm_auth()
        shadowpm_auth()
        ghostpm_auth()
        genocidepm_auth()
        chainspm_auth()
        moriapm_auth()
        basepm_auth()
        twistedpm_auth()
        mdpm_auth()
        asgardpm_auth()
        metvpm_auth()
        kversepm_auth()
        fourkpm_auth()
        rurlpm_auth()
        myaccountspm_auth()
        premiumizer_auth()
