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

def trakt_menu():
    from resources.libs import traktit

    for trakt in traktit.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(traktit.TRAKTID[trakt]['plugin'])):
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

            directory.add_file('{0}'.format(name), {'mode': 'opentraktsettings', 'name': trakt}, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)
            
            if not os.path.exists(path):
                directory.add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                directory.add_file('[COLOR red]Addon Data: Not Authorised[/COLOR]', {'mode': 'authtrakt', 'name': trakt}, icon=icon, fanart=fanart, menu=menu)
            else:
                directory.add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), {'mode': 'authtrakt', 'name': trakt}, icon=icon, fanart=fanart, menu=menu)

def debrid_menu():
    from resources.libs import debridit_rd

    for debrid in debridit_rd.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_rd.DEBRIDID[debrid]['plugin'])):
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

            directory.add_file('{0}'.format(name), {'mode': 'opendebridsettings', 'name': debrid}, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)

            if not os.path.exists(path):
                directory.add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                directory.add_file('[COLOR red]Addon Data: Not Authorized[/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, fanart=fanart, menu=menu)
            else:
                directory.add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), icon=icon, fanart=fanart, menu=menu)
                
def premiumize_menu():
    from resources.libs import debridit_pm

    for debrid in debridit_pm.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_pm.DEBRIDID[debrid]['plugin'])):
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

            directory.add_file('{0}'.format(name), {'mode': 'opendebridsettings', 'name': debrid}, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)

            if not os.path.exists(path):
                directory.add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                directory.add_file('[COLOR red]Addon Data: Not Authorized[/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, fanart=fanart, menu=menu)
            else:
                directory.add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), icon=icon, fanart=fanart, menu=menu)


def alldebrid_menu():
    from resources.libs import debridit_ad

    for debrid in debridit_ad.ORDER:
        if xbmc.getCondVisibility('System.HasAddon({0})'.format(debridit_ad.DEBRIDID[debrid]['plugin'])):
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

            directory.add_file('{0}'.format(name), {'mode': 'opendebridsettings', 'name': debrid}, icon=icon, fanart=fanart, themeit=CONFIG.THEME3)

            if not os.path.exists(path):
                directory.add_file('[COLOR red]Addon Data: Not Installed[/COLOR]', icon=icon, fanart=fanart, menu=menu)
            elif not auser:
                directory.add_file('[COLOR red]Addon Data: Not Authorized[/COLOR]', {'mode': 'authdebrid', 'name': debrid}, icon=icon, fanart=fanart, menu=menu)
            else:
                directory.add_file('[COLOR springgreen]Addon Data: {0}[/COLOR]'.format(auser), icon=icon, fanart=fanart, menu=menu)

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
