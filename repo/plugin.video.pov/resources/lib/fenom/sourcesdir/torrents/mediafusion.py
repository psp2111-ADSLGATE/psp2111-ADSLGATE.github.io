# created by Venom for Fenomscrapers (updated 3-02-2022)
"""
	Fenomscrapers Project
"""

#from json import loads as jsloads
import re, requests, queue
#from fenom import client
from fenom import source_utils
from fenom.control import setting as getSetting


class source:
	priority = 1
	pack_capable = True
	hasMovies = True
	hasEpisodes = True
	_queue = queue.SimpleQueue()
	def __init__(self):
		services = {
			'0': 'eJwBEALv_d8eMwmPMAH0OOXgqXZzpTAH9uhPZsBEL1TTrsTvCkr9KCIE_v4o5VdGPIQ-WXA2Z1F4_nv6Zw7MJTgSKTC6_b6rX-n2HsC3gDQIY-io84c8sjWkEd-1N1V226k2xmFImQq7eSWeGRUHz6YTHb4_9Qck9uSUoRW3xfnRaTPbp6nOABwYaexvPxDqKEyYz3H1tNlpq_kbH3qSUawSoFeU88SVgFrVw9yuohW8TN5Bs-jGkU_tp83mOifx2nVPvX1br3g0GgpRbXNWpEOCv-pa_0kTTV8WPZ6LBG9gjKkjESaAMtGJEtYmKVbErU1bLV_nsVEIYKBiIMzGHdE67Q43H4_ejQP9sbzG6J4NSX9i3E96v4LBllpWKmpLI7H-DFJ0RmsAvwrNwWvIVBRKIn-hTuq6SuPMprrBnqd5ICi8D0Rw4wGRihV2ugcYBlueDe4nvHNoA6By1tzEDnFt-SUr8kzc6QE7J9csKZlWh1pOLYtMRvQmzq8gK1z_ZAxixtdYIQtBCjyoumZZzarhgwJOuCJmkkzDBISCVbQmYs1enWvlpCGzJ4-gfZVU-HUahEZGjAjFm3T0jqDOTmVhv8pVxenaX8Mtkm558ms7lgzyCC3M2S23C5J4XLQL2pLd_pwDOrq0Q7aMlehz09D8Rq1ELvJHwXqJlr7HLH2yYOlHBqrkMpT-JA1SJ5GqCdnHbnQa6lNW_-U=',
			'1': 'eJwBEALv_SRpsWJ33q0gHCS8hCGKBJETkRM9pTk5EhKxL8qyUsYI55Y2-g06JIkKwTZVTcySesgP-mX4ddvfNe0G1MHDYfbmwDTUbLqi1Qg9vjTR982e5sBIyu81awv9iiBfqOYHb8ThqIRBPwtTFaKlC7OEANIv-dZmM7UuB8060VKCEnDxDZjDXIpOYBnB0nsI36QvRMS6fvONbB0fxDyLWOEY2J8t_Xz2TAl4y-GHip9rim-bYtlVgO1a_Tt_FtRAbl2u1OVEugwHanpBNn7qg79m4BRoWcksREhhiwMac9VwMZ2MLEc5eR205O-XuJFUBjBQspzjor1d5jSNp5J5_ObLC3TN4_sl3OCSnPfbKgwHv3GNYV78JzIu_JXzn90sotMNohe6qRrcSuKa-zUUcmn5hMZNPkMpjrS8YiZk204_Z4otuVeJwJxaY0gwA_Cr6PwYuwmUqvOerKqEtW5hMYFpdiwm5TMK9PIhgxYm5nmZtO4ZfMNujY6pKm6I4XwfQ4k64XxTgfRE_QKq8dadxVhjdsIlu9TiY5qZhvBAXqOWr111ejSJWqC_W_jDHLqX-CY-JF5bOKShNY7RrSp7qJdRhb5blVbWCYoUFkzQwU6CKdFVzUsclg9tSKq1lbV9G6ixKtyZYd1KpURpJpHLKJa_fom51ygsmDtM_-8lyZ-8up8oMMj37dGRRdxTPvfpKudrCccUCdg=',
			'2': 'eJwBEALv_YYta-vqXeyplvsLdRa9_gxrLyIAUKZSldRcxYdL5hpgJHeZ4yTo2elnviHYziZulfHPkPYRIeNvbDbfcmzEy7KZ3ezdsLPAkst6Wieeje9MJXegkfn27I_lrDRad0A56yAq8Gkics8dFbW1AukN8DEwo0ZS_s9JqSyjaqpQJb2Kvhu9rGY03fAeRKFm6bLRjeEOZOa7VuRixNvKPTj3oJmGQ53cfFqdAHxV572MeroKe0x7MauQK2ZT2QHYPS6C2wJ6nH2y8yG724JcNUGywZNeCmvboJRySQ1Vi-sRkpzrNUq8zw5uGOQoJ7hdXC96Dik-_3CUpU3XTW-sCCCp-ifsY-mQFv8UmZZ1D-TTJlN_Jj1mUcGSkMj89mb3Xdwwb3C50aqGNgT4MbIgHUwZ_DLnBcadfSQ3FKzWvf1qRGKiu1IoINCubweYjQ-0ApWvtneOKITKsjkRs6y8NJFNaaS3eyXSx6D_PLwQkxjfhA9aYATnuO5pB23u8hINXA2IR-jPVbhxj3HBe4VfyZLmZMYcED7c-Bx_wsOPVMLYpnD90tUIICQaDvdISfMEbGkq9ggvKy0MYqrkZsaMWwnKOAaSm29toAmkaORMzxi2zJrOT6-nOIFpAv0P-tfS6KzHmAMKrnSogaByWPWVTUP-GeSW-Gd74_cbnnJk8FusX6PrH7wv_Z8qxpDw4n9y-o-SPUZRDUg=',
			'3': 'eJwB4AEf_lnXQtODtVEQPYTzN5RH5ekzdON8j6UfgBIzKmwW1uMrQleG82Nq_AC3GmUVA0XDSiL2WzX3HgB6X6dyaNXQNui09IcpCE6JVfVcio7wjtL6a4dB64mBGFk4NCKxpZgr6J5D2tdURTyVdv15lJV0RUXp6OT-ojBKt13ldML-KPFFRe7KuHRwUhN7LF3bY7mdunCw88dpH7Il5HTZkZqVrrb4bu7RlsvgtSFs8bW-JP3emhHG37wen3PFG2OsK0kO1BYN0INshwF8nXnHX6dLnZO-lL7Ec7NsMpvsvnTJYRka6tPEZRQx3bFyMXXA8j2RgVUYxPbC6YSoamWp1Gd9MVPdY_kO8oftLC3jh1o3PdcTmuigdAtH0O6nkmBc3q8vye5Xp72GNnBgLXfGAhBqUv1bd9PvIu61_w-PL6Ch2JWRu9WuGVoY4ctbFJmqnwGXf-4x-0m50J-CaWxVE-c1ekOW7TTRGnpb1voDYWzVzqhcQBt7H9Fx9-DtXuFAxUi8Trxef3JKcSC3AoHXBEkkNAcOWoe7zXPEERcmFhriI4QRZBGjIih_o0lNRiyuoZFO9qmU28eKVbadfcKoIuqQmiFb5oNTPDsM3QXE0g0Hr8HM43URPStEh1B2TkfnuiKQ_rO2850='
		}
