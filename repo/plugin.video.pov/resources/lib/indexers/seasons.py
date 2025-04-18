import sys
from threading import Thread
from indexers.metadata import tvshow_meta, season_episodes_meta, all_episodes_meta
from caches.watched_cache import get_watched_info_tv, get_watched_status_season
from caches.watched_cache import get_bookmarks, get_resumetime, get_watched_status_episode
from modules import kodi_utils, settings
from modules.utils import adjust_premiered_date, get_datetime
# from modules.kodi_utils import logger

KODI_VERSION, make_cast_list = kodi_utils.get_kodi_version(), kodi_utils.make_cast_list
make_listitem, build_url, ls, tp = kodi_utils.make_listitem, kodi_utils.build_url, kodi_utils.local_string, kodi_utils.translate_path
remove_meta_keys, dict_removals = kodi_utils.remove_meta_keys, kodi_utils.episode_dict_removals
get_art_provider, show_specials = settings.get_art_provider, settings.show_specials
thumb_fanart_info, date_offset_info, = settings.thumb_fanart, settings.date_offset
tv_meta_function, season_meta_function, all_episodes_meta_function = tvshow_meta, season_episodes_meta, all_episodes_meta
adjust_premiered_date_function, get_datetime_function = adjust_premiered_date, get_datetime
poster_empty, fanart_empty = tp('special://home/addons/plugin.video.pov/resources/media/box_office.png'), tp('special://home/addons/plugin.video.pov/fanart.png')
run_plugin, unaired_label, tmdb_image_url = 'RunPlugin(%s)', '[COLOR cyan]%s[/COLOR]', 'https://image.tmdb.org/t/p/'
season_str, watched_str, unwatched_str, extras_str, options_str = ls(32537), ls(32642), ls(32643), ls(32645), ls(32646)
string, clearprog_str = str, ls(32651)

