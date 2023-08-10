import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import os.path
import time
from accountmgr.modules import var

timeout_start = time.time()
timeout = 60*5

def startup_sync():
        if str(var.chk_accountmgr_tk) != '': #Skip sync if Trakt is not authorized
                from accountmgr.modules import trakt_sync
                trakt_sync.sync_all() #Sync Trakt
        if str(var.chk_accountmgr_tk_rd) != '': #Skip sync if Real-Debrid is not authorized
                from accountmgr.modules import debrid_rd
                debrid_rd.debrid_auth_rd() #Sync Real-Debrid
        if str(var.chk_accountmgr_tk_pm) != '': #Skip sync if Premiumize is not authorized
                from accountmgr.modules import debrid_pm
                debrid_pm.debrid_auth_pm() #Sync Premiumize
        if str(var.chk_accountmgr_tk_ad) != '': #Skip sync if All-Debrid is not authorized
                from accountmgr.modules import debrid_ad 
                debrid_ad.debrid_auth_ad() #Sync All-Debrid

def api_check():

        while True:
                if time.time() > timeout_start + timeout: #Time out after 5min
                        break
                
                if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren) and str(var.chk_accountmgr_tk) != '': #Check that the addon is installed, settings.xml exists and Account Manager is authorized
                        with open(var.api_path_seren) as f: #Check add-on for Account Manager API keys. If found, move on to next add-on
                                if var.chk_api in f.read():
                                        pass
                                else:   #Insert Account Mananger API keys into add-on
                                        f = open(var.api_path_seren,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.seren_client,var.client_am).replace(var.seren_secret,var.secret_am)
                                        f = open(var.api_path_seren,'w')
                                        f.write(client)
                                        f.close()
                                        continue
              
                if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_fen) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_fen,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.fen_client,var.client_am).replace(var.fen_secret,var.secret_am)
                                        f = open(var.api_path_fen,'w')
                                        f.write(client)
                                        f.close()
                                        continue
         
                if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_pov) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_pov,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.pov_client,var.client_am).replace(var.pov_client,var.secret_am)
                                        f = open(var.api_path_pov,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_umb) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_umb,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.umb_client,var.client_am).replace(var.umb_secret,var.secret_am)
                                        f = open(var.api_path_umb,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_home) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_home,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.api_path_home,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_quick) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_quick,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.api_path_quick,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_genocide) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_genocide,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.api_path_genocide,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_crew) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_crew,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.crew_client,var.client_am).replace(var.crew_client,var.secret_am)
                                        f = open(var.api_path_crew,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_shazam) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_shazam,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.api_path_shazam,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_night) and xbmcvfs.exists(var.chkset_night) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_night) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_night,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.night_client,var.std_client_am).replace(var.night_secret,var.std_secret_am)
                                        f = open(var.api_path_night,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_promise) and xbmcvfs.exists(var.chkset_promise) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_promise) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_promise,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.api_path_promise,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_scrubs) and xbmcvfs.exists(var.chkset_scrubs) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_scrubs) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_scrubs,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.scrubs_client,var.client_am).replace(var.scrubs_secret,var.secret_am)
                                        f = open(var.api_path_scrubs,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_alvin) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_alvin,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.std_client,var.std_client_am).replace(var.std_secret,var.std_secret_am)
                                        f = open(var.api_path_alvin,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_shadow) and xbmcvfs.exists(var.chkset_shadow) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_shadow) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_shadow,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.shadow_client,var.client_am).replace(var.shadow_secret,var.secret_am)
                                        f = open(var.api_path_shadow,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_ghost) and xbmcvfs.exists(var.chkset_ghost) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_ghost) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_ghost,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.ghost_client,var.client_am).replace(var.ghost_secret,var.secret_am)
                                        f = open(var.api_path_ghost,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_unleashed) and xbmcvfs.exists(var.chkset_unleashed) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_unleashed) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_unleashed,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.unleashed_client,var.client_am).replace(var.unleashed_secret,var.secret_am)
                                        f = open(var.api_path_unleashed,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_chains) and xbmcvfs.exists(var.chkset_chains) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_chains) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_chains,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.chains_client,var.client_am).replace(var.chains_secret,var.secret_am)
                                        f = open(var.api_path_chains,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_md) and xbmcvfs.exists(var.chkset_md) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_md) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_md,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.md_client,var.client_am).replace(var.md_client,var.secret_am)
                                        f = open(var.api_path_md,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_asgard) and xbmcvfs.exists(var.chkset_asgard) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_asgard) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_asgard,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.asgard_client,var.client_am).replace(var.asgard_secret,var.secret_am)
                                        f = open(var.api_path_asgard,'w')
                                        f.write(client)
                                        f.close()
                                        continue
                                        
                if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_myaccounts) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_myaccounts,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.myacts_client,var.client_am).replace(var.myacts_secret,var.secret_am)
                                        f = open(var.api_path_myaccounts,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_tmdbh) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_tmdbh,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.tmdbh_client,var.client_am).replace(var.tmdbh_secret,var.secret_am)
                                        f = open(var.api_path_tmdbh,'w')
                                        f.write(client)
                                        f.close()
                                        continue

                if xbmcvfs.exists(var.chk_trakt) and xbmcvfs.exists(var.chkset_trakt) and str(var.chk_accountmgr_tk) != '':
                        with open(var.api_path_trakt) as f:
                                if var.chk_api in f.read():
                                        pass
                                else:
                                        f = open(var.api_path_trakt,'r')
                                        data = f.read()
                                        f.close()
                                        client = data.replace(var.trakt_client,var.client_am).replace(var.trakt_secret,var.secret_am)
                                        f = open(var.api_path_trakt,'w')
                                        f.write(client)
                                        f.close()
                                        pass


                xbmc.sleep(10000) #Pause for 10 seconds

if var.setting('sync.service')=='true':
        startup_sync()
else:
        pass
if var.setting('trakt.service')=='true':
        api_check()
else:
        quit()
