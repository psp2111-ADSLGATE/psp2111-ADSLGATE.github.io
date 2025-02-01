import xbmc, xbmcaddon
import xbmcvfs
import os

from pathlib import Path
from accountmgr.modules import control
from accountmgr.modules.db import ext_db
from libs.common import var

char_remov = ["'", ",", ")","("]

class Auth:
        def ext_auth(self):

        #Fen
                try:
                        if xbmcvfs.exists(var.chk_fen) and xbmcvfs.exists(var.chkset_fen) and xbmcvfs.exists(var.chk_coco): #Check that the addon and external provider are installed
                                addon = xbmcaddon.Addon("plugin.video.fen")
                                chk_auth = addon.getSetting("external_scraper.module")
                                if chk_auth == 'script.module.cocoscrapers':
                                        pass
                                else:
                                        addon.setSetting("provider.external", 'true')
                                        addon.setSetting("external_scraper.name", 'CocoScrapers Module')
                                        addon.setSetting("external_scraper.module", 'script.module.cocoscrapers')
                except:
                        xbmc.log('%s: Fen Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
 
        #Fen Light
                try:
                        if xbmcvfs.exists(var.chk_fenlt) and xbmcvfs.exists(var.chkset_fenlt) and xbmcvfs.exists(var.chk_coco): #Check that the addon and external provider are installed
                            
                            #Create database connection
                            from accountmgr.modules.db import ext_db
                            conn = ext_db.create_conn(var.fenlt_settings_db)
                            
                            #Get add-on settings to compare
                            with conn:
                                cursor = conn.cursor()
                                cursor.execute('''SELECT setting_value FROM settings WHERE setting_id = ?''', ('external_scraper.module',))
                                auth_ext = cursor.fetchone()
                                chk_auth_fenlt = str(auth_ext)
                                cursor.close()
                                
                                #Clean up database results
                                for char in char_remov:
                                    chk_auth_fenlt = chk_auth_fenlt.replace(char, "")
                                    
                                if not chk_auth_fenlt == 'script.module.cocoscrapers': #If external provider is set, authorization is skipped
                                    
                                    #Write settings to database
                                    from accountmgr.modules.db import ext_db
                                    ext_db.auth_fenlt_ext()
                                    var.remake_settings()
                except:
                        xbmc.log('%s: Fen Light Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Umbrella
                try:
                        if xbmcvfs.exists(var.chk_umb) and xbmcvfs.exists(var.chkset_umb) and xbmcvfs.exists(var.chk_coco):
                                addon = xbmcaddon.Addon("plugin.video.umbrella")
                                chk_auth = addon.getSetting("external_provider.module")
                                if chk_auth == 'script.module.cocoscrapers':
                                        pass
                                else:
                                        addon.setSetting("provider.external.enabled", 'true')
                                        addon.setSetting("external_provider.name", 'cocoscrapers')
                                        addon.setSetting("external_provider.module", 'script.module.cocoscrapers')
                except:
                        xbmc.log('%s: Umbrella Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass

        #Infinity
                try:
                        if xbmcvfs.exists(var.chk_infinity) and xbmcvfs.exists(var.chkset_infinity) and xbmcvfs.exists(var.chk_coco):
                                addon = xbmcaddon.Addon("plugin.video.infinity")
                                chk_auth = addon.getSetting("external_provider.module")
                                if chk_auth == 'script.module.cocoscrapers':
                                        pass
                                else:
                                        addon.setSetting("provider.external.enabled", 'true')
                                        addon.setSetting("external_provider.name", 'cocoscrapers')
                                        addon.setSetting("external_provider.module", 'script.module.cocoscrapers')
                except:
                        xbmc.log('%s: Infinity Ext Provider Failed!' % var.amgr, xbmc.LOGINFO)
                        pass
