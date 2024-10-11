from threading import Thread
from apis.alldebrid_api import AllDebridAPI
from modules import source_utils
from modules.utils import clean_file_name, normalize
from modules.settings import enabled_debrids_check, filter_by_name
# from modules.kodi_utils import logger

AllDebrid = AllDebridAPI()
extensions = source_utils.supported_video_extensions()
internal_results, check_title, clean_title = source_utils.internal_results, source_utils.check_title, source_utils.clean_title
get_file_info, release_info_format, seas_ep_filter = source_utils.get_file_info, source_utils.release_info_format, source_utils.seas_ep_filter

class source:
	def __init__(self):
		self.scrape_provider = 'ad_cloud'
		self.sources = []

	def results(self, info):
		try:
			if not enabled_debrids_check('ad'): return internal_results(self.scrape_provider, self.sources)
			self.folder_results, self.scrape_results = [], []
			title_filter = filter_by_name(self.scrape_provider)
			self.media_type, title = info.get('media_type'), info.get('title')
			self.year, self.season, self.episode = int(info.get('year')), info.get('season'), info.get('episode')
			if self.media_type == 'episode': self.seas_ep_query_list = source_utils.seas_ep_query_list(self.season, self.episode)
			self.folder_query = clean_title(normalize(title))
			self._scrape_cloud()
			if not self.scrape_results: return internal_results(self.scrape_provider, self.sources)
			self.aliases = source_utils.get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = normalize(item['filename'])
						if title_filter and not check_title(title, file_name, self.aliases, self.year, self.season, self.episode): continue
						file_dl, size = item['link'], round(float(int(item['size']))/1073741824, 2)
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
			logger('POV alldebrid scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _scrape_cloud(self):
		try:
			threads = []
			results_append = self.folder_results.append
			append = threads.append
			try: my_cloud_files = AllDebrid.user_cloud()['magnets']
			except: return self.sources
			my_cloud_files = [i for i in my_cloud_files if i['statusCode'] == 4]
			for item in my_cloud_files:
				normalized = normalize(item['filename'])
				folder_name = clean_title(normalized)
				if self.folder_query in folder_name or not folder_name: results_append((normalized, item))
			if not self.folder_results: return self.sources
			for i in self.folder_results: append(Thread(target=self._scrape_folders, args=(i,)))
			[i.start() for i in threads]
			[i.join() for i in threads]
		except: pass

	def _scrape_folders(self, folder_info):
		try:
			torrent_folder = folder_info[1]
			links = torrent_folder['links']
			append = self.scrape_results.append
			links = [i for i in links if i['filename'].lower().endswith(tuple(extensions))]
			for item in links:
				match = False
				normalized = normalize(item['filename'])
				filename = clean_title(normalized)
				if self.media_type == 'movie':
					if any(x in filename for x in self._year_query_list()) and self.folder_query in filename: match = True
				elif seas_ep_filter(self.season, self.episode, normalized): match = True
				if match: append(item)
		except: return

	def _year_query_list(self):
		return (str(self.year), str(self.year+1), str(self.year-1))

