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

ORDER = ['serenpm',
         'fenpm',
         'fenltpm',
         'affenpm',
         'ezrapm',
         'coalpm',
         'povpm',
         'umbpm',
         'onempm',
         'dradispm',
         'tazpm',
         'shadowpm',
         'ghostpm',
         'basepm',
         'unleashedpm',
         'chainspm',
         'twistedpm',
         'mdpm',
         'asgardpm',
         'patriotpm',
         'blacklpm',
         'metvpm',
         'aliundepm',
         'otakupm',
         'premxpm',
         'acctmgrpm',
         'allactpm',
         'myactpm',
         'rurlpm']

DEBRIDID = {
    'serenpm': {
        'name'     : 'Seren',
        'plugin'   : 'plugin.video.seren',
        'saved'    : 'serenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'ico-seren-3.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.seren/resources/images', 'fanart-seren-3.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'seren_pm'), #Backup location
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.seren', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.enabled', 'premiumize.username', 'premiumize.token'],
        'activate' : 'Addon.OpenSettings(plugin.video.seren)'},
    'fenpm': {
        'name'     : 'Fen',
        'plugin'   : 'plugin.video.fen',
        'saved'    : 'fenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fen/resources/media/', 'fen_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'fen_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fen', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.token', 'pm.account_id', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.fen)'},
    'fenltpm': {
        'name'     : 'Fen Light',
        'plugin'   : 'plugin.video.fenlight',
        'saved'    : 'fenltpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.fenlight/resources/media/', 'fenlight_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'fenlt_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.fenlight/databases', 'settings.db'),
        'fenlt'    : '',
        'data'     : [],
        'activate' : 'Addon.OpenSettings(plugin.video.fenlight)'},
    'affenpm': {
        'name'     : 'afFENity',
        'plugin'   : 'plugin.video.affenity',
        'saved'    : 'affenpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.affenity'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.affenity/resources/media/', 'affenity_icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.affenity/resources/media/', 'affenity_fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'affen_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.affenity/databases', 'settings.db'),
        'fenlt'    : '',
        'data'     : [],
        'activate' : 'Addon.OpenSettings(plugin.video.affenity)'},
    'ezrapm': {
        'name'     : 'Ezra',
        'plugin'   : 'plugin.video.ezra',
        'saved'    : 'ezrapm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ezra', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'ezra_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ezra', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.ezra)'},
    'coalpm': {
        'name'     : 'The Coalition',
        'plugin'   : 'plugin.video.coalition',
        'saved'    : 'coalpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.coalition', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'coal_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.coalition', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.coalition)'},
    'povpm': {
        'name'     : 'POV',
        'plugin'   : 'plugin.video.pov',
        'saved'    : 'povpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.pov', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'pov_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.pov', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.account_id', 'pm.token', 'pm.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.pov)'},
    'umbpm': {
        'name'     : 'Umbrella',
        'plugin'   : 'plugin.video.umbrella',
        'saved'    : 'umbpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.umbrella', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'umb_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.umbrella', 'settings.xml'),
        'default'  : 'premiumizeusername',
        'data'     : ['premiumizeusername', 'premiumizetoken', 'premiumize.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.umbrella)'},
    'onempm': {
        'name'     : 'OneMoar',
        'plugin'   : 'plugin.video.onemoar',
        'saved'    : 'onempm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.onemoar'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.onemoar', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.onemoar', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'onem_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.onemoar', 'settings.xml'),
        'default'  : 'premiumizeusername',
        'data'     : ['premiumizeusername', 'premiumizetoken', 'premiumize.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.onemoar)'},
    'dradispm': {
        'name'     : 'Dradis',
        'plugin'   : 'plugin.video.dradis',
        'saved'    : 'dradispm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.dradis', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'dradis_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.dradis', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.username', 'premiumize.token', 'premiumize.enable'],
        'activate' : 'Addon.OpenSettings(plugin.video.dradis)'},
    'tazpm': {
        'name'     : 'Taz19',
        'plugin'   : 'plugin.video.taz19',
        'saved'    : 'tazpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.taz19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.taz19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.taz19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'taz_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.taz19', 'settings.xml'),
        'default'  : 'pm.account_id',
        'data'     : ['pm.token', 'pm.account_id', 'pm.enabled', 'pm_priority'],
        'activate' : 'Addon.OpenSettings(plugin.video.taz19)'},
    'shadowpm': {
        'name'     : 'Shadow',
        'plugin'   : 'plugin.video.shadow',
        'saved'    : 'shadowpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.shadow', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'shadow_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.shadow', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.shadow)'},
    'ghostpm': {
        'name'     : 'Ghost',
        'plugin'   : 'plugin.video.ghost',
        'saved'    : 'ghostpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.ghost', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'ghost_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.ghost', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.ghost)'},
    'basepm': {
        'name'     : 'Base',
        'plugin'   : 'plugin.video.base',
        'saved'    : 'basepm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.base', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.base', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'base_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.base', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.base)'},
    'unleashedpm': {
        'name'     : 'Unleashed',
        'plugin'   : 'plugin.video.unleashed',
        'saved'    : 'unleashedpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.unleashed'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.unleashed', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.unleashed', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'unleashed_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.unleashed', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.unleashed)'},
    'chainspm': {
        'name'     : 'Chains Reaction',
        'plugin'   : 'plugin.video.thechains',
        'saved'    : 'chainspm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.thechains', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'chains_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.thechains', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.thechains)'},
    'twistedpm': {
        'name'     : 'Twisted',
        'plugin'   : 'plugin.video.twisted',
        'saved'    : 'twistedpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.twisted', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'twisted_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.twisted', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.twisted)'},
    'mdpm': {
        'name'     : 'Magic Dragon',
        'plugin'   : 'plugin.video.magicdragon',
        'saved'    : 'mdpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.magicdragon', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'md_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.magicdragon', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.magicdragon)'},
    'asgardpm': {
        'name'     : 'Asgard',
        'plugin'   : 'plugin.video.asgard',
        'saved'    : 'asgardpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.asgard', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'asgard_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.asgard', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.asgard)'},
    'patriotpm': {
        'name'     : 'Patriot',
        'plugin'   : 'plugin.video.patriot',
        'saved'    : 'patriotpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.patriot', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'patriot_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.patriot', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.patriot)'},
    'blacklpm': {
        'name'     : 'Black Lightning',
        'plugin'   : 'plugin.video.blacklightning',
        'saved'    : 'blacklpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.blacklightning', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'blackl_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.blacklightning', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.blacklightning)'},
    'metvpm': {
        'name'     : 'M.E.T.V',
        'plugin'   : 'plugin.video.metv19',
        'saved'    : 'metvpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.metv19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'metv_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.metv19', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.metv19)'},
    'aliundepm': {
        'name'     : 'Aliunde K19',
        'plugin'   : 'plugin.video.aliundek19',
        'saved'    : 'aliundepm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.aliundek19', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'aliunde_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.aliundek19', 'settings.xml'),
        'default'  : 'premiumize.token',
        'data'     : ['premiumize.token', 'debrid_select'],
        'activate' : 'Addon.OpenSettings(plugin.video.aliunde)'},
    'otakupm': {
        'name'     : 'Otaku',
        'plugin'   : 'plugin.video.otaku',
        'saved'    : 'otakupm',
        'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.otaku', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'otaku_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.otaku', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.username', 'premiumize.token', 'premiumize.enabled'],
        'activate' : 'Addon.OpenSettings(plugin.video.otaku)'},
   'premxpm': {
	'name'     : 'Premiumizer',
	'plugin'   : 'plugin.video.premiumizerx',
	'saved'    : 'premxpm',
	'path'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx'),
	'icon'     : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'icon.png'),
	'fanart'   : os.path.join(CONFIG.ADDONS, 'plugin.video.premiumizerx', 'fanart.jpg'),
	'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'premx_pm'),
	'settings' : os.path.join(CONFIG.ADDON_DATA, 'plugin.video.premiumizerx', 'settings.xml'),
	'default'  : 'premiumize.token',
	'data'     : ['premiumize.status', 'premiumize.token', 'premiumize.refresh'],
	'activate' : 'Addon.OpenSettings(plugin.video.premiumizerx)'},
   'acctmgrpm': {
        'name'     : 'Account Manager',
        'plugin'   : 'script.module.accountmgr',
        'saved'    : 'acctmgrpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.accountmgr', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'acctmgr_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.accountmgr', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.accountmgr)'},
   'allactpm': {
        'name'     : 'All Accounts',
        'plugin'   : 'script.module.allaccounts',
        'saved'    : 'allactpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.allaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'allact_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.allaccounts', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.allaccounts)'},
   'myactpm': {
        'name'     : 'My Accounts',
        'plugin'   : 'script.module.myaccounts',
        'saved'    : 'myactpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.myaccounts', 'fanart.png'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'myact_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.myaccounts', 'settings.xml'),
        'default'  : 'premiumize.username',
        'data'     : ['premiumize.token', 'premiumize.username'],
        'activate' : 'Addon.OpenSettings(script.module.myaccounts)'},
    'rurlpm': {
        'name'     : 'ResolveURL',
        'plugin'   : 'script.module.resolveurl',
        'saved'    : 'rurlpm',
        'path'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl'),
        'icon'     : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'icon.png'),
        'fanart'   : os.path.join(CONFIG.ADDONS, 'script.module.resolveurl', 'fanart.jpg'),
        'file'     : os.path.join(CONFIG.DEBRIDFOLD_PM, 'rurl_pm'),
        'settings' : os.path.join(CONFIG.ADDON_DATA, 'script.module.resolveurl', 'settings.xml'),
        'default'  : 'PremiumizeMeResolver_token',
        'data'     : ['PremiumizeMeResolver_token', 'PremiumizeMeResolver_cached_only'],
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
        xbmc.log('%s: Debridit_pm Failed!' % var.amgr, xbmc.LOGINFO)
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
                    cur.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.token',)) #Get setting to compare
                    auth = cur.fetchone()
                    user_data = str(auth)

                    if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None: #Check if addon is authorized
                        user = None #Return if not authorized
                    else:
                        user = user_data #Return if authorized
                    cur.close()
            except:
                xbmc.log('%s: Debridit_pm Fen Light Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        elif os.path.exists(DEBRIDID[who]['path']) and name == 'afFENity':
            try:
                conn = create_conn(var.affen_settings_db)
                with conn:
                    cur = conn.cursor()
                    cur.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('pm.token',))
                    auth = cur.fetchone()
                    user_data = str(auth)

                    if user_data == "('empty_setting',)" or user_data == "('',)" or user_data == '' or user_data == None:
                        user = None
                    else:
                        user = user_data
                    cur.close()
            except:
                xbmc.log('%s: Debridit_pm afFENity Failed!' % var.amgr, xbmc.LOGINFO)
                pass
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
    if not os.path.exists(CONFIG.DEBRIDFOLD_PM):
        os.makedirs(CONFIG.DEBRIDFOLD_PM)
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

def open_settings_debrid(who):
    addonid = tools.get_addon_by_id(DEBRIDID[who]['plugin'])
    addonid.openSettings()

