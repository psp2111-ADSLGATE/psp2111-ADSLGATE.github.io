import xbmc
import xbmcaddon
import xbmcgui

import os
import time

from xml.etree import ElementTree

from resources.libs.common.config import CONFIG
from resources.libs.common import logging
from resources.libs.common import tools

ORDER = ['serenpm',
         'ezrapm',
         'fenpm',
         'umbpm',
         'shadowpm',
         'ghostpm',
         'genocidepm',
         'chainspm',
         'base19pm',
         'twistedpm',
         'mdpm',
         'asgardpm',
         'metvpm',
         'kversepm',
         '4kpm',
         'myactpm',
         'mactpm',
         'rurlpm',
         'premiumizer',]

DEBRIDID = {
    'serenpm': {
        'name'     : 'Seren PM',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'ico-seren-3.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'fanart-seren-3.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'seren_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.enabled', 'premiumize.username', 'premiumize.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'ezrapm': {
        'name'     : 'Ezra PM',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezrapm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ezra_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'fenpm': {
        'name'     : 'Fen PM',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'fen_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.token', 'pm.account_id', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'umbpm': {
        'name'     : 'Umbrella PM',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'umb_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'premiumizeusername',
        'data'     : ['premiumizeusername', 'premiumizetoken', 'premiumize.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'shadowpm': {
        'name'     : 'Shadow PM',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'shadow_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'ghostpm': {
        'name'     : 'Ghost PM',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghostpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'ghost_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'genocidepm': {
        'name'     : 'Genocide PM',
        'plugin'   : 'script.module.myaccts',
        'saved'    : 'genocidepm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.Genocide', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'genocide_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.Genocide', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.Genocide)'},
    'chainspm': {
        'name'     : 'Chains Lite PM',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chainspm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'chains_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'base19pm': {
        'name'     : 'Base 19 PM',
        'plugin'   : 'plugin.video.base19',
        'saved'    : 'base19pm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'base19_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base19', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.base19)'},
    'twistedpm': {
        'name'     : 'Twisted PM',
        'plugin'   : 'plugin.video.twisted',
        'saved'    : 'twistedpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'twisted_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.twisted', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.twisted)'},
    'mdpm': {
        'name'     : 'Magic Dragon PM',
        'plugin'   : 'plugin.video.magicdragon',
        'saved'    : 'mdpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'md_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.magicdragon', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.magicdragon)'},
    'asgardpm': {
        'name'     : 'Asgard PM',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgardpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'asgard_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'metvpm': {
        'name'     : 'M.E.T.V PM',
        'plugin'   : 'plugin.video.metv19',
        'saved'    : 'metvpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'metv_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.metv19', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.metv19)'},
    'kversepm': {
        'name'     : 'KodiVerse PM',
        'plugin'   : 'script.module.myaccts',
        'saved'    : 'kversepm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.KodiVerse'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.KodiVerse', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.KodiVerse', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'kverse_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.KodiVerse', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.KodiVerse)'},
    '4kpm': {
        'name'     : '4K PM',
        'plugin'   : 'plugin.video.4k',
        'saved'    : '4kpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.4k'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.4k', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.4k', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, '4k_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.4k', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.4k)'},
   'myactpm': {
        'name'     : 'My Accounts PM',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myactpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
   'mactpm': {
        'name'     : 'Debrid Manager PM',
        'plugin'   : 'script.module.myaccts',
        'saved'    : 'myactpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'myact_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccts', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccts)'},
    'rurlpm': {
        'name'     : 'ResolveURL PM',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'rurl_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_token',
        'data'     : ['PremiumizeMeResolver_token', 'PremiumizeMeResolver_cached_only'],
        'activate' : 'Addon.OpenSettings(script.module.resolveurl)'},
   'premiumizer': {
	'name'     : 'Premiumizer',
	'plugin'   : 'plugin.video.premiumizerx',
	'saved'    : 'premiumizer',
	'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx'),
	'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'icon.png'),
	'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'fanart.jpg'),
	'file'     : os.path.join(CONFIG.DEBRIDFOLD, 'premiumizer_pm'),
	'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizerx', 'settings.xml'),
	'default'  : 'premiumize.token',
	'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
	'activate' : 'Addon.OpenSettings(plugin.video.premiumizerx)'}
}


def debrid_user(who):
    user = None
    if DEBRIDID[who]:
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
    if not os.path.exists(CONFIG.DEBRIDFOLD):
        os.makedirs(CONFIG.DEBRIDFOLD)
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
        CONFIG.set_setting('debridnextsave', tools.get_date(days=3, formatted=True))
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
            logging.log_notify('[COLOR {0}]{1}[/COLOR]'.format(CONFIG.COLOR1, DEBRIDID[who]['name']),
                               '[COLOR {0}]Debrid Info: Removed![/COLOR]'.format(CONFIG.COLOR2),
                               2000,
                               DEBRIDID[who]['icon'])
        CONFIG.set_setting(DEBRIDID[who]['saved'], '')
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


def open_settings_debrid(who):
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    addonid.openSettings()

