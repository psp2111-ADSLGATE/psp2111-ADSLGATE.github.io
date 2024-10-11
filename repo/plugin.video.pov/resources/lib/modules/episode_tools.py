import json
from sys import argv
from datetime import date
from random import choice
from threading import Thread
import _strptime  # fix bug in python import
from windows import open_window
from apis.trakt_api import trakt_get_hidden_items
from indexers.metadata import tvshow_meta, season_episodes_meta, all_episodes_meta
from caches.watched_cache import get_next_episodes, get_watched_status_tvshow, get_watched_info_tv
from modules import kodi_utils, settings
from modules.sources import Sources
from modules.player import POVPlayer
from modules.utils import get_datetime, make_thread_list, title_key, adjust_premiered_date
# from modules.kodi_utils import logger

KODI_VERSION, make_cast_list = kodi_utils.get_kodi_version(), kodi_utils.make_cast_list
ls, make_listitem, build_url = kodi_utils.local_string, kodi_utils.make_listitem, kodi_utils.build_url
dict_removals, remove_meta_keys = kodi_utils.tvshow_dict_removals, kodi_utils.remove_meta_keys
settings_icon= kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/settings.png')
poster_empty = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/box_office.png')
fanart_empty = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
string, amble_label = str, '[COLOR dimgray][I]%s[/I][/COLOR]'
included_str, excluded_str = ls(32804).upper(), ls(32805).upper()
extras_str, browse_str, heading = ls(32645), ls(32652), ls(32806).upper()

def build_next_episode_manager():
	def build_content(item):
		try:
			cm = []
			cm_append = cm.append
			meta = tvshow_meta('trakt_dict', item['media_ids'], meta_user_info, current_date)
			meta_get = meta.get
			tmdb_id, tvdb_id, imdb_id = meta_get('tmdb_id'), meta_get('tvdb_id'), meta_get('imdb_id')
			total_aired_eps, total_seasons = meta_get('total_aired_eps'), meta_get('total_seasons')
			title = meta_get('title')
			poster = meta_get(poster_main) or meta_get(poster_backup) or poster_empty
			fanart = meta_get(fanart_main) or meta_get(fanart_backup) or fanart_empty
			clearlogo = meta_get('clearlogo') or meta_get('tmdblogo') or ''
			if fanart_enabled: banner, clearart, landscape = meta_get('banner'), meta_get('clearart'), meta_get('landscape')
			else: banner, clearart, landscape = '', '', ''
			playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(watched_info, string(tmdb_id), total_aired_eps)
			meta.update({'playcount': playcount, 'overlay': overlay})
			if tmdb_id in exclude_list: color, action, status, sort_value = 'red', 'unhide', excluded_str, 1
			else: color, action, status, sort_value = 'green', 'hide', included_str, 0
			display = '[COLOR %s][%s][/COLOR] %s' % (color, status, title)
			extras_params = {'mode': 'extras_menu_choice', 'tmdb_id': tmdb_id, 'media_type': 'tvshow', 'is_widget': 'False'}
			url_params = {'mode': 'trakt.hide_unhide_trakt_items', 'action': action, 'media_type': 'shows', 'media_id': imdb_id, 'section': 'progress_watched'}
			url = build_url(url_params)
			if show_all_episodes:
				if all_episodes == 1 and total_seasons > 1: browse_params = {'mode': 'build_season_list', 'tmdb_id': tmdb_id}
				else: browse_params = {'mode': 'build_episode_list', 'tmdb_id': tmdb_id, 'season': 'all'}
			else: browse_params = {'mode': 'build_season_list', 'tmdb_id': tmdb_id}
			cm_append((extras_str, 'RunPlugin(%s)' % build_url(extras_params)))
			cm_append((browse_str, 'Container.Update(%s)' % build_url(browse_params)))
			props = {
				'sort_value': sort_value,
				'sort_title': title,
				'watchedepisodes': str(total_watched),
				'unwatchedepisodes': str(total_unwatched),
				'totalepisodes': str(total_aired_eps),
				'totalseasons': str(total_seasons)}
			listitem = make_listitem()
			listitem.addContextMenuItems(cm)
			listitem.setProperties(props)
			listitem.setLabel(display)
			listitem.setArt({'poster': poster, 'fanart': fanart, 'icon': poster, 'banner': banner, 'clearart': clearart, 'clearlogo': clearlogo, 'landscape': landscape,
							'tvshow.clearart': clearart, 'tvshow.clearlogo': clearlogo, 'tvshow.landscape': landscape, 'tvshow.banner': banner})
			if KODI_VERSION < 20:
				listitem.setCast(meta_get('cast', []))
				listitem.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				listitem.setInfo('video', remove_meta_keys(meta, dict_removals))
			else:
				videoinfo = listitem.getVideoInfoTag(offscreen=True)
				videoinfo.setCast(make_cast_list(meta_get('cast', [])))
				videoinfo.setUniqueIDs({'imdb': imdb_id, 'tmdb': string(tmdb_id), 'tvdb': string(tvdb_id)})
				kodi_utils.infoTagger(videoinfo, meta)
			append((url, listitem, False))
		except: pass
	__handle__ = int(argv[1])
	list_items = []
	append = list_items.append
	meta_user_info = settings.metadata_user_info()
	watched_indicators = settings.watched_indicators()
	watched_info = get_watched_info_tv(watched_indicators)
	fanart_enabled = meta_user_info['extra_fanart_enabled']
	current_date = get_datetime()
	include_year_in_title = settings.include_year_in_title('tvshow')
	open_extras = settings.extras_open_action('tvshow')
	all_episodes = settings.default_all_episodes()
	show_all_episodes = True if all_episodes in (1, 2) else False
	poster_main, poster_backup, fanart_main, fanart_backup = settings.get_art_provider()
	try: exclude_list = trakt_get_hidden_items('progress_watched')
	except: exclude_list = []
	show_list = get_next_episodes(watched_info)
	threads = list(make_thread_list(build_content, show_list, Thread))
	[i.join() for i in threads]
	list_items.sort(key=lambda k: (k[1].getProperty('sort_value'), title_key(k[1].getProperty('sort_title'), settings.ignore_articles())))
	kodi_utils.add_dir(__handle__, {'mode': 'amble'}, amble_label % heading, iconImage=settings_icon, isFolder=False)
	kodi_utils.add_items(__handle__, list_items)
	kodi_utils.set_content(__handle__, 'tvshows')
	kodi_utils.end_directory(__handle__, cacheToDisc=False)
	kodi_utils.set_view_mode('view.main', 'tvshows')
	kodi_utils.focus_index(1)