#		debrid = getSetting('mediafusion.debrid', '3')
		params = services['3'] # services[debrid]
		self.language = ['en']
		self.base_link = "https://mediafusion.elfhosted.com"
		self.movieSearch_link = f"/{params}/stream/movie/%s.json"
		self.tvSearch_link = f"/{params}/stream/series/%s:%s:%s.json"
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
			_INFO = re.compile(r'💾.*') # _INFO = re.compile(r'👤.*')
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('MEDIAFUSION')
			return sources

		for file in files:
			try:
				if 'url' in file:
					query = requests.utils.urlparse(file['url']).query
					params = dict(i.split('=') for i in query.split('&'))
					hash = params['info_hash']
				else: hash = file['infoHash']
				file_title = file['behaviorHints']['filename'].split('\n')
				file_info = [x for x in file['description'].split('\n') if _INFO.match(x)][0]
				# try:
					# index = file_title.index(file_info)
					# if index == 1: combo = file_title[0].replace(' ', '.')
					# else: combo = ''.join(file_title[0:2]).replace(' ', '.')
					# if '🇷🇺' in file_title[index+1] and not any(value in combo for value in ('.en.', '.eng.', 'english')): continue
				# except: pass

				name = source_utils.clean_name(file_title[0])

				if not source_utils.check_title(title, aliases, name.replace('.(Archie.Bunker', ''), hdlr, year): continue
				name_info = source_utils.info_from_name(name, title, year, hdlr, episode_title)
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name) 
				# if not episode_title: #filter for eps returned in movie query (rare but movie and show exists for Run in 2020)
					# ep_strings = [r'(?:\.|\-)s\d{2}e\d{2}(?:\.|\-|$)', r'(?:\.|\-)s\d{2}(?:\.|\-|$)', r'(?:\.|\-)season(?:\.|\-)\d{1,2}(?:\.|\-|$)']
					# name_lower = name.lower()
					# if any(re.search(item, name_lower) for item in ep_strings): continue

				try:
					seeders = int(re.search(r'(\d+)', file_info).group(1))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', file_info).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				append({'provider': 'mediafusion', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize})
			except:
				source_utils.scraper_error('MEDIAFUSION')
		return sources

	def sources_packs(self, data, hostDict, search_series=False, total_seasons=None, bypass_filter=False):
		sources = []
		if not data: return sources
		if not getSetting('mediafusion.packs') == 'true': return sources
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
			_INFO = re.compile(r'💾.*') # _INFO = re.compile(r'👤.*')
			undesirables = source_utils.get_undesirables()
			check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('MEDIAFUSION')
			return sources

		for file in files:
			try:
				if 'url' in file:
					query = requests.utils.urlparse(file['url']).query
					params = dict(i.split('=') for i in query.split('&'))
					hash = params['info_hash']
				else: hash = file['infoHash']
				file_title = file['description'].split('\n')
				file_info = [x for x in file_title if _INFO.match(x)][0]
				# try:
					# index = file_title.index(file_info)
					# if index == 1: combo = file_title[0].replace(' ', '.')
					# else: combo = ''.join(file_title[0:2]).replace(' ', '.')
					# if '🇷🇺' in file_title[index+1] and not any(value in combo for value in ('.en.', '.eng.', 'english')): continue
				# except: pass

				name = source_utils.clean_name(file_title[0].split('/')[0])

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
				if source_utils.remove_lang(name_info, check_foreign_audio): continue
				if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

				url = 'magnet:?xt=urn:btih:%s&dn=%s' % (hash, name)
				try:
					seeders = int(re.search(r'(\d+)', file_info).group(1))
					if self.min_seeders > seeders: continue
				except: seeders = 0

				quality, info = source_utils.get_release_quality(name_info, url)
				try:
					size = re.search(r'((?:\d+\,\d+\.\d+|\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|Gb|MB|MiB|Mb))', file_info).group(0)
					dsize, isize = source_utils._size(size)
					info.insert(0, isize)
				except: dsize = 0
				info = ' | '.join(info)

				item = {'provider': 'mediafusion', 'source': 'torrent', 'seeders': seeders, 'hash': hash, 'name': name, 'name_info': name_info, 'quality': quality,
							'language': 'en', 'url': url, 'info': info, 'direct': False, 'debridonly': True, 'size': dsize, 'package': package}
				if search_series: item.update({'last_season': last_season})
				elif episode_start: item.update({'episode_start': episode_start, 'episode_end': episode_end}) # for partial season packs
				sources_append(item)
			except:
				source_utils.scraper_error('MEDIAFUSION')
		return sources

