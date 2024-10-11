import xbmc
import xbmcaddon
import xbmcgui
import xbmcvfs
import glob
import os
import re
try:  # Python 3
    from urllib.parse import quote_plus
    from urllib.request import urlretrieve
except ImportError:  # Python 2
    from urllib import quote_plus
    from urllib import urlretrieve
from resources.libs.common import directory
from resources.libs.common.config import CONFIG

translatePath = xbmcvfs.translatePath
addons = translatePath('special://home/addons/')

def trakt_menu():
    from resources.libs import traktit
    for trakt in traktit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(traktit.TRAKTID[trakt]['plugin'])) or xbmcvfs.exists(addons + translatePath('plugin.video.NightwingLite/')):
            name = traktit.TRAKTID[trakt]['name']
            path = traktit.TRAKTID[trakt]['path']
            saved = traktit.TRAKTID[trakt]['saved']
            file = traktit.TRAKTID[trakt]['file']
            user = CONFIG.get_setting(saved)
            auser = traktit.trakt_user(trakt)
            icon = traktit.TRAKTID[trakt]['icon'] if os.path.exists(path) else CONFIG.ICONTRAKT
            fanart = traktit.TRAKTID[trakt]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Trakt', trakt)
            menu2 = create_save_data_menu('Trakt', trakt)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=trakt)'.format(CONFIG.ADDON_ID, trakt)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': trakt}, icon=icon, description='Your Trakt Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': trakt}, icon=icon, description='Your Trakt Authorizations', fanart=fanart, themeit=CONFIG.THEME3)

def debrid_menu():
    from resources.libs import debridit_rd
    for debrid in debridit_rd.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_rd.DEBRIDID[debrid]['plugin'])) or xbmcvfs.exists(addons + translatePath('plugin.video.NightwingLite/')):
            name = debridit_rd.DEBRIDID[debrid]['name']
            path = debridit_rd.DEBRIDID[debrid]['path']
            saved = debridit_rd.DEBRIDID[debrid]['saved']
            file = debridit_rd.DEBRIDID[debrid]['file']
            user = CONFIG.get_setting(saved)
            auser = debridit_rd.debrid_user(debrid)
            icon = debridit_rd.DEBRIDID[debrid]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = debridit_rd.DEBRIDID[debrid]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Debrid', debrid)
            menu2 = create_save_data_menu('Debrid', debrid)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=debrid)'.format(CONFIG.ADDON_ID, debrid)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': debrid}, icon=icon, description='Your Real-Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': debrid}, icon=icon, description='Your Real-Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)


def premiumize_menu():
    from resources.libs import debridit_pm

    for debrid in debridit_pm.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_pm.DEBRIDID[debrid]['plugin'])) or xbmcvfs.exists(addons + translatePath('plugin.video.NightwingLite/')):
            name = debridit_pm.DEBRIDID[debrid]['name']
            path = debridit_pm.DEBRIDID[debrid]['path']
            saved = debridit_pm.DEBRIDID[debrid]['saved']
            file = debridit_pm.DEBRIDID[debrid]['file']
            user = CONFIG.get_setting(saved)
            auser = debridit_pm.debrid_user(debrid)
            icon = debridit_pm.DEBRIDID[debrid]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = debridit_pm.DEBRIDID[debrid]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Debrid', debrid)
            menu2 = create_save_data_menu('Debrid', debrid)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=debrid)'.format(CONFIG.ADDON_ID, debrid)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': debrid}, icon=icon, description='Your Premiumize Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': debrid}, icon=icon, description='Your Premiumize Authorizations', fanart=fanart, themeit=CONFIG.THEME3)

def alldebrid_menu():
    from resources.libs import debridit_ad

    for debrid in debridit_ad.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_ad.DEBRIDID[debrid]['plugin'])) or xbmcvfs.exists(addons + translatePath('plugin.video.NightwingLite/')):
            name = debridit_ad.DEBRIDID[debrid]['name']
            path = debridit_ad.DEBRIDID[debrid]['path']
            saved = debridit_ad.DEBRIDID[debrid]['saved']
            file = debridit_ad.DEBRIDID[debrid]['file']
            user = CONFIG.get_setting(saved)
            auser = debridit_ad.debrid_user(debrid)
            icon = debridit_ad.DEBRIDID[debrid]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = debridit_ad.DEBRIDID[debrid]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Debrid', debrid)
            menu2 = create_save_data_menu('Debrid', debrid)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=debrid)'.format(CONFIG.ADDON_ID, debrid)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': debrid}, icon=icon, description='Your All-Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': debrid}, icon=icon, description='Your All-Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)

def offcloud_menu():
    from resources.libs import offit

    for offc in offit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(offit.OFFCID[offc]['plugin'])):
            name = offit.OFFCID[offc]['name']
            path = offit.OFFCID[offc]['path']
            saved = offit.OFFCID[offc]['saved']
            file = offit.OFFCID[offc]['file']
            user = CONFIG.get_setting(saved)
            auser = offit.offc_user(offc)
            icon = offit.OFFCID[offc]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = offit.OFFCID[offc]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('OffCloud', offc)
            menu2 = create_save_data_menu('OffCloud', offc)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=offc)'.format(CONFIG.ADDON_ID, offc)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': offc}, icon=icon, description='Your All-Easy Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': offc}, icon=icon, description='Your All-Easy Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
                
