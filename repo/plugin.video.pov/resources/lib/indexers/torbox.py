import sys
from apis.torbox_api import TorBoxAPI
from modules import kodi_utils
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, normalize
# from modules.kodi_utils import logger

ls, build_url, make_listitem = kodi_utils.local_string, kodi_utils.build_url, kodi_utils.make_listitem
folder_str, file_str, delete_str, down_str = ls(32742).upper(), ls(32743).upper(), ls(32785), ls(32747)
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
default_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/torbox.png')
default_art = {'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon}
TorBox, extensions = TorBoxAPI(), supported_video_extensions()

def tb_torrent_cloud(media_type):
	def _builder():
		for count, item in enumerate(folders, 1):
			try:
				cm = []
				cm_append = cm.append
				display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, folder_str, clean_file_name(normalize(item['name'])).upper())
				url_params = {'mode': 'torbox.browse_tb_cloud', 'folder_id': item['id'], 'media_type': item['mediatype']}
				delete_params = {'mode': 'torbox.delete', 'folder_id': item['id'], 'media_type': item['mediatype']}
				cm_append(('[B]%s %s[/B]' % (delete_str, folder_str.capitalize()), 'RunPlugin(%s)' % build_url(delete_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt(default_art)
				yield (url, listitem, True)
			except: pass
	if   media_type == 'usenet': folders = TorBox.user_cloud_usenet()
	elif media_type == 'webdl': folders = TorBox.user_cloud_webdl()
	else: folders = TorBox.user_cloud()
	folders = [{**i, 'mediatype': media_type} for i in folders if i['download_finished']]
	folders.sort(key=lambda k: k['updated_at'], reverse=True)
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_tb_cloud(folder_id, media_type):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				cm = []
				cm_append = cm.append
				name = clean_file_name(item['short_name']).upper()
				size = float(int(item['size']))/1073741824
				display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_str, size, name)
				params = {'url': item['url'], 'media_type': item['mediatype']}
				url_params = {'mode': 'torbox.resolve_tb', 'play': 'true', **params}
				down_file_params = {'mode': 'downloader', 'action': 'cloud.torbox', 'name': name, 'image': default_icon, **params}
				cm_append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt(default_art)
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	if   media_type == 'usenet': files = TorBox.user_cloud_usenet(folder_id)
	elif media_type == 'webdl': files = TorBox.user_cloud_webdl(folder_id)
	else: files = TorBox.user_cloud(folder_id)
	files = [
		{**i, 'url': '%d,%d' % (int(folder_id), i['id']), 'mediatype': media_type}
		for i in files['files'] if i['short_name'].lower().endswith(tuple(extensions))
	]
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def tb_usenet_query(params):
	def _builder():
		for count, item in enumerate(files, 1):
			try:
				name = clean_file_name(item['raw_title']).upper()
				age, parts, tracker = item['age'], item['files'], item['tracker']
				size = float(int(item['size']))/1073741824
				if item['owned']: display = '%02d | %.2f GB | [COLOR cyan]CLOUD[/COLOR] | [I]%s[/I]'
				elif item['cached']: display = '%02d | %.2f GB | [COLOR magenta]CACHED[/COLOR] | [I]%s[/I]'
				else: display = '%02d | %.2f GB | [I]%s[/I]'
				display = display % (count, size, name)
				plot = '[B]Tracker[/B]: [I]%s[/I][CR][CR][B]Files[/B]: %s[CR][CR][B]Age[/B]: %s' % (tracker, parts, age)
				url_params = {'mode': 'manual_add_nzb_to_cloud', 'provider': 'TorBox', 'url': item['nzb'], 'name': name}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt(default_art)
				listitem.setInfo('video', {'plot': plot}) if KODI_VERSION < 20 else listitem.getVideoInfoTag().setPlot(plot)
				yield (url, listitem, False)
			except: pass
	KODI_VERSION = kodi_utils.get_kodi_version()
	query, imdb_id = params.get('query'), params.get('imdb_id')
	season, episode = params.get('season'), params.get('episode')
	files = TorBox.usenet_query(query, season, episode, imdb_id)
	uncached = [i for i in files if not i['cached']]
	files = [i for i in files if i['cached']] + uncached
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def tb_delete(folder_id, media_type):
	if not kodi_utils.confirm_dialog(): return
	if   media_type == 'usenet': result = TorBox.delete_usenet(folder_id)
	elif media_type == 'webdl': result = TorBox.delete_webdl(folder_id)
	else: result = TorBox.delete_torrent(folder_id)
	if not result: return kodi_utils.notification(32574)
	TorBox.clear_cache()
	kodi_utils.container_refresh()

def resolve_tb(params):
	file_id, media_type = params['url'], params['media_type']
	if   media_type == 'usenet': resolved_link = TorBox.unrestrict_usenet(file_id)
	elif media_type == 'webdl': resolved_link = TorBox.unrestrict_webdl(file_id)
	else: resolved_link = TorBox.unrestrict_link(file_id)
	if params.get('play', 'false') != 'true': return resolved_link
	from modules.player import POVPlayer
	POVPlayer().run(resolved_link, 'video')

def tb_account_info():
	from datetime import datetime
	from modules.utils import datetime_workaround
	try:
		kodi_utils.show_busy_dialog()
		plans = {0: 'Free', 1: 'Essential', 2: 'Pro', 3: 'Standard'}
		account_info = TorBox.account_info()
		expires = datetime_workaround(account_info['premium_expires_at'], '%Y-%m-%dT%H:%M:%SZ')
		days_remaining = (expires - datetime.today()).days
		body = []
		append = body.append
		append(ls(32758) % account_info['email'])
		append(ls(32755) % account_info['customer'])
		append(ls(32757) % plans[account_info['plan']])
		append(ls(32750) % expires.strftime('%Y-%m-%d'))
		append(ls(32751) % days_remaining)
		append('[B]Downloaded[/B]: %s' % account_info['total_downloaded'])
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text('TorBox'.upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

