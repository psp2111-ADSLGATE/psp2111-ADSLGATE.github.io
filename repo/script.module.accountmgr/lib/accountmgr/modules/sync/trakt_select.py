import xbmcgui
import xbmc, xbmcaddon
import xbmcvfs
import os
import json
from libs.common import var
from accountmgr.modules import control

joinPath = os.path.join
dialog = xbmcgui.Dialog()
translatePath = xbmcvfs.translatePath
addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon = xbmcaddon.Addon(addon_id)
addoninfo = addon.getAddonInfo
addon_data = translatePath(addon.getAddonInfo('profile'))
file_path = addon_data + 'trakt_sync_list.json'
trakt_icon = joinPath(os.path.join(xbmcaddon.Addon('script.module.accountmgr').getAddonInfo('path'), 'resources', 'icons'), 'trakt.png')
NAMES = ['Seren', 'Fen', 'Fen Light', 'The Coalition', 'POV', 'Umbrella', 'Infinity', 'Dradis', 'Shadow', 'Ghost', 'Base', 'Chain Reaction', 'Asgard', 'Patriot', 'Black Lightning', 'Aliunde K19', 'Nightwing Lite', 'Homelander', 'Quicksilver', 'CHains Genocide', 'Absolution', 'Shazam', 'The Crew', 'Alvin', 'Moria', 'Nine Lives', 'Scrubs V2', 'TMDb Helper', 'Trakt Addon', 'All Accounts', ' My Accounts']

class tk_list():
        def create_list(self):
                menu = [] # Menu
                if xbmcvfs.exists(var.chk_seren):
                    menu.append('Seren')
                if xbmcvfs.exists(var.chk_fen):
                    menu.append('Fen')
                if xbmcvfs.exists(var.chk_fenlt):
                    menu.append('Fen Light')
                if xbmcvfs.exists(var.chk_coal):
                    menu.append('The Coalition')
                if xbmcvfs.exists(var.chk_pov):
                    menu.append('POV')
                if xbmcvfs.exists(var.chk_umb):
                    menu.append('Umbrella')
                if xbmcvfs.exists(var.chk_infinity):
                    menu.append('Infinity')
                if xbmcvfs.exists(var.chk_dradis):
                    menu.append('Dradis')
                if xbmcvfs.exists(var.chk_shadow):
                    menu.append('Shadow')
                if xbmcvfs.exists(var.chk_ghost):
                    menu.append('Ghost')
                if xbmcvfs.exists(var.chk_base):
                    menu.append('Base')
                if xbmcvfs.exists(var.chk_chains):
                    menu.append('Chain Reaction')
                if xbmcvfs.exists(var.chk_asgard):
                    menu.append('Asgard')
                if xbmcvfs.exists(var.chk_patriot):
                    menu.append('Patriot')
                if xbmcvfs.exists(var.chk_blackl):
                    menu.append('Black Lightning')
                if xbmcvfs.exists(var.chk_aliunde):
                    menu.append('Aliunde K19')
                if xbmcvfs.exists(var.chk_night):
                    menu.append('Nightwing Lite')
                if xbmcvfs.exists(var.chk_home):
                    menu.append('Homelander')
                if xbmcvfs.exists(var.chk_quick):
                    menu.append('Quicksilver')
                if xbmcvfs.exists(var.chk_genocide):
                    menu.append('Chains Genocide')
                if xbmcvfs.exists(var.chk_absol):
                    menu.append('Absolution')
                if xbmcvfs.exists(var.chk_shazam):
                    menu.append('Shazam')
                if xbmcvfs.exists(var.chk_crew):
                    menu.append('The Crew')
                if xbmcvfs.exists(var.chk_alvin):
                    menu.append('Alvin')
                if xbmcvfs.exists(var.chk_moria):
                    menu.append('Moria')
                if xbmcvfs.exists(var.chk_nine):
                    menu.append('Nine Lives')
                if xbmcvfs.exists(var.chk_scrubs):
                    menu.append('Scrubs V2')
                if xbmcvfs.exists(var.chk_tmdbh):
                    menu.append('TMDb Helper')
                if xbmcvfs.exists(var.chk_trakt):
                    menu.append('Trakt Addon')
                if xbmcvfs.exists(var.chk_allaccounts):
                    menu.append('All Accounts')
                if xbmcvfs.exists(var.chk_myaccounts):
                    menu.append('My Accounts')

                preselect = [] # Pre-select addons
                if xbmcvfs.exists(file_path):
                    with open(file_path, 'r') as synclist:
                        current = json.load(synclist)['addon_list']
                    for x in range(len(menu)):
                        if menu[x] in current:
                            preselect.append(x)
                            
                dialog_select = dialog.multiselect('اختر الإضافات المراد مزامنتها مع Trakt', menu, preselect=preselect) #Select add-ons to sync

                if dialog_select == None or dialog_select == preselect: #Quit if no changes made
                    control.notification('Account Manager', 'No Changes Made!', icon=trakt_icon)
                    quit()
                    
                addon_list = []
                for x in dialog_select: #Create user selected list
                    addon_list.append(menu[x])

                if not xbmcvfs.exists(addon_data):
                    xbmcvfs.mkdir(addon_data)
                with open(file_path, 'w') as synclist:
                    json.dump({'addon_list': addon_list}, synclist, indent = 4) #Create json
                    control.setSetting('trakt.synclist', 'true')
                    control.notification('Account Manager', 'Trakt Sync List Saved!', icon=trakt_icon)
