import sys
from threading import Thread
from apis.trakt_api import trakt_fetch_collection_watchlist, trakt_get_hidden_items, trakt_get_my_calendar, trakt_my_anime_calendar, trakt_anime_calendar
from indexers.metadata import tvshow_meta, season_episodes_meta
from caches.watched_cache import get_resumetime, get_watched_status_episode, get_watched_info_tv, get_bookmarks, get_next_episodes, get_in_progress_episodes
from modules import kodi_utils, settings
#from modules.utils import jsondate_to_datetime, adjust_premiered_date, make_day, get_datetime, title_key, date_difference, make_thread_list_enumerate
from modules.utils import jsondate_to_datetime, adjust_premiered_date, make_day, get_datetime, title_key, date_difference, TaskPool
# logger = kodi_utils.logger

string, ls, KODI_VERSION, make_cast_list = str, kodi_utils.local_string, kodi_utils.get_kodi_version(), kodi_utils.make_cast_list
build_url, remove_meta_keys, dict_removals = kodi_utils.build_url, kodi_utils.remove_meta_keys, kodi_utils.episode_dict_removals
get_art_provider, calendar_sort_order, ignore_articles = settings.get_art_provider, settings.calendar_sort_order, settings.ignore_articles
nextep_content_settings, nextep_display_settings, calendar_focus_today = settings.nextep_content_settings, settings.nextep_display_settings, settings.calendar_focus_today
thumb_fanart_info, date_offset_info, default_all_episodes = settings.thumb_fanart, settings.date_offset, settings.default_all_episodes
single_ep_display_title, single_ep_format = settings.single_ep_display_title, settings.single_ep_format
tv_meta_function, season_meta_function = tvshow_meta, season_episodes_meta
adjust_premiered_date_function, jsondate_to_datetime_function = adjust_premiered_date, jsondate_to_datetime
date_difference_function, make_day_function, title_key_function, get_datetime_function = date_difference, make_day, title_key, get_datetime
get_watched_status, get_watched_info = get_watched_status_episode, get_watched_info_tv
run_plugin, container_refresh, container_update = 'RunPlugin(%s)', 'Container.Refresh(%s)', 'Container.Update(%s)'
poster = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/box_office.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
watched_str, unwatched_str, extras_str, options_str = ls(32642), ls(32643), ls(32645), ls(32646)
clearprog_str, browse_str, browse_seas_str, traktmanager_str = ls(32651), ls(32652), ls(32544), ls(32198)

