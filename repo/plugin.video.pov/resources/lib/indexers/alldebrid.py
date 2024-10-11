from sys import argv
import json
from apis.alldebrid_api import AllDebridAPI
from modules import kodi_utils
from modules.source_utils import supported_video_extensions
from modules.utils import clean_file_name, normalize
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
make_listitem = kodi_utils.make_listitem
default_ad_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/alldebrid.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
folder_str, file_str, archive_str, down_str = ls(32742).upper(), ls(32743).upper(), ls(32982), ls(32747)
extensions = supported_video_extensions()
AllDebrid = AllDebridAPI()

def ad_torrent_cloud(folder_id=None):
	def _builder():
		for count, item in enumerate(cloud_dict, 1):
			try:
				folder_name = item['filename']
				display = '%02d | [B]%s[/B] | [I]%s [/I]' % (count, folder_str, clean_file_name(normalize(folder_name)).upper())
				url_params = {'mode': 'alldebrid.browse_ad_cloud', 'folder': json.dumps(item['links'])}
				url = build_url(url_params)
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_ad_icon, 'poster': default_ad_icon, 'thumb': default_ad_icon, 'fanart': fanart, 'banner': default_ad_icon})
				yield (url, listitem, True)
			except: pass
	try: cloud_dict = [i for i in AllDebrid.user_cloud()['magnets'] if i['statusCode'] == 4]
	except: cloud_dict = []
	__handle__ = int(argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def browse_ad_cloud(folder):
	def _builder():
		for count, item in enumerate(links, 1):
			try:
				cm = []
				url_link = item['link']
				name = clean_file_name(item['filename']).upper()
				size = item['size']
				display_size = float(int(size))/1073741824
				display = '%02d | [B]%s[/B] | %.2f GB | [I]%s [/I]' % (count, file_str, display_size, name)
				url_params = {'mode': 'alldebrid.resolve_ad', 'url': url_link, 'play': 'true'}
				url = build_url(url_params)
				down_file_params = {'mode': 'downloader', 'name': name, 'url': url_link,
									'action': 'cloud.alldebrid', 'image': default_ad_icon}
				cm.append((down_str,'RunPlugin(%s)' % build_url(down_file_params)))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.addContextMenuItems(cm)
				listitem.setArt({'icon': default_ad_icon, 'poster': default_ad_icon, 'thumb': default_ad_icon, 'fanart': fanart, 'banner': default_ad_icon})
				listitem.setInfo('video', {})
				yield (url, listitem, False)
			except: pass
	try: links = [i for i in json.loads(folder) if i['filename'].lower().endswith(tuple(extensions))]
	except: links = []
	__handle__ = int(argv[1])
	kodi_utils.add_items(__handle__, list(_builder()))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.premium')

def resolve_ad(params):
	url = params['url']
	resolved_link = AllDebrid.unrestrict_link(url)
	if params.get('play', 'false') != 'true' : return resolved_link
	from modules.player import POVPlayer
	POVPlayer().run(resolved_link, 'video')

def ad_account_info():
	from datetime import datetime
	try:
		kodi_utils.show_busy_dialog()
		account_info = AllDebrid.account_info()['user']
		username = account_info['username']
		email = account_info['email']
		status = 'Premium' if account_info['isPremium'] else 'Not Active'
		expires = datetime.fromtimestamp(account_info['premiumUntil'])
		days_remaining = (expires - datetime.today()).days
		body = []
		append = body.append
		append(ls(32755) % username)
		append(ls(32756) % email)
		append(ls(32757) % status)
		append(ls(32750) % expires)
		append(ls(32751) % days_remaining)
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text(ls(32063).upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

