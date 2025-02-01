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

ORDER = ['fenlt',
         'umb',
         'pov',
         'infin',
         'dradis',
         'otaku',
         'acctmgr']

TBID = {
    'fenlt': {
        'name'     : 'Fen Light',
        'plugin'   : 'plugin.video.fenlight',
        'saved'    : 'fenlt',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_fanart2.jpg'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'fenlt_tb'),
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
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'umb_tb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'torboxtoken',
        'data'     : ['torboxtoken', 'torbox.username', 'torbox.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'pov': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'pov',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'pov_tb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : 'tb.token',
        'data'     : ['tb.token', 'tb.account_id', 'tb.expires', 'tb.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'infin': {
        'name'     : 'Infinity',
        'plugin'   : 'plugin.video.infinity',
        'saved'    : 'infin',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'infinity_tb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.infinity', 'settings.xml'),
        'default'  : 'torboxtoken',
        'data'     : ['torboxtoken', 'torbox.username', 'torbox.enabled', 'torbox.priority', 'torbox.saveToCloud', 'tb_cloud.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.infinity)'},
    'dradis': {
        'name'     : 'Dradis',
        'plugin'   : 'plugin.video.dradis',
        'saved'    : 'dradis',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'dradis_tb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dradis', 'settings.xml'),
        'default'  : 'torbox.token',
        'data'     : ['torbox.token', 'torbox.username', 'torbox.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.dradis)'},
    'otaku': {
        'name'     : 'Otaku',
        'plugin'   : 'plugin.video.otaku',
        'saved'    : 'otaku',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'otaku_tb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.otaku', 'settings.xml'),
        'default'  : 'tb.apikey',
        'data'     : ['tb.apikey', 'tb.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.otaku)'},
   'acctmgr': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.TBFOLD, 'acctmgr_tb'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : 'torbox.token',
        'data'     : ['torbox.token', 'torbox.acct_id', 'torbox.enabled'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'}
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
        xbmc.log('%s: tbit.py Failed!' % var.amgr, xbmc.LOGINFO)
        pass
    
def tb_user(who):
    user_tb = None
    if TBID[who]:
       name = TBID[who]['name']
       if os.path.exists(TBID[who]['path']) and name == 'Fen Light':
           try:
               # Create database connection
               conn = create_conn(var.fenlt_settings_db)
               with conn:
                   cur = conn.cursor()
                   cur.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('tb.token',)) #Get setting to compare
                   auth = cur.fetchone()
                   user_data = str(auth)

                   if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None: #Check if addon is authorized
                       user_tb = None #Return if not authorized
                   else:
                       user_tb = user_data #Return if authorized
                   cur.close()
           except:
               xbmc.log('%s: Tbit Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
               pass
       else:
           if os.path.exists(TBID[who]['path']):
               try:
                   add = tools.get_addon_by_id(TBID[who]['plugin'])
                   user_tb = add.getSetting(TBID[who]['default'])
               except:
                   pass
    return user_tb
    
def tb_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.TBFOLD):
        os.makedirs(CONFIG.TBFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(TBID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(TBID[log]['plugin'])
                    default = TBID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_tb(do, log)
                except:
                    pass
            else:
                logging.log('[TorBox Info] {0}({1}) is not installed'.format(TBID[log]['name'], TBID[log]['plugin']), level=xbmc.LOGERROR)
    else:
        if TBID[who]:
            if os.path.exists(TBID[who]['path']):
                update_tb(do, who)
        else:
            logging.log('[TorBox Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def clear_saved(who, over=False):
    if who == 'all':
        for tb in TBID:
            clear_saved(tb,  True)
    elif TBID[who]:
        file = TBID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')

def update_tb(do, who):
    file = TBID[who]['file']
    settings = TBID[who]['settings']
    data = TBID[who]['data']
    addonid = tools.get_addon_by_id(TBID[who]['plugin'])
    saved = TBID[who]['saved']
    default = TBID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = TBID[who]['name']
    icon = TBID[who]['icon']

    if do == 'update':
        if name == 'Fen Light':
            pass
        else:
            if not user == '':
                try:
                    root = ElementTree.Element(saved)
                    for setting in data:
                        tb = ElementTree.SubElement(root, 'tb')
                        id = ElementTree.SubElement(tb, 'id')
                        id.text = setting
                        value = ElementTree.SubElement(tb, 'value')
                        value.text = addonid.getSetting(setting)
                      
                    tree = ElementTree.ElementTree(root)
                    tree.write(file)
                    user = addonid.getSetting(default)
                    CONFIG.set_setting(saved, user)
                    
                    logging.log('TorBox Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
                except Exception as e:
                    logging.log("[TorBox Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
            else:
                logging.log('TorBox Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('tb'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('TorBox Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[TorBox Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('TorBox Info Not Found for {0}'.format(name))
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
                logging.log("[TorBocx Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
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
                    logging.log("[TorBox Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
            xbmc.executebuiltin('Container.Refresh()')

def auto_update(who):
    if who == 'all':
        for log in TBID:
            if os.path.exists(TBID[log]['path']):
                auto_update(log)
    elif TBID[who]:
        if os.path.exists(TBID[who]['path']):
            u = tb_user(who)
            su = CONFIG.get_setting(TBID[who]['saved'])
            n = TBID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                tb_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]OffCloud Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save OffCloud[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    tb_it('update', who)
            else:
                tb_it('update', who)

def import_list(who):
    if who == 'all':
        for log in TBID:
            if os.path.exists(TBID[log]['file']):
                import_list(log)
    elif TBID[who]:
        if os.path.exists(TBID[who]['file']):
            file = TBID[who]['file']
            addonid = tools.get_addon_by_id(TBID[who]['plugin'])
            saved = TBID[who]['saved']
            default = TBID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = TBID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('tb'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]TorBox Info: Imported![/COLOR]'.format(CONFIG.COLOR2))

def settings(who):
    user = None
    user = TBID[who]['name']
    return user

def open_settings(who):
    addonid = tools.get_addon_by_id(TBID[who]['plugin'])
    addonid.openSettings()