class Seasons:
	def __init__(self, params):
		self.params = params
		self.id_type = params.get('id_type', 'tmdb_id')
		self.items = []

	def run(self):
		__handle__, is_widget = int(sys.argv[1]), kodi_utils.external_browse()
		mode = self.params.get('mode', 'build_season_list')
		if 'episode' in mode: content_type, view_type = 'episodes', 'view.episodes'
		else: content_type, view_type = 'seasons', 'view.seasons'
		items, name = self.build_season_list(self.params)
		kodi_utils.add_items(__handle__, items)
		kodi_utils.set_category(__handle__, name)
		kodi_utils.set_sort_method(__handle__, content_type)
		kodi_utils.set_content(__handle__, content_type)
		kodi_utils.end_directory(__handle__, False if is_widget else None)
		kodi_utils.set_view_mode(view_type, content_type)

	def build_season_list(self, params):
		def _process_season_list():
			use_season_title = settings.use_season_title()
			image_resolution = meta_user_info['image_resolution']['poster']
			season_data = meta_get('season_data')
			if season_data:
				if 'season' in params: season_data = [i for i in season_data if i['season_number'] == params['season']]
				if not show_specials(): season_data = [i for i in season_data if not i['season_number'] == 0]
				season_data.sort(key=lambda k: k['season_number'])
			else: season_data = []
			running_ep_count = total_aired_eps
			for item in season_data:
				try:
					props = {}
					cm = []
					cm_append = cm.append
					item_get = item.get
					name, overview, rating = item_get('name'), item_get('overview'), item_get('vote_average')
					season_number, episode_count = item_get('season_number'), item_get('episode_count')
					poster_path, air_date = item_get('poster_path'), item_get('air_date')
					poster =  ''.join([tmdb_image_url, image_resolution, poster_path]) if poster_path is not None else show_poster
					if season_number == 0: unaired = False
					elif episode_count == 0: unaired = True
					elif season_number != total_seasons: unaired = False
					else:
						episode_airs = adjust_premiered_date_function(air_date, 0)[0]
						if not episode_airs or current_date < episode_airs: unaired = True
						else: unaired = False
					if unaired:
						if not show_unaired: return
						episode_count = 0
					elif season_number != 0:
						running_ep_count -= episode_count
						if running_ep_count < 0: episode_count = running_ep_count + episode_count
					try: year = air_date.split('-')[0]
					except: year = show_year
					plot = overview or show_plot
					title = name if use_season_title and name else ' '.join([season_str, string(season_number)])
					if 'season' in params: title = '%s: %s' % (show_title, title)
					if unaired: title = '[I]%s[/I]' % (unaired_label % title)
					playcount, overlay, watched, unwatched = get_watched_status_season(watched_info, string(tmdb_id), season_number, episode_count)
					url_params = build_url({'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': season_number})
					extras_params = build_url({'mode': 'extras_menu_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id, 'is_widget': is_widget})
					options_params = build_url({'mode': 'options_menu_choice', 'content': 'season', 'tmdb_id': tmdb_id, 'is_widget': is_widget})
					cm_append((options_str, run_plugin % options_params))
					cm_append((extras_str, run_plugin % extras_params))
					if not playcount:
						watched_params = build_url({'mode': 'mark_as_watched_unwatched_season', 'action': 'mark_as_watched', 'title': show_title, 'year': show_year,
															'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season_number})
						cm_append((watched_str % watched_title, run_plugin % watched_params))
					if watched:
						if hide_watched: continue
						unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_season', 'action': 'mark_as_unwatched', 'title': show_title, 'year': show_year,
																'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'season': season_number})
						cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
					props['unwatchedepisodes'] = string(unwatched)
					props['totalepisodes'] = string(episode_count)
					props['pov_sort_order'] = string(params.get('sort', ''))
					listitem = make_listitem()
					listitem.addContextMenuItems(cm)
					listitem.setProperties(props)
					listitem.setLabel(title)
#					listitem.setContentLookup(False)
					listitem.setArt({'poster': poster, 'icon': poster, 'thumb': poster, 'fanart': fanart, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo,
									'landscape': landscape, 'tvshow.poster': poster, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape, 'tvshow.banner': banner})
					if KODI_VERSION < 20:
						listitem.setCast(show_cast)
						listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
						listitem.setInfo('video', {'mediatype': 'season', 'trailer': trailer, 'title': title, 'size': '0', 'duration': episode_run_time, 'plot': plot,
									'rating': rating, 'premiered': air_date, 'studio': studio, 'year': year, 'genre': genre, 'mpaa': mpaa, 'tvshowtitle': show_title,
									'imdbnumber': imdb_id, 'votes': votes, 'season': season_number, 'playcount': playcount, 'overlay': overlay})
						listitem.setProperty('watchedepisodes', string(watched))
					else:
						if watched > 0: listitem.setProperty('watchedepisodes', string(watched))
						videoinfo = listitem.getVideoInfoTag(offscreen=True)
						videoinfo.setCast(make_cast_list(show_cast))
						videoinfo.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
						videoinfo.setDuration(episode_run_time)
						videoinfo.setGenres(genre.split(', '))
						videoinfo.setIMDBNumber(imdb_id)
						videoinfo.setMediaType('season')
						videoinfo.setMpaa(mpaa)
						videoinfo.setPlaycount(playcount)
						videoinfo.setPlot(plot)
						videoinfo.setPremiered(air_date)
						videoinfo.setRating(rating)
						videoinfo.setSeason(season_number)
						videoinfo.setStudios((studio,))
						videoinfo.setTitle(title)
						videoinfo.setTrailer(trailer)
						videoinfo.setTvShowStatus(show_status)
						videoinfo.setTvShowTitle(show_title)
						videoinfo.setVotes(votes)
						videoinfo.setYear(int(year))
					append((url_params, listitem, True))
				except: pass
		def _process_episode_list():
			thumb_fanart = thumb_fanart_info()
			adjust_hours = date_offset_info()
			bookmarks = get_bookmarks(watched_indicators, 'episode')
			all_episodes = True if params.get('season') == 'all' else False
			if all_episodes:
				episodes_data = all_episodes_meta_function(meta, meta_user_info, Thread)
				if not show_specials(): episodes_data = [i for i in episodes_data if not i['season'] == 0]
			else: episodes_data = season_meta_function(params['season'], meta, meta_user_info)
			for item in episodes_data:
				try:
					props = {}
					cm = []
					cm_append = cm.append
					item_get = item.get
					season, episode, ep_name = item_get('season'), item_get('episode'), item_get('title')
					premiered, cast = item_get('premiered'), show_cast + item_get('guest_stars', [])
					props['episode_type'] = item_get('episode_type')
					episode_date, premiered = adjust_premiered_date_function(premiered, adjust_hours)
					playcount, overlay = get_watched_status_episode(watched_info, string(tmdb_id), season, episode)
					resumetime, progress = get_resumetime(bookmarks, tmdb_id, season, episode)
					thumb = item_get('thumb', None) or fanart
					if thumb_fanart: background = thumb
					else: background = fanart
					item.update({'trailer': trailer, 'tvshowtitle': show_title, 'premiered': premiered, 'genre': genre, 'duration': episode_run_time, 'mpaa': mpaa, 'studio': studio,
								'playcount': playcount, 'overlay': overlay})
					extras_params = build_url({'mode': 'extras_menu_choice', 'media_type': 'tvshow', 'tmdb_id': tmdb_id, 'is_widget': is_widget})
					options_params = build_url({'mode': 'options_menu_choice', 'content': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode, 'is_widget': is_widget})
					url_params = build_url({'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'season': season, 'episode': episode})
					display = ep_name
					unaired = False
					if not episode_date or current_date < episode_date:
						if not show_unaired: continue
						if season != 0:
							unaired = True
							display = '[I]%s[/I]' % (unaired_label % ep_name)
							item['title'] = display
					try: year = premiered.split('-')[0]
					except: year = show_year
					cm_append((options_str, run_plugin % options_params))
					cm_append((extras_str, run_plugin % extras_params))
					clearprog_params, unwatched_params, watched_params = '', '', ''
					if not unaired:
						if progress != '0' or resumetime != '0':
							clearprog_params = build_url({'mode': 'watched_unwatched_erase_bookmark', 'media_type': 'episode', 'tmdb_id': tmdb_id,
														'season': season, 'episode': episode, 'refresh': 'true'})
							cm_append((clearprog_str, run_plugin % clearprog_params))
						if playcount:
							if hide_watched: continue
							unwatched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_unwatched', 'tmdb_id': tmdb_id,
														'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': show_title, 'year': show_year})
							cm_append((unwatched_str % watched_title, run_plugin % unwatched_params))
						else:
							watched_params = build_url({'mode': 'mark_as_watched_unwatched_episode', 'action': 'mark_as_watched', 'tmdb_id': tmdb_id,
														'tvdb_id': tvdb_id, 'season': season, 'episode': episode,  'title': show_title, 'year': show_year})
							cm_append((watched_str % watched_title, run_plugin % watched_params))
					listitem = make_listitem()
					listitem.addContextMenuItems(cm)
					listitem.setProperties(props)
					listitem.setLabel(display)
#					listitem.setContentLookup(False)
					listitem.setArt({'poster': show_poster, 'fanart': background, 'thumb': thumb, 'icon': thumb, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo,
									'landscape': thumb, 'tvshow.poster': show_poster, 'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': thumb, 'tvshow.banner': banner})
					if KODI_VERSION < 20:
						listitem.setCast(cast)
						listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
						listitem.setInfo('video', remove_meta_keys(item, dict_removals))
						listitem.setProperty('resumetime', resumetime)
					else:
						if int(progress): listitem.setProperty('watchedprogress', progress)
						videoinfo = listitem.getVideoInfoTag(offscreen=True)
						videoinfo.setCast(make_cast_list(cast))
						videoinfo.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
						videoinfo.setDirectors(item_get('director').split(', '))
						videoinfo.setDuration(item_get('duration'))
						videoinfo.setEpisode(episode)
						videoinfo.setFirstAired(premiered)
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
						videoinfo.setTvShowTitle(show_title)
						videoinfo.setVotes(item_get('votes'))
						videoinfo.setWriters(item_get('writer').split(', '))
						videoinfo.setYear(int(year))
					append((url_params, listitem, False))
				except: pass
		current_date = get_datetime_function()
		meta_user_info = settings.metadata_user_info()
		watched_indicators = settings.watched_indicators()
		watched_info = get_watched_info_tv(watched_indicators)
		watched_title = 'Trakt' if watched_indicators == 1 else 'POV'
		show_unaired = settings.show_unaired()
		is_widget = kodi_utils.external_browse()
		fanart_enabled = meta_user_info['extra_fanart_enabled']
		hide_watched = is_widget and meta_user_info['widget_hide_watched']
		poster_main, poster_backup, fanart_main, fanart_backup = get_art_provider()
		meta = tv_meta_function('tmdb_id', params['tmdb_id'], meta_user_info, current_date)
		meta_get = meta.get
		tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
		rootname, show_status = meta_get('rootname'), meta_get('status')
		show_title, show_year, show_plot = meta_get('title'), meta_get('year'), meta_get('plot')
		show_poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
		fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
		clearlogo = meta_get('clearlogo') or meta_get('tmdblogo') or ''
		if fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
		else: banner, clearart, landscape = '', '', ''
		show_cast, mpaa, votes = meta_get('cast', []), meta_get('mpaa'), meta_get('votes')
		trailer, genre, studio = string(meta_get('trailer')), meta_get('genre'), meta_get('studio')
		episode_run_time, rating, premiered = meta_get('duration'), meta_get('rating'), meta_get('premiered')
		total_seasons, total_aired_eps = meta_get('total_seasons'), meta_get('total_aired_eps')
		append = self.items.append
		mode = params.get('mode', 'build_season_list')
		if 'episode' in mode: _process_episode_list()
		else: _process_season_list()
		if self.id_type == 'trakt_dict': return self.items
		else: return self.items, show_title

