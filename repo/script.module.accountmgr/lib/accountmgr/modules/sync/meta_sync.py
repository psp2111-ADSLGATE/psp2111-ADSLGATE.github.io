import xbmc, xbmcaddon
import xbmcvfs
import json
import os

from pathlib import Path
from accountmgr.modules import control
from libs.common import var

char_remov = ["'", ",", ")","("]

#Account Manager Metadata
accountmgr = xbmcaddon.Addon("script.module.accountmgr")
your_tmdb_user = accountmgr.getSetting("tmdb.username")
your_tmdb_pass = accountmgr.getSetting("tmdb.password")
your_tmdb_session = accountmgr.getSetting("tmdb.session_id")
your_tmdb_api = accountmgr.getSetting("tmdb.api.key")
your_imdb_api = accountmgr.getSetting("imdb.user")
your_fanart_api = accountmgr.getSetting("fanart.tv.api.key")
your_mdb_api = accountmgr.getSetting("mdb.api.key")
your_omdb_api = accountmgr.getSetting("omdb.api.key")
your_tvdb_api = accountmgr.getSetting("tvdb.api.key")

class Auth:
        def meta_auth(self):
        #Seren
                try:
                        if xbmcvfs.exists(var.chk_seren) and xbmcvfs.exists(var.chkset_seren): #Check that the addon is installed and settings.xml exists
                            
                                #Get add-on setting to compare
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.seren').getSetting("fanart.apikey")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.seren').getSetting("omdb.apikey")
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.seren').getSetting("tmdb.apikey")
                                chk_tvdb_api = xbmcaddon.Addon('plugin.video.seren').getSetting("tvdb.apikey")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("fanart.apikey", your_fanart_api)
                                        
                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("omdb.apikey", your_omdb_api)

                                if not str(var.chk_accountmgr_tvdb) == str(chk_tvdb_api) or str(chk_tvdb_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("tvdb.apikey", your_tvdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '': #Compare Account Mananger API to Add-on API. If they match authorization is skipped
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("plugin.video.seren")
                                        addon.setSetting("tmdb.apikey", your_tmdb_api)
                except:
                        xbmc.log('%s: Seren Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.fen').getSetting("fanart_client_key")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.fen').getSetting("omdb_api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.fen').getSetting("imdb_user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.fen').getSetting("tmdb_api")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("fanart_client_key", your_fanart_api)

                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("omdb_api", your_omdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("imdb_user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.fen")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        xbmc.log('%s: Fen Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Fen Light
                try:
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt): #Check that the addon is installed and settings.db exists
                            
                            #Create database connection
                            from accountmgr.modules.db import meta_db
                            conn = meta_db.create_conn(var.fenlt_settings_db)
                            
                            #Get add-on settings to compare
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('omdb_api',))
                                auth_omdb = cursor.fetchone()
                                chk_auth_fenlt_omdb = str(auth_omdb)

                                cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('tmdb_api',))
                                auth_tmdb = cursor.fetchone()
                                chk_auth_fenlt_tmdb = str(auth_tmdb)
                                cursor.close()
                                
                                #Clean up database results
                                for char in char_remov:
                                    chk_auth_fenlt_omdb = chk_auth_fenlt_omdb.replace(char, "")

                                for char in char_remov:
                                    chk_auth_fenlt_tmdb = chk_auth_fenlt_tmdb.replace(char, "")

                                if str(var.chk_accountmgr_omdb) == '':
                                        pass
                                else:
                                        if str(var.chk_accountmgr_omdb) != chk_auth_fenlt_omdb: #Compare Account Mananger data to Add-on data. If they match, authorization is skipped
                                                #Write settings to database
                                                from accountmgr.modules.db import meta_db
                                                meta_db.auth_fenlt_omdb()
                                                var.remake_settings()
                                        
                                if str(var.chk_accountmgr_tmdb) == '':
                                        pass
                                    
                                else:
                                        if str(var.chk_accountmgr_tmdb) != chk_auth_fenlt_tmdb: #Compare Account Mananger data to Add-on data. If they match, authorization is skipped
                                                #Write settings to database
                                                from accountmgr.modules.db import meta_db
                                                meta_db.auth_fenlt_tmdb()
                                                var.remake_settings()
                except:
                        xbmc.log('%s: Fen Light Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #afFENity
                '''try:
                        if xbmcvfs.exists(var.chk_affen) and xbmcvfs.exists(var.chkset_affen):
                            
                            from accountmgr.modules.db import meta_db
                            conn = meta_db.create_conn(var.affen_settings_db)
                            
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute(''''''SELECT setting_value FROM settings WHERE setting_id = ?'''''', ('omdb_api',))
                                auth_meta = cursor.fetchone()
                                chk_auth_affen = str(auth_meta)
                                cursor.close()

                                for char in char_remov:
                                    chk_auth_affen = chk_auth_affen.replace(char, "")
                                    
                                if not str(var.chk_accountmgr_omdb) == chk_auth_affen:

                                    from accountmgr.modules.db import meta_db
                                    meta_db.auth_affen_meta()
                                    var.remake_settings()
                except:
                        xbmc.log('%s: afFENity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass'''

        #Coalition
                try:
                        if xbmcvfs.exists(var.chk_coal) and xbmcvfs.exists(var.chkset_coal):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("fanart_client_key")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("omdb_api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("imdb_user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.coalition').getSetting("tmdb_api")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("fanart_client_key", your_fanart_api)

                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("omdb_api", your_omdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("imdb_user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.coalition")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        xbmc.log('%s: Coalition Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

                
        #POV
                try:
                        if xbmcvfs.exists(var.chk_pov) and xbmcvfs.exists(var.chkset_pov):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.pov').getSetting("fanart_client_key")   
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.pov').getSetting("tmdb_api")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("fanart_client_key", your_fanart_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.pov")
                                        addon.setSetting("tmdb_api", your_tmdb_api)
                except:
                        xbmc.log('%s: POV Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("fanart_tv.api_key")
                                chk_mdb_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("mdblist.api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("imdbuser")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdb.apikey")
                                chk_tmdb_user = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdbusername")
                                chk_tmdb_pass = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdbpassword")
                                chk_tmdb_session = xbmcaddon.Addon('plugin.video.umbrella').getSetting("tmdb.sessionid")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("fanart_tv.api_key", your_fanart_api)

                                if not str(var.chk_accountmgr_mdb) == str(chk_mdb_api) or str(chk_mdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("mdblist.api", your_mdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("imdbuser", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdb.apikey", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdbusername", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdbpassword", your_tmdb_pass)

                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("plugin.video.umbrella")
                                        addon.setSetting("tmdb.sessionid", your_tmdb_session)
                except:
                        xbmc.log('%s: Umbrella Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Infinity
                try:
                        if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.infinity').getSetting("fanart_tv.api_key")
                                chk_mdb_api = xbmcaddon.Addon('plugin.video.infinity').getSetting("mdblist.api")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.infinity').getSetting("imdbuser")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.infinity').getSetting("tmdb.apikey")
                                chk_tmdb_user = xbmcaddon.Addon('plugin.video.infinity').getSetting("tmdbusername")
                                chk_tmdb_pass = xbmcaddon.Addon('plugin.video.infinity').getSetting("tmdbpassword")
                                chk_tmdb_session = xbmcaddon.Addon('plugin.video.infinity').getSetting("tmdb.sessionid")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("fanart_tv.api_key", your_fanart_api)

                                if not str(var.chk_accountmgr_mdb) == str(chk_mdb_api) or str(chk_mdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("mdblist.api", your_mdb_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("imdbuser", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("tmdb.apikey", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("tmdbusername", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("tmdbpassword", your_tmdb_pass)

                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("plugin.video.infinity")
                                        addon.setSetting("tmdb.sessionid", your_tmdb_session)
                except:
                        xbmc.log('%s: Infinity Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Dradis
                try:
                        if xbmcvfs.exists(var.chk_dradis) and xbmcvfs.exists(var.chkset_dradis):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.dradis').getSetting("fanart_tv.api_key")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.dradis').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.dradis').getSetting("tmdb.api.key")
                                chk_tmdb_user = xbmcaddon.Addon('plugin.video.dradis').getSetting("tmdb.username")
                                chk_tmdb_pass = xbmcaddon.Addon('plugin.video.dradis').getSetting("tmdb.password")
                                chk_tmdb_session = xbmcaddon.Addon('plugin.video.dradis').getSetting("tmdb.session_id")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("fanart_tv.api_key", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("tmdb.api.key", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("tmdb.username", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("tmdb.password", your_tmdb_pass)

                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("plugin.video.dradis")
                                        addon.setSetting("tmdb.session_id", your_tmdb_session)
                except:
                        xbmc.log('%s: Dradis Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #The Crew
                try:
                        if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.crew_ud):
                                os.mkdir(var.crew_ud)
                                xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))
                                
                        if xbmcvfs.exists(var.chk_crew) and not xbmcvfs.exists(var.chkset_crew):
                                xbmcvfs.copy(os.path.join(var.crew), os.path.join(var.chkset_crew))

                        if xbmcvfs.exists(var.chk_crew) and xbmcvfs.exists(var.chkset_crew):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("tm.user")
                                chk_tvdb_api = xbmcaddon.Addon('plugin.video.thecrew').getSetting("tvdb.user")

                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tvdb) == str(chk_tvdb_api) or str(chk_tvdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("tvdb.user", your_tvdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.thecrew")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: The Crew Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Homelander
                try:
                        if xbmcvfs.exists(var.chk_home) and not xbmcvfs.exists(var.home_ud):
                                os.mkdir(var.home_ud)
                                xbmcvfs.copy(os.path.join(var.home), os.path.join(var.chkset_home))
                                
                        if xbmcvfs.exists(var.chk_home) and not xbmcvfs.exists(var.chkset_home):
                                xbmcvfs.copy(os.path.join(var.homelander), os.path.join(var.chkset_home))

                        if xbmcvfs.exists(var.chk_home) and xbmcvfs.exists(var.chkset_home):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.homelander').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.homelander').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.homelander').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.homelander")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Homelander Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Quicksilver
                try:
                        if xbmcvfs.exists(var.chk_quick) and not xbmcvfs.exists(var.quick_ud):
                                os.mkdir(var.quick_ud)
                                xbmcvfs.copy(os.path.join(var.quick), os.path.join(var.chkset_quick))
                                
                        if xbmcvfs.exists(var.chk_quick) and not xbmcvfs.exists(var.chkset_quick):
                                xbmcvfs.copy(os.path.join(var.quick), os.path.join(var.chkset_quick))

                        if xbmcvfs.exists(var.chk_quick) and xbmcvfs.exists(var.chkset_quick):
                                
                                chk_fanart_api = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.quicksilver').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.quicksilver")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Quicksilver Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Chains Genocide
                try:
                        if xbmcvfs.exists(var.chk_genocide) and not xbmcvfs.exists(var.genocide_ud):
                                os.mkdir(var.genocide_ud)
                                xbmcvfs.copy(os.path.join(var.genocide), os.path.join(var.chkset_genocide))
                                
                        if xbmcvfs.exists(var.chk_genocide) and not xbmcvfs.exists(var.chkset_genocide):
                                xbmcvfs.copy(os.path.join(var.genocide), os.path.join(var.chkset_genocide))

                        if xbmcvfs.exists(var.chk_genocide) and xbmcvfs.exists(var.chkset_genocide):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.chainsgenocide').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.chainsgenocide")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Chains Genocide Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Shazam
                try:
                        if xbmcvfs.exists(var.chk_shazam) and not xbmcvfs.exists(var.shazam_ud):
                                os.mkdir(var.shazam_ud)
                                xbmcvfs.copy(os.path.join(var.shazam), os.path.join(var.chkset_shazam))
                                
                        if xbmcvfs.exists(var.chk_shazam) and not xbmcvfs.exists(var.chkset_shazam):
                                xbmcvfs.copy(os.path.join(var.shazam), os.path.join(var.chkset_shazam))

                        if xbmcvfs.exists(var.chk_shazam) and xbmcvfs.exists(var.chkset_shazam):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.shazam').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.shazam').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.shazam').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.shazam")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Shazam Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Alvin
                try:
                        if xbmcvfs.exists(var.chk_alvin) and not xbmcvfs.exists(var.alvin_ud):
                                os.mkdir(var.alvin_ud)
                                xbmcvfs.copy(os.path.join(var.alvin), os.path.join(var.chkset_alvin))
                                
                        if xbmcvfs.exists(var.chk_alvin) and not xbmcvfs.exists(var.chkset_alvin):
                                xbmcvfs.copy(os.path.join(var.alvin), os.path.join(var.chkset_alvin))

                        if xbmcvfs.exists(var.chk_alvin) and xbmcvfs.exists(var.chkset_alvin):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.alvin').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.alvin').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.alvin').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.alvin")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Alvin Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Moria
                try:
                        if xbmcvfs.exists(var.chk_moria) and not xbmcvfs.exists(var.moria_ud):
                                os.mkdir(var.moria_ud)
                                xbmcvfs.copy(os.path.join(var.moria), os.path.join(var.chkset_moria))
                                
                        if xbmcvfs.exists(var.chk_moria) and not xbmcvfs.exists(var.chkset_moria):
                                xbmcvfs.copy(os.path.join(var.moria), os.path.join(var.chkset_moria))

                        if xbmcvfs.exists(var.chk_moria) and xbmcvfs.exists(var.chkset_moria):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.moria').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.moria').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.moria').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.moria")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Moria Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Absolution
                try:
                        if xbmcvfs.exists(var.chk_absol) and not xbmcvfs.exists(var.absol_ud):
                                os.mkdir(var.absol_ud)
                                xbmcvfs.copy(os.path.join(var.absol), os.path.join(var.chkset_absol))
                                
                        if xbmcvfs.exists(var.chk_absol) and not xbmcvfs.exists(var.chkset_absol):
                                xbmcvfs.copy(os.path.join(var.absol), os.path.join(var.chkset_absol))

                        if xbmcvfs.exists(var.chk_absol) and xbmcvfs.exists(var.chkset_absol):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.absolution').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.absolution').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.absolution').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.absolution")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Absolution Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #Nine Lives
                try:
                        if xbmcvfs.exists(var.chk_nine) and not xbmcvfs.exists(var.nine_ud):
                                os.mkdir(var.nine_ud)
                                xbmcvfs.copy(os.path.join(var.nine), os.path.join(var.chkset_nine))
                                
                        if xbmcvfs.exists(var.chk_nine) and not xbmcvfs.exists(var.chkset_nine):
                                xbmcvfs.copy(os.path.join(var.nine), os.path.join(var.chkset_nine))

                        if xbmcvfs.exists(var.chk_nine) and xbmcvfs.exists(var.chkset_nine):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.nine').getSetting("fanart.tv.user")
                                chk_imdb_api = xbmcaddon.Addon('plugin.video.nine').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('plugin.video.nine').getSetting("tm.user")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("fanart.tv.user", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.nine")
                                        addon.setSetting("tm.user", your_tmdb_api)
                except:
                        xbmc.log('%s: Nine Lives Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #TMDB Helper
                try:
                        if xbmcvfs.exists(var.chk_tmdbh) and not xbmcvfs.exists(var.tmdbh_ud):
                                os.mkdir(var.tmdbh_ud)
                                xbmcvfs.copy(os.path.join(var.tmdbh), os.path.join(var.chkset_tmdbh))
                                
                        if xbmcvfs.exists(var.chk_tmdbh) and not xbmcvfs.exists(var.chkset_tmdbh):
                                xbmcvfs.copy(os.path.join(var.tmdbh), os.path.join(var.chkset_tmdbh))

                        if xbmcvfs.exists(var.chk_tmdbh) and xbmcvfs.exists(var.chkset_tmdbh):

                                chk_fanart_api = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("fanarttv_clientkey")
                                chk_omdb_api = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("omdb_apikey")    
                                chk_mdb_api = xbmcaddon.Addon('plugin.video.themoviedb.helper').getSetting("mdblist_apikey")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                                        addon.setSetting("fanarttv_clientkey", your_fanart_api)

                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                                        addon.setSetting("omdb_apikey", your_omdb_api)
                                        
                                if not str(var.chk_accountmgr_mdb) == str(chk_mdb_api) or str(chk_mdb_api) == '':
                                        addon = xbmcaddon.Addon("plugin.video.themoviedb.helper")
                                        addon.setSetting("mdblist_apikey", your_mdb_api)
                except:
                        xbmc.log('%s: TMDBh Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Embuary Info
                try:
                        if xbmcvfs.exists(var.chk_embuary) and not xbmcvfs.exists(var.embuary_ud):
                                os.mkdir(var.embuary_ud)
                                xbmcvfs.copy(os.path.join(var.embuary), os.path.join(var.chkset_embuary))
                                
                        if xbmcvfs.exists(var.chk_embuary) and not xbmcvfs.exists(var.chkset_embuary):
                                xbmcvfs.copy(os.path.join(var.embuary), os.path.join(var.chkset_embuary))

                        if xbmcvfs.exists(var.chk_embuary) and xbmcvfs.exists(var.chkset_embuary):
                                
                                chk_omdb_api = xbmcaddon.Addon('script.embuary.info').getSetting("omdb_api_key")
                                chk_tmdb_api = xbmcaddon.Addon('script.embuary.info').getSetting("tmdb_api_key")
                                                                       
                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("script.embuary.info")
                                        addon.setSetting("omdb_api_key", your_omdb_api)
                                       
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.embuary.info")
                                        addon.setSetting("tmdb_api_key", your_tmdb_api)
                except:
                        xbmc.log('%s: Embuary Info Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Metahandler
                try:
                        if xbmcvfs.exists(var.chk_meta) and not xbmcvfs.exists(var.meta_ud):
                                os.mkdir(var.meta_ud)
                                xbmcvfs.copy(os.path.join(var.meta), os.path.join(var.chkset_meta))
                                
                        if xbmcvfs.exists(var.chk_meta) and not xbmcvfs.exists(var.chkset_meta):
                                xbmcvfs.copy(os.path.join(var.meta), os.path.join(var.chkset_meta))

                        if xbmcvfs.exists(var.chk_meta) and xbmcvfs.exists(var.chkset_meta):
                                
                                chk_tvdb_api = xbmcaddon.Addon('script.module.metahandler').getSetting("tvdb_api_key")
                                chk_omdb_api = xbmcaddon.Addon('script.module.metahandler').getSetting("omdb_api_key")
                                chk_tmdb_api = xbmcaddon.Addon('script.module.metahandler').getSetting("tmdb_api_key")
                                enable_tvdb = ("true")
                                enable_omdb_fallback = ("true")
                                enable_omdb_override = ("true")
                                enable_tmdb = ("true")
                                
                                if not str(var.chk_accountmgr_tvdb) == str(chk_tvdb_api) or str(chk_tvdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("tvdb_api_key", your_tvdb_api)
                                        
                                if not str(var.chk_accountmgr_omdb) == str(chk_omdb_api) or str(chk_omdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("omdb_api_key", your_omdb_api)
                                       
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("tmdb_api_key", your_tmdb_api)
                                        
                                if str(var.chk_accountmgr_tvdb) != '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("override_tvdb_key", enable_tvdb)

                                if str(var.chk_accountmgr_omdb) != '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("omdbapi_fallback", enable_omdb_fallback)
                                        
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("override_omdb_key", enable_omdb_override)

                                if str(var.chk_accountmgr_tmdb) != '':
                                        addon = xbmcaddon.Addon("script.module.metahandler")
                                        addon.setSetting("override_tmdb_key", enable_tmdb)
                                        
                except:
                        xbmc.log('%s: Metahandler Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #PVR Artwork Module
                try:
                        if xbmcvfs.exists(var.chk_pvr) and not xbmcvfs.exists(var.pvr_ud):
                                os.mkdir(var.pvr_ud)
                                xbmcvfs.copy(os.path.join(var.pvr), os.path.join(var.chkset_pvr))
                                
                        if xbmcvfs.exists(var.chk_pvr) and not xbmcvfs.exists(var.chkset_tmdbh):
                                xbmcvfs.copy(os.path.join(var.tmdbh), os.path.join(var.chkset_tmdbh))

                        if xbmcvfs.exists(var.chk_pvr) and xbmcvfs.exists(var.chkset_pvr):
                                
                                chk_trakt_api = xbmcaddon.Addon('script.module.pvr.artwork').getSetting("fanart_apikey")
                                chk_tmdb_api = xbmcaddon.Addon('script.module.pvr.artwork').getSetting("tmdb_apikey")
                                enable_fanart = ("true")
                                enable_fanart_prefer = ("true")
                                enable_tmdb = ("true")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("fanart_apikey", your_fanart_api)
                                       
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("tmdb_apikey", your_tmdb_api)

                                if str(var.chk_accountmgr_fanart) != '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("use_fanart_tv", enable_fanart)

                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("prefer_fanart_tv", enable_fanart_prefer)

                                if str(var.chk_accountmgr_tmdb) != '':
                                        addon = xbmcaddon.Addon("script.module.pvr.artwork")
                                        addon.setSetting("use_tmdb", enable_tmdb)
                except:
                        xbmc.log('%s: PVR Artwork Module Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #All Accounts
                try:
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.allaccounts_ud):
                                os.mkdir(var.allaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))
                                
                        if xbmcvfs.exists(var.chk_allaccounts) and not xbmcvfs.exists(var.chkset_allaccounts):
                                xbmcvfs.copy(os.path.join(var.allaccounts), os.path.join(var.chkset_allaccounts))

                        if xbmcvfs.exists(var.chk_allaccounts) and xbmcvfs.exists(var.chkset_allaccounts):
                                #Check Add-on API Keys
                                chk_fanart_api = xbmcaddon.Addon('script.module.allaccounts').getSetting("fanart.tv.api.key")
                                chk_imdb_api = xbmcaddon.Addon('script.module.allaccounts').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('script.module.allaccounts').getSetting("tmdb.api.key")
                                chk_tmdb_user = xbmcaddon.Addon('script.module.allaccounts').getSetting("tmdb.username")
                                chk_tmdb_pass = xbmcaddon.Addon('script.module.allaccounts').getSetting("tmdb.password")
                                chk_tmdb_session = xbmcaddon.Addon('script.module.allaccounts').getSetting("tmdb.session_id")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        #Write Meta API to settings.xml
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("fanart.tv.api.key", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("tmdb.api.key", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("tmdb.username", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("tmdb.password", your_tmdb_pass)
                                        
                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("script.module.allaccounts")
                                        addon.setSetting("tmdb.session_id", your_tmdb_session)
                except:
                        xbmc.log('%s: All Accounts Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
                
        #My Accounts
                try:
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.myaccounts_ud):
                                os.mkdir(var.myaccounts_ud)
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                                
                        if xbmcvfs.exists(var.chk_myaccounts) and not xbmcvfs.exists(var.chkset_myaccounts):
                                xbmcvfs.copy(os.path.join(var.myaccounts), os.path.join(var.chkset_myaccounts))
                        
                        if xbmcvfs.exists(var.chk_myaccounts) and xbmcvfs.exists(var.chkset_myaccounts):

                                chk_fanart_api = xbmcaddon.Addon('script.module.myaccounts').getSetting("fanart.tv.api.key")
                                chk_imdb_api = xbmcaddon.Addon('script.module.myaccounts').getSetting("imdb.user")    
                                chk_tmdb_api = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.api.key")
                                chk_tmdb_user = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.username")
                                chk_tmdb_pass = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.password")
                                chk_tmdb_session = xbmcaddon.Addon('script.module.myaccounts').getSetting("tmdb.session_id")
                                
                                if not str(var.chk_accountmgr_fanart) == str(chk_fanart_api) or str(chk_fanart_api) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("fanart.tv.api.key", your_fanart_api)

                                if not str(var.chk_accountmgr_imdb) == str(chk_imdb_api) or str(chk_imdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("imdb.user", your_imdb_api)
                                        
                                if not str(var.chk_accountmgr_tmdb) == str(chk_tmdb_api) or str(chk_tmdb_api) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.api.key", your_tmdb_api)

                                if not str(var.chk_accountmgr_tmdb_user) == str(chk_tmdb_user) or str(chk_tmdb_user) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.username", your_tmdb_user)

                                if not str(var.chk_accountmgr_tmdb_pass) == str(chk_tmdb_pass) or str(chk_tmdb_pass) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.password", your_tmdb_pass)
                                        
                                if not str(var.chk_accountmgr_tmdb_session) == str(chk_tmdb_session) or str(chk_tmdb_session) == '':
                                        addon = xbmcaddon.Addon("script.module.myaccounts")
                                        addon.setSetting("tmdb.session_id", your_tmdb_session)
                except:
                        xbmc.log('%s: My Accounts Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Fentastic & Nimbus Skin
                try:
                        json_query = xbmc.executeJSONRPC('{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"lookandfeel.skin"}, "id":1}')
                        json_query = json.loads(json_query)
                        skin = ''
                        if 'result' in json_query and 'value' in json_query['result']:
                                skin_chk = json_query['result']['value']
                                #xbmc.log(str(skin), xbmc.LOGINFO)
                        if xbmcvfs.exists(var.chk_fentastic) and xbmcvfs.exists(var.chkset_fentastic) and skin_chk == 'skin.fentastic':
                                with open(var.path_fentastic) as f:
                                        if var.chk_accountmgr_mdb in f.read():
                                                pass
                                        else:  
                                                xbmc.executebuiltin("Skin.SetString(mdblist_api_key, %s)" % your_mdb_api)
                        if xbmcvfs.exists(var.chk_nimbus) and xbmcvfs.exists(var.chkset_nimbus) and skin_chk == 'skin.nimbus':
                                with open(var.path_nimbus) as f:
                                        if var.chk_accountmgr_mdb in f.read():
                                                pass
                                        else:
                                                xbmc.executebuiltin("Skin.SetString(mdblist_api_key, %s)" % your_mdb_api)
                except:
                        xbmc.log('%s: Skin Metadata Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
