import sys
from apis.offcloud_api import OffcloudAPI
from modules import kodi_utils
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, normalize
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
make_listitem = kodi_utils.make_listitem
build_url = kodi_utils.build_url
default_oc_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/offcloud.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
folder_str, file_str, delete_str, down_str = ls(32742).upper(), ls(32743).upper(), ls(32785), ls(32747)
extensions = supported_video_extensions()
Offcloud = OffcloudAPI()

def oc_torrent_cloud():
	def _builder():
		for count, item in enumerate(folders, 1):
			try:
				cm = []
				cm_append = cm.append
				is_folder = item['isDirectory']
				request_id, folder_name, server = item['requestId'], item['fileName'], item['server']
				delete_params = {'mode': 'offcloud.delete', 'folder_id': request_id}
				if is_folder:
					display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, folder_str, clean_file_name(normalize(folder_name)).upper())
					# need to complete downloader for zip filenames, oc head request does not give Content-Length header
#					zip = Offcloud.requote_uri(Offcloud.build_zip(server, request_id, folder_name))
					url_params = {'mode': 'offcloud.browse_oc_cloud', 'folder_id': request_id}
#					down_file_params = {'mode': 'downloader', 'action': 'archive', 'name': folder_name, 'url': zip, 'image': default_oc_icon}
					cm_append(('[B]%s %s[/B]' % (delete_str, folder_str.capitalize()), 'RunPlugin(%s)' % build_url(delete_params)))
#					cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				else:
					display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, file_str, clean_file_name(normalize(folder_name)).upper())
					link = Offcloud.requote_uri(Offcloud.build_url(server, request_id, folder_name))
					url_params = {'mode': 'offcloud.resolve_oc', 'url': link, 'play': 'true'}
					down_file_params = {'mode': 'downloader', 'action': 'cloud.offcloud_direct', 'name': folder_name, 'url': link, 'image': default_oc_icon}
					cm_append(('[B]%s %s[/B]' % (delete_str, file_str.capitalize()), 'RunPlugin(%s)' % build_url(delete_params)))
					cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_oc_icon, 'poster': default_oc_icon, 'thumb': default_oc_icon, 'fanart': fanart, 'banner': default_oc_icon})
				yield (url, listitem, is_folder)
			except: pass
	cloud_folders = Offcloud.user_cloud()
	folders = [i for i in cloud_folders if i['status'] == 'downloaded']
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_oc_cloud(folder_id):
	def _builder():
		for count, item in enumerate(video_files, 1):
			try:
				cm = []
				name = item.split('/')[-1]
				name = clean_file_name(name).upper()
				link = Offcloud.requote_uri(item)
				display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, file_str, name)
				url_params = {'mode': 'offcloud.resolve_oc', 'url': link, 'play': 'true'}
				down_file_params = {'mode': 'downloader', 'action': 'cloud.offcloud_direct', 'name': name, 'url': link, 'image': default_oc_icon}
				cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_oc_icon, 'poster': default_oc_icon, 'thumb': default_oc_icon, 'fanart': fanart, 'banner': default_oc_icon})
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	torrent_files = Offcloud.user_cloud(folder_id)
	video_files = [i for i in torrent_files if i.lower().endswith(tuple(extensions))]
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def oc_delete(folder_id):
	if not kodi_utils.confirm_dialog(): return
	result = Offcloud.delete_torrent(folder_id)
	if 'success' not in result: return kodi_utils.notification(32574)
	Offcloud.clear_cache()
	kodi_utils.container_refresh()

def resolve_oc(params):
	url = params['url']
	if params.get('play', 'false') != 'true': return url
	from modules.player import POVPlayer
	POVPlayer().run(url, 'video')

def oc_account_info():
	try:
		kodi_utils.show_busy_dialog()
		account_info = Offcloud.account_info()
		body = []
		append = body.append
		append('[B]Email[/B]: %s' % account_info['email'])
		append('[B]userId[/B]: %s' % account_info['userId'])
		append('[B]Premium[/B]: %s' % account_info['isPremium'])
		append('[B]Expires[/B]: %s' % account_info['expirationDate'])
		append('[B]Cloud Limit[/B]: {:,}'.format(account_info['limits']['cloud']))
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text('Offcloud'.upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

