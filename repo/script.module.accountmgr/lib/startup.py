import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path
import time
import sqlite3
import _strptime

from libs.common import var
from accountmgr.modules import control
from accountmgr.modules import log_utils

accountmgr = xbmcaddon.Addon("script.module.accountmgr")
dialog = xbmcgui.Dialog()
LOGINFO = 1

timeout_start = time.time()
timeout = 60*5

def startup_sync():
        try:
                if str(var.chk_accountmgr_tk) != '': #Skip sync if Trakt is not authorized
                        from accountmgr.modules import trakt_sync
                        trakt_sync.Auth().trakt_auth() #Sync Trakt
        except:
                xbmc.log('%s: Startup Trakt Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        try:
                if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Real-Debrid is not authorized
                        from accountmgr.modules import debrid_rd
                        debrid_rd.Auth().realdebrid_auth() #Sync Real-Debrid
        except:
                xbmc.log('%s: Startup Real-Debrid Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        try:
                if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Premiumize is not authorized
                        from accountmgr.modules import debrid_pm
                        debrid_pm.Auth().premiumize_auth() #Sync Premiumize
        except:
                xbmc.log('%s: Startup Premiumize Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        try:
                if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if All-Debrid is not authorized
                        from accountmgr.modules import debrid_ad 
                        debrid_ad.Auth().alldebrid_auth() #Sync All-Debrid
        except:
                xbmc.log('%s: Startup All-Debrid Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass

def startup_nondebrid_sync():
        try:    
                if str(var.chk_accountmgr_offc) != '': #Skip sync if no data is available to sync
                        from accountmgr.modules import offcloud_sync
                        offcloud_sync.Auth().offcloud.auth() #Sync OffCloud Data
        except:
                xbmc.log('%s: Startup OffCloud Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        try:    
                if str(var.chk_accountmgr_easy) != '': #Skip sync if no data is available to sync
                        from accountmgr.modules import easy_sync
                        easy_sync.Auth().easy_auth() #Sync Easynews Data
        except:
                xbmc.log('%s: Startup Easynews Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
        try:    
                if str(var.chk_accountmgr_file) != '': #Skip sync if no data is available to sync
                        from accountmgr.modules import filepursuit_sync
                        filepursuit_sync.Auth().file_auth() #Sync Filepursuit Data
        except:
                xbmc.log('%s: Startup Filepursuit Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
def startup_meta_sync():
        try:    
                if str(var.chk_accountmgr_fanart) != '' or str(var.chk_accountmgr_omdb) != '' or str(var.chk_accountmgr_mdb) != '' or str(var.chk_accountmgr_imdb) != '' or str(var.chk_accountmgr_tmdb) != '' or str(var.chk_accountmgr_tmdb_user) != '' or str(var.chk_accountmgr_tvdb) != '': #Skip sync if no data is available to sync
                        from accountmgr.modules import meta_sync
                        meta_sync.Auth().meta_auth() #Sync Metadata
        except:
                xbmc.log('%s: Startup Meta Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
def dradis_sync():
        try:  
                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.dradis/?action=tools_forceTraktSync)') #Start Trakt Sync
                xbmc.sleep(1000)
                if xbmc.getCondVisibility('Window.IsTopMost(yesnodialog)'):
                        xbmc.executebuiltin('SendClick(yesnodialog, 11)')
                accountmgr.setSetting("dradis_traktsync", 'false')
        except:
                xbmc.log('%s: Startup Dradis Trakt Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass

def genocide_sync():
        try:               
                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.chainsgenocide/?action=tools_forceTraktSync)') #Start Trakt Sync
                xbmc.sleep(1000)
                if xbmc.getCondVisibility('Window.IsTopMost(yesnodialog)'):
                        xbmc.executebuiltin('SendClick(yesnodialog, 11)')
                accountmgr.setSetting("genocide_traktsync", 'false')
        except:
                xbmc.log('%s: Startup Chains Genocide Trakt Sync Failed!' % var.amgr, xbmc.LOGINFO)
                pass
                
class AddonCheckUpdate:
        def run(self):
            xbmc.log('[ script.module.accountmgr ]  Addon checking available updates', LOGINFO)
            try:
                import re
                import requests
                repo_xml = requests.get('https://raw.githubusercontent.com/Zaxxon709/nexus/main/zips/script.module.accountmgr/addon.xml')
                if repo_xml.status_code != 200:
                    return xbmc.log('[ script.module.accountmgr ]  Could not connect to remote repo XML: status code = %s' % repo_xml.status_code, LOGINFO)
                repo_version = re.search(r'<addon id=\"script.module.accountmgr\".*version=\"(\d*.\d*.\d*)\"', repo_xml.text, re.I).group(1)
                local_version = control.addonVersion()[:5] # 5 char max so pre-releases do try to compare more chars than github version
                def check_version_numbers(current, new): # Compares version numbers and return True if github version is newer
                    current = current.split('.')
                    new = new.split('.')
                    step = 0
                    for i in current:
                        if int(new[step]) > int(i): return True
                        if int(i) > int(new[step]): return False
                        if int(i) == int(new[step]):
                            step += 1
                            continue
                    return False
                if check_version_numbers(local_version, repo_version):
                    while control.condVisibility('Library.IsScanningVideo'):
                        control.sleep(10000)
                    xbmc.log('[ script.module.accountmgr ]  A newer version is available. Installed Version: v%s' % (local_version), LOGINFO)
                    control.notification(message=control.lang(32072) % repo_version, time=5000)
                return xbmc.log('[ script.module.accountmgr ]  Addon update check complete', LOGINFO)
            except:
                import traceback
                traceback.print_exc()

class PremAccntNotification:
	def run(self):
		from datetime import datetime
		from accountmgr.modules import alldebrid
		from accountmgr.modules import premiumize
		from accountmgr.modules import realdebrid
		xbmc.log('[ script.module.accountmgr ]  Debrid Account Expiry Notification Service Starting...', LOGINFO)
		self.duration = [(15, 10), (11, 7), (8, 4), (5, 2), (3, 0)]
		if control.setting('alldebrid.username') != '' and control.setting('alldebrid.expiry.notice') == 'true':
			account_info = alldebrid.AllDebrid().account_info()['user']
			if account_info:
				if not account_info['isSubscribed']:
					expires = datetime.fromtimestamp(account_info['premiumUntil'])
					days_remaining = (expires - datetime.today()).days # int
					if days_remaining < 15:
						control.notification(message='AllDebrid Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'alldebrid.png'))

		if control.setting('premiumize.username') != '' and control.setting('premiumize.expiry.notice') == 'true':
			account_info = premiumize.Premiumize().account_info()
			if account_info:
				expires = datetime.fromtimestamp(account_info['premium_until'])
				days_remaining = (expires - datetime.today()).days # int
				if days_remaining < 15:
					control.notification(message='Premiumize.me Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'premiumize.png'))

		if control.setting('realdebrid.username') != '' and control.setting('realdebrid.expiry.notice') == 'true':
			account_info = realdebrid.RealDebrid().account_info()
			if account_info:
				import time
				FormatDateTime = "%Y-%m-%dT%H:%M:%S.%fZ"
				try: expires = datetime.strptime(account_info['expiration'], FormatDateTime)
				except: expires = datetime(*(time.strptime(account_info['expiration'], FormatDateTime)[0:6]))
				days_remaining = (expires - datetime.today()).days # int
				if days_remaining < 15:
					control.notification(message='Real-Debrid Account expires in %s days' % days_remaining, icon=control.joinPath(control.artPath(), 'realdebrid.png'))
		
def check_api():
        while True:
                if time.time() > timeout_start + timeout: #Time out after 5min
                        break
                # Trakt
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren) and str(var.chk_accountmgr_tk) != '' and (var.setting('traktuserkey.enabled') == 'true' or var.setting('devuserkey.enabled') == 'true'): #Check that the addon is installed, settings.xml exists and Account Manager is authorized
                        try:
                                with open(var.path_seren) as f: #Check add-on for Account Manager API keys. If found, move on to next add-on
                                        if var.chk_api in f.read():
                                                pass
                                        else:   #Insert Account Mananger API keys into add-on
                                                with open(var.path_seren,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)

                                                with open(var.path_seren,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Seren API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass

                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_fen) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:   
                                                with open(var.path_fen,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)

                                                with open(var.path_fen,'w') as f:
                                                    f.write(client) 
                        except:
                                xbmc.log('%s: Fen API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_affen) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:   
                                                with open(var.path_affen,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.affen_client,var.client_am).replace(var.affen_secret,var.secret_am)

                                                with open(var.path_affen,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: afFENity API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass

                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb) and str(var.chk_accountmgr_tk) != '':
                        try:
                                chk_auth_umb = xbmcaddon.Addon('plugin.video.umbrella').getSetting("trakt.user.token")
                                chk_client = xbmcaddon.Addon('plugin.video.umbrella').getSetting("trakt.clientid")
                                
                                if not str(chk_client) == str(var.chk_api) and str(var.chk_accountmgr_tk) == str(chk_auth_umb):
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("traktuserkey.customenabled", 'true')
                                        addon.setSetting("trakt.clientid", var.client_am)
                                        addon.setSetting("trakt.clientsecret", var.secret_am)
                        except:
                                xbmc.log('%s: Umbrella API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass

                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity) and str(var.chk_accountmgr_tk) != '':
                        try:
                                chk_auth_infen = xbmcaddon.Addon('plugin.video.infinity').getSetting("trakt.user.token")
                                chk_client = xbmcaddon.Addon('plugin.video.infinity').getSetting("trakt.clientid")
                                
                                if not str(chk_client) == str(var.chk_api) and str(var.chk_accountmgr_tk) == str(chk_auth_infinity):
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("traktuserkey.customenabled", 'true')
                                        addon.setSetting("trakt.clientid", var.client_am)
                                        addon.setSetting("trakt.clientsecret", var.secret_am)
                        except:
                                xbmc.log('%s: Infinity API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_coal) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:   
                                                with open(var.path_coal,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.coal_client,var.client_am).replace(var.coal_secret,var.secret_am)

                                                with open(var.path_coal,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Coalition API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                                
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov) and str(var.chk_accountmgr_tk) != '':
                        try:
                                chk_auth_pov = xbmcaddon.Addon('plugin.video.pov').getSetting("trakt.token")
                                chk_client = xbmcaddon.Addon('plugin.video.pov').getSetting("trakt.client_id")
                                
                                if not str(chk_client) == str(var.chk_api) and str(var.chk_accountmgr_tk) == str(chk_auth_pov):
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("trakt.client_id", var.client_am)
                                        addon.setSetting("trakt.client_secret", var.secret_am)
                        except:
                                xbmc.log('%s: POV API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis) and str(var.chk_accountmgr_tk) != '':
                        try:
                                chk_auth_dradis = xbmcaddon.Addon('plugin.video.dradis').getSetting("trakt.token")
                                chk_client = xbmcaddon.Addon('plugin.video.dradis').getSetting("trakt.client_id")
                                
                                if not str(chk_client) == str(var.chk_api) and str(var.chk_accountmgr_tk) == str(chk_auth_dradis):
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("trakt.client_id", var.client_am)
                                        addon.setSetting("trakt.client_secret", var.secret_am)
                        except:
                                xbmc.log('%s: Dradis API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_taz) and xbmcvfs.exists(var.chkset_taz) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_taz) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_taz,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.taz_client,var.client_am)

                                                with open(var.path_taz,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Taz API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and  xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_shadow) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_shadow,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)

                                                with open(var.path_shadow,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Shadow API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_ghost) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_ghost,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)

                                                with open(var.path_ghost,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Ghost API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_base) and xbmcvfs.exists(var.chkset_base) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_base) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_base,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.base_client,var.client_am).replace(var.base_secret,var.secret_am)

                                                with open(var.path_base,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Base API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_unleashed) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_unleashed,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)

                                                with open(var.path_unleashed,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Unleashed API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_chains) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_chains,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)

                                                with open(var.path_chains,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Chain Reaction API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_md) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_md,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.md_client,var.client_am).replace(var.md_secret,var.secret_am)

                                                with open(var.path_md,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Magic Dragon API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_asgard) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_asgard,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)

                                                with open(var.path_asgard,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Asgard API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_patriot) and xbmcvfs.exists(var.chkset_patriot) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_patriot) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_patriot,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.patriot_client,var.client_am).replace(var.patriot_secret,var.secret_am)

                                                with open(var.path_patriot,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Patriot API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_blackl) and xbmcvfs.exists(var.chkset_blackl) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_blackl) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_blackl,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.blackl_client,var.client_am).replace(var.blackl_secret,var.secret_am)

                                                with open(var.path_blackl,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Black Lightning API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_aliunde) and xbmcvfs.exists(var.chkset_aliunde) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_aliunde) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_aliunde,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.aliunde_client,var.client_am).replace(var.aliunde_secret,var.secret_am)

                                                with open(var.path_aliunde,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Aliunde API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass

                if var.setting('api.service')=='true' and  xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_night) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_night,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.night_client,var.client_am).replace(var.night_secret,var.secret_am)

                                                with open(var.path_night,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Nightwing Lite API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass

                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_genocide) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:   
                                                with open(var.path_genocide,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.genocide_client,var.client_am).replace(var.genocide_secret,var.secret_am)

                                                with open(var.path_genocide,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Chains Genocide API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_crew) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_crew,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.crew_client,var.client_am).replace(var.crew_secret,var.secret_am)

                                                with open(var.path_crew,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: The Crew API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_scrubs) and xbmcvfs.exists(var.chkset_scrubs) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_scrubs) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_scrubs,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)

                                                with open(var.path_scrubs,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Scrubs V2 API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_tmdbh) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_tmdbh,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)

                                                with open(var.path_tmdbh,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: TMDbH API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_trakt) and xbmcvfs.exists(var.chkset_trakt) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_trakt) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_trakt,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)

                                                with open(var.path_trakt,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: Trakt Addon API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                      
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_allaccounts) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_allaccounts,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.allacts_client,var.client_am).replace(var.allacts_secret,var.secret_am)

                                                with open(var.path_allaccounts,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: All Accounts API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass
                        
                if var.setting('api.service')=='true' and xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts) and str(var.chk_accountmgr_tk) != '':
                        try:
                                with open(var.path_myaccounts) as f:
                                        if var.chk_api in f.read():
                                                pass
                                        else:
                                                with open(var.path_myaccounts,'r') as f:
                                                    data = f.read()

                                                client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)

                                                with open(var.path_myaccounts,'w') as f:
                                                    f.write(client)
                        except:
                                xbmc.log('%s: My Accounts API Failed!' % var.amgr, xbmc.LOGINFO)
                                pass

                xbmc.sleep(10000) #Pause for 10 seconds

