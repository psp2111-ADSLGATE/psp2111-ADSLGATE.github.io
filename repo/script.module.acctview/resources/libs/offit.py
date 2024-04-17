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

ORDER = ['pov',
         'dradis',
         'acctmgr']

OFFCID = {
    'pov': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'pov',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.OFFCFOLD, 'pov_offc'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : 'oc.token',
        'data'     : ['oc.token', 'oc.account_id', 'oc.enabled', 'oc.torrent.enabled', 'provider.oc_cloud', 'oc_cloud.title_filter', 'check.oc_cloud', 'results.sort_occloud_first', 'oc.priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'dradis': {
        'name'     : 'Dradis',
        'plugin'   : 'plugin.video.dradis',
        'saved'    : 'dradis',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'fanart.png'),
        'file'     : os.path.join(CONFIG.OFFCFOLD, 'dradis_offc'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dradis', 'settings.xml'),
        'default'  : 'offcloud.token',
        'data'     : ['offcloud.token', 'offcloud.username', 'offcloud.enabled', 'oc.cloud.enabled', 'offcloud.priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.dradis)'},
   'acctmgr': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgr',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.OFFCFOLD, 'acctmgr_offc'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : 'offcloud.token',
        'data'     : ['offcloud.token', 'offcloud.pass', 'offcloud.user', 'offcloud.userid', 'offcloud.enabled'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'}
}

def offc_user(who):
    user = None
    if OFFCID[who]:
        if os.path.exists(OFFCID[who]['path']):
            try:
                add = tools.get_addon_by_id(OFFCID[who]['plugin'])
                user = add.getSetting(OFFCID[who]['default'])
            except:
                pass
    return user
    
def offc_it(do, who):
    if not os.path.exists(CONFIG.ADDON_DATA):
        os.makedirs(CONFIG.ADDON_DATA)
    if not os.path.exists(CONFIG.OFFCFOLD):
        os.makedirs(CONFIG.OFFCFOLD)
    if who == 'all':
        for log in ORDER:
            if os.path.exists(OFFCID[log]['path']):
                try:
                    addonid = tools.get_addon_by_id(OFFCID[log]['plugin'])
                    default = OFFCID[log]['default']
                    user = addonid.getSetting(default)
                    
                    update_offc(do, log)
                except:
                    pass
            else:
                logging.log('[OffCloud Info] {0}({1}) is not installed'.format(OFFCID[log]['name'], OFFCID[log]['plugin']), level=xbmc.LOGERROR)
    else:
        if OFFCID[who]:
            if os.path.exists(OFFCID[who]['path']):
                update_offc(do, who)
        else:
            logging.log('[OffCloud Info] Invalid Entry: {0}'.format(who), level=xbmc.LOGERROR)

def clear_saved(who, over=False):
    if who == 'all':
        for offc in OFFCID:
            clear_saved(offc,  True)
    elif OFFCID[who]:
        file = OFFCID[who]['file']
        if os.path.exists(file):
            os.remove(file)
    if not over:
        xbmc.executebuiltin('Container.Refresh()')

def update_offc(do, who):
    file = OFFCID[who]['file']
    settings = OFFCID[who]['settings']
    data = OFFCID[who]['data']
    addonid = tools.get_addon_by_id(OFFCID[who]['plugin'])
    saved = OFFCID[who]['saved']
    default = OFFCID[who]['default']
    user = addonid.getSetting(default)
    suser = CONFIG.get_setting(saved)
    name = OFFCID[who]['name']
    icon = OFFCID[who]['icon']

    if do == 'update':
        if not user == '':
            try:
                root = ElementTree.Element(saved)
                
                for setting in data:
                    offc = ElementTree.SubElement(root, 'offc')
                    id = ElementTree.SubElement(offc, 'id')
                    id.text = setting
                    value = ElementTree.SubElement(offc, 'value')
                    value.text = addonid.getSetting(setting)
                  
                tree = ElementTree.ElementTree(root)
                tree.write(file)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                
                logging.log('OffCloud Info Saved for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[OffCloud Info] Unable to Update {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('OffCloud Info Not Registered for {0}'.format(name))
    elif do == 'restore':
        if os.path.exists(file):
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            try:
                for setting in root.findall('offc'):
                    id = setting.find('id').text
                    value = setting.find('value').text
                    addonid.setSetting(id, value)
                
                user = addonid.getSetting(default)
                CONFIG.set_setting(saved, user)
                logging.log('OffCloud Info Restored for {0}'.format(name), level=xbmc.LOGINFO)
            except Exception as e:
                logging.log("[OffCloud Info] Unable to Restore {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        else:
            logging.log('OffCloud Info Not Found for {0}'.format(name))
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
                logging.log("[OffCloud Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
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
                logging.log("[OffCloud Info] Unable to Clear Addon {0} ({1})".format(who, str(e)), level=xbmc.LOGERROR)
        xbmc.executebuiltin('Container.Refresh()')

def auto_update(who):
    if who == 'all':
        for log in OFFCID:
            if os.path.exists(OFFCID[log]['path']):
                auto_update(log)
    elif OFFCID[who]:
        if os.path.exists(OFFCID[who]['path']):
            u = offc_user(who)
            su = CONFIG.get_setting(OFFCID[who]['saved'])
            n = OFFCID[who]['name']
            if not u or u == '':
                return
            elif su == '':
                offc_it('update', who)
            elif not u == su:
                dialog = xbmcgui.Dialog()

                if dialog.yesno(CONFIG.ADDONTITLE,
                                    "Would you like to save the [COLOR {0}]OffCloud Info[/COLOR] for [COLOR {1}]{2}[/COLOR]?".format(CONFIG.COLOR2, CONFIG.COLOR1, n),
                                    "Addon: [COLOR springgreen][B]{0}[/B][/COLOR]".format(u),
                                    "Saved:[/COLOR] [COLOR red][B]{0}[/B][/COLOR]".format(su) if not su == '' else 'Saved:[/COLOR] [COLOR red][B]None[/B][/COLOR]',
                                    yeslabel="[B][COLOR springreen]Save OffCloud[/COLOR][/B]",
                                    nolabel="[B][COLOR red]No, Cancel[/COLOR][/B]"):
                    offc_it('update', who)
            else:
                offc_it('update', who)

def import_list(who):
    if who == 'all':
        for log in OFFCID:
            if os.path.exists(OFFCID[log]['file']):
                import_list(log)
    elif OFFCID[who]:
        if os.path.exists(OFFCID[who]['file']):
            file = OFFCID[who]['file']
            addonid = tools.get_addon_by_id(OFFCID[who]['plugin'])
            saved = OFFCID[who]['saved']
            default = OFFCID[who]['default']
            suser = CONFIG.get_setting(saved)
            name = OFFCID[who]['name']
            
            tree = ElementTree.parse(file)
            root = tree.getroot()
            
            for setting in root.findall('offc'):
                id = setting.find('id').text
                value = setting.find('value').text
            
                addonid.setSetting(id, value)

            logging.log_notify("[COLOR {0}]{1}[/COLOR]".format(CONFIG.COLOR1, name),
                       '[COLOR {0}]OffCloud Info: Imported![/COLOR]'.format(CONFIG.COLOR2))

def open_settings_offc(who):
    addonid = tools.get_addon_by_id(OFFCID[who]['plugin'])
    addonid.openSettings()
