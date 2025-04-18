import json
from indexers import metadata
from modules import kodi_utils, source_utils, settings
from modules.cache_utils import clear_cache
from modules.utils import get_datetime, clean_file_name
# logger = kodi_utils.logger

ls, build_url, translate_path, select_dialog = kodi_utils.local_string, kodi_utils.build_url, kodi_utils.translate_path, kodi_utils.select_dialog
show_busy_dialog, hide_busy_dialog, notification, ok_dialog = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.notification, kodi_utils.ok_dialog
get_property, set_property, clear_property, container_refresh = kodi_utils.get_property, kodi_utils.set_property, kodi_utils.clear_property, kodi_utils.container_refresh
execute_builtin, confirm_dialog, container_content, sleep = kodi_utils.execute_builtin, kodi_utils.confirm_dialog, kodi_utils.container_content, kodi_utils.sleep
get_setting, set_setting = kodi_utils.get_setting, kodi_utils.set_setting

def trailer_choice(media_type, poster, tmdb_id, trailer_url, all_trailers=[]):
	if settings.get_language() != 'en' and not trailer_url and not all_trailers:
		from apis.tmdb_api import tmdb_media_videos
		try: all_trailers = tmdb_media_videos(media_type, tmdb_id)['results']
		except: pass
	if all_trailers:
		if len(all_trailers) > 1:
			all_trailers.sort(key=lambda k: k.get('published_at'))
			list_items = [
				{'line1': clean_file_name(i['name']), 'line2': '%s (%s)' % (i['type'], i.get('site') or 'NA'), 'icon': poster}
				for i in all_trailers
			]
			kwargs = {'items': json.dumps(list_items), 'heading': ls(32606), 'multi_line': 'true'}
			video_id = select_dialog([i['key'] for i in all_trailers], **kwargs)
		else: video_id = next(iter(all_trailers), {}).get('key')
		if video_id is None: return 'canceled'
		trailer_url = 'plugin://plugin.video.youtube/play/?video_id=%s' % video_id
	return trailer_url

def genres_choice(media_type, genres, poster, return_genres=False):
	from modules.meta_lists import movie_genres, tvshow_genres
	def _process_dicts(genre_str, _dict):
		final_genres_list = []
		append = final_genres_list.append
		for key, value in _dict.items():
			if key in genre_str: append({'genre': key, 'value': value})
		return final_genres_list
	if media_type in ('movie', 'movies'): genre_action, meta_type, action = movie_genres, 'movie', 'tmdb_movies_genres'
	else: genre_action, meta_type, action = tvshow_genres, 'tvshow', 'tmdb_tv_genres'
	genre_list = _process_dicts(genres, genre_action)
	if return_genres: return genre_list
	if len(genre_list) == 0:
		notification(32760, 1500)
		return None
	mode = 'build_%s_list' % meta_type
	list_items = [{'line1': i['genre'], 'icon': poster} for i in genre_list]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32470)}
	return select_dialog([{'mode': mode, 'action': action, 'genre_id': i['value'][0]} for i in genre_list], **kwargs)

def imdb_keywords_choice(media_type, imdb_id, poster):
	from apis.imdb_api import imdb_keywords
	from indexers.history import add_to_search_history
	show_busy_dialog()
	keywords_info = imdb_keywords(imdb_id)
	if len(keywords_info) == 0:
		hide_busy_dialog()
		notification(32760, 1500)
		return None
	meta_type = 'movie' if media_type == 'movies' else 'tvshow'
	mode = 'build_%s_list' % meta_type
	list_items = [{'line1': i, 'icon': poster, 'list_id': i, 'media_type': media_type} for i in keywords_info]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32092)}
	hide_busy_dialog()
	keyword_choice = select_dialog([{'mode': mode, 'action': 'imdb_keywords_list_contents', 'list_id': i, 'media_type': media_type} for i in keywords_info], **kwargs)
	if keyword_choice: add_to_search_history(keyword_choice['list_id'], 'imdb_keyword_%s_queries' % meta_type)
	return keyword_choice

def imdb_videos_choice(videos, poster):
	try: videos = json.loads(videos)
	except: pass
	videos.sort(key=lambda x: x['quality_rank'])
	list_items = [{'line1': i['quality'], 'icon': poster} for i in videos]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32241)}
	return select_dialog([i['url'] for i in videos], **kwargs)

def random_choice(choice, meta):
	tmdb_id = meta.get('tmdb_id')
	if not tmdb_id: return
	from modules.episode_tools import play_random
	play_random(tmdb_id, True if choice == 'play_random_continual' else False)

def trakt_manager_choice(params):
	if not get_setting('trakt_user', ''): return notification(32760, 3500)
	icon = translate_path('special://home/addons/plugin.video.pov/resources/media/trakt.png')
	choices = [('[B][I]%s [/I][/B]' % ls(32499), 'Collection'), ('[B][I]%s [/I][/B]' % ls(32500), 'Watchlist')]
	choices += [('%s %s...' % (ls(32602), ls(32199)), 'Add'), ('%s %s...' % (ls(32603), ls(32199)), 'Remove')]
	choices += [('%s %s...' % ('Toggle', 'Dropped'), 'Drop')] if params['media_type'] == 'tvshow' else []
	list_items = [{'line1': item[0], 'icon': icon} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32198).replace('[B]', '').replace('[/B]', '')}
	choice = select_dialog([i[1] for i in choices], **kwargs)
	if choice is None: return
	from apis import trakt_api
	add_str, rem_str = 'Add to %s?' % choice, 'Remove from %s?' % choice
	if   choice == 'Collection':
		data = trakt_api.trakt_fetch_collection_watchlist('collection', params['media_type'])
		action = 'remove' if params['tmdb_id'] in {str(i['media_ids']['tmdb']) for i in data} else 'add'
		data = {
			i[0]: i[1] if i[0] == 'imdb' else int(i[1])
			for i in (('imdb', params.get('imdb_id')), ('tmdb', params.get('tmdb_id')), ('tvdb', params.get('tvdb_id')))
			if not i[1] in ('', 'None', None)
		}
		data = {'shows' if params['media_type'] == 'tvshow' else 'movies': [{'ids': data}]}
		if action == 'remove':
			if not kodi_utils.confirm_dialog(text=rem_str, top_space=True): return
			trakt_api.remove_from_collection(data)
		else: trakt_api.add_to_collection(data)
	elif choice == 'Watchlist':
		data = trakt_api.trakt_fetch_collection_watchlist('watchlist', params['media_type'])
		action = 'remove' if params['tmdb_id'] in {str(i['media_ids']['tmdb']) for i in data} else 'add'
		data = {
			i[0]: i[1] if i[0] == 'imdb' else int(i[1])
			for i in (('imdb', params.get('imdb_id')), ('tmdb', params.get('tmdb_id')), ('tvdb', params.get('tvdb_id')))
			if not i[1] in ('', 'None', None)
		}
		data = {'shows' if params['media_type'] == 'tvshow' else 'movies': [{'ids': data}]}
		if action == 'remove':
			if not kodi_utils.confirm_dialog(text=rem_str, top_space=True): return
			trakt_api.remove_from_watchlist(data)
		else: trakt_api.add_to_watchlist(data)
	elif choice == 'Add': trakt_api.trakt_add_to_list(params)
	elif choice == 'Remove': trakt_api.trakt_remove_from_list(params)
	else: trakt_api.hide_unhide_trakt_items(params['tmdb_id'], 'shows', params['imdb_id'], 'dropped')