def restore_api():
        #Restore API Keys for all add-ons
        accountmgr.setSetting("api_restore", 'false')
        # Trakt
        if xbmcvfs.exists(var.chk_seren) and (var.setting('traktuserkey.enabled') == 'true' or var.setting('devuserkey.enabled') == 'true'): #Check if add-on is installed
            try:
                #Insert Account Mananger API keys into add-on
                with open(var.path_seren,'r') as f:
                    data = f.read()

                client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)

                with open(var.path_seren,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Seren Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_fen):
            try:
                with open(var.path_fen,'r') as f:
                    data = f.read()

                client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)

                with open(var.path_fen,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Fen Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
        if xbmcvfs.exists(var.chk_coal):
            try:
                with open(var.path_coal,'r') as f:
                    data = f.read()

                client = data.replace(var.coal_client,var.client_am).replace(var.coal_secret,var.secret_am)

                with open(var.path_coal,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Coalition Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_pov):
            try:
                addon = xbmcaddon.Addon("plugin.video.pov")
                addon.setSetting("trakt.client_id", var.client_am)
                addon.setSetting("trakt.client_secret", var.secret_am)
            except:
                xbmc.log('%s: Restore API POV Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_dradis):
            try:
                addon = xbmcaddon.Addon("plugin.video.dradis")
                addon.setSetting("trakt.client_id", var.client_am)
                addon.setSetting("trakt.client_secret", var.secret_am)
            except:
                xbmc.log('%s: Restore API Dradis Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_taz):
            try:
                with open(var.path_taz,'r') as f:
                    data = f.read()

                client = data.replace(var.taz_client,var.client_am)

                with open(var.path_taz,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Taz Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_shadow):
            try:
                with open(var.path_shadow,'r') as f:
                    data = f.read()

                client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)

                with open(var.path_shadow,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Shadow Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_ghost):
            try:
                with open(var.path_ghost,'r') as f:
                    data = f.read()

                client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)

                with open(var.path_ghost,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Ghost Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_base):
            try:
                with open(var.path_base,'r') as f:
                    data = f.read()

                client = data.replace(var.base_client,var.client_am).replace(var.base_secret,var.secret_am)

                with open(var.path_base,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Base Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_unleashed):
            try:
                with open(var.path_unleashed,'r') as f:
                    data = f.read()

                client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)

                with open(var.path_unleashed,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Unleashed Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_chains):
            try:
                with open(var.path_chains,'r') as f:
                    data = f.read()

                client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)

                with open(var.path_chains,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Chain Reaction Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_md):
            try:
                with open(var.path_md,'r') as f:
                    data = f.read()

                client = data.replace(var.md_client,var.client_am).replace(var.md_secret,var.secret_am)

                with open(var.path_md,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Magic Dragon Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        if xbmcvfs.exists(var.chk_asgard):
            try:
                with open(var.path_asgard,'r') as f:
                    data = f.read()

                client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)

                with open(var.path_asgard,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Asgard Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_patriot):
            try:
                with open(var.path_patriot,'r') as f:
                    data = f.read()

                client = data.replace(var.patriot_client,var.client_am).replace(var.patriot_secret,var.secret_am)

                with open(var.path_patriot,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Patriot Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_blackl):
            try:
                with open(var.path_blackl,'r') as f:
                    data = f.read()

                client = data.replace(var.blackl_client,var.client_am).replace(var.blackl_secret,var.secret_am)

                with open(var.path_blackl,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Black Lightning Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_aliunde):
            try:
                with open(var.path_aliunde,'r') as f:
                    data = f.read()

                client = data.replace(var.aliunde_client,var.client_am).replace(var.aliunde_secret,var.secret_am)

                with open(var.path_aliunde,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Aliunde Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_night):
            try:
                with open(var.path_night,'r') as f:
                    data = f.read()

                client = data.replace(var.night_client,var.client_am).replace(var.night_secret,var.secret_am)

                with open(var.path_night,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Nightwing Lite Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_genocide):
            try:
                with open(var.path_genocide,'r') as f:
                    data = f.read()

                client = data.replace(var.genocide_client,var.client_am).replace(var.genocide_secret,var.secret_am)

                with open(var.path_genocide,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Chains Genocide Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
        if xbmcvfs.exists(var.chk_crew):
            try:
                with open(var.path_crew,'r') as f:
                    data = f.read()

                client = data.replace(var.crew_client,var.client_am).replace(var.crew_secret,var.secret_am)

                with open(var.path_crew,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API The Crew Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_scrubs):
            try:
                with open(var.path_scrubs,'r') as f:
                    data = f.read()

                client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)

                with open(var.path_scrubs,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Scrubs V2 Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_tmdbh):
            try:
                with open(var.path_tmdbh,'r') as f:
                    data = f.read()

                client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)

                with open(var.path_tmdbh,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API TMDbH Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_trakt):
            try:
                with open(var.path_trakt,'r') as f:
                    data = f.read()

                client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)

                with open(var.path_trakt,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API Trakt Addon Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_allaccounts):
            try:
                with open(var.path_allaccounts,'r') as f:
                    data = f.read()

                client = data.replace(var.allacts_client,var.client_am).replace(var.allacts_secret,var.secret_am)

                with open(var.path_allaccounts,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API All Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                pass

        if xbmcvfs.exists(var.chk_myaccounts):
            try:
                with open(var.path_myaccounts,'r') as f:
                    data = f.read()

                client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)

                with open(var.path_myaccounts,'w') as f:
                    f.write(client)
            except:
                xbmc.log('%s: Restore API My Accounts Failed!' % var.amgr, xbmc.LOGINFO)
                pass
        
       
