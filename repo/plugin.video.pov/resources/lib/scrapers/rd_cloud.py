from threading import Thread
from apis.real_debrid_api import RealDebridAPI
from modules import source_utils
from modules.utils import clean_file_name, normalize
from modules.settings import enabled_debrids_check, filter_by_name
# from modules.kodi_utils import logger

RealDebrid = RealDebridAPI()
extensions = source_utils.supported_video_extensions()
internal_results, check_title, clean_title = source_utils.internal_results, source_utils.check_title, source_utils.clean_title
get_file_info, release_info_format, seas_ep_filter = source_utils.get_file_info, source_utils.release_info_format, source_utils.seas_ep_filter

class source:
	def __init__(self):
		self.scrape_provider = 'rd_cloud'
		self.sources = []

	def results(self, info):
		try:
			if not enabled_debrids_check('rd'): return internal_results(self.scrape_provider, self.sources)
			self.folder_results, self.scrape_results = [], []
			title_filter = filter_by_name(self.scrape_provider)
			self.media_type, title, self.tmdb_id = info.get('media_type'), info.get('title'), info.get('tmdb_id')
			self.year, self.season, self.episode = int(info.get('year')), info.get('season'), info.get('episode')
			if self.media_type == 'episode': self.seas_ep_query_list = source_utils.seas_ep_query_list(self.season, self.episode)
			self.folder_query = clean_title(normalize(title))
			self._scrape_downloads()
			self._scrape_cloud()
			if not self.scrape_results: return internal_results(self.scrape_provider, self.sources)
			aliases = source_utils.get_aliases_titles(info.get('aliases', []))
			def _process():
				for item in self.scrape_results:
					try:
						file_name = self._get_filename(item['path'])
						if title_filter and not check_title(title, file_name, aliases, self.year, self.season, self.episode): continue
						file_dl, size = item['url_link'], round(float(item['bytes'])/1073741824, 2)
						direct_debrid_link, URLName = item.get('direct_debrid_link', False), clean_file_name(file_name).replace('html', ' ').replace('+', ' ').replace('-', ' ')
						video_quality, details = get_file_info(name_info=release_info_format(file_name))
						source_item = {'name': file_name, 'title': file_name, 'URLName': URLName, 'quality': video_quality, 'size': size, 'size_label': '%.2f GB' % size,
									'extraInfo': details, 'url_dl': file_dl, 'id': file_dl, 'downloads': False, 'direct': True, 'source': self.scrape_provider,
									'scrape_provider': self.scrape_provider, 'direct_debrid_link': direct_debrid_link}
						yield source_item
					except: pass
			self.sources = list(_process())
		except Exception as e:
			from modules.kodi_utils import logger
			logger('POV real-debrid scraper Exception', e)
		internal_results(self.scrape_provider, self.sources)
		return self.sources

	def _scrape_cloud(self):
		try:
			try: my_cloud_files = [i for i in RealDebrid.user_cloud() if i.get('ended')]
			except: return self.sources
			folder_results_append = self.folder_results.append
			for item in my_cloud_files:
				normalized = normalize(item['filename'])
				folder_name = clean_title(normalized)
				if self.folder_query in folder_name or not folder_name:
					folder_results_append((normalized, item['id']))
			if not self.folder_results: return self.sources
			threads = []
			threads_append = threads.append
			for i in self.folder_results: threads_append(Thread(target=self._scrape_folders, args=(i,)))
			[i.start() for i in threads]
			[i.join() for i in threads]
		except: pass

	def _scrape_folders(self, folder_info):
		try:
			folder_files = RealDebrid.user_cloud_info(folder_info[1])
			contents = [i for i in folder_files['files'] if i['path'].lower().endswith(tuple(extensions))]
			file_urls = folder_files['links']
			scrape_results_append = self.scrape_results.append
			for c, i in enumerate(contents):
				try: i.update({'folder_name': folder_info[0], 'url_link': file_urls[c]})
				except: pass
			contents.sort(key=lambda k: k['path'])
			for item in contents:
				match = False
				normalized = normalize(item['path'])
				filename = clean_title(normalized)
				if self.media_type == 'movie':
					if any(x in filename for x in self._year_query_list()) and self.folder_query in filename: match = True
				elif seas_ep_filter(self.season, self.episode, normalized): match = True
				if match: scrape_results_append(item)
		except: pass

	def _scrape_downloads(self):
		try:
			my_downloads = RealDebrid.downloads()
			my_downloads = [i for i in my_downloads if i['download'].lower().endswith(tuple(extensions))]
			scrape_results_append = self.scrape_results.append
			for item in my_downloads:
				match = False
				normalized = normalize(item['filename'])
				filename = clean_title(normalized)
				if self.media_type == 'movie':
					if any(x in filename for x in self._year_query_list()): match = True
				elif seas_ep_filter(self.season, self.episode, normalized): match = True
				if match and self.folder_query in filename:
					item = self.make_downloads_item(item)
					if item['path'] not in [d['path'] for d in self.scrape_results]: scrape_results_append(item)
		except: pass

	def make_downloads_item(self, item):
		return {'folder_name': item['filename'], 'url_link': item['download'], 'bytes': item['filesize'], 'path': item['filename'], 'direct_debrid_link': True}

	def _get_filename(self, name):
		if name.startswith('/'): name = name.split('/')[-1]
		return clean_file_name(normalize(name))

	def _year_query_list(self):
		return (str(self.year), str(self.year+1), str(self.year-1))

