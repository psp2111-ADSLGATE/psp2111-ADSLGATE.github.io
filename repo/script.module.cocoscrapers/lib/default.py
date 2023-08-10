# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from sys import argv
from urllib.parse import parse_qsl
from cocoscrapers import sources_cocoscrapers
from cocoscrapers.modules import control

params = dict(parse_qsl(argv[2].replace('?', '')))
action = params.get('action')

if action is None:
	control.openSettings('0.0', 'script.module.cocoscrapers')

if action == "CocoScrapersSettings":
	control.openSettings('0.0', 'script.module.cocoscrapers')

elif action == 'ShowChangelog':
	from cocoscrapers.modules import changelog
	changelog.get()

elif action == 'ShowHelp':
	from cocoscrapers.help import help
	help.get(params.get('name'))

elif action == "Defaults":
	control.setProviderDefaults()

elif action == "toggleAll":
	sourceList = []
	sourceList = sources_cocoscrapers.all_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllHosters":
	sourceList = []
	sourceList = sources_cocoscrapers.hoster_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllTorrent":
	sourceList = []
	sourceList = sources_cocoscrapers.torrent_providers
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == "toggleAllPackTorrent":
	control.execute('RunPlugin(plugin://script.module.cocoscrapers/?action=toggleAllTorrent&amp;setting=false)')
	control.sleep(500)
	sourceList = []
	from cocoscrapers import pack_sources
	sourceList = pack_sources()
	for i in sourceList:
		source_setting = 'provider.' + i
		control.setSetting(source_setting, params['setting'])

elif action == 'cleanSettings':
	control.clean_settings()

elif action == 'undesirablesSelect':
	from cocoscrapers.modules.undesirables import undesirablesSelect
	undesirablesSelect()

elif action == 'undesirablesInput':
	from cocoscrapers.modules.undesirables import undesirablesInput
	undesirablesInput()

elif action == 'undesirablesUserRemove':
	from cocoscrapers.modules.undesirables import undesirablesUserRemove
	undesirablesUserRemove()

elif action == 'undesirablesUserRemoveAll':
	from cocoscrapers.modules.undesirables import undesirablesUserRemoveAll
	undesirablesUserRemoveAll()

elif action == 'tools_clearLogFile':
	from cocoscrapers.modules import log_utils
	cleared = log_utils.clear_logFile()
	if cleared == 'canceled': pass
	elif cleared: control.notification(message='CocoScrapers Log File Successfully Cleared')
	else: control.notification(message='Error clearing CocoScrapers Log File, see kodi.log for more info')

elif action == 'tools_viewLogFile':
	from cocoscrapers.modules import log_utils
	log_utils.view_LogFile(params.get('name'))

elif action == 'tools_uploadLogFile':
	from cocoscrapers.modules import log_utils
	log_utils.upload_LogFile()

elif action == 'plexAuth':
	from cocoscrapers.modules import plex
	plex.Plex().auth()

elif action == 'plexRevoke':
	from cocoscrapers.modules import plex
	plex.Plex().revoke()

elif action == 'plexSelectShare':
	from cocoscrapers.modules import plex
	plex.Plex().get_plexshare_resource()

elif action == 'plexSeeShare':
	from cocoscrapers.modules import plex
	plex.Plex().see_active_shares()

elif action == 'ShowOKDialog':
	control.okDialog(params.get('title', 'default'), int(params.get('message', '')))