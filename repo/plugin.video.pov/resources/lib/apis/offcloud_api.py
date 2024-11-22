import re
import requests
from sys import exit as sysexit
from threading import Thread
from caches.main_cache import cache_object
from modules import kodi_utils
# logger = kodi_utils.logger

ls, get_setting, set_setting = kodi_utils.local_string, kodi_utils.get_setting, kodi_utils.set_setting
base_url = 'https://offcloud.com/api'
timeout = 3.05
session = requests.Session()
session.mount(base_url, requests.adapters.HTTPAdapter(max_retries=1))

NOT_AVAILABLE = {
	'premium': 'User must purchase a premium downloading addon for this download',
	'links': 'User must purchase a Link increase addon for this download',
	'proxy': 'User must purchase a proxy downloading addon for this download',
	'video': 'User must purchase a video sharing site support addon for this download'
}

class OffcloudAPI:
	download = 'https://%s.offcloud.com/cloud/download/%s/%s'
	zip = 'https://%s.offcloud.com/cloud/zip/%s/%s.zip'
	remove = 'https://offcloud.com/cloud/remove/%s' # undocumented
	stats = '/account/stats' # undocumented
	history = '/cloud/history' # undocumented
	explore = '/cloud/explore/%s'
	files = '/cloud/list/%s'
	status = '/cloud/status'
	cache = '/cache'
	cloud = '/cloud'

	def __init__(self):
		self.api_key = get_setting('oc.token')

	def _request(self, method, path, params=None, data=None):
		if not self.api_key: pass
		elif not params: params = {'key': self.api_key}
		else: params['key'] = self.api_key
		full_path = '%s%s' % (base_url, path)
		r = session.request(method, full_path, params=params, json=data, timeout=timeout)
		try: r.raise_for_status()
		except Exception as e: kodi_utils.logger('offcloud error', str(e))
		try: r = r.json()
		except: r = {}
		if 'not_available' in r:
			reason = NOT_AVAILABLE.get(r.get('not_available'))
			kodi_utils.notification(reason)
		elif 'error' in r:
			reason = '\n%s\n%s' % (r.get('error'), full_path)
			kodi_utils.logger('offcloud error', reason)
		return r

	def _GET(self, url):
		return self._request('get', url)

	def _POST(self, url, data=None):
		return self._request('post', url, data=data)

	@staticmethod
	def requote_uri(url):
		return requests.utils.requote_uri(url)

	def build_url(self, server, request_id, file_name):
		return self.download % (server, request_id, file_name)

	def build_zip(self, server, request_id, file_name):
		return self.zip % (server, request_id, file_name)

	def requestid_from_url(self, url):
		match = re.search(r'download/[A-Za-z0-9]+/', url)
		if not match: return None
		request_id = match.group(0).split('/')[-2]
		return request_id

	def account_info(self):
		return self._GET(self.stats)

	def user_cloud(self):
		string = 'pov_oc_user_cloud'
		url = self.history
		return cache_object(self._GET, string, url, False, 0.5)

	def user_cloud_info(self, request_id=''):
		string = 'pov_oc_user_cloud_%s' % request_id
		url = self.explore % request_id
		return cache_object(self._GET, string, url, False, 0.5)

	def torrent_info(self, request_id=''):
		url = self.explore % request_id
		return self._GET(url)

	def torrent_status(self, request_id=''):
		data = {'requestId': request_id}
		return self._POST(self.status, data=data)

	def delete_torrent(self, request_id=''):
		params = {'key': self.api_key}
		url = self.remove % request_id
		r = session.get(url, params=params, timeout=timeout)
		try: r = r.json()
		except: r = {}
		return r

	def add_magnet(self, magnet):
		data = {'url': magnet}
		return self._POST(self.cloud, data=data)

	def check_cache(self, hashlist):
		data = {'hashes': hashlist}
		return self._POST(self.cache, data=data)

	def create_transfer(self, magnet_url):
		result = self.add_magnet(magnet_url)
		if result.get('status') not in ('created', 'downloaded'): return 'failed'
		return result

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, extras_filter
		try:
			file_url, match = None, False
			extensions = supported_video_extensions()
			extras_filtering_list = extras_filter()
			match = info_hash in self.check_cache([info_hash]).get('cachedItems', [])
			if not match: return None
			torrent = self.add_magnet(magnet_url)
			if not torrent['status'] == 'downloaded': return None
			single_file_torrent = '%s/%s' % (torrent['url'], torrent['fileName'])
			torrent_id = torrent['requestId']
			torrent_files = self.torrent_info(torrent_id)
			if not isinstance(torrent_files, list): torrent_files = [single_file_torrent]
			valid_results = [item for item in torrent_files if item.lower().endswith(tuple(extensions))]
			if not valid_results: return None
			if season:
				correct_files = [i for i in valid_results if seas_ep_filter(season, episode, i.split('/')[-1])]
				if len(correct_files) == 1: file_url = correct_files[0]
				else: file_url = [i for i in correct_files if not any(x in i for x in extras_filtering_list)][0]
			else:
				if self._m2ts_check(valid_results): self.delete_torrent(torrent_id) ; return None
				if len(valid_results) == 1: file_url = valid_results[0]
				else: file_url = [i for i in valid_results if not any(x in i for x in extras_filtering_list)][0]
			return self.requote_uri(file_url) # requote, oc why give us a list of urls that may have spaces in name
		except Exception as e:
			kodi_utils.logger('main exception', str(e))
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			extensions = supported_video_extensions()
			torrent = self.add_magnet(magnet_url)
			if not torrent['status'] == 'downloaded': return None
			torrent_id = torrent['requestId']
			torrent_files = self.torrent_info(torrent_id)
			end_results = []
			append = end_results.append
			for item in torrent_files:
				if item.lower().endswith(tuple(extensions)):
					append({'link': self.requote_uri(item), 'filename': item.split('/')[-1], 'size': 0})
			#self.delete_torrent(torrent_id) # cannot delete the torrent, play link will not persist, will return 502
			return end_results
		except Exception:
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		kodi_utils.show_busy_dialog()
		result = self.create_transfer(magnet_url)
		kodi_utils.hide_busy_dialog()
		if result == 'failed': kodi_utils.ok_dialog(heading=32733, text=32574)
		else: kodi_utils.ok_dialog(heading=32733, text=ls(32732) % 'Offcloud', top_space=True)
		if result == 'downloaded': return True
		return False

	def _m2ts_check(self, folder_items):
		for item in folder_items:
			if item.endswith('.m2ts'): return True
		return False

	def user_cloud_clear(self):
		if not kodi_utils.confirm_dialog(): return
		files = self.user_cloud()
		if not files: return
		threads = []
		append = threads.append
		len_files = len(files)
		progressBG = kodi_utils.progressDialogBG
		progressBG.create('Offcloud', 'Clearing cloud files')
		for count, req in enumerate(files, 1):
			try:
				i = Thread(target=self.delete_torrent, args=(req['requestId'],))
				append(i)
				i.start()
				progressBG.update(int(count / len_files * 100), 'Deleting %s...' % req['fileName'])
				kodi_utils.sleep(200)
			except: pass
		[i.join() for i in threads]
		try: progressBG.close()
		except: pass
		self.clear_cache()

	def auth(self):
		username = kodi_utils.dialog.input('Offcloud Email:')
		password = kodi_utils.dialog.input('Offcloud Password:', option=2)
		if not all((username, password)): return
		data = {'username': username, 'password': password}
		r = self._POST('/login', data=data)
		user_id = r.get('userId')
		if not user_id: kodi_utils.notification(32574) ; return False
		r = self._POST('/key')
		api_key = r.get('apiKey')
		if not api_key: kodi_utils.notification(32574) ; return False
		self.api_key = api_key
		set_setting('oc.token', api_key)
		set_setting('oc.account_id', user_id)
		kodi_utils.notification('%s %s' % (ls(32576), 'Offcloud'))
		return True

	def revoke_auth(self):
		if not kodi_utils.confirm_dialog(): return
		self.api_key = ''
		set_setting('oc.token', '')
		set_setting('oc.account_id', '')
		kodi_utils.notification('%s %s' % (ls(32576), ls(32059)))

	def clear_cache(self):
		try:
			if not kodi_utils.path_exists(kodi_utils.maincache_db): return True
			from caches.debrid_cache import DebridCache
			dbcon = kodi_utils.database.connect(kodi_utils.maincache_db)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('pov_oc_user_cloud',))
				kodi_utils.clear_property('pov_oc_user_cloud')
				dbcon.commit()
				user_cloud_success = True
			except: user_cloud_success = False
			# HASH CACHED STATUS
			try:
				DebridCache().clear_debrid_results('oc')
				hash_cache_status_success = True
			except: hash_cache_status_success = False
		except: return False
		if False in (user_cloud_success, hash_cache_status_success): return False
		return True

