from threading import Thread
from apis.torbox_api import TorBoxAPI
from modules import source_utils
from modules.utils import clean_file_name, normalize
from modules.settings import enabled_debrids_check, filter_by_name
# from modules.kodi_utils import logger

internal_results, check_title, clean_title = source_utils.internal_results, source_utils.check_title, source_utils.clean_title
get_file_info, release_info_format, seas_ep_filter = source_utils.get_file_info, source_utils.release_info_format, source_utils.seas_ep_filter
extensions = source_utils.supported_video_extensions()
TorBox = TorBoxAPI()

class source:
	def __init__(self):
		self.scrape_provider = 'tb_cloud'
		self.sources = []

	def results(self, info):
		try:
			if not enabled_debrids_check('tb'): return internal_results(self.scrape_provider, self.sources)
			self.scrape_results = []
			title_filter = filter_by_name(self.scrape_provider)
			self.media_type, title = info.get('media_type'), info.get('title')
			self.year, self.season, self.episode = int(info.get('year')), info.get('season'), info.get('episode')
			if self.media_type == 'episode': self.seas_ep_query_list = source_utils.seas_ep_query_list(self.season, self.episode)
			self.folder_query, self.year_query_list = clean_title(normalize(title)), tuple(map(str, range(self.year - 1, self.year + 2)))
			self._scrape_cloud()
			if not self.scrape_results: return internal_results(self.scrape_provider, self.sources)
			self.aliases = source_utils.get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = item['filename']
						if title_filter and not check_title(title, file_name, self.aliases, self.year, self.season, self.episode): continue
						file_dl, size = item['url'], round(float(int(item['size']))/1073741824, 2)
						URLName = clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						video_quality, details = get_file_info(name_info=release_info_format(file_name))
						source_item = {'name': file_name, 'title': file_name, 'URLName': URLName, 'quality': video_quality, 'size': size, 'size_label': '%.2f GB' % size,
									'extraInfo': details, 'url_dl': file_dl, 'id': file_dl, 'downloads': False, 'direct': True, 'source': self.scrape_provider,
									'scrape_provider': self.scrape_provider}
						yield source_item
					except: pass
			self.sources = list(_process())
		except Exception as e:
			from modules.kodi_utils import logger
			logger('POV torbox scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _scrape_cloud(self):
		try:
			results_append = self.scrape_results.append
			try: my_cloud_files = TorBox.user_cloud()
			except: return self.sources
			for item in my_cloud_files['data']:
				if not item['download_finished']: continue
				for file in item['files']:
					if not file['short_name'].endswith(tuple(extensions)): continue
					match = False
					normalized = normalize(file['short_name'])
					filename = clean_title(normalized)
					if self.media_type == 'movie':
						if any(x in filename for x in self.year_query_list) and self.folder_query in filename: match = True
					elif seas_ep_filter(self.season, self.episode, normalized): match = True
					if match: results_append({'filename': normalized, 'url': '%d,%d' % (item['id'], file['id']), 'size': file['size']})
		except: return