def easynews_menu():
    from resources.libs import easyit

    for easy in easyit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(easyit.EASYID[easy]['plugin'])):
            name = easyit.EASYID[easy]['name']
            path = easyit.EASYID[easy]['path']
            saved = easyit.EASYID[easy]['saved']
            file = easyit.EASYID[easy]['file']
            user = CONFIG.get_setting(saved)
            auser = easyit.easy_user(easy)
            icon = easyit.EASYID[easy]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = easyit.EASYID[easy]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Easynews', easy)
            menu2 = create_save_data_menu('Easynews', easy)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=easy)'.format(CONFIG.ADDON_ID, easy)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': easy}, icon=icon, description='Your All-Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': easy}, icon=icon, description='Your All-Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)

def filepursuit_menu():
    from resources.libs import fileit

    for filep in fileit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(fileit.FILEID[filep]['plugin'])):
            name = fileit.FILEID[filep]['name']
            path = fileit.FILEID[filep]['path']
            saved = fileit.FILEID[filep]['saved']
            file = fileit.FILEID[filep]['file']
            user = CONFIG.get_setting(saved)
            auser = fileit.filep_user(filep)
            icon = fileit.FILEID[filep]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = fileit.FILEID[filep]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Filepursuit', filep)
            menu2 = create_save_data_menu('Filepursuit', filep)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=file)'.format(CONFIG.ADDON_ID, filep)))

            if not auser:
                directory.add_file('{0} - [COLOR red]Not Authorized[/COLOR]'.format(name), {'name': filep}, icon=icon, description='Your All-Easy Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('{0} - [COLOR springgreen]Authorized[/COLOR]'.format(name), {'name': filep}, icon=icon, description='Your All-Easy Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
                
def all_accounts_menu():
    from resources.libs import debridit_all

    for debrid in debridit_all.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_all.DEBRIDID[debrid]['plugin'])):
            name = debridit_all.DEBRIDID[debrid]['name']
            path = debridit_all.DEBRIDID[debrid]['path']
            saved = debridit_all.DEBRIDID[debrid]['saved']
            file = debridit_all.DEBRIDID[debrid]['file']
            user = CONFIG.get_setting(saved)
            user_rd = debridit_all.debrid_user_rd(debrid)
            user_pm = debridit_all.debrid_user_pm(debrid)
            user_ad = debridit_all.debrid_user_ad(debrid)
            icon = debridit_all.DEBRIDID[debrid]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = debridit_all.DEBRIDID[debrid]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Debrid', debrid)
            menu2 = create_save_data_menu('Debrid', debrid)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=debrid)'.format(CONFIG.ADDON_ID, debrid)))

            directory.add_file('{0}'.format(name), {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            
            if not user_rd:
                directory.add_file('Real-Debrid - [COLOR red]Not Authorized[/COLOR]', {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('Real-Debrid - [COLOR springgreen]Authorized[/COLOR]', {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            
            if not user_pm:
                directory.add_file('Premiumize - [COLOR red]Not Authorized[/COLOR]', {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('Premiumize - [COLOR springgreen]Authorized[/COLOR]', {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            
            if not user_ad:
                directory.add_file('All-Debrid - [COLOR red]Not Authorized[/COLOR]', {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            else:
                directory.add_file('All-Debrid - [COLOR springgreen]Authorized[/COLOR]', {'name': debrid}, icon=icon, description='Your Debrid Authorizations', fanart=fanart, themeit=CONFIG.THEME3)
            
            directory.add_separator_allaccts()
           
def meta_accounts_menu():
    from resources.libs import metait_all

    for debrid in metait_all.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(metait_all.DEBRIDID[debrid]['plugin'])):
            name = metait_all.DEBRIDID[debrid]['name']
            path = metait_all.DEBRIDID[debrid]['path']
            saved = metait_all.DEBRIDID[debrid]['saved']
            file = metait_all.DEBRIDID[debrid]['file']
            user = CONFIG.get_setting(saved)
            user_fanart = metait_all.debrid_user_fanart(debrid)
            user_omdb = metait_all.debrid_user_omdb(debrid)
            user_mdb = metait_all.debrid_user_mdb(debrid)
            user_imdb = metait_all.debrid_user_imdb(debrid)
            user_tvdb = metait_all.debrid_user_tvdb(debrid)
            user_tmdb = metait_all.debrid_user_tmdb(debrid)
            user_tmdb_user = metait_all.debrid_user_tmdb_user(debrid)
            user_tmdb_pass = metait_all.debrid_user_tmdb_pass(debrid)
            user_tmdb_session = metait_all.debrid_user_tmdb_session(debrid)
            icon = metait_all.DEBRIDID[debrid]['icon'] if os.path.exists(path) else CONFIG.ICONDEBRID
            fanart = metait_all.DEBRIDID[debrid]['fanart'] if os.path.exists(path) else CONFIG.ADDON_FANART
            menu = create_addon_data_menu('Debrid', debrid)
            menu2 = create_save_data_menu('Debrid', debrid)
            menu.append((CONFIG.THEME2.format('{0} Settings'.format(name)), 'RunPlugin(plugin://{0}/?mode=opensettings&name={1}&url=debrid)'.format(CONFIG.ADDON_ID, debrid)))

            directory.add_file('{0}'.format(name), {'mode': 'opendebridsettings', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, themeit=CONFIG.THEME3)

            if user_fanart == None or len(user_fanart) == 1:
                directory.add_file('[COLOR red]Fanart.TV API Key - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_fanart) > 1:
                directory.add_file('[COLOR springgreen]Fanart.TV API Key: {0}[/COLOR]'.format(user_fanart), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_omdb == None or len(user_omdb) == 1:
                directory.add_file('[COLOR red]OMDb API Key - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_omdb) > 1:
                directory.add_file('[COLOR springgreen]OMDb API Key: {0}[/COLOR]'.format(user_omdb), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_mdb == None or len(user_mdb) == 1:
                directory.add_file('[COLOR red]MDbList API Key - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_mdb) > 1:
                directory.add_file('[COLOR springgreen]MDbList API Key: {0}[/COLOR]'.format(user_mdb), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_imdb == None or len(user_imdb) == 1:
                directory.add_file('[COLOR red]IMDb API Key - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_imdb) > 1:
                directory.add_file('[COLOR springgreen]IMDb API Key: {0}[/COLOR]'.format(user_imdb), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_tvdb == None or len(user_tvdb) == 1:
                directory.add_file('[COLOR red]TVDb API Key - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_tvdb) > 1:
                directory.add_file('[COLOR springgreen]TVDb API Key: {0}[/COLOR]'.format(user_tvdb), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_tmdb == None or len(user_tmdb) == 1:
                directory.add_file('[COLOR red]TMDb API Key - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_tmdb) > 1:
                directory.add_file('[COLOR springgreen]TMDb API Key: {0}[/COLOR]'.format(user_tmdb), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_tmdb_user == None or len(user_tmdb_user) == 1:
                directory.add_file('[COLOR red]TMDb Username - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_tmdb_user) > 1:
                directory.add_file('[COLOR springgreen]TMDb Username: {0}[/COLOR]'.format(user_tmdb_user), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_tmdb_pass == None or len(user_tmdb_pass) == 1:
                directory.add_file('[COLOR red]TMDb Password - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_tmdb_pass) > 1:
                directory.add_file('[COLOR springgreen]TMDb Password: {0}[/COLOR]'.format(user_tmdb_pass), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass

            if user_tmdb_session == None or len(user_tmdb_session) == 1:
                directory.add_file('[COLOR red]TMDb Session ID - No Data Found![/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            elif len(user_tmdb_session) > 1:
                directory.add_file('[COLOR springgreen]TMDb Session ID: {0}[/COLOR]'.format(user_tmdb_session), icon=icon, description='View Your Metadata Accounts', fanart=fanart, menu=menu)
            else:
                pass
            
            directory.add_separator_meta()
            
def create_addon_data_menu(add='', name=''):
    menu_items = []

    add2 = quote_plus(add.lower().replace(' ', ''))
    add3 = add.replace('Debrid', 'Real Debrid')
    name2 = quote_plus(name.lower().replace(' ', ''))
    name = name.replace('url', 'URL Resolver')
    menu_items.append((CONFIG.THEME2.format(name.title()), ' '))
    menu_items.append((CONFIG.THEME3.format('Save {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=save{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Restore {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=restore{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Clear {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=clear{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))

    menu_items.append((CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID)))

    return menu_items


def create_save_data_menu(add='', name=''):
    menu_items = []

    add2 = quote_plus(add.lower().replace(' ', ''))
    add3 = add.replace('Debrid', 'Real Debrid')
    name2 = quote_plus(name.lower().replace(' ', ''))
    name = name.replace('url', 'URL Resolver')
    menu_items.append((CONFIG.THEME2.format(name.title()), ' '))
    menu_items.append((CONFIG.THEME3.format('Register {0}'.format(add3)), 'RunPlugin(plugin://{0}/?mode=auth{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Save {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=save{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Restore {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=restore{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Import {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=import{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))
    menu_items.append((CONFIG.THEME3.format('Clear Addon {0} Data'.format(add3)), 'RunPlugin(plugin://{0}/?mode=addon{1}&name={2})'.format(CONFIG.ADDON_ID, add2, name2)))

    menu_items.append((CONFIG.THEME2.format('{0} Settings'.format(CONFIG.ADDONTITLE)), 'RunPlugin(plugin://{0}/?mode=settings)'.format(CONFIG.ADDON_ID)))

    return menu_items
