# -*- coding: utf-8 -*-
# created by Venom
# modified for multiple shares -ud (01/10/23) modified to remove plex.direct and accept first result (3/31/23)
"""
	CocoScrapers Project
"""
import re
import time
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from urllib.parse import quote
from cocoscrapers.modules import cleantitle, source_utils
from cocoscrapers.modules.client import parseDOM, replaceHTMLCodes
from cocoscrapers.modules import source_utils
from cocoscrapers.modules import workers
from cocoscrapers.modules import control
from cocoscrapers.modules import plex as plexShare

PLEX_AUDIO = {'dca': 'dts', 'dca-ma': 'hdma'}

class source:
	priority = 2
	pack_capable = False
	hasMovies = True
	hasEpisodes = True
	def __init__(self):
		self.language = ['en']
		self.client_id = control.setting('plex.client_id')
		self.composite_installed = control.addonEnabled('plugin.video.composite_for_plex')


	def sources(self, data, hostDict):
		self.sources = []
		if not data: return self.sources
		self.sources_append = self.sources.append
		try:
			shares = plexShare.Plex().plex_get_all()
			########################################################
			threads = []
			append = threads.append
			for share in shares:
				append(workers.Thread(self.get_sources, share[0], share[1], share[2], data))
			[i.start() for i in threads]
			# alive = [x for x in threads if x.is_alive() is True]
			# while alive:
			# 	alive = [x for x in threads if x.is_alive() is True] #i suck this wasn't needed peter helped me fix by changing to below code.
			# 	time.sleep(0.1)
			[i.join() for i in threads]
			#from cocoscrapers.modules import log_utils
			#log_utils.log('sources = %s' % str(self.sources))
			return self.sources
		except:
			source_utils.scraper_error('PLEXSHARE')
			return self.sources

	def get_sources(self, sourceTitle, accessToken, plexShareURL, data):
		base_link = plexShareURL
		moviesearch = '/search?type=1&query=%s&year=%s&limit=100&X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % ('%s', '%s', self.client_id, accessToken)
		episodesearch = '/hubs/search?query=%s&limit=30&X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % ('%s', self.client_id, accessToken)
		if self.composite_installed: play_link = 'plugin://plugin.video.composite_for_plex/?url=%s' % base_link
		else: play_link = base_link

		try:
			aliases = data['aliases']
			year = data['year']
			if 'tvshowtitle' in data:
				title, episode_title = data['tvshowtitle'], data['title']
				hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode']))
				url = '%s%s' % (base_link, episodesearch % (quote(title+' '+episode_title)))
				years = None
			else:
				title, episode_title = data['title'], None
				hdlr = year
				url = '%s%s' % (base_link, moviesearch % (quote(title), year))
				years = [str(int(year)-1), str(year), str(int(year)+1)]
			#rom cocoscrapers.modules import log_utils
			#log_utils.log('url = %s' % url)

			try: results = requests.get(url,timeout=6)
			except requests.exceptions.SSLError: 
				results = requests.get(url, verify=False)

			if episode_title: results = re.findall(r'(<Video.+?type="episode".+?</Video>)', results.text, flags=re.M | re.S)
			else: results = re.findall(r'(<Video.+?type="movie".+?</Video>)', results.text, flags=re.M | re.S)

			# undesirables = source_utils.get_undesirables()
			# check_foreign_audio = source_utils.check_foreign_audio()
		except:
			source_utils.scraper_error('PLEXSHARE')
			return self.sources

		for result in results:
			#from cocoscrapers.modules import log_utils
			#log_utils.log('result = %s' % result)
			media = re.findall(r'(<Media.+?</Media>)', result, flags=re.M | re.S)
			for count, m in enumerate(media):
				try:
					name = cleantitle.normalize(replaceHTMLCodes(parseDOM(result, 'Part', ret='file')[count].replace(' ', '.')))
					if '/' in name: name = name.rsplit('/', 1)[1]
					elif '\\' in name: name = name.rsplit('\\', 1)[1]
					if not episode_title:
						source_year = re.search(r'(?:19|20)[0-9]{2}', name)
						if not source_year:
							source_year = parseDOM(result, 'Video', ret='year')[0]
							name = name.rsplit('.', 1)
							name = '%s.%s.%s' % (name[0], source_year, name[1])
					file_name = name

					if cleantitle.get(title.replace('&', 'and')) not in cleantitle.get(name.replace('&', 'and')): # use meta title in case file naming is whacked
						if not episode_title:
							meta_title = cleantitle.normalize(replaceHTMLCodes(parseDOM(result, 'Video', ret='title')[0].replace(' ', '.')))
							meta_year = parseDOM(result, 'Video', ret='year')[0]
							name = '%s.%s' % (meta_title, meta_year)
						else:
							meta_title = cleantitle.normalize(replaceHTMLCodes(parseDOM(result, 'Video', ret='grandparentTitle')[0].replace('&amp;', '&').replace(' ', '.')))
							meta_season, meta_episode = parseDOM(result, 'Video', ret='parentIndex')[0], parseDOM(result, 'Video', ret='index')[0]
							name = '%s.%s' % (meta_title, 'S%02dE%02d' % (int(meta_season), int(meta_episode)))

					if not source_utils.check_title(title, aliases, name, hdlr, year, years): continue
					name_info = source_utils.info_from_name(file_name, title, year, hdlr)
					# if source_utils.remove_lang(name_info, check_foreign_audio): continue
					# if undesirables and source_utils.remove_undesirables(name_info, undesirables): continue

					if not name_info or len(name_info) <= 5: # use meta info because file name lacks info, or has video extension only
						quality = parseDOM(result, 'Media', ret='videoResolution')[count]
						video_codec = parseDOM(result, 'Media', ret='videoCodec')[count]
						audio_codec = parseDOM(result, 'Media', ret='audioCodec')[count]
						try:
							if audio_codec.startswith('dca'): audio_codec = PLEX_AUDIO.get(audio_codec)
						except: pass
						audio_channels = parseDOM(result, 'Media', ret='audioChannels')[count]
						container = parseDOM(result, 'Media', ret='container')[count]
						name_info = '.' + quality + '.' + video_codec + '.' + audio_codec + '.' + audio_channels + 'ch.' + container

					if self.composite_installed:
						key = parseDOM(result, 'Video', ret='key')[0]
						url = '%s%s?X-Plex-Client-Identifier=%s&X-Plex-Token=%s&mode=5' % (play_link, key, self.client_id, accessToken)
					else:
						key = parseDOM(result, 'Part', ret='key')[count].rsplit('/', 1)[0] # remove "/file.mkv" to replace with true file name for dnld
						url = '%s%s/%s?X-Plex-Client-Identifier=%s&X-Plex-Token=%s' % (play_link, key, file_name, self.client_id, accessToken)

					size = parseDOM(result, 'Part', ret='size')[count]
					quality, info = source_utils.get_release_quality(name_info, url)
					try:
						dsize, isize = source_utils.convert_size(float(size), to='GB')
						if isize: info.insert(0, isize)
					except: dsize = 0
					info = ' | '.join(info)
					self.sources_append({'provider': 'plexshare', 'plexsource': sourceTitle, 'source': 'direct', 'name': file_name, 'name_info': name_info,
									'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': True, 'debridonly': False, 'size': dsize})
				except:
					source_utils.scraper_error('PLEXSHARE')