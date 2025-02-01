import re
import os
import json
from sys import argv
from threading import Thread
from apis.opensubtitles_api import OpenSubtitlesAPI
from caches import watched_cache as ws
from windows import open_window
from modules import kodi_utils, settings
from modules.meta_lists import language_choices
from modules.utils import sec2time, clean_file_name, make_title_slug
# from modules.kodi_utils import logger

KODI_VERSION, make_cast_list = kodi_utils.get_kodi_version(), kodi_utils.make_cast_list
ls, get_setting = kodi_utils.local_string, kodi_utils.get_setting
poster_empty = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/box_office.png')
fanart_empty = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')

class POVPlayer(kodi_utils.xbmc_player):
	def __init__ (self):
		kodi_utils.xbmc_player.__init__(self)
		self.set_resume, self.set_watched, self.playback_event = 5, 90, None
		self.media_marked, self.subs_searched, self.nextep_info_gathered = False, False, False
		self.nextep_started, self.random_continual_started = False, False
		self.autoplay_next_episode, self.play_random_continual = False, False
		self.autoplay_nextep = settings.autoplay_next_episode()
		self.autoscrape_next_episode = False
		self.autoscrape_nextep = settings.autoscrape_next_episode()
		self.volume_check = get_setting('volumecheck.enabled', 'false') == 'true'

	def run(self, url=None, media_type=None):
		if not url: return
		try:
			if media_type == 'video':
				playlist = kodi_utils.make_playlist(media_type)
				playlist.clear()
				listitem = kodi_utils.make_listitem()
				listitem.setInfo(type=media_type, infoLabels={})
				playlist.add(url, listitem)
				kodi_utils.close_all_dialog()
				return self.play(playlist)
			self.meta = json.loads(kodi_utils.get_property('pov_playback_meta'))
			kodi_utils.clear_property('pov_playback_meta')
			self.meta_get = self.meta.get
			self.tmdb_id, self.imdb_id, self.tvdb_id = self.meta_get('tmdb_id'), self.meta_get('imdb_id'), self.meta_get('tvdb_id')
			self.media_type, self.title, self.year = self.meta_get('media_type'), self.meta_get('title'), self.meta_get('year')
			self.season, self.episode = self.meta_get('season', ''), self.meta_get('episode', '')
			background = self.meta_get('background', False) is True
			library_item = True if 'from_library' in self.meta else False
			if 'random' in self.meta or 'random_continual' in self.meta: bookmark = 0
			elif library_item: bookmark = self.bookmarkLibrary()
			else: bookmark = self.bookmarkPOV()
			if bookmark == 'cancel': return
			self.meta.update({'url': url, 'bookmark': bookmark})
			try:
				duration, plot, genre, trailer = self.meta_get('duration'), self.meta_get('plot'), self.meta_get('genre'), self.meta_get('trailer')
				rating, votes, premiered, studio = self.meta_get('rating'), self.meta_get('votes'), self.meta_get('premiered'), self.meta_get('studio')
				poster_main, poster_backup, fanart_main, fanart_backup = settings.get_art_provider()
				poster = self.meta_get(poster_main) or self.meta_get(poster_backup) or poster_empty
				fanart = self.meta_get(fanart_main) or self.meta_get(fanart_backup) or fanart_empty
				clearlogo = self.meta_get('clearlogo') or self.meta_get('tmdblogo') or ''
				listitem = kodi_utils.make_listitem()
				listitem.setPath(url)
				if self.media_type == 'movie':
					if KODI_VERSION < 20:
						listitem.setCast(self.meta_get('cast', []))
						listitem.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id)})
						listitem.setInfo('video', {'mediatype': 'movie', 'trailer': trailer, 'title': self.title, 'size': '0', 'duration': duration, 'plot': plot,
							'rating': rating, 'premiered': premiered, 'studio': studio, 'year': self.year, 'genre': genre, 'tagline': self.meta_get('tagline'), 'code': self.imdb_id,
							'imdbnumber': self.imdb_id, 'director': self.meta_get('director'), 'writer': self.meta_get('writer'), 'votes': votes})
					else:
						videoinfo = listitem.getVideoInfoTag(offscreen=True)
						videoinfo.setCast(make_cast_list(self.meta_get('cast', [])))
						videoinfo.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id)})
						kodi_utils.infoTagger(videoinfo, self.meta)
						videoinfo.setMediaType('movie')
				else:
					if KODI_VERSION < 20:
						listitem.setCast(self.meta_get('cast', []))
						listitem.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id), 'tvdb': str(self.tvdb_id)})
						listitem.setInfo('video', {'mediatype': 'episode', 'trailer': trailer, 'title': self.meta_get('ep_name'), 'imdbnumber': self.imdb_id,
							'tvshowtitle': self.title, 'size': '0', 'plot': plot, 'year': self.year, 'votes': votes, 'premiered': premiered, 'studio': studio, 'genre': genre,
							'season': self.season, 'episode': self.episode, 'duration': duration, 'rating': rating, 'FileNameAndPath': url})
					else:
						videoinfo = listitem.getVideoInfoTag(offscreen=True)
						videoinfo.setCast(make_cast_list(self.meta_get('cast', [])))
						videoinfo.setUniqueIDs({'imdb': self.imdb_id, 'tmdb': str(self.tmdb_id), 'tvdb': str(self.tvdb_id)})
						kodi_utils.infoTagger(videoinfo, self.meta)
						videoinfo.setMediaType('episode')
				if settings.get_fanart_data():
					banner, clearart, landscape = self.meta_get('banner'), self.meta_get('clearart'), self.meta_get('landscape')
				else: banner, clearart, landscape = '', '', ''
				listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
								'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape, 'tvshow.banner': banner})
				if not library_item: listitem.setProperty('StartPercent', str(bookmark))
				try:
					kodi_utils.clear_property('script.trakt.ids')
					trakt_ids = {'tmdb': self.tmdb_id, 'imdb': self.imdb_id, 'slug': make_title_slug(self.title)}
					if self.media_type == 'episode': trakt_ids['tvdb'] = self.tvdb_id
					kodi_utils.set_property('script.trakt.ids', json.dumps(trakt_ids))
				except: pass
			except: pass
			if library_item and not background:
				listitem.setProperty('IsPlayable', 'true')
				kodi_utils.set_resolvedurl(int(argv[1]), listitem)
			else: self.play(url, listitem)
			while not self.playback_event: kodi_utils.sleep(100)
			if self.isPlayingVideo(): self.monitor()
		except: return

	def bookmarkPOV(self):
		bookmark = 0
		watched_indicators = settings.watched_indicators()
		try: resume_point, curr_time, resume_id = ws.detect_bookmark(ws.get_bookmarks(watched_indicators, self.media_type), self.tmdb_id, self.season, self.episode)
		except: resume_point, curr_time = 0, 0
		resume_check = float(resume_point)
		if resume_check > 0:
			percent = str(resume_point)
			raw_time = float(curr_time)
			if watched_indicators == 1: _time = '%s%%' % str(percent)
			else: _time = sec2time(raw_time, n_msec=0)
			bookmark = self.getResumeStatus(_time, percent, bookmark)
			if bookmark == 0: ws.erase_bookmark(self.media_type, self.tmdb_id, self.season, self.episode)
		return bookmark

	def bookmarkLibrary(self):
		bookmark = 0
		try: curr_time = ws.get_bookmark_kodi_library(self.media_type, self.tmdb_id, self.season, self.episode)
		except: curr_time = 0.0
		if curr_time > 0:
			self.kodi_library_resumed = False
			_time = sec2time(curr_time, n_msec=0)
			bookmark = self.getResumeStatus(_time, curr_time, bookmark)
			if bookmark == 0: ws.erase_bookmark(self.media_type, self.tmdb_id, self.season, self.episode)
		return bookmark

	def getResumeStatus(self, _time, percent, bookmark):
		if settings.auto_resume(self.media_type): return percent
		choice = open_window(('windows.yes_no_progress_media', 'YesNoProgressMedia'), 'yes_no_progress_media.xml',
								meta=self.meta, text=ls(32790) % _time, enable_buttons=True, true_button=ls(32832), false_button=ls(32833), focus_button=10, percent=percent)
		return percent if choice is True else bookmark if choice is False else 'cancel'

	def monitor(self):
		kodi_utils.close_all_dialog()
		if self.media_type == 'episode':
			self.play_random_continual = 'random_continual' in self.meta
			if not self.play_random_continual and self.autoscrape_nextep: self.autoscrape_next_episode = 'random' not in self.meta
			if not self.play_random_continual and self.autoplay_nextep: self.autoplay_next_episode = 'random' not in self.meta
			if self.autoplay_nextep and self.autoscrape_nextep: self.autoscrape_next_episode = False
		if self.volume_check: kodi_utils.volume_checker(get_setting('volumecheck.percent', '100'))
		if not self.subs_searched: self.run_subtitles()
		kodi_utils.sleep(1000)
		while self.isPlayingVideo():
			try:
				kodi_utils.sleep(1000)
				self.total_time, self.curr_time = self.getTotalTime(), self.getTime()
				self.current_point = round(float(self.curr_time/self.total_time * 100), 1)
				if self.current_point >= self.set_watched and not self.media_marked:
					self.media_watched_marker()
				if self.play_random_continual:
					if not self.nextep_info_gathered: self.info_next_ep()
					self.remaining_time = round(self.total_time - self.curr_time)
					if self.remaining_time <= self.start_prep:
						if not self.nextep_started:
							self.run_random_continual()
				if self.autoplay_next_episode or self.autoscrape_next_episode:
					if not self.nextep_info_gathered: self.info_next_ep()
					self.remaining_time = round(self.total_time - self.curr_time)
					if self.remaining_time <= self.start_prep:
						if not self.nextep_started and self.autoplay_nextep:
							self.run_next_ep()
						if not self.nextep_started and self.autoscrape_nextep:
							self.run_scrape_next_ep()
			except: pass
		if not self.media_marked: self.media_watched_marker()
		ws.clear_local_bookmarks()

	def media_watched_marker(self):
		self.media_marked = True
		try:
			if self.current_point >= self.set_watched:
				if self.media_type == 'movie':
					watched_function = ws.mark_as_watched_unwatched_movie
					watched_params = {'mode': 'mark_as_watched_unwatched_movie', 'action': 'mark_as_watched', 'tmdb_id': self.tmdb_id, 'title': self.title, 'year': self.year,
									'refresh': 'false', 'from_playback': 'true'}
				else:
					watched_function = ws.mark_as_watched_unwatched_episode
					watched_params = {'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'season': self.season, 'episode': self.episode,
									'tmdb_id': self.tmdb_id, 'title': self.title, 'year': self.year, 'tvdb_id': self.tvdb_id, 'refresh': 'false', 'from_playback': 'true'}
				Thread(target=self.run_media_watched, args=(watched_function, watched_params)).start()
			else:
				kodi_utils.clear_property('pov_nextep_autoplays')
				kodi_utils.clear_property('pov_random_episode_history')
				if self.current_point >= self.set_resume:
					ws.set_bookmark(self.media_type, self.tmdb_id, self.curr_time, self.total_time, self.title, self.season, self.episode)
		except: pass

	def run_media_watched(self, function, params):
		try:
			function(params)
			kodi_utils.sleep(1000)
		except: pass

	def run_scrape_next_ep(self):
		self.nextep_started = True
		try:
			from modules.episode_tools import execute_scrape_nextep
			execute_scrape_nextep(self.meta)
		except: pass

	def run_next_ep(self):
		self.nextep_started = True
		try:
			from modules.episode_tools import execute_nextep
			Thread(target=execute_nextep, args=(self.meta, self.nextep_settings)).start()
		except: pass

	def run_random_continual(self):
		self.nextep_started = True
		try:
			from modules.episode_tools import execute_nextep
			Thread(target=execute_nextep, args=(self.meta, self.nextep_settings)).start()
		except: pass

	def run_subtitles(self):
		self.subs_searched = True
		try:
			season = self.season if self.media_type == 'episode' else None
			episode = self.episode if self.media_type == 'episode' else None
			Thread(target=Subtitles().get, args=(self.title, self.imdb_id, season, episode)).start()
		except: pass

	def info_next_ep(self):
		self.nextep_info_gathered = True
		try:
			self.nextep_settings = settings.autoplay_next_settings()
			if not self.nextep_settings['run_popup']:
				window_time = round(0.02 * self.total_time)
				self.nextep_settings['window_time'] = window_time
			elif self.nextep_settings['timer_method'] == 'percentage':
				percentage = self.nextep_settings['window_percentage']
				window_time = round((percentage/100) * self.total_time)
				self.nextep_settings['window_time'] = window_time
			else:
				window_time = self.nextep_settings['window_time']
			threshold_check = window_time + 21
			self.start_prep = self.nextep_settings['scraper_time'] + threshold_check
			self.nextep_settings.update({'threshold_check': threshold_check, 'start_prep': self.start_prep})
		except: pass

	def onAVStarted(self):
		kodi_utils.clear_property('pov.progress_is_alive')
		self.playback_event = True
		try: kodi_utils.close_all_dialog()
		except: pass

	def onPlayBackStarted(self):
		try: kodi_utils.hide_busy_dialog()
		except: pass

	def onPlayBackStopped(self):
		kodi_utils.clear_property('pov.progress_is_alive')
		self.playback_event = 'stop'