def tmdb_manager_choice(params):
	if not get_setting('tmdb.token', ''): return notification(32760, 3500)
	from apis import tmdb_api
	image_resolution = settings.get_resolution()
	heading = ls(tmdb_api.list_heading).replace('[B]', '').replace('[/B]', '')
	icon = translate_path('special://home/addons/plugin.video.pov/resources/media/tmdb.png')
	list_name = params.get('trakt_list_name') or params.get('mdbl_list_name') or ''
	choices = []
	choices += [
		(str(item['id']), item['name'], '%s items' % item['number_of_items'],
		tmdb_api.tmdb_image_base % (image_resolution['poster'], item['poster_path']) if item['poster_path'] else icon)
		for item in tmdb_api.user_lists_all()
	]
	if not list_name:
		infolabel = kodi_utils.get_infolabel('Container.FolderPath')
		watch_media_type = 'TV Show' if params['media_type'] == 'tvshow' else 'Movie'
		choices += [
			('watchlist_rem', 'Remove from Watchlist', watch_media_type, icon)
			if 'tmdb_watchlist' in infolabel else
			('watchlist_add', 'Add to Watchlist', watch_media_type, icon),
			('favorite_rem', 'Remove from Favorite', watch_media_type, icon)
			if 'tmdb_favorite' in infolabel else
			('favorite_add', 'Add to Favorite', watch_media_type, icon)
		]
	choices += [('new', 'Create a new list', list_name, icon), ('clear', 'Clear list cache', '', icon)]
	if not choices: return
	list_items = [{'line1': item[1], 'line2': item[2], 'icon': item[3]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_line': 'true'}
	choice = select_dialog([(i[0], i[1]) for i in choices], **kwargs)
	if choice is None: return
	if 'new' in choice[0]:
		obj = tmdb_api.list_obj.copy()
		obj['name'] = kodi_utils.dialog.input('New List Name', defaultt=list_name)
		if not obj['name']: return tmdb_manager_choice(params)
		if not tmdb_api.list_create(obj)['success']: return notification(32574)
		tmdb_api.clear_tmdbl_cache()
		return tmdb_manager_choice(params)
	if 'clear' in choice[0]:
		tmdb_api.clear_tmdbl_cache()
		return tmdb_manager_choice(params)
	if 'trakt_list_id' in params or 'mdbl_list_id' in params:
		function = tmdb_api.import_trakt_list if 'trakt_list_id' in params else tmdb_api.import_mdbl_list
		return function({**params, 'list_id': choice[0]})
	if 'watchlist' in choice[0] or 'favorite' in choice[0]:
		action = False if choice[0] in ('watchlist_rem', 'favorite_rem') else True
		list_type = 'favorite' if 'favorite' in choice[0] else 'watchlist'
		params['media_type'] = 'tv' if params['media_type'] == 'tvshow' else 'movie'
		item = {'media_type': params['media_type'], 'media_id': params['tmdb_id'], list_type: action}
		if tmdb_api.add_to_watchlist_favorite(item, list_type)['success']:
			tmdb_api.clear_tmdbl_cache()
			if not action: container_refresh()
			return notification(32576)
		else: return notification(32574)
	add_str, rem_str = 'Add to %s?' % choice[1], 'Remove from %s?' % choice[1]
	params['media_type'] = 'tv' if params['media_type'] == 'tvshow' else 'movie'
	items = {'items': [{'media_type': params['media_type'], 'media_id': params['tmdb_id']}]}
	status = tmdb_api.list_status(choice[0], params['media_type'], params['tmdb_id'])
	if status and status['success']:
		if not confirm_dialog(text=rem_str, top_space=True): return
		action, function = 'remove', tmdb_api.list_remove_items
	else: action, function = 'add', tmdb_api.list_add_items
	if function(choice[0], items)['success']:
		tmdb_api.clear_tmdbl_cache()
		if action == 'remove': container_refresh()
		notification(32576)
	else: notification(32574)

def mdb_manager_choice(params):
	if not get_setting('mdblist.token', ''): return notification(32760, 3500)
	from apis.mdblist_api import mdb_userlists, mdb_list_items, mdb_modify_list, watchlist_obj, clear_mdbl_cache
	heading = ls(32200).replace('[B]', '').replace('[/B]', '')
	icon = translate_path('special://home/addons/plugin.video.pov/resources/media/mdblist.png')
	choices = [(str(item['id']), item['name'], '%s items' % item['items']) for item in mdb_userlists() if not item['dynamic']]
	choices += [(str(watchlist_obj['id']), watchlist_obj['name'], ''), ('clear', 'Clear list cache', '')]
	if not choices: return
	list_items = [{'line1': item[1], 'line2': item[2],'icon': icon} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_line': 'true'}
	choice = select_dialog([(i[0], i[1]) for i in choices], **kwargs)
	if choice is None: return
	if choice[0] == 'clear':
		clear_mdbl_cache()
		return mdb_manager_choice(params)
	list_items = (True for item in mdb_list_items(choice[0], None) if item['imdb_id'] == params['imdb_id'])
	action, message = ('remove', 'Remove from') if next(list_items, False) else ('add', 'Add to')
	if action == 'remove' and not confirm_dialog(text='%s %s list?' % (message, choice[1]), top_space=True): return
	key = 'shows' if params['media_type'] == 'tvshow' else 'movies'
	val = [{'tmdb': int(params.get('tmdb_id')), 'imdb': params.get('imdb_id')}]
	if mdb_modify_list(choice[0], {key: val}, action):
		clear_mdbl_cache()
		notification(32576)
		if action == 'remove': container_refresh()
	else: notification(32574)

def playback_choice(content, poster, meta):
	items = [{'line': ls(32014), 'function': 'clear_and_rescrape'},
			 {'line': ls(32006), 'function': 'rescrape_with_disabled'},
			 {'line': ls(32807), 'function': 'scrape_with_filters_ignored'},
			 {'line': ls(32135), 'function': 'scrape_with_custom_values'}]
	list_items = [{'line1': i['line'], 'icon': poster} for i in items]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32174)}
	choice = select_dialog([i['function'] for i in items], **kwargs)
	if choice is None: return
	if choice == 'clear_and_rescrape': clear_and_rescrape(content, meta)
	elif choice == 'rescrape_with_disabled': rescrape_with_disabled(content, meta)
	elif choice == 'scrape_with_filters_ignored': scrape_with_filters_ignored(content, meta)
	else: scrape_with_custom_values(content, meta)

def set_quality_choice(quality_setting):
	include = ls(32188)
	dl = ['%s SD' % include, '%s 720p' % include, '%s 1080p' % include, '%s 4K' % include]
	fl = ['SD', '720p', '1080p', '4K']
	try: preselect = [fl.index(i) for i in get_setting(quality_setting).split(', ')]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	choice = select_dialog(fl, **kwargs)
	if choice is None: return
	if choice == []:
		ok_dialog(text=32574, top_space=True)
		return set_quality_choice(quality_setting)
	set_setting(quality_setting, ', '.join(choice))

def extras_lists_choice():
	fl = [2050, 2051, 2052, 2053, 2054, 2055, 2056, 2057, 2058, 2059, 2060, 2061, 2062]
	dl = [ls(32664), ls(32503), ls(32607), ls(32984), ls(32986), ls(32989), ls(33032), ls(32616), ls(32617),
			'%s %s' % (ls(32612), ls(32543)), '%s %s' % (ls(32612), ls(32470)), '%s %s' % (ls(32612), ls(32480)), '%s %s' % (ls(32612), ls(32499))]
	try: preselect = [fl.index(i) for i in settings.extras_enabled_menus()]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	selection = select_dialog(fl, **kwargs)
	if selection == []: return set_setting('extras.enabled_menus', 'noop')
	elif selection is None: return
	selection = [str(i) for i in selection]
	set_setting('extras.enabled_menus', ','.join(selection))

def set_language_filter_choice(filter_setting):
	from modules.meta_lists import language_choices
	lang_choices = language_choices
	lang_choices.pop('None')
	dl = list(lang_choices.keys())
	fl = list(lang_choices.values())
	try: preselect = [fl.index(i) for i in get_setting(filter_setting).split(', ')]
	except: preselect = []
	list_items = [{'line1': item} for item in dl]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	choice = select_dialog(fl, **kwargs)
	if choice is None: return
	if choice == []: return set_setting(filter_setting, 'eng')
	set_setting(filter_setting, ', '.join(choice))

def enable_scrapers_choice():
	scrapers = ['external', 'easynews', 'rd_cloud', 'pm_cloud', 'ad_cloud', 'oc_cloud', 'folders']
	cloud_scrapers = {'rd_cloud': 'rd.enabled', 'pm_cloud': 'pm.enabled', 'ad_cloud': 'ad.enabled', 'oc_cloud': 'oc.enabled'}
	scraper_names = [ls(32118).upper(), ls(32069).upper(), ls(32070).upper(), ls(32098).upper(), ls(32097).upper(), ls(32099).upper(), ls(32108).upper()]
	preselect = [scrapers.index(i) for i in settings.active_internal_scrapers()]
	list_items = [{'line1': item} for item in scraper_names]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false', 'preselect': preselect}
	choice = select_dialog(scrapers, **kwargs)
	if choice is None: return
	for i in scrapers:
		set_setting('provider.%s' % i, ('true' if i in choice else 'false'))
		if i in cloud_scrapers and i in choice: set_setting(cloud_scrapers[i], 'true')

def folder_scraper_manager_choice(folder_info=None):
	def _get_property(setting_id):
		return get_property('pov_%s' % setting_id) or get_setting(setting_id)
	def _set_property(setting_id, setting_value):
		set_property('pov_%s' % setting_id, setting_value)
	def _clear_property(setting_id):
		clear_property(setting_id)
	def _exit_save_settings():
		for folder_no in range(1,6):
			set_setting(name_setting % folder_no,  _get_property(name_setting % folder_no))
			set_setting(movie_dir_setting % folder_no,  _get_property(movie_dir_setting % folder_no))
			set_setting(tvshow_dir_setting % folder_no,  _get_property(tvshow_dir_setting % folder_no))
			_clear_property('pov_%s' % name_setting % folder_no)
			_clear_property('pov_%s' % movie_dir_setting % folder_no)
			_clear_property('pov_%s' % tvshow_dir_setting % folder_no)
	def _return(passed_folder_info):
		return folder_scraper_manager_choice(passed_folder_info)
	def _make_folders():
		return [
			{'number': folder_no, 'name': folder_names[folder_no], 'display_setting': name_setting % folder_no,
			'movie_setting': movie_dir_setting % folder_no, 'tvshow_setting': tvshow_dir_setting % folder_no, 'display': _get_property(name_setting % folder_no),
			'movie_dir': _get_property(movie_dir_setting % folder_no), 'tvshow_dir': _get_property(tvshow_dir_setting % folder_no)}
			for folder_no in range(1,6)
		]
	def _update_folder_info():
		folder_info.update({'display': _get_property(name_setting % folder_info['number']), 'movie_dir': _get_property(movie_dir_setting % folder_info['number']),
							'tvshow_dir': _get_property(tvshow_dir_setting % folder_info['number'])})
	def _make_listing():
		return [('[B]%s[/B]:  [I]%s[/I]' % (folder_name_str, folder_info['display']), folder_info['display_setting']),
				('[B]%s[/B]:  [I]%s[/I]' % (movie_dir_str, folder_info['movie_dir']), folder_info['movie_setting']),
				('[B]%s[/B]:  [I]%s[/I]' % (tv_dir_str, folder_info['tvshow_dir']), folder_info['tvshow_setting'])]
	def _process_setting():
		if setting is None: _return(None)
		if 'display_name' in setting: _set_display()
		else: _set_folder_path()
	def _set_display():
		default = folder_info['display']
		folder_title = dialog.input(folder_name_str, defaultt=default)
		if not folder_title: folder_title = 'None'
		_set_property(folder_info['display_setting'], folder_title)
		_return(folder_info)
	def _set_folder_path():
		if _get_property(setting) not in ('', 'None'):
			list_items = [{'line1': item} for item in [ls(32682), ls(32683)]]
			kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
			action = select_dialog([1, 2], **kwargs)
			if action is None: _return(folder_info)
			if action == 1:
				_set_property(setting, 'None')
				_return(folder_info)
			else:
				folder = dialog.browse(0, 'POV', '')
				if not folder: folder = 'None'
				_set_property(setting, folder)
				_return(folder_info)
		else:
			folder = dialog.browse(0, 'POV', '')
			if not folder: folder = 'None'
			_set_property(setting, folder)
			_return(folder_info)
	try:
		dialog = kodi_utils.dialog
		choose_folder_str, folder_name_str, movie_dir_str, tv_dir_str = ls(32109), ls(32115), ls(32116), ls(32117)
		name_setting, movie_dir_setting, tvshow_dir_setting = 'folder%d.display_name', 'folder%d.movies_directory', 'folder%d.tv_shows_directory'
		folder_names = {1: ls(32110), 2: ls(32111), 3: ls(32112), 4: ls(32113), 5: ls(32114)}
		if not folder_info:
			folders = _make_folders()
			list_items = [{'line1': '%s:  [I]%s[/I]' % (item['name'], item['display'])} for item in folders]
			kwargs = {'items': json.dumps(list_items), 'heading': choose_folder_str, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
			folder_info = select_dialog(folders, **kwargs)
			if folder_info is None: return _exit_save_settings()
		else: _update_folder_info()
		listing = _make_listing()
		list_items = [{'line1': item[0]} for item in listing]
		kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		setting = select_dialog([i[1] for i in listing], **kwargs)
		_process_setting()
	except Exception as e:
		return

def results_sorting_choice():
	quality, provider, size = ls(32241), ls(32583), ls(32584)
	choices = [('%s, %s, %s' % (quality, provider, size), '0'), ('%s, %s, %s' % (quality, size, provider), '1'), ('%s, %s, %s' % (provider, quality, size), '2'),
			   ('%s, %s, %s' % (provider, size, quality), '3'), ('%s, %s, %s' % (size, quality, provider), '4'), ('%s, %s, %s' % (size, provider, quality), '5')]
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = select_dialog(choices, **kwargs)
	if choice:
		set_setting('results.sort_order_display', choice[0])
		set_setting('results.sort_order', choice[1])

def results_highlights_choice():
	choices = ((ls(32240), '0'), (ls(32583), '1'), (ls(32241), '2'))
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = select_dialog([i[1] for i in choices], **kwargs)
	if choice: return set_setting('highlight.type', choice)

def results_layout_choice():
	xml_choices = [
		'List Default', 'List Contrast Default',
		'InfoList Default', 'InfoList Contrast Default',
		'WideList Default', 'WideList Contrast Default'
	]
	list_items = [{'line1': item} for item in xml_choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = select_dialog(xml_choices, **kwargs)
	if choice in xml_choices: set_setting('results.xml_style', choice)

def set_subtitle_choice():
	choices = ((ls(32192), '0'), (ls(32193), '1'), (ls(32027), '2'))
	list_items = [{'line1': item[0]} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = select_dialog([i[1] for i in choices], **kwargs)
	if choice: return set_setting('subtitles.subs_action', choice)

def scraper_dialog_color_choice(setting):
	setting ='int_dialog_highlight' if setting == 'internal' else 'ext_dialog_highlight'
	chosen_color = color_choice()
	if chosen_color: set_setting(setting, chosen_color)

def scraper_quality_color_choice(setting):
	chosen_color = color_choice()
	if chosen_color: set_setting(setting, chosen_color)

def scraper_color_choice(setting):
	choices = [
		('easynews', 'provider.easynews_colour'),
		('debrid_cloud', 'provider.debrid_cloud_colour'),
		('folders', 'provider.folders_colour'),
		('hoster', 'hoster.identify'),
		('torrent', 'torrent.identify'),
		('rd', 'provider.rd_colour'),
		('pm', 'provider.pm_colour'),
		('ad', 'provider.ad_colour'),
		('oc', 'provider.oc_colour'),
		('tb', 'provider.tb_colour'),
		('ed', 'provider.ed_colour'),
		('free', 'provider.free_colour')
	]
	setting = [i[1] for i in choices if i[0] == setting][0]
	chosen_color = color_choice()
	if chosen_color: set_setting(setting, chosen_color)

def color_choice(msg_dialog='POV', no_color=False):
	from modules.meta_lists import meta_colors
	color_chart = meta_colors
	color_display = ['[COLOR %s]%s[/COLOR]' % (i, i.capitalize()) for i in color_chart]
	if no_color:
		color_chart.insert(0, 'No Color')
		color_display.insert(0, 'No Color')
	list_items = [{'line1': item} for item in color_display]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	choice = select_dialog(color_chart, **kwargs)
	if choice is None: return
	return choice

def meta_language_choice():
	from modules.meta_lists import meta_languages
	langs = meta_languages
	list_items = [{'line1': i['name']} for i in langs]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32145), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	list_choose = select_dialog(langs, **kwargs)
	if list_choose is None: return None
	chosen_language, chosen_language_display = list_choose['iso'], list_choose['name']
	set_setting('meta_language', chosen_language)
	set_setting('meta_language_display', chosen_language_display)
	clear_cache('meta', silent=True)

def favourites_choice(params):
	icon = translate_path('special://home/addons/plugin.video.pov/resources/media/favourites.png')
	if params.get('cache'):
		from caches.favourites_cache import favourites_cache
		list = [('%s %s' % (ls(32028), ls(32453)), 'movie'), ('%s %s' % (ls(32029), ls(32453)), 'tvshow')]
		list_items = [{'line1': item[0], 'icon': icon} for item in list]
		kwargs = {'items': json.dumps(list_items), 'heading': ls(32453), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		media_type = select_dialog([item[1] for item in list], **kwargs)
		if media_type is None: return
		if not favourites_cache.clear_favourites(media_type): notification(32574)
	else:
		from caches.favourites_cache import favourites_cache
		media_type, tmdb_id, title = params['media_type'], params['tmdb_id'], params['title']
		current_favourites = favourites_cache.get_favourites(media_type)
		if any(i['tmdb_id'] == tmdb_id for i in current_favourites): action, text = favourites_cache.remove_from_favourites, '%s POV %s?' % (ls(32603), ls(32453))
		else: action, text = favourites_cache.add_to_favourites, '%s POV %s?' % (ls(32602), ls(32453))
		if not confirm_dialog(text='%s[CR][CR]%s' % (title, text)): return
		if action(media_type, tmdb_id, title): notification(32576)
		else: notification(32574)

def external_scrapers_choice():
#	icon = translate_path('special://home/addons/script.module.fenomscrapers/icon.png')
	icon = translate_path('special://home/addons/plugin.video.pov/resources/lib/fenom/media/icon.png')
	all_color, hosters_color, torrent_color = 'mediumvioletred', get_setting('hoster.identify'), get_setting('torrent.identify')
	enable_string, disable_string, specific_string, all_string = ls(32055), ls(32024), ls(32536), ls(32525)
	scrapers_string, hosters_string, torrent_string = ls(32533), ls(33031), ls(32535)
	fs_default_string = ls(32137)
	all_scrapers_string = '%s %s' % (all_string, scrapers_string)
	hosters_scrapers_string = '%s %s' % (hosters_string, scrapers_string)
	torrent_scrapers_string = '%s %s' % (torrent_string, scrapers_string)
	enable_string_base = '%s %s %s %s' % (enable_string, all_string, '%s', scrapers_string)
	disable_string_base = '%s %s %s %s' % (disable_string, all_string, '%s', scrapers_string)
	enable_disable_string_base = '%s/%s %s %s %s' % (enable_string, disable_string, specific_string, '%s', scrapers_string)
	all_scrapers_base = '[COLOR %s]%s [/COLOR]' % (all_color, all_scrapers_string.upper())
	debrid_scrapers_base = '[COLOR %s]%s [/COLOR]' % (hosters_color, hosters_scrapers_string.upper())
	torrent_scrapers_base = '[COLOR %s]%s [/COLOR]' % (torrent_color, torrent_scrapers_string.upper())
	tools_menu = [
		(all_scrapers_base, fs_default_string, {'mode': 'set_default_scrapers'}),
		(all_scrapers_base, enable_string_base % '', {'mode': 'toggle_all', 'folder': 'all', 'setting': 'true'}),
		(all_scrapers_base, disable_string_base % '', {'mode': 'toggle_all', 'folder': 'all', 'setting': 'false'}),
		(all_scrapers_base, enable_disable_string_base % '', {'mode': 'enable_disable', 'folder': 'all'}),
		(debrid_scrapers_base, enable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'true'}),
		(debrid_scrapers_base, disable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'false'}),
		(debrid_scrapers_base, enable_disable_string_base % hosters_string, {'mode': 'enable_disable', 'folder': 'hosters'}),
		(torrent_scrapers_base, enable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'true'}),
		(torrent_scrapers_base, disable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'false'}),
		(torrent_scrapers_base, enable_disable_string_base % torrent_string, {'mode': 'enable_disable', 'folder': 'torrents'})
	]
	list_items = [{'line1': item[0], 'line2': item[1], 'icon': icon} for item in tools_menu]
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'true'}
	chosen_tool = select_dialog(tools_menu, **kwargs)
	if chosen_tool is None: return
	params = chosen_tool[2]
	mode = params['mode']
	if mode == 'toggle_all': source_utils.toggle_all(params['folder'], params['setting'])
	elif mode == 'enable_disable': source_utils.enable_disable(params['folder'])
	elif mode == 'set_default_scrapers': source_utils.set_default_scrapers()
	return external_scrapers_choice()

