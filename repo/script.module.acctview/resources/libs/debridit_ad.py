import xbmc
import xbmcaddon
import xbmcgui
import os.path
import xbmcvfs
import os
import time
import sqlite3

from sqlite3 import Error
from xml.etree import ElementTree
from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common import var

ORDER = ['serenad',
         'fenad',
         'fenltad',
         'coalad', 
         'povad',
         'umbad',
         'infinityad',
         'dradisad',
         'shadowad',
         'ghostad',
         'basead',
         'chainsad',
         'asgardad',
         'metvad',
         'aliundead',
         'nightlitead',
         'patriotad',
         'blacklad',
         'otakuad',
         'acctmgrad',
         'allactad',
         'myactad',
         'rurlad']

DEBRIDID = {
    'serenad': {
        'name'     : 'Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'ico-seren-3.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'fanart-seren-3.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'seren_ad'), #Backup location
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.enabled', 'alldebrid.username', 'alldebrid.apikey'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'fenad': {
        'name'     : 'Fen',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'fen_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'ad.account_id',
        'data'     : ['ad.token', 'ad.enabled', 'ad.account_id'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'fenltad': {
        'name'     : 'Fen Light',
        'plugin'   : 'plugin.video.fenlight',
        'saved'    : 'fenltad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_fanart2.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'fenlt_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fenlight/databases', 'settings.db'),
        'fenlt'    : '',
        'data'     : [],
        'activate' : 'Addon.OpenSettings(plugin.video.fenlight)'},
    'coalad': {
        'name'     : 'The Coalition',
        'plugin'   : 'plugin.video.coalition',
        'saved'    : 'coalad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'coal_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.coalition', 'settings.xml'),
        'default'  : 'ad.account_id',
        'data'     : ['ad.account_id', 'ad.enabled', 'ad.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.coalition)'},
    'povad': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'povad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'pov_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : 'ad.account_id',
        'data'     : ['ad.account_id', 'ad.enabled', 'ad.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'umbad': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'umb_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'alldebridusername',
        'data'     : ['alldebridusername', 'alldebridtoken', 'alldebrid.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'infinityad': {
        'name'     : 'Infinity',
        'plugin'   : 'plugin.video.infinity',
        'saved'    : 'infinityad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media/', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'infinity_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.infinity', 'settings.xml'),
        'default'  : 'alldebridusername',
        'data'     : ['alldebridusername', 'alldebridtoken', 'alldebrid.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.infinity)'},
    'dradisad': {
        'name'     : 'Dradis',
        'plugin'   : 'plugin.video.dradis',
        'saved'    : 'dradisad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'dradis_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dradis', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'alldebrid.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.dradis)'},
    'shadowad': {
        'name'     : 'Shadow',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'shadow_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'ghostad': {
        'name'     : 'Ghost',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghostad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'ghost_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'basead': {
        'name'     : 'Base',
        'plugin'   : 'plugin.video.base',
        'saved'    : 'base',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'base_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.base)'},
    'chainsad': {
        'name'     : 'Chains Reaction',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chainsad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'chains_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'asgardad': {
        'name'     : 'Asgard',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgardad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'asgard_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'patriotad': {
        'name'     : 'Patriot',
        'plugin'   : 'plugin.video.patriot',
        'saved'    : 'patriotad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'patriot_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.patriot', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.patriot)'},
    'blacklad': {
        'name'     : 'Black Lightning',
        'plugin'   : 'plugin.video.blacklightning',
        'saved'    : 'blacklad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'blackl_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.blacklightning', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.blacklightning)'},
    'metvad': {
        'name'     : 'M.E.T.V',
        'plugin'   : 'plugin.video.metv19',
        'saved'    : 'metvad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'metv_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.metv19', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.metv19)'},
    'aliundead': {
        'name'     : 'Aliunde K19',
        'plugin'   : 'plugin.video.aliundek19',
        'saved'    : 'aliundead',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'aliunde_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.aliundek19', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.aliundek19)'},
    'nightlitead': {
        'name'     : 'Nightwing Lite',
        'plugin'   : 'plugin.video.NightwingLite',
        'saved'    : 'nightlitead',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.NightwingLite'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.NightwingLite', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.NightwingLite', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'nightlite_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.NightwingLite', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.NightwingLite)'},
    'otakuad': {
        'name'     : 'Otaku',
        'plugin'   : 'plugin.video.otaku',
        'saved'    : 'otakuad',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'otaku_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.otaku', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.username', 'alldebrid.apikey', 'alldebrid.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.otaku)'},
   'acctmgrad': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgrad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'acctmgr_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.token', 'alldebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'},
   'allactad': {
        'name'     : 'All Accounts',
        'plugin'   : 'script.module.allaccounts',
        'saved'    : 'allactad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'allact_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.allaccounts', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.token', 'alldebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.allaccounts)'},
   'myactad': {
        'name'     : 'My Accounts',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myactad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'myact_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'alldebrid.username',
        'data'     : ['alldebrid.token', 'alldebrid.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
    'rurlad': {
        'name'     : 'ResolveURL',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlad',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_AD, 'rurl_ad'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'AllDebridResolver_client_id',
        'data'     : ['AllDebridResolver_client_id', 'AllDebridResolver_enabled', 'AllDebridResolver_login', 'AllDebridResolver_priority', 'AllDebridResolver_token', 'AllDebridResolver_torrents', 'AllDebridResolver_cached_only'],
        'activate' : 'Addon.OpenSettings(script.module.resolveurl)'}
}

def create_conn(db_file):
    try:
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except Error as e:
            print(e)
            
        return conn
    except:
        xbmc.log('%s: Debridit_ad Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def debrid_user(who):
    user = None
    if DEBRIDID[who]:
        name = DEBRIDID[who]['name']
        if os.path.exists(DEBRIDID[who]['path']) and name == 'Fen Light':
            try:
                # Create database connection
                conn = create_conn(var.fenlt_settings_db)
                with conn:
                    cur = conn.cursor()
                    cur.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('ad.token',)) #Get setting to compare
                    auth = cur.fetchone()
                    user_data = str(auth)

                    if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None: #Check if addon is authorized
                        user = None #Return if not authorized
                    else:
                        user = user_data #Return if authorized
                    cur.close()
            except:
                xbmc.log('%s: Debridit_ad Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            '''elif os.path.exists(DEBRIDID[who]['path']) and name == 'afFENity':
            try:
                conn = create_conn(var.affen_settings_db)
                with conn:
                    cur = conn.cursor()
                    cur.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('ad.token',))
                    auth = cur.fetchone()
                    user_data = str(auth)

                    if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None:
                        user = None
                    else:
                        user = user_data
                    cur.close()
            except:
                xbmc.log('%s: Debridit_ad afFENity Failed!' % var.amgr, xbmc.LOGINFO)
                pass'''
        else:
            if os.path.exists(DEBRIDID[who]['path']):
                try:
                    add = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
                    user = add.getSetting(DEBRIDID[who]['default'])
                except:
                    pass
    return user

def debrid_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.DEBRIDFOLD_AD):
        os.makedirs(CONFIG.DEBRIDFOLD_AD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(DEBRIDID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(DEBRIDID[log]['plugin'])
                    default = DEBRIDID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_debrid(do, log)
                except:
                    pass
            else:
                logging.log('[Debrid Info] {0}({1}) is not installed'.format(DEBRIDID[log]['name'], DEBRIDID[log]['plugin']), level=xbmc.LOGERROR)
    else:
        if DEBRIDID[who]:
            if os.path.exists(DEBRIDID[who]['path']):
                update_debrid(do, who)
        else:
            logging.log('[Debrid Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def clear_saved(who, over=False):
    if who == 'all':
        for debrid in DEBRIDID:
            clear_saved(debrid,  True)
    elif DEBRIDID[who]:
        file = DEBRIDID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')

def update_debrid(do, who):
    file = DEBRIDID[who]['file']
    settings = DEBRIDID[who]['settings']
    data = DEBRIDID[who]['data']
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    saved = DEBRIDID[who]['saved']
    default = DEBRIDID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = DEBRIDID[who]['name']
    icon = DEBRIDID[who]['icon']

    if do == 'update':
        if name == 'Fen Light':
            pass
        else:
            if not user == '':
                try:
                    root = ElementTree.Element(saved)
                    
                    for setting in data:
                        debrid = ElementTree.SubElement(root, 'debrid')
                        id = ElementTree.SubElement(debrid, 'id')
                        id.text = setting
                        value = ElementTree.SubElement(debrid, 'value')
                        value.text = addonid.getSetting(setting)
                      
                    tree = ElementTree.ElementTree(root)
                    tree.write(file)
                    
                    user = addonid.getSetting(default)
                    CONFIG.set_setting(saved, user)
                    
                    logging.log('Debrid Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
                except Exception as e:
                    logging.log("[Debrid Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
            else:
                logging.log('Debrid Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('debrid'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Debrid Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Debrid Info Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if os.path.exists(settings):
            try:
                tree = ElementTree.parse(settings)
                root = tree.getroot()
                
                for setting in root.findall('setting'):
                    if setting.attrib['id'] in data:
                        logging.log('Removing Setting: {0}'.format(setting.attrib))
                        root.remove(setting)
                            
                tree.write(settings)
                
                logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                                   '[COLOR {0}]Addon Data: Cleared![/COLOR]'.format(CONFIG.COLOR2),
                                   2000,
                                   icon)
            except Exception as e:
                logging.log("[Debrid Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        xbmc.executebuiltin('Container.Refresh()')
    elif do == 'wipeaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if name == 'Fen Light':
        #if name == 'Fen Light' or name == 'afFENity':
            pass
        else:
            if os.path.exists(settings):
                try:
                    tree = ElementTree.parse(settings)
                    root = tree.getroot()
                    
                    for setting in root.findall('setting'):
                        if setting.attrib['id'] in data:
                            logging.log('Removing Setting: {0}'.format(setting.attrib))
                            root.remove(setting)
                                
                    tree.write(settings)
                    
                except Exception as e:
                    logging.log("[Debrid Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
            xbmc.executebuiltin('Container.Refresh()')

def auto_update(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['path']):
                auto_update(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['path']):
            u = debrid_user(who)
            su = CONFIG.get_setting(DEBRIDID[who]['saved'])
            n = DEBRIDID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                debrid_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Debrid Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save Debrid[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    debrid_it('update', who)
            else:
                debrid_it('update', who)

def import_list(who):
    if who == 'all':
        for log in DEBRIDID:
            if os.path.exists(DEBRIDID[log]['file']):
                import_list(log)
    elif DEBRIDID[who]:
        if os.path.exists(DEBRIDID[who]['file']):
            file = DEBRIDID[who]['file']
            addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
            saved = DEBRIDID[who]['saved']
            default = DEBRIDID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = DEBRIDID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('debrid'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Debrid Info: Imported![/COLOR]'.format(CONFIG.COLOR2))

def settings(who):
    user = None
    user = DEBRIDID[who]['name']
    return user

def open_settings(who):
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    addonid.openSettings()