def nextep_playback_info(meta):
	def _build_next_episode_play():
		ep_data = season_episodes_meta(season, meta, settings.metadata_user_info())
		if not ep_data: return 'no_next_episode'
		ep_data = [i for i in ep_data if i['episode'] == episode][0]
		airdate = ep_data['premiered']
		d = airdate.split('-')
		episode_date = date(int(d[0]), int(d[1]), int(d[2]))
		if current_date < episode_date: return 'no_next_episode'
		custom_title = meta_get('custom_title', None)
		title = custom_title or meta_get('title')
		display_name = '%s - %dx%.2d' % (title, int(season), int(episode))
		meta.update({'media_type': 'episode', 'rootname': display_name, 'season': season, 'ep_name': ep_data['title'],
					'episode': episode, 'premiered': airdate, 'plot': ep_data['plot']})
		url_params = {'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': tmdb_id, 'tvshowtitle': meta_get('rootname'), 'season': season,
					'episode': episode, 'background': 'true'}
		if custom_title: url_params['custom_title'] = custom_title
		return url_params
	meta_get = meta.get
	tmdb_id, current_season, current_episode = meta_get('tmdb_id'), int(meta_get('season')), int(meta_get('episode'))
	try:
		current_date = get_datetime()
		season_data = meta_get('season_data')
		curr_season_data = [i for i in season_data if i['season_number'] == current_season][0]
		season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
		episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
		nextep_info = _build_next_episode_play()
	except: nextep_info = 'error'
	return meta, nextep_info

def execute_scrape_nextep(meta):
	nextep_meta, nextep_params = nextep_playback_info(meta)
	if nextep_params == 'error': return kodi_utils.notification(32574)
	elif nextep_params == 'no_next_episode': return
	player = POVPlayer()
	Sources().playback_prep(nextep_params)
	while player.isPlayingVideo(): kodi_utils.sleep(100)
	Sources().playback_prep({**nextep_params, 'background': 'false'})

