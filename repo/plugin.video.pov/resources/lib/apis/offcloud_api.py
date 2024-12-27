import re
import requests
from threading import Thread
from caches.main_cache import cache_object
from modules import kodi_utils
# logger = kodi_utils.logger

ls, get_setting, set_setting = kodi_utils.local_string, kodi_utils.get_setting, kodi_utils.set_setting
base_url = 'https://offcloud.com/api'
timeout = 10.0
session = requests.Session()
session.mount(base_url, requests.adapters.HTTPAdapter(max_retries=1))

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
		try:
			response, result = None, None
			response = session.request(method, full_path, params=params, json=data, timeout=timeout)
			response.raise_for_status()
			result = response.json()
		except Exception as e: kodi_utils.logger('offcloud error',
			f"{e}\n{full_path}\n{response.text}" if response else f"{e}\n{full_path}"
		)
		return result

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

	def torrent_info(self, request_id=''):
		url = self.explore % request_id
		return self._GET(url)

	def delete_torrent(self, request_id=''):
		params = {'key': self.api_key}
		url = self.remove % request_id
		r = session.get(url, params=params, timeout=timeout)
		try: r = r.json()
		except: r = {}
		return r

	def check_cache(self, hashlist):
		data = {'hashes': hashlist}
		return self._POST(self.cache, data=data)

	def add_magnet(self, magnet):
		data = {'url': magnet}
		return self._POST(self.cloud, data=data)

	def create_transfer(self, magnet_url):
		result = self.add_magnet(magnet_url)
		if not result['status'] in ('created', 'downloaded'): return ''
		return result.get('requestId', '')

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, extras_filter
		try:
			file_url, match = None, False
			extensions = supported_video_extensions()
			extras_filtering_list = tuple(i for i in extras_filter() if not i in title.lower())
			match = info_hash in self.check_cache([info_hash]).get('cachedItems', [])
			if not match: return None
			torrent = self.add_magnet(magnet_url)
			if not torrent['status'] == 'downloaded': return None
			single_file_torrent = '%s/%s' % (torrent['url'], torrent['fileName'])
			torrent_id = torrent['requestId']
			torrent_files = self.torrent_info(torrent_id)
			if not isinstance(torrent_files, list): torrent_files = [single_file_torrent]
			selected_files = [
				{'link': i, 'filename': i.split('/')[-1], 'size': 0}
				for i in torrent_files if i.lower().endswith(tuple(extensions))
			]
			if not selected_files: return None
			if season:
				selected_files = [i for i in selected_files if seas_ep_filter(season, episode, i['filename'])]
			else:
				if self._m2ts_check(selected_files): raise Exception('_m2ts_check failed')
				selected_files = [i for i in selected_files if not any(x in i['filename'] for x in extras_filtering_list)]
			if not selected_files: return None
			file_key = selected_files[0]['link']
			file_url = self.requote_uri(file_key) # requote, oc why give us a list of urls that may have spaces in name
			return file_url
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
			torrent_files = [
				{'link': self.requote_uri(item), 'filename': item.split('/')[-1], 'size': 0}
				for item in torrent_files if item.lower().endswith(tuple(extensions))
			]
#			self.delete_torrent(torrent_id) # cannot delete the torrent, play link will not persist, will return 502
			return torrent_files
		except Exception:
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		kodi_utils.show_busy_dialog()
		result = self.create_transfer(magnet_url)
		kodi_utils.hide_busy_dialog()
		if result: kodi_utils.ok_dialog(heading=32733, text=ls(32732) % 'Offcloud', top_space=True)
		else: return kodi_utils.ok_dialog(heading=32733, text=32574)
		return True

	def _m2ts_check(self, folder_items):
		for item in folder_items:
			if item['filename'].endswith('.m2ts'): return True
		return False

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

	def user_cloud(self, request_id=None, check_cache=True):
		string = 'pov_oc_user_cloud_info_%s' % request_id if request_id else 'pov_oc_user_cloud'
		url = self.explore % request_id if request_id else self.history
		if check_cache: result = cache_object(self._GET, string, url, False, 0.5)
		else: result = self._GET(url)
		return result

	def user_cloud_clear(self):
		if not kodi_utils.confirm_dialog(): return
		files = self.user_cloud(check_cache=False)
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

	def clear_cache(self):
		try:
			if not kodi_utils.path_exists(kodi_utils.maincache_db): return True
			from caches.debrid_cache import DebridCache
			user_cloud_success = False
			dbcon = kodi_utils.database.connect(kodi_utils.maincache_db)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
				dbcur.execute("""SELECT data FROM maincache WHERE id=?""", ('pov_oc_user_cloud',))
				try:
					user_cloud_cache = eval(dbcur.fetchone()[0])
					user_cloud_info_caches = [i['requestId'] for i in user_cloud_cache]
				except: user_cloud_success = True
				if not user_cloud_success:
					dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('pov_oc_user_cloud',))
					kodi_utils.clear_property('pov_oc_user_cloud')
					for i in user_cloud_info_caches:
						dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('pov_oc_user_cloud_info_%s' % i,))
						kodi_utils.clear_property("pov_oc_user_cloud_info_%s" % i)
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

