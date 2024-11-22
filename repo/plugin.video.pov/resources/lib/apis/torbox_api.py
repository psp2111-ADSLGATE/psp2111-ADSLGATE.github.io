import re
import requests
from sys import exit as sysexit
from threading import Thread
from caches.main_cache import cache_object
from modules import kodi_utils
# logger = kodi_utils.logger

ls, get_setting, set_setting = kodi_utils.local_string, kodi_utils.get_setting, kodi_utils.set_setting
base_url = 'https://api.torbox.app/v1/api'
timeout = 10.0
session = requests.Session()
session.mount(base_url, requests.adapters.HTTPAdapter(max_retries=1))

class TorBoxAPI:
	download = '/torrents/requestdl'
	remove = '/torrents/controltorrent'
	stats = '/user/me'
	history = '/torrents/mylist'
	explore = '/torrents/mylist?id=%s'
	cache = '/torrents/checkcached'
	cloud = '/torrents/createtorrent'

	def __init__(self):
		self.api_key = get_setting('tb.token')

	def _request(self, method, path, params=None, json=None, data=None):
		if not self.api_key: return
		session.headers['Authorization'] = 'Bearer %s' % self.api_key
		full_path = '%s%s' % (base_url, path)
		r = session.request(method, full_path, params=params, json=json, data=data, timeout=timeout)
		try: r.raise_for_status()
		except Exception as e: kodi_utils.logger('torbox error', f"{e}\n{r.json()}")
		try: r = r.json()
		except: r = {}
		return r

	def _GET(self, url, params=None):
		return self._request('get', url, params=params)

	def _POST(self, url, params=None, json=None, data=None):
		return self._request('post', url, params=params, json=json, data=data)

	def account_info(self):
		return self._GET(self.stats)

	def user_cloud(self):
		string = 'pov_tb_user_cloud'
		url = self.history
		return cache_object(self._GET, string, url, False, 0.5)

	def user_cloud_info(self, request_id=''):
		string = 'pov_tb_user_cloud_%s' % request_id
		url = self.explore % request_id
		return cache_object(self._GET, string, url, False, 0.5)

	def torrent_info(self, request_id=''):
		url = self.explore % request_id
		return self._GET(url)

	def delete_torrent(self, request_id=''):
		data = {'torrent_id': request_id, 'operation': 'delete'}
		return self._POST(self.remove, json=data)

	def unrestrict_link(self, file_id):
		torrent_id, file_id = file_id.split(',')
		params = {'token': self.api_key, 'torrent_id': torrent_id, 'file_id': file_id}
		try: return self._GET(self.download, params=params)['data']
		except: return None

	def add_magnet(self, magnet):
		data = {'magnet': magnet, 'seed': 3, 'allow_zip': False}
		return self._POST(self.cloud, data=data)

	def check_cache_single(self, hash):
		return self._GET(self.cache, params={'hash': hash, 'format': 'list'})

	def check_cache(self, hashlist):
		data = {'hashes': hashlist}
		return self._POST(self.cache, params={'format': 'list'}, json=data)

	def create_transfer(self, magnet_url):
		result = self.add_magnet(magnet_url)
		if not result['success']: return 'failed'
		return result

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, extras_filter
		try:
			file_url, match = None, False
			extensions = supported_video_extensions()
			extras_filtering_list = extras_filter()
			check = self.check_cache_single(info_hash)
			match = info_hash in [i['hash'] for i in check['data']]
			if not match: return None
			torrent = self.add_magnet(magnet_url)
			if not torrent['success']: return None
			torrent_id = torrent['data']['torrent_id']
			torrent_files = self.torrent_info(torrent_id)
			torrent_files = [(i['id'], i['short_name'], i['size']) for i in torrent_files['data']['files']]
			vid_only = [item for item in torrent_files if item[1].lower().endswith(tuple(extensions))]
			remainder = [i for i in torrent_files if i not in vid_only]
			torrent_files = vid_only + remainder
			if not torrent_files: return None
			if season:
				torrent_files = [i for i in torrent_files if seas_ep_filter(season, episode, i[1])]
				if not torrent_files: return None
			else:
				if self._m2ts_check(torrent_files): self.delete_torrent(torrent_id) ; return None
				else: torrent_files.sort(key=lambda k: k[2], reverse=True)
			file_key = [i[0] for i in torrent_files if not any(x in i[1] for x in extras_filtering_list)][0]
			file_link = self.unrestrict_link('%d,%d' % (torrent_id, file_key))
			return file_link
		except Exception as e:
			kodi_utils.logger('main exception', str(e))
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			extensions = supported_video_extensions()
			torrent = self.add_magnet(magnet_url)
			if not torrent['success']: return None
			torrent_id = torrent['data']['torrent_id']
			torrent_files = torrent_files = self.torrent_info(torrent_id)
			torrent_files = [(i['id'], i['short_name'], i['size']) for i in torrent_files['data']['files']]
			end_results = []
			append = end_results.append
			for item in torrent_files:
				if item[1].lower().endswith(tuple(extensions)):
					append({'link': '%d,%d' % (torrent_id, item[0]), 'filename': item[1], 'size': item[2]})
			#self.delete_torrent(torrent_id) # untested if link will play if torrent deleted
			return end_results
		except Exception:
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		kodi_utils.show_busy_dialog()
		result = self.create_transfer(magnet_url)
		kodi_utils.hide_busy_dialog()
		if result == 'failed': kodi_utils.ok_dialog(heading=32733, text=32574)
		else: kodi_utils.ok_dialog(heading=32733, text=ls(32732) % 'TorBox', top_space=True)
		if 'torrent_id' in result['data']: return True
		return False

	def _m2ts_check(self, folder_items):
		for item in folder_items:
			if item[1].endswith('.m2ts'): return True
		return False

	def user_cloud_clear(self):
		if not kodi_utils.confirm_dialog(): return
		data = {'all': True, 'operation': 'delete'}
		self._POST(self.remove, json=data)
		self.clear_cache()

	def auth(self):
		api_key = kodi_utils.dialog.input('TorBox API Key:')
		if not api_key: return
		self.api_key = api_key
		r = self._GET('/user/me')
		customer = r['data']['customer']
		set_setting('tb.token', api_key)
		set_setting('tb.account_id', customer)
		kodi_utils.notification('%s %s' % (ls(32576), 'TorBox'))
		return True

	def revoke_auth(self):
		if not kodi_utils.confirm_dialog(): return
		set_setting('tb.token', '')
		set_setting('tb.account_id', '')
		kodi_utils.notification('%s %s' % (ls(32576), ls(32059)))

	def clear_cache(self):
		try:
			if not kodi_utils.path_exists(kodi_utils.maincache_db): return True
			from caches.debrid_cache import DebridCache
			dbcon = kodi_utils.database.connect(kodi_utils.maincache_db)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('pov_tb_user_cloud',))
				kodi_utils.clear_property('pov_tb_user_cloud')
				dbcon.commit()
				user_cloud_success = True
			except: user_cloud_success = False
			# HASH CACHED STATUS
			try:
				DebridCache().clear_debrid_results('tb')
				hash_cache_status_success = True
			except: hash_cache_status_success = False
		except: return False
		if False in (user_cloud_success, hash_cache_status_success): return False
		return True