def execute_nextep(meta, nextep_settings):
	def _get_nextep_params():
		if 'random_continual' in meta: nextep_params = get_random_episode(meta['tmdb_id'], True)
		else: nextep_params = nextep_playback_info(meta)
		return nextep_params
	def _get_nextep_url():
		Sources().playback_prep(nextep_params)
		return kodi_utils.get_property('pov_background_url')
	def _confirm_threshold():
		nextep_threshold = nextep_settings['threshold']
		if nextep_threshold == 0: return True
		try: current_number = int(kodi_utils.get_property('pov_total_autoplays'))
		except: current_number = 1
		if current_number == nextep_threshold:
			current_number = 1
			kodi_utils.set_property('pov_total_autoplays', str(current_number))
			if open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=nextep_meta, function='confirm'): return True
			else:
				kodi_utils.notification(32736, 2000)
				return False
		else:
			current_number += 1
			kodi_utils.set_property('pov_total_autoplays', str(current_number))
			return True
	def _continue_action():
		if run_popup: action = open_window(('windows.next_episode', 'NextEpisode'), 'next_episode.xml', meta=nextep_meta, function='next_ep')
		else: action = 'close'
		return action
	def _control():
		confirm_threshold = False
		final_action = 'cancel'
		while player.isPlayingVideo():
			try:
				total_time = player.getTotalTime()
				curr_time = player.getTime()
				remaining_time = round(total_time - curr_time)
				if remaining_time <= nextep_threshold_check:
					if not confirm_threshold:
						confirm_threshold = _confirm_threshold()
						if not confirm_threshold:
							final_action = 'cancel'
							break
				if remaining_time <= display_nextep_popup:
					final_action = _continue_action()
					break
				kodi_utils.sleep(200)
			except: pass
		return final_action
	kodi_utils.clear_property('pov_background_url')
	player = POVPlayer()
	run_popup, display_nextep_popup = nextep_settings['run_popup'], nextep_settings['window_time']
	nextep_prep, nextep_threshold_check = nextep_settings['start_prep'], nextep_settings['threshold_check']
	nextep_meta, nextep_params = _get_nextep_params()
	if nextep_params == 'error': return kodi_utils.notification(32574)
	elif nextep_params == 'no_next_episode': return
	nextep_url = _get_nextep_url()
	if not nextep_url: return kodi_utils.notification(32760)
	action = _control()
	if action == 'cancel': return kodi_utils.notification(32736)
	elif action == 'play': player.stop()
	elif action == 'close':
		if not run_popup: kodi_utils.notification('%s %s S%02dE%02d' % (ls(32801), nextep_meta['title'], nextep_meta['season'], nextep_meta['episode']), 6500, nextep_meta['poster'])
		while player.isPlayingVideo(): kodi_utils.sleep(100)
	kodi_utils.sleep(1000)
	player.run(nextep_url)

def get_random_episode(tmdb_id, continual=False):
	meta_user_info, adjust_hours, current_date = settings.metadata_user_info(), settings.date_offset(), get_datetime()
	tmdb_key = str(tmdb_id)
	meta = tvshow_meta('tmdb_id', tmdb_id, meta_user_info, current_date)
	try:
		episodes_data = [i for i in all_episodes_meta(meta, meta_user_info, Thread) if i['premiered']]
		episodes_data = [i for i in episodes_data if not i['season']  == 0 and adjust_premiered_date(i['premiered'], adjust_hours)[0] <= current_date]
	except: episodes_data = []
	if not episodes_data: return None
	if continual:
		episode_list = []
		try:
			episode_history = json.loads(kodi_utils.get_property('pov_random_episode_history'))
			if tmdb_key in episode_history: episode_list = episode_history[tmdb_key]
			else: kodi_utils.set_property('pov_random_episode_history', '')
		except: pass
#		first_run = len(episode_list) == 0
		episodes_data = [i for i in episodes_data if not i in episode_list]
		if not episodes_data:
			kodi_utils.set_property('pov_random_episode_history', '')
			return get_random_episode(tmdb_id, continual=True)
#	else: first_run = True
	chosen_episode = choice(episodes_data)
	if continual:
		episode_list.append(chosen_episode)
		episode_history = {str(tmdb_id): episode_list}
		kodi_utils.set_property('pov_random_episode_history', json.dumps(episode_history))
	title, season, episode = meta['title'], int(chosen_episode['season']), int(chosen_episode['episode'])
	query = title + ' S%.2dE%.2d' % (season, episode)
	display_name = '%s - %dx%.2d' % (title, season, episode)
	ep_name, plot = chosen_episode['title'], chosen_episode['plot']
	try: premiered = adjust_premiered_date(chosen_episode['premiered'], adjust_hours)[1]
	except: premiered = chosen_episode['premiered']
	meta.update({'media_type': 'episode', 'rootname': display_name, 'season': season, 'episode': episode, 'premiered': premiered, 'ep_name': ep_name, 'plot': plot})
	if continual: meta['random_continual'] = 'true'
	else: meta['random'] = 'true'
	url_params = {'mode': 'play_media', 'media_type': 'episode', 'tmdb_id': meta['tmdb_id'], 'query': query,
					'tvshowtitle': meta['rootname'], 'season': season, 'episode': episode, 'background': 'true', 'meta': json.dumps(meta)}
#	if not first_run: url_params['background'] = 'true'
	return meta, url_params

def play_random(tmdb_id, continual=False):
	meta, url_params = get_random_episode(tmdb_id, continual)
	if not url_params: return {'pass': True}
	url_params.update({'autoplay': 'True', 'background': 'false'})
#	return kodi_utils.execute_builtin('RunPlugin(%s)' % build_url(url_params))
	Sources().playback_prep(url_params)

