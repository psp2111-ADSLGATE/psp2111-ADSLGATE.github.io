import requests
from threading import Thread
from caches.main_cache import cache_object
from modules import kodi_utils
# logger = kodi_utils.logger

ls, get_setting, set_setting = kodi_utils.local_string, kodi_utils.get_setting, kodi_utils.set_setting
base_url = 'https://api.torbox.app/v1/api'
user_agent = 'POV for Kodi'
timeout = 28.0
session = requests.Session()
session.headers['User-Agent'] = user_agent
session.mount(base_url, requests.adapters.HTTPAdapter(max_retries=1))

class TorBoxAPI:
	download = '/torrents/requestdl'
	download_usenet = '/usenet/requestdl'
	download_webdl = '/webdl/requestdl'
	remove = '/torrents/controltorrent'
	remove_usenet = '/usenet/controlusenetdownload'
	remove_webdl = '/webdl/controlwebdownload'
	stats = '/user/me'
	history = '/torrents/mylist'
	history_usenet = '/usenet/mylist'
	history_webdl = '/webdl/mylist'
	explore = '/torrents/mylist?id=%s'
	explore_usenet = '/usenet/mylist?id=%s'
	explore_webdl = '/webdl/mylist?id=%s'
	cache = '/torrents/checkcached'
	cloud = '/torrents/createtorrent'
	cloud_usenet = '/usenet/createusenetdownload'

	def __init__(self):
		self.api_key = get_setting('tb.token')
		self.tb_sort = int(get_setting('tb.sort', '0'))

	def _request(self, method, path, params=None, json=None, data=None):
		if not self.api_key: return
		session.headers['Authorization'] = 'Bearer %s' % self.api_key
		url = '%s%s' % (base_url, path) if not path.startswith('http') else path
		try:
			response, result = None, None
			response = session.request(method, url, params=params, json=json, data=data, timeout=timeout)
			response.raise_for_status()
			result = response.json()
			if 'control' in path: result = result.get('success')
			elif result.get('success') and 'data' in result: result = result['data']
		except Exception as e: kodi_utils.logger('torbox error',
			f"{e}\n{url}\n{response.text}" if response else f"{e}\n{url}"
		)
		return result

	def _GET(self, url, params=None):
		return self._request('get', url, params=params)

	def _POST(self, url, params=None, json=None, data=None):
		return self._request('post', url, params=params, json=json, data=data)

	def add_headers_to_url(self, url):
		return url + '|' + kodi_utils.urlencode(self.headers())

	def headers(self):
		return {'User-Agent': user_agent}

	@property
	def days_remaining(self):
		import datetime
		try:
			account_info = self.account_info()
			date_string = account_info['premium_expires_at'][:10]
			expires = datetime.datetime.strptime(date_string, '%Y-%m-%d')
			days_remaining = (expires - datetime.datetime.today()).days
		except: days_remaining = None
		return days_remaining

	def account_info(self):
		return self._GET(self.stats)

	def torrent_info(self, request_id=''):
		url = self.explore % request_id
		return self._GET(url)

	def delete_torrent(self, request_id=''):
		data = {'torrent_id': request_id, 'operation': 'delete'}
		return self._POST(self.remove, json=data)

	def delete_usenet(self, request_id=''):
		data = {'usenet_id': request_id, 'operation': 'delete'}
		return self._POST(self.remove_usenet, json=data)

	def delete_webdl(self, request_id=''):
		data = {'webdl_id': request_id, 'operation': 'delete'}
		return self._POST(self.remove_webdl, json=data)

	def unrestrict_link(self, file_id):
		torrent_id, file_id = file_id.split(',')
		params = {'token': self.api_key, 'torrent_id': torrent_id, 'file_id': file_id}
		return self._GET(self.download, params=params)

	def unrestrict_usenet(self, file_id):
		usenet_id, file_id = file_id.split(',')
		params = {'token': self.api_key, 'usenet_id': usenet_id, 'file_id': file_id}
		return self._GET(self.download_usenet, params=params)

	def unrestrict_webdl(self, file_id):
		webdl_id, file_id = file_id.split(',')
		params = {'token': self.api_key, 'web_id': webdl_id, 'file_id': file_id}
		return self._GET(self.download_webdl, params=params)

	def check_cache_single(self, hash):
		return self._GET(self.cache, params={'hash': hash, 'format': 'list'})

	def check_cache(self, hashlist):
		data = {'hashes': hashlist}
		return self._POST(self.cache, params={'format': 'list'}, json=data)

	def add_nzb(self, nzb, name=''):
		data = {'link': nzb}
		if name: data['name'] = name
		return self._POST(self.cloud_usenet, data=data)

	def add_magnet(self, magnet):
		data = {'magnet': magnet, 'seed': 3, 'allow_zip': 'false'}
		return self._POST(self.cloud, data=data)

	def create_transfer(self, link, name=''):
		if link.startswith('magnet'): key, result = 'torrent_id', self.add_magnet(link)
		else: key, result = 'usenetdownload_id', self.add_nzb(link, name)
		if not result: return ''
		return result.get(key, '')

	def resolve_magnet(self, magnet_url, info_hash, store_to_cloud, title, season, episode):
		from modules.source_utils import supported_video_extensions, seas_ep_filter, extras_filter
		try:
			file_url, match = None, False
			extensions = supported_video_extensions()
			extras_filtering_list = tuple(i for i in extras_filter() if not i in title.lower())
			check = self.check_cache_single(info_hash)
			match = info_hash in [i['hash'] for i in check]
			if not match: return None
			torrent = self.add_magnet(magnet_url)
			if not torrent: return None
			torrent_id = torrent['torrent_id']
			torrent_files = self.torrent_info(torrent_id)
			selected_files = [
				{'link': '%d,%d' % (torrent_id, i['id']), 'filename': i['short_name'], 'size': i['size']}
				for i in torrent_files['files'] if i['short_name'].lower().endswith(tuple(extensions))
			]
			if not selected_files: return None
			if season:
				selected_files = [i for i in selected_files if seas_ep_filter(season, episode, i['filename'])]
			else:
				if self._m2ts_check(selected_files): raise Exception('_m2ts_check failed')
				selected_files = [i for i in selected_files if not any(x in i['filename'].lower() for x in extras_filtering_list)]
				selected_files.sort(key=lambda k: k['size'], reverse=True)
			if not selected_files: return None
			file_key = selected_files[0]['link']
			file_url = self.unrestrict_link(file_key)
			if not store_to_cloud: Thread(target=self.delete_torrent, args=(torrent_id,)).start()
			return file_url
		except Exception as e:
			kodi_utils.logger('main exception', str(e))
			if torrent_id: Thread(target=self.delete_torrent, args=(torrent_id,)).start()
			return None

	def display_magnet_pack(self, magnet_url, info_hash):
		from modules.source_utils import supported_video_extensions
		try:
			extensions = supported_video_extensions()
			torrent = self.add_magnet(magnet_url)
			if not torrent: return None
			torrent_id = torrent['torrent_id']
			torrent_files = self.torrent_info(torrent_id)
			torrent_files = [
				{'link': '%d,%d' % (torrent_id, item['id']), 'filename': item['short_name'], 'size': item['size']}
				for item in torrent_files['files'] if item['short_name'].lower().endswith(tuple(extensions))
			]
			self.delete_torrent(torrent_id)
			return torrent_files
		except Exception:
			if torrent_id: self.delete_torrent(torrent_id)
			return None

	def add_uncached_torrent(self, magnet_url, pack=False):
		kodi_utils.show_busy_dialog()
		result = self.create_transfer(magnet_url)
		kodi_utils.hide_busy_dialog()
		if result: kodi_utils.ok_dialog(heading=32733, text=ls(32732) % 'TorBox', top_space=True)
		else: return kodi_utils.ok_dialog(heading=32733, text=32574)
		return True

	def _m2ts_check(self, folder_items):
		for item in folder_items:
			if item['filename'].endswith('.m2ts'): return True
		return False

	def auth(self):
		api_key = kodi_utils.dialog.input('TorBox API Key:')
		if not api_key: return
		self.api_key = api_key
		result = self.account_info()
		customer = result['customer']
		set_setting('tb.token', api_key)
		set_setting('tb.account_id', customer)
		kodi_utils.notification('%s %s' % (ls(32576), 'TorBox'))
		return True

	def revoke_auth(self):
		if not kodi_utils.confirm_dialog(): return
		self.api_key = ''
		set_setting('tb.token', '')
		set_setting('tb.account_id', '')
		kodi_utils.notification('%s %s' % (ls(32576), ls(32059)))

	def usenet_query(self, query, season='', episode='', imdb=''):
		if imdb: query = 'imdb:%s' % imdb
		else: query = 'search/%s' % requests.utils.quote(query)
		url = 'https://search-api.torbox.app/usenet/%s' % query
		params = {'check_cache': 'true', 'check_owned': 'true', 'search_user_engines': 'true'}
		if season and episode: params.update({'season': int(season), 'episode': int(episode)})
		result = self._GET(url, params=params)
		try: result = result['nzbs']
		except: result = []
		if   self.tb_sort == 1: result.sort(key=lambda k: int(k['size']), reverse=True)
		elif self.tb_sort == 2: result.sort(key=lambda k: k['tracker'], reverse=False)
		else: result.sort(key=lambda k: int(k['age'].rstrip('d')), reverse=False)
		return result

	def user_cloud(self, request_id=None, check_cache=True):
		string = 'pov_tb_user_cloud_info_%s' % request_id if request_id else 'pov_tb_user_cloud'
		url = self.explore % request_id if request_id else self.history
		if check_cache: result = cache_object(self._GET, string, url, False, 0.5)
		else: result = self._GET(url)
		return result

	def user_cloud_usenet(self, request_id=None, check_cache=True):
		string = 'pov_tb_user_cloud_usenet_info_%s' % request_id if request_id else 'pov_tb_user_cloud_usenet'
		url = self.explore_usenet % request_id if request_id else self.history_usenet
		if check_cache: result = cache_object(self._GET, string, url, False, 0.5)
		else: result = self._GET(url)
		return result

	def user_cloud_webdl(self, request_id=None, check_cache=True):
		string = 'pov_tb_user_cloud_webdl_info_%s' % request_id if request_id else 'pov_tb_user_cloud_webdl'
		url = self.explore_webdl % request_id if request_id else self.history_webdl
		if check_cache: result = cache_object(self._GET, string, url, False, 0.5)
		else: result = self._GET(url)
		return result

	def user_cloud_clear(self):
		if not kodi_utils.confirm_dialog(): return
		data = {'all': True, 'operation': 'delete'}
		self._POST(self.remove, json=data)
		self._POST(self.remove_usenet, json=data)
		self.clear_cache()

	def clear_cache(self):
		try:
			if not kodi_utils.path_exists(kodi_utils.maincache_db): return True
			from caches.debrid_cache import DebridCache
			user_cloud_success = False
			dbcon = kodi_utils.database.connect(kodi_utils.maincache_db)
			dbcur = dbcon.cursor()
			try:
				dbcur.execute("""DELETE FROM maincache WHERE id = ?""", ('torbox_usenet_queries',))
				kodi_utils.clear_property(str(i))
			except: pass
			# USER CLOUD
			try:
				dbcur.execute("""SELECT id FROM maincache WHERE id LIKE ?""", ('pov_tb_user_cloud%',))
				try:
					user_cloud_cache = dbcur.fetchall()
					user_cloud_cache = [i[0] for i in user_cloud_cache]
				except:
					user_cloud_success = True
				if not user_cloud_success:
					for i in user_cloud_cache:
						dbcur.execute("""DELETE FROM maincache WHERE id = ?""", (i,))
						kodi_utils.clear_property(str(i))
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

