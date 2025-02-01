import xbmc
import xbmcgui
import xbmcaddon
import os
import time
import xbmcvfs
import sqlite3

from sqlite3 import Error
from xml.etree import ElementTree
from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools
from resources.libs.common import var

ORDER = ['fen',
         'fenlt',
         'umb',
         'infinity']

EXTID = {
    'fen': {
        'name'     : 'Fen',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fen',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.EXTFOLD, 'fen_ext'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'external_scraper.module',
        'data'     : ['external_scraper.module', 'external_scraper.name', 'provider.external'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'fenlt': {
        'name'     : 'Fen Light',
        'plugin'   : 'plugin.video.fenlight',
        'saved'    : 'fenlt',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_fanart2.jpg'),
        'file'     : os.path.join(CONFIG.EXTFOLD, 'fenlt_ext'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fenlight/databases', 'settings.db'),
        'default'  : '',
        'data'     : [],
        'activate' : 'Addon.OpenSettings(plugin.video.fenlight)'},
    'umb': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umb',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.EXTFOLD, 'umb_ext'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'external_provider.module',
        'data'     : ['external_provider.module', 'external_provider.name', 'provider.external.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'infinity': {
        'name'     : 'Infinity',
        'plugin'   : 'plugin.video.infinity',
        'saved'    : 'infinity',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media/', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media', 'fanart.png'),
        'file'     : os.path.join(CONFIG.EXTFOLD, 'infinity_ext'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.infinity', 'settings.xml'),
        'default'  : 'external_provider.module',
        'data'     : ['external_provider.module', 'external_provider.name', 'provider.external.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.infinity)'}
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
        xbmc.log('%s: extit.py Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def ext_user(who):
    user_ext = None
    if EXTID[who]:
        name = EXTID[who]['name']
        if os.path.exists(EXTID[who]['path']) and name == 'Fen Light':
            try:
                # Create database connection
                conn = create_conn(var.fenlt_settings_db)
                with conn:
                    cur = conn.cursor()
                    cur.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('external_scraper.module',)) #Get setting to compare
                    auth = cur.fetchone()
                    user_data = str(auth)

                    if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None: #Check if addon is authorized
                        user_ext = None #Return if not authorized
                    else:
                        user_ext = user_data #Return if authorized
                    cur.close()
            except:
                xbmc.log('%s: Extit Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
                pass
            '''elif os.path.exists(ExtID[who]['path']) and name == 'afFENity':
            try:
                conn = create_conn(var.affen_settings_db)
                with conn:
                    cur = conn.cursor()
                    cur.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('easynews_user',))
                    auth = cur.fetchone()
                    user_data = str(auth)

                    if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None:
                        user_ext = None
                    else:
                        user_ext = user_data
                    cur.close()
            except:
                xbmc.log('%s: Extit afFENity Failed!' % var.amgr, xbmc.LOGINFO)
                pass'''
        else:
            if os.path.exists(EXTID[who]['path']):
                try:
                    add = tools.get_addon_by_id(EXTID[who]['plugin'])
                    user_ext = add.getSetting(EXTID[who]['default'])
                except:
                    pass
    return user_ext

def ext_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.EXTFOLD):
        os.makedirs(CONFIG.EXTFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(EXTID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(EXTID[log]['plugin'])
                    default = EXTID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_ext(do, log)
                except:
                    pass
            else:
                logging.log('[Ext Providers Info] {0}({1}) is not installed'.format(EXTID[log]['name'], EXTID[log]['plugin']), level=xbmc.LOGERROR)
        CONFIG.set_setting('extnextsave', tools.get_date(days=3, formatted=True))
    else:
        if EXTID[who]:
            if os.path.exists(EXTID[who]['path']):
                update_ext(do, who)
        else:
            logging.log('[Ext Providers Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def clear_saved(who, over=False):
    if who == 'all':
        for ext in EXTID:
            clear_saved(ext,  True)
    elif EXTID[who]:
        file = EXTID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')

def update_ext(do, who):
    file = EXTID[who]['file']
    settings = EXTID[who]['settings']
    data = EXTID[who]['data']
    addonid = tools.get_addon_by_id(EXTID[who]['plugin'])
    saved = EXTID[who]['saved']
    default = EXTID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = EXTID[who]['name']
    icon = EXTID[who]['icon']

    if do == 'update':
        if name == 'Fen Light':
            pass
        else:
            if not user == '':
                try:
                    root = ElementTree.Element(saved)
                    
                    for setting in data:
                        ext = ElementTree.SubElement(root, 'ext')
                        id = ElementTree.SubElement(ext, 'id')
                        id.text = setting
                        value = ElementTree.SubElement(ext, 'value')
                        value.text = addonid.getSetting(setting)
                      
                    tree = ElementTree.ElementTree(root)
                    tree.write(file)
                    
                    user = addonid.getSetting(default)
                    CONFIG.set_setting(saved, user)
                    
                    logging.log('Ext Providers Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
                except Exception as e:
                    logging.log("[Ext Providers Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
            else:
                logging.log('OffCloud Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('ext'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('Ext Providers Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Ext Providers Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Ext Providers Info Not Found for {0}'.format(name))
    elif do == 'clearaddon':
        logging.log('{0} SETTINGS: {1}'.format(name, settings))
        if name == 'Fen Light':
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
                    logging.log("[Ext Providers Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
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
                    logging.log("[Ecxt Providers Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
            xbmc.executebuiltin('Container.Refresh()')
    
def auto_update(who):
    if who == 'all':
        for log in EXTID:
            if os.path.exists(EXTID[log]['path']):
                auto_update(log)
    elif EXTID[who]:
        if os.path.exists(EXTID[who]['path']):
            u = ext_user(who)
            su = CONFIG.get_setting(EXTID[who]['saved'])
            n = EXTID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                ext_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Ext Providers Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save Ext Providers[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    ext_it('update', who)
            else:
                ext_it('update', who)

def import_list(who):
    if who == 'all':
        for log in EXTID:
            if os.path.exists(EXTID[log]['file']):
                import_list(log)
    elif EXTID[who]:
        if os.path.exists(EXTID[who]['file']):
            file = EXTID[who]['file']
            addonid = tools.get_addon_by_id(EXTID[who]['plugin'])
            saved = EXTID[who]['saved']
            default = EASYID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = EXTID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('ext'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Ext Providers Info: Imported![/COLOR]'.format(CONFIG.COLOR2))

def settings(who):
    user = None
    user = EXTID[who]['name']
    return user

def open_settings(who):
    addonid = tools.get_addon_by_id(EXTID[who]['plugin'])
    addonid.openSettings()