def options_menu(params, meta=None):
	def _builder():
		for item in listing:
			kwargs = {'line1': item[1], 'line2': item[2] or item[1]}
			if len(item) == 4: kwargs['icon'] = item[3]
			yield kwargs
	is_widget = params.get('is_widget', 'false').lower() == 'true'
	content = params.get('content', None) or container_content()[:-1]
	season, episode = params.get('season', None), params.get('episode', None)
	if not meta:
		function = metadata.movie_meta if content == 'movie' else metadata.tvshow_meta
		meta = function('tmdb_id', params['tmdb_id'], settings.metadata_user_info(), get_datetime())
	watched_indicators = settings.watched_indicators()
	on_str, off_str, currently_str, open_str, settings_str = ls(32090), ls(32027), ls(32598), ls(32641), ls(32247)
	results_xml_style_status = get_setting('results.xml_style', 'Default')
	active_internal_scrapers = [i.replace('_', '') for i in settings.active_internal_scrapers()]
	uncached_torrents_status, uncached_torrents_toggle = (on_str, 'false') if settings.display_uncached_torrents() else (off_str, 'true')
	base_str1, base_str2 = '%s%s', '%s: [B]%s[/B]' % (currently_str, '%s')
	scraper_options_str = '%s %s' % (ls(32533), ls(32841))
	multi_line = 'true' if content in ('movie', 'episode') else 'false'
	listing = (
		('clear_and_rescrape', ls(32014), scraper_options_str, meta['poster']) if multi_line == 'true' else None,
		('rescrape_with_disabled', ls(32006), scraper_options_str, meta['poster']) if multi_line == 'true' else None,
		('scrape_with_filters_ignored', ls(32807), scraper_options_str, meta['poster']) if multi_line == 'true' else None,
		('scrape_with_custom_values', ls(32135), scraper_options_str, meta['poster']) if multi_line == 'true' else None,
		('scrape_from_episode_group', 'Scrape From Episode Group', scraper_options_str, meta['poster']) if content == 'episode' else None,
		('play_random', ls(32541), '', meta['poster']) if content in ('tvshow') and meta else None,
		('play_random_continual', ls(32542), '', meta['poster']) if content in ('tvshow') and meta else None,
		('clear_scrapers_cache', ls(32637), '') if content in ('movie', 'episode') else None,
		('open_external_scrapers_choice', '%s %s' % (ls(32118), ls(32513)), ''),
		('torbox_usenet_query', 'TorBox Usenet Search', scraper_options_str, meta['poster']) if content in ('movie', 'tvshow', 'episode') and meta else None,
		('toggle_torrents_display_uncached', base_str1 % ('', ls(32160)), base_str2 % uncached_torrents_status) if multi_line == 'true' and 'external' in active_internal_scrapers else None,
		('set_results_xml_display', base_str1 % ('', '%s %s' % (ls(32139), ls(32140))), base_str2 % results_xml_style_status) if multi_line == 'true' else None,
		('clear_trakt_cache', ls(32497) % ls(32037), '') if watched_indicators == 1 else None,
		('clear_media_cache', ls(32604) % (ls(32028) if meta['mediatype'] == 'movie' else ls(32029)), '', meta['poster']) if content in ('movie', 'tvshow') and meta else None,
		('open_pov_settings', '%s %s %s' % (open_str, ls(32036), settings_str), ''),
		('reload_widgets', ls(40001).replace('[B]', '').replace('[/B]', ''), '') if is_widget else None
	)
	listing = [item for item in listing if item]
	list_items = list(_builder())
	heading = ls(32646).replace('[B]', '').replace('[/B]', '')
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': multi_line}
	choice = select_dialog([i[0] for i in listing], **kwargs)
	if   choice in (None, 'save_and_exit'): return
	elif choice == 'clear_and_rescrape': return clear_and_rescrape(content, meta, season, episode)
	elif choice == 'rescrape_with_disabled': return rescrape_with_disabled(content, meta, season, episode)
	elif choice == 'scrape_with_filters_ignored': return scrape_with_filters_ignored(content, meta, season, episode)
	elif choice == 'scrape_with_custom_values': return scrape_with_custom_values(content, meta, season, episode)
	elif choice == 'scrape_from_episode_group': return scrape_from_episode_group(meta, season, episode)
	elif choice == 'play_random': return random_choice(choice, meta)
	elif choice == 'play_random_continual': return random_choice(choice, meta)
	elif choice == 'clear_scrapers_cache': return clear_scrapers_cache()
	elif choice == 'open_external_scrapers_choice': return source_utils.enable_disable('all')
	elif choice == 'torbox_usenet_query': return torbox_usenet_query(meta, season, episode)
	elif choice == 'toggle_torrents_display_uncached': set_setting('torrent.display.uncached', uncached_torrents_toggle)
	elif choice == 'set_results_xml_display': results_layout_choice()
	elif choice == 'clear_trakt_cache': return clear_cache('trakt')
	elif choice == 'clear_media_cache': return refresh_cached_meta(meta)
	elif choice == 'open_pov_settings': return kodi_utils.open_settings('0.0')
