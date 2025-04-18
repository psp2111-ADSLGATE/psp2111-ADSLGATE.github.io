# created by kodifitzwell for Fenomscrapers
"""
	Fenomscrapers Project
"""

#from json import loads as jsloads
import re, requests, queue
#from resources.lib.fenom import client
from fenom import source_utils


class source:
	priority = 1
	pack_capable = True
	hasMovies = True
	hasEpisodes = True
	_queue = queue.SimpleQueue()
	def __init__(self):
		params = 'E2-AL4WGqDrj2M0MPdlx8ttOA%3D%3D-RpXaUvTCgu6DtWci%2FJWqVg5S4ZmxAALYaEbE80%2Br%2FdxY1eeZrJr7L7dIiWMeyB%2BzucFEILtMsP49bezJXGFsV%2FrN5S7Zpik1qcsaePN108DTqiskzTyNIblAawM7eAmh06I6SVs4VYm891OlzagAkeMEvchsYhrczGWfi6cEO3t6cO5QC2HRKPRe6GpoXZXXzDMqVeaDbRzmEJuyXGovv1MLxnEbGWjdQJggLU8EkmXtUo1j%2F7o21Y8%2FpVQdjxnipw6DwKxyIyQ255vXoQvXtaK8dqaLbHhbmaldpNfz9xIgJC5I1441OtlEd9ysqygbHg7W%2FYsLs%2F1E%2BJrZFqzss5bm28viMuT8WIWUOE8xHP%2B99%2FlKdADRMQtT0GdvxTyjq%2F2r8AsOuGvbBk1%2Ffo%2FcIN%2Fk9KDelLfiaOY4j7qCVjQzbkQKPLiCMMMJxu57xvpNlqwKzqbAp5UN8jXEQCwuu%2FXbpAGERFYLHINBAzdZZE9lV4PnFrATX5YYBwWHDawdI4XxOjJ4gtoMDUTdJYYzbtlL6clHzHIpKZ1s%2Bb0drhr3VGGKyxD%2F%2FaZVskykGRriwVM1gIHR00BK4kNTi6Gb4cnMrliy7SyaBKk2Xq3b29uB4uqusdpOCdI7vhBme1Jg'
		self.language = ['en']
		self.base_link = f"https://aiostreams.elfhosted.com/{params}"
		self.movieSearch_link = '/stream/movie/%s.json'
		self.tvSearch_link = '/stream/series/%s:%s:%s.json'
		self.min_seeders = 0

	def sources(self, data, hostDict):
		sources = []
		if not data: return sources
		append = sources.append
		try:
			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')
			aliases = data['aliases']
			episode_title = data['title'] if 'tvshowtitle' in data else None
			year = data['year']
			imdb = data['imdb']
			if 'tvshowtitle' in data:
				season = data['season']
				episode = data['episode']
				hdlr = 'S%02dE%02d' % (int(season), int(episode))
				url = '%s%s' % (self.base_link, self.tvSearch_link % (imdb, season, episode))
			else:
				url = '%s%s' % (self.base_link, self.movieSearch_link % imdb)
				hdlr = year
			# log_utils.log('url = %s' % url)
			try:
				results = requests.get(url, timeout=7) # client.request(url, timeout=7)
				files = results.json()['streams'] # jsloads(results)['streams']
			except: files = []
			self._queue.put_nowait(files) # if seasons
			self._queue.put_nowait(files) # if shows
			_INFO = re.compile(r'👤|💾.*')
		except:
			source_utils.scraper_error('AIOSTREAMS')
			return sources

		for file in files:
			try:
				hash = file['infoHash']
				file_title = file['description'].split('\n')
				file_info = [x for x in file_title if _INFO.match(x)][0]
				# try:
					# index = file_title.index(file_info)
					# if index == 1: combo = file_title[0].replace(' ', '.')
					# else: combo = ''.join(file_title[0:2]).replace(' ', '.')
					# if '🇷🇺' in file_title[index+1] and not any(value in combo for value in ('.en.', '.eng.', 'english')): continue
				# except: pass

				name = source_utils.clean_name(file_title[1])

				if not source_utils.check_title(title, aliases, name.replace('.(Archie.Bunker', ''), hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name) 
				# if not episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					# ep_strings = [r'(?:\.|\-)s\d{2}e\d{2}(?:\.|\-|$)', r'(?:\.|\-)s\d{2}(?:\.|\-|$)', r'(?:\.|\-)season(?:\.|\-)\d{1,2}(?:\.|\-|$)']
					# name_lower = name.lower()
					# if any(re.search(item, name_lower) for item in ep_strings): continue

				try:
					seeders = int(re.search(r'👤 (\d+)', file_info).group(1))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', file_info).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				append({'provider': 'aiostreams', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('AIOSTREAMS')
		return sources

	def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		sources = []
		if not data: return sources
		sources_append = sources.append
		try:
			title = data['tvshowtitle'].replace('&', 'and').replace('Special Victims Unit', 'SVU').replace('/', ' ')
			aliases = data['aliases']
			imdb = data['imdb']
			year = data['year']
			season = data['season']
			url = '%s%s' % (self.base_link, self.tvSearch_link % (imdb, season, data['episode']))
#			results = requests.get(url, timeout=7) # client.request(url, timeout=7)
			files = self._queue.get(timeout=8) # jsloads(results)['streams']
			_INFO = re.compile(r'👤|💾.*')
		except:
			source_utils.scraper_error('AIOSTREAMS')
			return sources

		for file in files:
			try:
				hash = file['infoHash']
				file_title = file['description'].split('\n')
				file_info = [x for x in file_title if _INFO.match(x)][0]
				# try:
					# index = file_title.index(file_info)
					# if index == 1: combo = file_title[0].replace(' ', '.')
					# else: combo = ''.join(file_title[0:2]).replace(' ', '.')
					# if '🇷🇺' in file_title[index+1] and not any(value in combo for value in ('.en.', '.eng.', 'english')): continue
				# except: pass

				name = source_utils.clean_name(file_title[1])

				episode_start, episode_end = 0, 0
				if not search_series:
					if not bypass_filter:
						valid, episode_start, episode_end = source_utils.filter_season_pack(title, aliases, year, season, name.replace('.(Archie.Bunker', ''))
						if not valid: continue
					package = 'season'

				elif search_series:
					if not bypass_filter:
						valid, last_season = source_utils.filter_show_pack(title, aliases, imdb, year, season, name.replace('.(Archie.Bunker', ''), total_seasons)
						if not valid: continue
					else: last_season = total_seasons
					package = 'show'

				name_info = source_utils.info_from_name(name, title, year, season=season, pack=package)

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
				try:
					seeders = int(re.search(r'👤 (\d+)', file_info).group(1))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', file_info).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'aiostreams', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if search_series: item.update({'last_season': last_season})
				elif episode_start: item.update({'episode_start': episode_start, 'episode_end': episode_end}) # for partial season packs
				sources_append(item)
			except:
				source_utils.scraper_error('AIOSTREAMS')
		return sources