class Episodes:
	def __init__(self, params):
		self.params = params
		self.list_type = self.params.get('id_type', '')
		self.list = self.params.get('list', [])
		self.items = []
		self.set_constants()

	def run(self):
		try:
			params_get = self.params.get
			__handle__ = int(sys.argv[1])
			view_type, content_type = 'view.episodes', 'episodes'
			sort_type, category = 'unsorted', ls(params_get('name'))
			mode = params_get('mode')
			if   'in_progress' in mode:
				self.list_type = 'in_progress'
				self.list = get_in_progress_episodes()
			elif 'next_episode' in mode:
				indicators = settings.watched_indicators()
				watched_info = get_watched_info_tv(indicators)
				if indicators == 1: self.list_type = 'next_episode_trakt'
				else: self.list_type = 'next_episode_pov'
				self.list = get_next_episodes(watched_info)
			elif 'my_calendar' in mode:
				recently_aired = params_get('recently_aired', None)
				self.list = trakt_get_my_calendar(recently_aired, get_datetime())
				if recently_aired:
					self.list_type = 'trakt_recently_aired'
					self.list = self.list[:20]
				else:
					self.list_type = 'trakt_calendar'
					self.list = sorted(self.list, key=lambda k: k['sort_title'])
			elif 'my_anime_calendar' in mode:
				self.list = trakt_my_anime_calendar(get_datetime())
				self.list_type = 'trakt_calendar'
				self.list = sorted(self.list, key=lambda k: k['sort_title'])
			elif 'anime_calendar' in mode:
				self.list = trakt_anime_calendar(get_datetime())
				self.list_type = 'trakt_calendar'
				self.list = sorted(self.list, key=lambda k: k['sort_title'])
			kodi_utils.add_items(__handle__, self.worker())
		except: pass
		kodi_utils.set_category(__handle__, category)
		kodi_utils.set_sort_method(__handle__, sort_type)
		kodi_utils.set_content(__handle__, content_type)
		kodi_utils.end_directory(__handle__, False)
		kodi_utils.set_view_mode(view_type, content_type)
		if self.list_type == 'trakt_calendar' and calendar_focus_today():
			today = '[%s]' % ls(32849).upper()
			labels = enumerate([i[1].getLabel() for i in self.items], 1)
			try: index = max([i for i, x in labels if today in x])
			except: return
			kodi_utils.focus_index(index)

	def build_episode_content(self, _position, ep_data):
		try:
			ep_data_get = ep_data.get
			meta = tv_meta_function('trakt_dict', ep_data_get('media_ids'), self.meta_user_info, self.current_date)
			meta_get = meta.get
			if not meta: return
			if self.list_type.startswith('next_episode'):
				last_played = ep_data_get('last_played', self.resinsert)
				props = {'pov_last_played': last_played}
			else: props = {'pov_sort_order': string(ep_data_get('sort', _position))}
			cm = []
			cm_append = cm.append
			tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
			title, year, rootname, show_status = meta_get('title'), meta_get('year'), meta_get('rootname'), meta_get('status')
			show_poster = meta_get(self.poster_main) or meta_get(self.poster_backup) or poster
			show_fanart = meta_get(self.fanart_main) or meta_get(self.fanart_backup) or fanart
			clearlogo = meta_get('clearlogo') or meta_get('tmdblogo') or ''
			if self.fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
			else: banner, clearart, landscape = '', '', ''
			cast, mpaa, duration, tvshow_plot = meta_get('cast', []), meta_get('mpaa'), meta_get('duration'), meta_get('plot')
			trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
			orig_season, orig_episode = ep_data_get('season'), ep_data_get('episode')
			curr_season_data = next((i for i in meta_get('season_data') if i['season_number'] == orig_season), {})
			season_poster = curr_season_data.get('poster_path')
			if season_poster: season_poster = '%s%s%s' % ('https://image.tmdb.org/t/p/', self.meta_user_info['image_resolution']['poster'], season_poster)
			else: season_poster = show_poster
			if self.list_type.startswith('next_episode'):
				if orig_episode >= curr_season_data['episode_count']: orig_season, orig_episode, new_season = orig_season + 1, 1, True
				else: orig_episode, new_season = orig_episode + 1, False
			episodes_data = season_meta_function(orig_season, meta, self.meta_user_info)
			try: item = [i for i in episodes_data if i['episode'] == orig_episode][0]
			except: return
			item_get = item.get
			season, episode, ep_name = item_get('season'), item_get('episode'), item_get('title')
			props['episode_type'] = item_get('episode_type')
			str_season_zfill2, str_episode_zfill2 = string(season).zfill(1), string(episode).zfill(2)
			orig_premiered = item_get('premiered')
			episode_date, premiered = adjust_premiered_date_function(orig_premiered, self.adjust_hours)
			if not episode_date or self.current_date < episode_date:
				if self.list_type.startswith('next_episode'):
					if not self.nextep_include_unaired: return
					if episode_date and new_season and not date_difference_function(self.current_date, episode_date, 7): return
				elif not self.show_unaired: return
				unaired = True
				props['pov_unaired'] = 'true'
			else:
				unaired = False
				props['pov_unaired'] = 'false'
			playcount, overlay = get_watched_status(self.watched_info, string(tmdb_id), season, episode)
			resumetime, progress = get_resumetime(self.bookmarks, tmdb_id, season, episode)
			if self.display_title == 0: title_string = ''.join([title, ': '])
			else: title_string = ''
			if self.display_title in (0,1): seas_ep = ''.join([str_season_zfill2, 'x', str_episode_zfill2, ' - '])
			else: seas_ep = ''
			if self.list_type.startswith('next_episode'):
				unwatched = ep_data_get('unwatched', False)
				if episode_date: display_premiered = make_day_function(self.current_date, episode_date, self.date_format)
				else: display_premiered == 'UNKNOWN'
				airdate = ''.join(['[[COLOR magenta]', display_premiered, '[/COLOR]] ']) if self.nextep_include_airdate else ''
				highlight_color = self.nextep_unaired_color if unaired else self.nextep_unwatched_color if unwatched else ''
				italics_open, italics_close = ('[I]', '[/I]') if highlight_color else ('', '')
				if highlight_color: episode_info = ''.join([seas_ep, italics_open, '[COLOR', highlight_color, ']', ep_name, '[/COLOR]', italics_close])
				else: episode_info = ''.join([seas_ep, italics_open, ep_name, italics_close])
				display = ''.join([airdate, title_string.upper(), episode_info])
			elif self.list_type == 'trakt_calendar':
				if episode_date: display_premiered = make_day_function(self.current_date, episode_date, self.date_format)
				else: display_premiered == 'UNKNOWN'
				display = ''.join(['[', display_premiered, '] ', title_string.upper(), seas_ep, ep_name])
				if unaired:
					displays = display.split(']')
					display = ''.join(['[COLOR cyan]', displays[0], '][/COLOR]', displays[1]])
			else:
				color_tags = ('[COLOR cyan]', '[/COLOR]') if unaired else ('', '')
				display = ''.join([title_string.upper(), seas_ep, color_tags[0], ep_name, color_tags[1]])
			thumb = item_get('thumb', None) or show_fanart
			if self.thumb_fanart: background = thumb
			else: background = show_fanart
			item.update({'trailer': trailer, 'tvshowtitle': title, 'premiered': premiered, 'genre': genre, 'duration': duration,
						'mpaa': mpaa, 'studio': studio, 'playcount': playcount, 'overlay': overlay, 'title': display})
			extras_params = build_url({'mode': 'extras_menu_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id, 'is_widget': self.is_widget})
			options_params = build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode, 'is_widget': self.is_widget})
			url_params = build_url({'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
			if self.show_all_episodes:
				if self.all_episodes == 1 and meta_get('total_seasons') > 1: browse_params = build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
				else: browse_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all'})
			else: browse_params = build_url({'mode': 'build_season_list', 'tmdb_id': tmdb_id})
			browse_seas_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': season})
			cm_append((options_str, run_plugin % options_params))
			cm_append((extras_str, run_plugin % extras_params))
			cm_append((browse_str, self.container_update % browse_params))
			cm_append((browse_seas_str, self.container_update % browse_seas_params))
			clearprog_params, unwatched_params, watched_params = '', '', ''
			if not unaired:
				if progress != '0' or resumetime != '0':
					clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'media_type': 'episode', 'tmdb_id': tmdb_id,
												'season': season, 'episode': episode, 'refresh': 'true'})
					cm_append((clearprog_str, run_plugin % clearprog_params))
				if playcount:
					if self.hide_watched: return
					unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id,
												'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
					cm_append((unwatched_str % self.watched_title, run_plugin % unwatched_params))
				else:
					watched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id,
												'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': title, 'year': year})
					cm_append((watched_str % self.watched_title, run_plugin % watched_params))
			if self.list_type == 'next_episode_trakt':
				trakt_manager_params = build_url({'mode': 'trakt_manager_choice', 'tmdb_id': tmdb_id, 'imdb_id': imdb_id, 'tvdb_id': tvdb_id, 'media_type': 'tvshow'})
				cm_append((traktmanager_str, run_plugin % trakt_manager_params))
			props['pov_name'] = '%s - %sx%s' % (title, str_season_zfill2, str_episode_zfill2)
			props['pov_first_aired'] = premiered
			listitem = kodi_utils.make_listitem()
			listitem.addContextMenuItems(cm)
			listitem.setProperties(props)
			listitem.setLabel(display)
