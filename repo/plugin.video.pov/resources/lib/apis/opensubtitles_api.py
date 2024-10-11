import requests
from datetime import timedelta
from io import BytesIO
from urllib.parse import quote
from zipfile import ZipFile
from caches.main_cache import main_cache
from modules.kodi_utils import notification, sleep, delete_file, rename_file
# from modules.kodi_utils import logger

base_url = 'https://rest.opensubtitles.org/search'
user_agent = {'User-Agent': 'TemporaryUserAgent'}
timeout = 3.05

class OpenSubtitlesAPI:
	def search(self, query, imdb_id, language, season=None, episode=None):
		cache_name = 'opensubtitles_%s_%s' % (imdb_id, language)
		if season: cache_name += '_%s_%s' % (season, episode)
		cache = main_cache.get(cache_name)
		if cache: return cache
		url = '/imdbid-%s/query-%s' % (imdb_id, quote(query))
		if season: url += '/season-%d/episode-%d' % (season, episode)
		url += '/sublanguageid-%s' % language
		url = base_url + url
		response = self._get(url, retry=True)
		response = response.json()
		main_cache.set(cache_name, response, expiration=timedelta(hours=24))
		return response

	def download(self, url, filepath, temp_zip, temp_path, final_path):
		result = self._get(url, stream=True, retry=True)
		f = BytesIO(b''.join(result.iter_content(1024*1024)))
		with ZipFile(f, 'r') as zip_file: zip_file.extractall(filepath, [i for i in zip_file.namelist() if not i.endswith('nfo')])
		f.close()
		rename_file(temp_path, final_path)
		return final_path

	def _get(self, url, stream=False, retry=False):
		response = requests.get(url, headers=user_agent, stream=stream, timeout=timeout)
		if response.ok: return response
		elif retry and response.status_code == 429:
			notification(32740, 3000)
			sleep(10000)
			return self._get(url, stream)
		else: return

