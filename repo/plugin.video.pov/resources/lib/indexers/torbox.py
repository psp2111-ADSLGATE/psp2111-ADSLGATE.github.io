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
				url_params = {'mode': 'torbox.browse_tb_cloud', 'folder_id': item['id']}
				delete_params = {'mode': 'torbox.delete', 'folder_id': item['id']}
				cm_append(('[B]%s %s[/B]' % (delete_str, folder_str.capitalize()), 'RunPlugin(%s)' % build_url(delete_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_tb_icon, 'poster': default_tb_icon, 'thumb': default_tb_icon, 'fanart': fanart, 'banner': default_tb_icon})
				yield (url, listitem, True)
			except: pass
	cloud_folders = TorBox.user_cloud()
	folders = [i for i in cloud_folders['data'] if i['download_finished']]
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_tb_cloud(folder_id):
	def _builder():
		for count, item in enumerate(video_files, 1):
			try:
				cm = []
				name = clean_file_name(item['short_name']).upper()
				size = float(int(item['size']))/1073741824
				display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_str, size, name)
				url_params = {'mode': 'torbox.resolve_tb', 'url': '%d,%d' % (int(folder_id), item['id']), 'play': 'true'}
				url = build_url(url_params)
				down_file_params = {'mode': 'downloader', 'url': '%d,%d' % (int(folder_id), item['id']),
									'name': name, 'action': 'cloud.torbox', 'image': default_tb_icon}
				cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_tb_icon, 'poster': default_tb_icon, 'thumb': default_tb_icon, 'fanart': fanart, 'banner': default_tb_icon})
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	torrent_files = TorBox.user_cloud_info(folder_id)
	video_files = [i for i in torrent_files['data']['files'] if i['short_name'].lower().endswith(tuple(extensions))]
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def tb_delete(folder_id):
	if not kodi_utils.confirm_dialog(): return
	result = TorBox.delete_torrent(folder_id)
	if not result['success']: return kodi_utils.notification(32574)
	TorBox.clear_cache()
	kodi_utils.container_refresh()

def resolve_tb(params):
	file_id = params['url']
	resolved_link = TorBox.unrestrict_link(file_id)
	if params.get('play', 'false') != 'true': return resolved_link
	from modules.player import POVPlayer
	POVPlayer().run(resolved_link, 'video')

def tb_account_info():
	try:
		kodi_utils.show_busy_dialog()
		plans = {0: 'Free plan', 1: 'Essential plan', 2: 'Pro plan', 3: 'Standard plan'}
		account_info = TorBox.account_info()
		account_info = account_info['data']
		body = []
		append = body.append
		append('[B]Email[/B]: %s' % account_info['email'])
		append('[B]customer[/B]: %s' % account_info['customer'])
		append('[B]Plan[/B]: %s' % plans[account_info['plan']])
		append('[B]Expires[/B]: %s' % account_info['premium_expires_at'])
		append('[B]Downloaded[/B]: {:,}'.format(account_info['total_downloaded']))
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text('TorBox'.upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