#	elif choice == 'reload_widgets': return kodi_utils.widget_refresh()
	elif choice == 'reload_widgets': return execute_builtin('ReloadSkin()')
	if   choice == 'clear_trakt_cache' and content in ('movie', 'tvshow', 'season', 'episode'): container_refresh()
	show_busy_dialog()
	sleep(200)
	hide_busy_dialog()
	options_menu(params, meta=meta)

def extras_menu(params):
	from windows import open_window
	function = metadata.movie_meta if params['media_type'] == 'movie' else metadata.tvshow_meta
	meta = function('tmdb_id', params['tmdb_id'], settings.metadata_user_info(), get_datetime())
	open_window(('windows.extras', 'Extras'), 'extras.xml', meta=meta, is_widget=params.get('is_widget', 'false'), is_home=params.get('is_home', 'false'))

def media_extra_info(media_type, meta):
	extra_info = meta.get('extra_info', None)
	body = []
	append = body.append
	tagline_str, premiered_str, rating_str, votes_str, runtime_str = ls(32619), ls(32620), ls(32621), ls(32623), ls(32622)
	genres_str, budget_str, revenue_str, director_str, writer_str = ls(32624), ls(32625), ls(32626), ls(32627), ls(32628)
	studio_str, collection_str, homepage_str, status_str, type_str, classification_str = ls(32615), ls(32499), ls(32629), ls(32630), ls(32631), ls(32632)
	network_str, created_by_str, last_aired_str, next_aired_str, seasons_str, episodes_str = ls(32480), ls(32633), ls(32634), ls(32635), ls(32636), ls(32506)
	try:
		if media_type == 'movie':
			def _process_budget_revenue(info):
				if isinstance(info, int): info = '${:,}'.format(info)
				return info
			if 'tagline' in meta and meta['tagline']: append('[B]%s:[/B] %s' % (tagline_str, meta['tagline']))
			if 'alternative_titles' in meta and meta['alternative_titles']: append('[B]%s:[/B] %s' % ('Aliases', ', '.join(meta['alternative_titles'])))
			if 'status' in extra_info: append('[B]%s:[/B] %s' % (status_str, extra_info['status']))
			append('[B]%s:[/B] %s' % (premiered_str, meta['premiered']))
			append('[B]%s:[/B] %s (%s %s)' % (rating_str, meta['rating'], meta['votes'], votes_str))
			append('[B]%s:[/B] %d mins' % (runtime_str, int(float(meta['duration'])/60)))
			append('[B]%s:[/B] %s' % (genres_str, meta['genre']))
			if 'budget' in extra_info: append('[B]%s:[/B] %s' % (budget_str, _process_budget_revenue(extra_info['budget'])))
			if 'revenue' in extra_info: append('[B]%s:[/B] %s' % (revenue_str, _process_budget_revenue(extra_info['revenue'])))
			append('[B]%s:[/B] %s' % (director_str, meta['director']))
			append('[B]%s:[/B] %s' % (writer_str, meta['writer'] or 'N/A'))
			append('[B]%s:[/B] %s' % (studio_str, meta['studio'] or 'N/A'))
			if extra_info.get('collection_name'): append('[B]%s:[/B] %s' % (collection_str, extra_info['collection_name']))
			if extra_info.get('homepage'): append('[B]%s:[/B] %s' % (homepage_str, extra_info['homepage']))
		else:
			if 'type' in extra_info: append('[B]%s:[/B] %s' % (type_str, extra_info['type']))
			if 'alternative_titles' in meta and meta['alternative_titles']: append('[B]%s:[/B] %s' % ('Aliases', ', '.join(meta['alternative_titles'])))
			if 'status' in extra_info: append('[B]%s:[/B] %s' % (status_str, extra_info['status']))
			append('[B]%s:[/B] %s' % (premiered_str, meta['premiered']))
			append('[B]%s:[/B] %s (%s %s)' % (rating_str, meta['rating'], meta['votes'], votes_str))
			append('[B]%s:[/B] %d mins' % (runtime_str, int(float(meta['duration'])/60)))
			append('[B]%s:[/B] %s' % (classification_str, meta['mpaa']))
			append('[B]%s:[/B] %s' % (genres_str, meta['genre']))
			append('[B]%s:[/B] %s' % (network_str, meta['studio']))
			if 'created_by' in extra_info: append('[B]%s:[/B] %s' % (created_by_str, extra_info['created_by']))
			if extra_info.get('last_episode_to_air', False):
				last_ep = extra_info['last_episode_to_air']
				lastep_str = '[%s] S%.2dE%.2d - %s' % (last_ep['air_date'], last_ep['season_number'], last_ep['episode_number'], last_ep['name'])
				append('[B]%s:[/B] %s' % (last_aired_str, lastep_str))
			if extra_info.get('next_episode_to_air', False):
				next_ep = extra_info['next_episode_to_air']
				nextep_str = '[%s] S%.2dE%.2d - %s' % (next_ep['air_date'], next_ep['season_number'], next_ep['episode_number'], next_ep['name'])
				append('[B]%s:[/B] %s' % (next_aired_str, nextep_str))
			append('[B]%s:[/B] %s' % (seasons_str, meta['total_seasons']))
			append('[B]%s:[/B] %s' % (episodes_str, meta['total_aired_eps']))
			if 'homepage' in extra_info: append('[B]%s:[/B] %s' % (homepage_str, extra_info['homepage']))
	except: return notification(32574)
	return '\n\n'.join(body)

