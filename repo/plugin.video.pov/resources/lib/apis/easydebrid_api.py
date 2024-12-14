import requests
from modules import kodi_utils
# logger = kodi_utils.logger

ls, get_setting, set_setting = kodi_utils.local_string, kodi_utils.get_setting, kodi_utils.set_setting
base_url = 'https://easydebrid.com/api/v1'
timeout = 10.0
session = requests.Session()
session.mount(base_url, requests.adapters.HTTPAdapter(max_retries=1))

class EasyDebridAPI:
	download = '/link/generate'
	stats = '/user/details'
	cache = '/link/lookup'

	def __init__(self):
		self.api_key = get_setting('ed.token')

	def _request(self, method, path, params=None, json=None, data=None):
		if not self.api_key: return
		session.headers['Authorization'] = 'Bearer %s' % self.api_key
		full_path = '%s%s' % (base_url, path)
		response = session.request(method, full_path, params=params, json=json, data=data, timeout=timeout)
		try: response.raise_for_status()
		except Exception as e: kodi_utils.logger('easydebrid error', f"{e}\n{response.text}")
		try: result = response.json()
		except: result = {}
		return result

	def _GET(self, url, params=None):
		return self._request('get', url, params=params)

	def _POST(self, url, params=None, json=None, data=None):
		return self._request('post', url, params=params, json=json, data=data)

	def account_info(self):
		return self._GET(self.stats)

	def check_cache_single(self, hash):
		return self._POST(self.cache, json={'urls': [hash]})

	def check_cache(self, hashlist):
		data = {'urls': hashlist}
		return self._POST(self.cache, json=data)

	def add_magnet(self, magnet):
		data = {'url': magnet}
		return self._POST(self.download, json=data)

	def create_transfer(self, magnet_url):
		result = self.add_magnet(magnet_url)
		if not 'files' in result: return ''
		return result.get('files', '')

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, extras_filter
		try:
			file_url, match = None, False
			extensions = supported_video_extensions()
			extras_filtering_list = tuple(i for i in extras_filter() if not i in title.lower())
			check = self.check_cache_single(info_hash)
			match = 'cached' in check and check['cached'][0]
			if not match: return None
			torrent = self.add_magnet(magnet_url)
			torrent_files = torrent['files']
			selected_files = [i for i in torrent_files if i['filename'].lower().endswith(tuple(extensions))]
			if not selected_files: return None
			if season:
				selected_files = [i for i in selected_files if seas_ep_filter(season, episode, i['filename'])]
			else:
				if self._m2ts_check(selected_files): raise Exception('_m2ts_check failed')
				selected_files = [i for i in selected_files if not any(x in i['filename'] for x in extras_filtering_list)]
				selected_files.sort(key=lambda k: k['size'], reverse=True)
			if not selected_files: return None
			file_url = selected_files[0]['url']
			return file_url
		except Exception as e:
			kodi_utils.logger('main exception', str(e))
			return None

	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			extensions = supported_video_extensions()
			torrent = self.create_transfer(magnet_url)
			if not torrent: return None
			torrent_files = [
				{'link': item['url'], 'filename': item['filename'], 'size': item['size']}
				for item in torrent if item['filename'].lower().endswith(tuple(extensions))
			]
			return torrent_files
		except Exception:
			return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		return kodi_utils.ok_dialog(heading=32733, text=32574)

	def _m2ts_check(self, folder_items):
		for item in folder_items:
			if item['filename'].endswith('.m2ts'): return True
		return False

	def auth(self):
		api_key = kodi_utils.dialog.input('EasyDebrid API Key:')
		if not api_key: return
		self.api_key = api_key
		r = self.account_info()
		customer = r['id']
		set_setting('ed.token', api_key)
		set_setting('ed.account_id', customer)
		kodi_utils.notification('%s %s' % (ls(32576), 'EasyDebrid'))
		return True

	def revoke_auth(self):
		if not kodi_utils.confirm_dialog(): return
		self.api_key = ''
		set_setting('ed.token', '')
		set_setting('ed.account_id', '')
		kodi_utils.notification('%s %s' % (ls(32576), ls(32059)))

	def clear_cache(self):
		try:
			if not kodi_utils.path_exists(kodi_utils.maincache_db): return True
			from caches.debrid_cache import DebridCache
			dbcon = kodi_utils.database.connect(kodi_utils.maincache_db)
			dbcur = dbcon.cursor()
			# USER CLOUD
			try:
#				dbcur.execute("""DELETE FROM maincache WHERE id=?""", ('pov_ed_user_cloud',))
				kodi_utils.clear_property('pov_ed_user_cloud')
#				dbcon.commit()
				user_cloud_success = True
			except: user_cloud_success = False
			# HASH CACHED STATUS
			try:
				DebridCache().clear_debrid_results('ed')
				hash_cache_status_success = True
			except: hash_cache_status_success = False
		except: return False
		if False in (user_cloud_success, hash_cache_status_success): return False
		return True

