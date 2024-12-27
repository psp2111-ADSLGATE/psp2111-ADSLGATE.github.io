import sys
from apis.torbox_api import TorBoxAPI
from modules import kodi_utils
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, normalize
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
default_tb_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/torbox.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
folder_str, file_str, delete_str, down_str = ls(32742).upper(), ls(32743).upper(), ls(32785), ls(32747)
extensions = supported_video_extensions()
TorBox = TorBoxAPI()

def tb_torrent_cloud():
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
				listitem.setArt({'icon': default_tb_icon, 'poster': default_tb_icon, 'thumb': default_tb_icon, 'fanart': fanart, 'banner': default_tb_icon})
				yield (url, listitem, True)
			except: pass
	folders = []
	try: folders += [{**i, 'mediatype': 'torent'} for i in TorBox.user_cloud() if i['download_finished']]
	except: pass
	try: folders += [{**i, 'mediatype': 'usenet'} for i in TorBox.user_cloud_usenet() if i['download_finished']]
	except: pass
	folders.sort(key=lambda k: k['updated_at'], reverse=True)
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_tb_cloud(folder_id, media_type):
	def _builder():
		for count, item in enumerate(video_files, 1):
			try:
				cm = []
				name = clean_file_name(item['short_name']).upper()
				size = float(int(item['size']))/1073741824
				display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_str, size, name)
				params = {'url': item['url'], 'media_type': item['mediatype']}
				url_params = {'mode': 'torbox.resolve_tb', 'play': 'true', **params}
				down_file_params = {'mode': 'downloader', 'action': 'cloud.torbox', 'name': name, 'image': default_tb_icon, **params}
				cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_tb_icon, 'poster': default_tb_icon, 'thumb': default_tb_icon, 'fanart': fanart, 'banner': default_tb_icon})
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	if media_type == 'usenet': files = TorBox.user_cloud_usenet(folder_id)
	else: files = TorBox.user_cloud(folder_id)
	video_files = [
		{**i, 'url': '%d,%d' % (int(folder_id), i['id']), 'mediatype': media_type}
		for i in files['files'] if i['short_name'].lower().endswith(tuple(extensions))
	]
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def tb_delete(folder_id, media_type):
	if not kodi_utils.confirm_dialog(): return
	if media_type == 'usenet': result = TorBox.delete_usenet(folder_id)
	else: result = TorBox.delete_torrent(folder_id)
	if not result: return kodi_utils.notification(32574)
	TorBox.clear_cache()
	kodi_utils.container_refresh()

def resolve_tb(params):
	file_id, media_type = params['url'], params['media_type']
	if media_type == 'usenet': resolved_link = TorBox.unrestrict_usenet(file_id)
	else: resolved_link = TorBox.unrestrict_link(file_id)
	if params.get('play', 'false') != 'true': return resolved_link
	from modules.player import POVPlayer
	POVPlayer().run(resolved_link, 'video')

def tb_account_info():
	try:
		kodi_utils.show_busy_dialog()
		plans = {0: 'Free plan', 1: 'Essential plan', 2: 'Pro plan', 3: 'Standard plan'}
		account_info = TorBox.account_info()
		body = []
		append = body.append
		append('[B]Email[/B]: %s' % account_info['email'])
		append('[B]Customer[/B]: %s' % account_info['customer'])
		append('[B]Plan[/B]: %s' % plans[account_info['plan']])
		append('[B]Expires[/B]: %s' % account_info['premium_expires_at'])
		append('[B]Downloaded[/B]: %s' % account_info['total_downloaded'])
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text('TorBox'.upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