def refresh_cached_meta(meta):
	from caches.meta_cache import MetaCache
	try:
		media_type, tmdb_id = meta['mediatype'], meta['tmdb_id']
		MetaCache().delete(media_type, 'tmdb_id', tmdb_id, meta)
		if media_type == 'tvshow': MetaCache().delete_all_seasons_memory_cache(tmdb_id)
		notification(32576, 1500)
		container_refresh()
	except: notification(32574)

def build_navigate_to_page(params):
	use_alphabet = settings.nav_jump_use_alphabet() == 2
	icon = translate_path('special://home/addons/plugin.video.pov/resources/media/item_jump.png')
	fanart = translate_path('special://home/addons/plugin.video.pov/fanart.png')
	media_type = params.get('media_type')
	def _builder(use_alphabet):
		for i in start_list:
			if use_alphabet: line1, line2 = i.upper(), ls(32821) % (media_type, i.upper())
			else: line1, line2 = '%s %s' % (ls(32022), i), ls(32822) % i
			yield {'line1': line1, 'line2': line2, 'icon': icon}
	if use_alphabet:
		start_list = [chr(i) for i in range(97,123)]
	else:
		start_list = [str(i) for i in range(1, int(params.get('total_pages'))+1)]
		start_list.remove(params.get('current_page'))
	list_items = list(_builder(use_alphabet))
	kwargs = {'items': json.dumps(list_items), 'heading': 'POV', 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
	new_start = select_dialog(start_list, **kwargs)
	sleep(100)
	if new_start is None: return
	if use_alphabet: new_page, new_letter = '', new_start
	else: new_page, new_letter = new_start, None
	url_params = {'mode': params.get('transfer_mode', ''), 'action': params.get('transfer_action', ''), 'new_page': new_page, 'new_letter': new_letter,
				'media_type': params.get('media_type', ''), 'query': params.get('query', ''), 'actor_id': params.get('actor_id', ''),
				'user': params.get('user', ''), 'slug': params.get('slug', ''), 'list_id': params.get('list_id', ''), 'name': params.get('name', '')}
	execute_builtin('Container.Update(%s)' % build_url(url_params))

def clear_scrapers_cache(silent=False):
	for item in ('internal_scrapers', 'external_scrapers'): clear_cache(item, silent=True)
	if not silent: notification(32576)

def clear_and_rescrape(media_type, meta, season=None, episode=None):
	from caches.providers_cache import ExternalProvidersCache
	from modules.sources import Sources
	show_busy_dialog()
	deleted = ExternalProvidersCache().delete_cache_single(media_type, str(meta['tmdb_id']))
	hide_busy_dialog()
	if not deleted: return notification(32574)
	play_params = {'mode': 'play_media', 'tmdb_id': meta['tmdb_id'], 'autoplay': 'False'}
	if media_type == 'movie': play_params.update({'media_type': 'movie'})
	else: play_params.update({'media_type': 'episode', 'season': season, 'episode': episode})
	Sources().playback_prep(play_params)

def rescrape_with_disabled(media_type, meta, season=None, episode=None):
	from modules.sources import Sources
	play_params = {'mode': 'play_media', 'tmdb_id': meta['tmdb_id'], 'disabled_ignored': 'true', 'prescrape': 'false'}
	if media_type == 'movie': play_params.update({'media_type': 'movie'})
	else: play_params.update({'media_type': 'episode', 'season': season, 'episode': episode})
	Sources().playback_prep(play_params)

def scrape_with_filters_ignored(media_type, meta, season=None, episode=None):
	from modules.sources import Sources
	play_params = {'mode': 'play_media', 'tmdb_id': meta['tmdb_id'], 'ignore_scrape_filters': 'true'}
	if media_type == 'movie': play_params.update({'media_type': 'movie'})
	else: play_params.update({'media_type': 'episode', 'season': season, 'episode': episode})
	Sources().playback_prep(play_params)

def scrape_with_custom_values(media_type, meta, season=None, episode=None):
	from windows import open_window
	from modules.sources import Sources
	play_params = {'mode': 'play_media', 'tmdb_id': meta['tmdb_id']}
	if media_type in ('movie', 'movies'): play_params.update({'media_type': 'movie'})
	else: play_params.update({'media_type': 'episode', 'season': season, 'episode': episode})
	custom_title = kodi_utils.dialog.input(ls(32228), defaultt=meta['title'])
	if not custom_title: return
	play_params['custom_title'] = custom_title
	if media_type in ('movie', 'movies'):
		custom_year = kodi_utils.dialog.input('%s (%s)' % (ls(32543), ls(32669)), type=kodi_utils.numeric_input, defaultt=str(meta['year']))
		if custom_year: play_params.update({'custom_year': custom_year})
	else:
		custom_season = kodi_utils.dialog.input('%s (%s)' % (ls(32537).title(), ls(32669)), type=kodi_utils.numeric_input, defaultt=str(season))
		custom_episode = kodi_utils.dialog.input('%s (%s)' % (ls(32203).title(), ls(32669)), type=kodi_utils.numeric_input, defaultt=str(episode))
		if custom_season and custom_episode: play_params.update({'custom_season': custom_season, 'custom_episode': custom_episode})
	kwargs = {'meta': meta, 'enable_buttons': True, 'true_button': ls(32824), 'false_button': ls(32828), 'focus_button': 11}
	choice = open_window(('windows.sources', 'ProgressMedia'), 'progress_media.xml', text='%s?' % ls(32006), **kwargs)
	if choice is None: return
	if choice: play_params['disabled_ignored'] = 'true'
	choice = open_window(('windows.sources', 'ProgressMedia'), 'progress_media.xml', text=ls(32808), **kwargs)
	if choice is None: return
	if choice:
		play_params['ignore_scrape_filters'] = 'true'
		set_property('fs_filterless_search', 'true')
	Sources().playback_prep(play_params)

def scrape_from_episode_group(meta, season=None, episode=None):
	from apis.tmdb_api import episode_groups, episode_group_details
	from modules.sources import Sources
	user_info = settings.metadata_user_info()
	tmdb_id, heading, poster = meta['tmdb_id'], meta['tvshowtitle'], meta['poster']
	groups = episode_groups(tmdb_id, user_info['tmdb_api'])
	choices = [
		(item['id'], '%s (%s)' % (item['name'], item['type']), '%s Groups, %s Episodes' % (item['group_count'], item['episode_count']))
		for item in groups
	]
	if not choices: return notification(32760)
	list_items = [{'line1': item[1], 'line2': item[2], 'icon': poster} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'true', 'multi_line': 'true'}
	choice = select_dialog([i[0] for i in choices], **kwargs)
	if choice is None: return
	episodes_data = metadata.season_episodes_meta(season, meta, user_info)
	orig_ep = next((i for i in episodes_data if i['season'] == int(season) and i['episode'] == int(episode)), {})
	title, premiered = orig_ep.get('title', ''), orig_ep.get('premiered', '')
	episodes = episode_group_details(choice, user_info['tmdb_api'])
	if not episodes: return notification(32760)
	episodes = [
		{**episode, 'custom_episode': episode['order'] + 1, 'custom_season': group['order'],
		'custom_name': f"S{group['order']}xE{episode['order'] + 1:02d} - {episode['name']}",
		'custom_title': f"S{episode['season_number']}xE{episode['episode_number']:02d} - {episode['name']}"}
		for group in episodes for episode in group['episodes']
	]
	title_check = (episodes.index(i) for i in episodes if (title and title.lower() in i['name'].lower()))
	meta_check = (
		episodes.index(i) for i in episodes
		if (premiered and premiered in i['air_date'])
		or (i['season_number'] == int(season) and i['episode_number'] == int(episode))
	)
	index = next(title_check, None) or next(meta_check, None)
	if index is None: preselect = []
	else: episodes, preselect = episodes[index:] + episodes[:index], [0]
	choices = [(item['custom_season'], item['custom_episode'], item['custom_name'], item['custom_title']) for item in episodes]
	if not choices: return
	list_items = [{'line1': item[2], 'line2': item[3], 'icon': poster} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': title, 'multi_line': 'true', 'preselect': preselect}
	choice = select_dialog([(i[0], i[1]) for i in choices], **kwargs)
	if choice is None: return
	play_params = {'mode': 'play_media', 'tmdb_id': tmdb_id, 'media_type': 'episode', 'season': season, 'episode': episode}
	play_params.update({'custom_season': choice[0], 'custom_episode': choice[1]})
	Sources().playback_prep(play_params)

def torbox_usenet_query(meta, season, episode):
	from apis.torbox_api import TorBoxAPI as TorBox
	def _builder():
		for item in files:
			try:
				name = clean_file_name(item['raw_title']).upper()
				age, tracker, size = item['age'], item['tracker'], float(int(item['size']))/1073741824
				if item['owned']: line2 = '%.2f GB | [COLOR cyan][B]CLOUD[/B][/COLOR] | %s | %s'
				elif item['cached']: line2 = '%.2f GB | [COLOR magenta][B]CACHED[/B][/COLOR] | %s | %s'
				else: line2 = '%.2f GB | %s | %s'
				line2 = line2 % (size, age, tracker)
				url_params = {'mode': 'manual_add_nzb_to_cloud', 'provider': 'TorBox', 'url': item['nzb'], 'name': name}
				yield (url_params, name, line2)
			except: pass
	query = meta.get('tvshowtitle') or '%s %s' % (meta['title'], meta['year'])
	show_busy_dialog()
#	files = TorBox().usenet_query(query, season, episode, meta.get('imdb_id', ''))
	files = TorBox().usenet_query(query, season, episode, None)
	uncached = [i for i in files if not i['cached']]
	files = [i for i in files if i['cached']] + uncached
	hide_busy_dialog()
	if not files: return notification(32760)
	choices = list(_builder())
	if not choices: return
	list_items = [{'line1': item[1], 'line2': item[2], 'icon': meta['poster']} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': query, 'enumerate': 'true', 'multi_line': 'true'}
	choice = select_dialog([i[0] for i in choices], **kwargs)
	if choice is None: return
	execute_builtin('RunPlugin(%s)' % build_url(choice))

