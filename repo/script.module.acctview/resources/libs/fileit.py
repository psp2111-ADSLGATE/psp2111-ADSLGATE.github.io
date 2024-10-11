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

ORDER = ['umbrella',
         'infinity',
         'dradis',
         'allact',
         'myact',
         'acctmgr']

FILEID = {
    'umbrella': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbrella',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.FILEFOLD, 'umbrella_file'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'filepursuit.api',
        'data'     : ['filepursuit.enable', 'filepursuit.api', 'filepursuit.priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'infinity': {
        'name'     : 'Infinity',
        'plugin'   : 'plugin.video.infinity',
        'saved'    : 'infinity',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity/resources/media/', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.infinity', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.FILEFOLD, 'infinity_file'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.infinity', 'settings.xml'),
        'default'  : 'filepursuit.api',
        'data'     : ['filepursuit.enable', 'filepursuit.api', 'filepursuit.priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.infinity)'},
    'dradis': {
        'name'     : 'Dradis',
        'plugin'   : 'plugin.video.dradis',
        'saved'    : 'dradis',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.FILEFOLD, 'dradis_file'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dradis', 'settings.xml'),
        'default'  : 'filepursuit.api',
        'data'     : ['filepursuit.api', 'filepursuit.priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.dradis)'},
   'acctmgr': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.FILEFOLD, 'acctmgr_file'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : 'filepursuit.api.key',
        'data'     : ['filepursuit.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'},
    'allact': {
        'name'     : 'All Accounts',
        'plugin'   : 'script.module.allaccounts',
        'saved'    : 'allact',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.FILEFOLD, 'allact_file'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.allaccounts', 'settings.xml'),
        'default'  : 'filepursuit.api.key',
        'data'     : ['filepursuit.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.allaccounts)'},
    'myact': {
        'name'     : 'My Accounts',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myact',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.FILEFOLD, 'myact_file'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'filepursuit.api.key',
        'data'     : ['filepursuit.api.key'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'}
}

def filep_user(who):
    user = None
    if FILEID[who]:
        if os.path.exists(FILEID[who]['path']):
            try:
                add = tools.get_addon_by_id(FILEID[who]['plugin'])
                user = add.getSetting(FILEID[who]['default'])
            except:
                pass
    return user
    
def filep_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.FILEFOLD):
        os.makedirs(CONFIG.FILEFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(FILEID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(FILEID[log]['plugin'])
                    default = FILEID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_filep(do, log)
                except:
                    pass
            else:
                logging.log('[Filepursuit Info] {0}({1}) is not installed'.format(FILEID[log]['name'], FILEID[log]['plugin']), level=xbmc.LOGERROR)
    else:
        if FILEID[who]:
            if os.path.exists(FILEID[who]['path']):
                update_filep(do, who)
        else:
            logging.log('[Filepursuit Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def clear_saved(who, over=False):
    if who == 'all':
        for filep in FILEID:
            clear_saved(filep,  True)
    elif FILEID[who]:
        file = FILEID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')

def update_filep(do, who):
    file = FILEID[who]['file']
    settings = FILEID[who]['settings']
    data = FILEID[who]['data']
    addonid = tools.get_addon_by_id(FILEID[who]['plugin'])
    saved = FILEID[who]['saved']
    default = FILEID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = FILEID[who]['name']
    icon = FILEID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    filep = ElementTree.SubElement(root, 'filep')
                    id = ElementTree.SubElement(filep, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(filep, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('Filepursuit Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Filepursuit Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Filepursuit Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('filep'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('Filepursuit Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[Filepursuit Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('Filepursuit Info Not Found for {0}'.format(name))
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
                logging.log("[Filepursuit Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        xbmc.executebuiltin('Container.Refresh()')
    elif do == 'wipeaddon':
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
                
            except Exception as e:
                logging.log("[Filepursuit Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        xbmc.executebuiltin('Container.Refresh()')

def auto_update(who):
    if who == 'all':
        for log in FILEID:
            if os.path.exists(FILEID[log]['path']):
                auto_update(log)
    elif FILEID[who]:
        if os.path.exists(FILEID[who]['path']):
            u = filep_user(who)
            su = CONFIG.get_setting(FILEID[who]['saved'])
            n = FILEID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                filep_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]Filepursuit Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save Filepursuit[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    filep_it('update', who)
            else:
                filep_it('update', who)

def import_list(who):
    if who == 'all':
        for log in FILEID:
            if os.path.exists(FILEID[log]['file']):
                import_list(log)
    elif FILEID[who]:
        if os.path.exists(FILEID[who]['file']):
            file = FILEID[who]['file']
            addonid = tools.get_addon_by_id(FILEID[who]['plugin'])
            saved = FILEID[who]['saved']
            default = FILEID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = FILEID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('filep'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]Filepursuit Info: Imported![/COLOR]'.format(CONFIG.COLOR2))

def open_settings_filep(who):
    addonid = tools.get_addon_by_id(FILEID[who]['plugin'])
    addonid.openSettings()