#			listitem.setContentLookup(False)
			listitem.setArt({'poster': show_poster, 'fanart': background, 'thumb': thumb, 'icon': thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': thumb,
							'season.poster': season_poster, 'tvshow.poster': show_poster, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': thumb, 'tvshow.banner': banner})
			if KODI_VERSION < 20:
				listitem.setCast(cast + item_get('guest_stars', []))
				listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				listitem.setInfo('video', remove_meta_keys(item, dict_removals))
				listitem.setProperty('resumetime', resumetime)
			else:
				if int(progress): listitem.setProperty('watchedprogress', progress)
				videoinfo = listitem.getVideoInfoTag(offscreen=True)
				videoinfo.setCast(make_cast_list(cast + item_get('guest_stars', [])))
				videoinfo.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				videoinfo.setDirectors(item_get('director').split(', '))
				videoinfo.setDuration(item_get('duration'))
				videoinfo.setEpisode(episode)
				videoinfo.setFirstAired(item_get('premiered'))
				videoinfo.setGenres(genre.split(', '))
				videoinfo.setIMDBNumber(imdb_id)
				videoinfo.setMediaType('episode')
				videoinfo.setMpaa(mpaa)
				videoinfo.setPlaycount(playcount)
				videoinfo.setPlot(item_get('plot'))
				videoinfo.setRating(item_get('rating'))
				videoinfo.setResumePoint(float(resumetime) or float(progress))
				videoinfo.setSeason(season)
				videoinfo.setStudios((studio,))
				videoinfo.setTitle(item_get('title'))
				videoinfo.setTrailer(trailer)
				videoinfo.setTvShowStatus(show_status)
				videoinfo.setTvShowTitle(title)
				videoinfo.setVotes(item_get('votes'))
				videoinfo.setWriters(item_get('writer').split(', '))
				videoinfo.setYear(int(year))
			self.append((url_params, listitem, False))
		except: pass

	def set_constants(self):
		self.meta_user_info = settings.metadata_user_info()
		self.watched_indicators = settings.watched_indicators()
		self.watched_info = get_watched_info(self.watched_indicators)
		self.show_unaired = settings.show_unaired()
		self.thumb_fanart = thumb_fanart_info()
		self.is_widget = kodi_utils.external_browse()
		self.fanart_enabled = self.meta_user_info['extra_fanart_enabled']
		self.hide_watched = self.is_widget and self.meta_user_info['widget_hide_watched']
		self.current_date = get_datetime_function()
		self.adjust_hours = date_offset_info()
		self.bookmarks = get_bookmarks(self.watched_indicators, 'episode')
		self.display_title, self.date_format = single_ep_display_title(), single_ep_format()
		self.all_episodes = default_all_episodes()
		self.show_all_episodes = self.all_episodes in (1, 2)
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = get_art_provider()
		self.watched_title = 'Trakt' if self.watched_indicators == 1 else 'POV'
		self.container_update = 'ActivateWindow(Videos,%s,return)' if self.is_widget else 'Container.Update(%s)'
		self.append = self.items.append

	def worker(self):
		if self.list_type.startswith('next_episode'):
			nextep_settings, nextep_disp_settings = nextep_content_settings(), nextep_display_settings()
			self.nextep_unaired_color, self.nextep_unwatched_color = nextep_disp_settings['unaired_color'], nextep_disp_settings['unwatched_color']
			self.nextep_include_airdate, self.nextep_include_unaired = nextep_disp_settings['include_airdate'], nextep_settings['include_unaired']
			if self.watched_indicators == 1:
				try:
					hidden_data = trakt_get_hidden_items('dropped')
					self.list = [i for i in self.list if not i['media_ids']['tmdb'] in hidden_data]
				except: pass
#				if nextep_settings['include_unwatched']:
#					try: unwatched = [{'media_ids': i['media_ids'], 'season': 1, 'episode': 0, 'unwatched': True} for i in trakt_fetch_collection_watchlist('watchlist', 'tvshow')]
#					except: unwatched = []
#					self.list += unwatched
				resformat, self.resinsert = '%Y-%m-%dT%H:%M:%S.%fZ', '2000-01-01T00:00:00.000Z'
			else: resformat, self.resinsert = '%Y-%m-%d %H:%M:%S', '2000-01-01 00:00:00'
#		threads = list(make_thread_list_enumerate(self.build_episode_content, self.list, Thread))
		threads = TaskPool().tasks_enumerate(self.build_episode_content, self.list, Thread)
		[i.join() for i in threads]
		if self.list_type.startswith('trakt_dict'):
			pass
		elif self.list_type.startswith('next_episode'):
			def func(function):
				if sort_key == 'pov_name': return title_key_function(function, ignore_articles())
				elif sort_key == 'pov_last_played': return jsondate_to_datetime_function(function, resformat)
				else: return function
			sort_key = nextep_settings['sort_key']
			sort_direction = nextep_settings['sort_direction']
			if nextep_settings['sort_airing_today_to_top']:
				airing_today = [i for i in self.items
								if date_difference_function(self.current_date, jsondate_to_datetime_function(i[1].getProperty('pov_first_aired'), '%Y-%m-%d').date(), 0)]
				airing_today.sort(key=lambda i: i[1].getProperty('pov_first_aired'))
				remainder = [i for i in self.items if not i in airing_today]
				remainder.sort(key=lambda i: func(i[1].getProperty(sort_key)), reverse=sort_direction)
				unaired = [i for i in remainder if i[1].getProperty('pov_unaired') == 'true']
				aired = [i for i in remainder if not i in unaired]
				self.items = airing_today + aired + unaired
			else:
				self.items.sort(key=lambda i: func(i[1].getProperty(sort_key)), reverse=sort_direction)
				unaired = [i for i in self.items if i[1].getProperty('pov_unaired') == 'true']
				aired = [i for i in self.items if not i in unaired]
				self.items = aired + unaired
		else:
			if self.list_type in ('trakt_calendar', 'trakt_recently_aired'):
				if self.list_type == 'trakt_calendar': reverse = calendar_sort_order() == 0
				else: reverse = True
				self.items.sort(key=lambda k: int(k[1].getProperty('pov_sort_order')))
				self.items.sort(key=lambda k: k[1].getProperty('pov_first_aired'), reverse=reverse)
			else: self.items.sort(key=lambda k: int(k[1].getProperty('pov_sort_order')))
		return self.items