class Subtitles(kodi_utils.xbmc_player):
	def __init__(self):
		kodi_utils.xbmc_player.__init__(self)
		self.os = OpenSubtitlesAPI()
		self.language_dict = language_choices
		self.auto_enable = get_setting('subtitles.auto_enable')
		self.subs_action = get_setting('subtitles.subs_action')
		self.language1 = self.language_dict[get_setting('subtitles.language')]
		self.quality = ['bluray', 'hdrip', 'brrip', 'bdrip', 'dvdrip', 'webdl', 'webrip', 'webcap', 'web', 'hdtv', 'hdrip']

	def get(self, query, imdb_id, season, episode):
		def _notification(line, _time=3000):
			return kodi_utils.notification(line, _time)
		def _video_file_subs():
			try: available_sub_language = self.getSubtitles()
			except: available_sub_language = ''
			if available_sub_language == self.language1:
				if self.auto_enable == 'true': self.showSubtitles(True)
				_notification(32852)
				return True
			return False
		def _downloaded_subs():
			files = kodi_utils.list_dirs(subtitle_path)[1]
			if len(files) > 0:
				match_lang1 = None
				match_lang2 = None
				files = [i for i in files if i.endswith('.srt')]
				for item in files:
					if item == search_filename:
						match_lang1 = item
						break
				final_match = match_lang1 if match_lang1 else match_lang2 if match_lang2 else None
				if final_match:
					subtitle = os.path.join(subtitle_path, final_match)
					_notification(32792)
					return subtitle
			return False
		def _searched_subs():
			chosen_sub = None
			search_language = self.language1
			result = self.os.search(query, imdb_id, search_language, season, episode)
			if not result or len(result) == 0:
				_notification(32793)
				return False
			try: video_path = self.getPlayingFile()
			except: video_path = ''
			if '|' in video_path: video_path = video_path.split('|')[0]
			video_path = os.path.basename(video_path)
			if self.subs_action == '1':
				self.pause()
				choices = [i for i in result if i['SubLanguageID'] == search_language and i['SubSumCD'] == '1']
				if len(choices) == 0:
					_notification(32793)
					return False
				string = '%s - %s' % (ls(32246).upper(), video_path)
				dialog_list = ['[B]%s[/B] | [I]%s[/I]' % (i['SubLanguageID'].upper(), i['MovieReleaseName']) for i in choices]
				list_items = [{'line1': item} for item in dialog_list]
				kwargs = {'items': json.dumps(list_items), 'heading': string, 'enumerate': 'true', 'multi_choice': 'false', 'multi_line': 'false'}
				chosen_sub = kodi_utils.select_dialog(choices, **kwargs)
				self.pause()
				if not chosen_sub:
					_notification(32736, 1500)
					return False
			else:
				try: chosen_sub = [i for i in result if i['MovieReleaseName'].lower() in video_path.lower() and i['SubLanguageID'] == search_language and i['SubSumCD'] == '1'][0]
				except: pass
				if not chosen_sub:
					fmt = re.split(r'\.|\(|\)|\[|\]|\s|\-', video_path)
					fmt = [i.lower() for i in fmt]
					fmt = [i for i in fmt if i in self.quality]
					if season and fmt == '': fmt = 'hdtv'
					result = [i for i in result if i['SubSumCD'] == '1']
					filter = [
						i for i in result
						if i['SubLanguageID'] == search_language and any(x in i['MovieReleaseName'].lower() for x in fmt) and any(x in i['MovieReleaseName'].lower() for x in self.quality)
					]
					filter += [i for i in result if any(x in i['MovieReleaseName'].lower() for x in self.quality)]
					filter += [i for i in result if i['SubLanguageID'] == search_language]
					if len(filter) > 0: chosen_sub = filter[0]
					else: chosen_sub = result[0]
			try: lang = kodi_utils.convert_language(chosen_sub['SubLanguageID'])
			except: lang = chosen_sub['SubLanguageID']
			sub_format = chosen_sub['SubFormat']
			final_filename = sub_filename + '_%s.%s' % (lang, sub_format)
			download_url = chosen_sub['ZipDownloadLink']
			temp_zip = os.path.join(subtitle_path, 'temp.zip')
			temp_path = os.path.join(subtitle_path, chosen_sub['SubFileName'])
			final_path = os.path.join(subtitle_path, final_filename)
			subtitle = self.os.download(download_url, subtitle_path, temp_zip, temp_path, final_path)
			kodi_utils.sleep(1000)
			return subtitle
		if self.subs_action == '2': return
		kodi_utils.sleep(2500)
		imdb_id = re.sub(r'[^0-9]', '', imdb_id)
		subtitle_path = kodi_utils.translate_path('special://temp/')
		sub_filename = 'POVSubs_%s_%s_%s' % (imdb_id, season, episode) if season else 'POVSubs_%s' % imdb_id
		search_filename = sub_filename + '_%s.srt' % self.language1
		subtitle = _video_file_subs()
		if subtitle: return
		subtitle = _downloaded_subs()
		if subtitle: return self.setSubtitles(subtitle)
		subtitle = _searched_subs()
		if subtitle: return self.setSubtitles(subtitle)