var.rm_traktcache()     
        
if var.setting('api_restore')=='true': #Check if API restore is enabled
        restore_api() #Restore API Keys
else:
        pass

if var.setting('sync.service')=='true': #Check if service is enabled
        startup_sync() #Start service
else:
        pass

if var.setting('sync.nondebrid.service')=='true': #Check if service is enabled
        startup_nondebrid_sync() #Start service
else:
        pass

if var.setting('sync.metaservice')=='true': #Check if service is enabled
        startup_meta_sync() #Start service
else:
        pass

if var.setting('checkAddonUpdates')=='true': #Check if service is enabled
	AddonCheckUpdate().run() #Start service
else:
        pass

PremAccntNotification().run()

if var.setting('dradis_traktsync')=='true': #Check if Trakt Sync is enabled for Dradis add-on
        dradis_sync() #Start Dradis Trakt sync
else:
        pass

if var.setting('genocide_traktsync')=='true': #Check if Trakt Sync is enabled for Chains Genocide add-on
        genocide_sync() #Start Chains Genocide Trakt sync
else:
        pass

if var.setting('reset_settings')=='true': #Check if reset settings is enabled
        yes = dialog.yesno('Account Manager', 'Choose proceed to remove all settings applied by Account Manager or cancel to quit.', 'Cancel', 'Proceed') # Ask user for permission
        if yes:
                xbmc.executebuiltin('PlayMedia(plugin://script.module.acctview/?mode=wipeclean&name=all)') #Reset settings
                control.setSetting("reset_settings", "false")
        else:
                if str(var.chk_accountmgr_tk) != '':
                        control.setSetting("api.service", "true") #Re-enable service
                        control.setSetting("reset_settings", "false") #Disable reset settings
else:
        pass

if var.setting('api.service')=='true' and (str(var.chk_accountmgr_tk) != ''): #Check if service is enabled and Trakt is authorized
        check_api() #Start service
else:
        quit()
