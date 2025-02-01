# created by kodifitzwell for Fenomscrapers
"""
	Fenomscrapers Project
"""

import base64
import re, requests
from urllib.parse import quote_plus, urlparse, parse_qsl
from fenom import client
from fenom import source_utils

session = requests.Session()
session.headers = {'User-Agent': client.randomagent()}


class source:
	priority = 5
	pack_capable = True
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.base_link = "https://animetosho.org"
		self.search_link = '/search?q=%s'
		self.min_seeders = 0

	def sources(self, data, hostDict):
		self.sources = []
		if not data: return self.sources
		self.sources_append = self.sources.append
		try:
			self.title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			self.title = self.title.replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')
			self.aliases = data['aliases']
			self.episode_title = data['title'] if 'tvshowtitle' in data else None
			self.year = data['year']
			self.hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else self.year
			self.hdlr2 = 'S%d - %d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else self.year
			self.undesirables = source_utils.get_undesirables()
			self.check_foreign_audio = source_utils.check_foreign_audio()

			query = '%s %s' % (self.title, self.hdlr)
#			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query)
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)
			query2 = '%s %s' % (self.title, self.hdlr2)
#			query2 = re.sub(r'[^A-Za-z0-9\s\.-]+', '', query2)
			query2 = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query2)

			urls = []
			url = self.search_link % quote_plus(query)
			url = '%s%s' % (self.base_link, url)
			urls.append(url)
			url2 = self.search_link % quote_plus(query2)
			url2 = '%s%s' % (self.base_link, url2)
			urls.append(url2)
			# log_utils.log('urls = %s' % urls)
			threads = []
			append = threads.append
			for url in urls:
				append(source_utils.Thread(self.get_sources, url))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('ANIMETOSHO')
			return self.sources

	def get_sources(self, url):
		try:
#			results = client.request(url, timeout=5)
			results = session.get(url, timeout=5).text
			if not results: return
			rows = client.parseDOM(results, 'div', attrs={'class': 'home_list_entry home_list_entry_alt home_list_entry_compl_1'})
		except:
			source_utils.scraper_error('ANIMETOSHO')
			return

		for row in rows:
			try:
				links = client.parseDOM(row, 'div', attrs={'class': 'links'})
				link = client.parseDOM(links, 'a', ret='href')
				magnet = next((i for i in link if 'magnet' in i), '').replace('&amp;', '&')
				magnet = urlparse(magnet).query
				magnet = dict(parse_qsl(magnet))

				hash = magnet.get('xt').split(':')[-1]
				hash = base64.b16encode(base64.b32decode(hash)).decode('utf-8')
				name = magnet.get('dn')
				# name = client.parseDOM(row, 'div', attrs={'class': 'link'})
				# name = client.parseDOM(name, 'a')[0]
				name = source_utils.clean_name(name)

				if not source_utils.check_title(self.title, self.aliases, name, self.hdlr, self.year): continue
				name_info = source_utils.info_from_name(name, self.title, self.year, self.hdlr, self.episode_title)
				if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
				if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

				if not self.episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					ep_strings = [r'[.-]s\d{2}e\d{2}([.-]?)', r'[.-]s\d{2}([.-]?)', r'[.-]season[.-]?\d{1,2}[.-]?']
					name_lower = name.lower()
					if any(re.search(item, name_lower) for item in ep_strings): continue

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
				try:
					seeders = client.parseDOM(links, 'span', ret='title')[0]
					seeders = int(seeders.split()[1])
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = client.parseDOM(row, 'div', attrs={'class': 'size'})[0]
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				self.sources_append({'provider': 'animetosho', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info,
													'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('ANIMETOSHO')

	def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		self.sources = []
		if not data: return self.sources
		self.sources_append = self.sources.append
		try:
			self.search_series = search_series
			self.total_seasons = total_seasons
			self.bypass_filter = bypass_filter

			self.title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')
			self.aliases = data['aliases']
			self.imdb = data['imdb']
			self.year = data['year']
			self.season_x = data['season']
			self.season_xx = self.season_x.zfill(2)
			self.undesirables = source_utils.get_undesirables()
			self.check_foreign_audio = source_utils.check_foreign_audio()

#			query = re.sub(r'[^A-Za-z0-9\s\.-]+', '', self.title)
			query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', self.title)
			if search_series:
				queries = [
						self.search_link % quote_plus(query + ' Season'),
						self.search_link % quote_plus(query + ' Complete')]
			else:
				queries = [
						self.search_link % quote_plus(query + ' S%s' % self.season_xx),
						self.search_link % quote_plus(query + ' Season %s' % self.season_x)]
			threads = []
			append = threads.append
			for url in queries:
				link = '%s%s' % (self.base_link, url)
				append(source_utils.Thread(self.get_sources_packs, link))
			[i.start() for i in threads]
			[i.join() for i in threads]
			return self.sources
		except:
			source_utils.scraper_error('ANIMETOSHO')
			return self.sources

	def get_sources_packs(self, link):
		try:
#			results = client.request(link, timeout=5)
			results = session.get(link, timeout=5).text
			if not results: return
			rows = client.parseDOM(results, 'div', attrs={'class': 'home_list_entry home_list_entry_alt home_list_entry_compl_1'})
		except:
			source_utils.scraper_error('ANIMETOSHO')
			return

		for row in rows:
			try:
				links = client.parseDOM(row, 'div', attrs={'class': 'links'})
				link = client.parseDOM(links, 'a', ret='href')
				magnet = next((i for i in link if 'magnet' in i), '').replace('&amp;', '&')
				magnet = urlparse(magnet).query
				magnet = dict(parse_qsl(magnet))

				hash = magnet.get('xt').split(':')[-1]
				hash = base64.b16encode(base64.b32decode(hash)).decode('utf-8')
				name = magnet.get('dn')
				# name = client.parseDOM(row, 'div', attrs={'class': 'link'})
				# name = client.parseDOM(name, 'a')[0]
				name = source_utils.clean_name(name)

				episode_start, episode_end = 0, 0
				if not self.search_series:
					if not self.bypass_filter:
						valid, episode_start, episode_end = source_utils.filter_season_pack(self.title, self.aliases, self.year, self.season_x, name)
						if not valid: continue
					package = 'season'

				elif self.search_series:
					if not self.bypass_filter:
						valid, last_season = source_utils.filter_show_pack(self.title, self.aliases, self.imdb, self.year, self.season_x, name, self.total_seasons)
						if not valid: continue
					else: last_season = self.total_seasons
					package = 'show'

				name_info = source_utils.info_from_name(name, self.title, self.year, season=self.season_x, pack=package)
				if source_utils.remove_lang(name_info, self.check_foreign_audio): continue
				if self.undesirables and source_utils.remove_undesirables(name_info, self.undesirables): continue

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
				try:
					seeders = client.parseDOM(links, 'span', ret='title')[0]
					seeders = int(seeders.split()[1])
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = client.parseDOM(row, 'div', attrs={'class': 'size'})[0]
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'animetosho', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if self.search_series: item.update({'last_season': last_season})
				elif episode_start: item.update({'episode_start': episode_start, 'episode_end': episode_end}) # for partial season packs
				self.sources_append(item)
			except:
				source_utils.scraper_error('ANIMETOSHO')

