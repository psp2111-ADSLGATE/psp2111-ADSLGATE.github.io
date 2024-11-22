import json
from windows import open_window
from indexers import metadata
from modules import kodi_utils, source_utils, settings
from modules.cache_utils import clear_cache
from modules.utils import get_datetime
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
		from modules.utils import clean_file_name
		if len(all_trailers) == 1:
			video_id = all_trailers[0].get('key')
		else:
			list_items = [{'line1': clean_file_name(i['name']), 'icon': poster} for i in all_trailers]
			kwargs = {'items': json.dumps(list_items), 'heading': ls(32606)}
			video_id = select_dialog([i['key'] for i in all_trailers], **kwargs)
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
		notification(32760, 2500)
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
		notification(32760, 2500)
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
	choices = [('%s %s...' % (ls(32602), ls(32199)), 'Add'), ('%s %s...' % (ls(32603), ls(32199)), 'Remove')]
	list_items = [{'line1': item[0], 'icon': icon} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32198).replace('[B]', '').replace('[/B]', '')}
	choice = select_dialog([i[1] for i in choices], **kwargs)
	if choice is None: return
	if choice == 'Add':
		from apis.trakt_api import trakt_add_to_list
		trakt_add_to_list(params)
	else:
		from apis.trakt_api import trakt_remove_from_list
		trakt_remove_from_list(params)

def playback_choice(content, poster, meta):
	items = [{'line': ls(32014), 'function': 'clear_and_rescrape'},
			 {'line': ls(32006), 'function': 'rescrape_with_disabled'},
			 {'line': ls(32807), 'function': 'scrape_with_filters_ignored'},
			 {'line': ls(32135), 'function': 'scrape_with_custom_values'}]
	list_items = [{'line1': i['line'], 'icon': poster} for i in items]
	kwargs = {'items': json.dumps(list_items), 'heading': ls(32174)}
	choice = select_dialog([i['function'] for i in items], **kwargs)
	if choice is None: return
	if choice == 'clear_and_rescrape': source_utils.clear_and_rescrape(content, meta)
	elif choice == 'rescrape_with_disabled': source_utils.rescrape_with_disabled(content, meta)
	elif choice == 'scrape_with_filters_ignored': source_utils.scrape_with_filters_ignored(content, meta)
	else: source_utils.scrape_with_custom_values(content, meta)

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
		'List Default', 'List Contrast Default', # 'List Details', 'List Contrast Details',
		'InfoList Default', 'InfoList Contrast Default', # 'InfoList Details', 'InfoList Contrast Details',
		'Columns Default', 'Columns Contrast Default', # 'Columns Details', 'Columns Contrast Details'
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
#	from modules.cache_utils import clear_cache
	chosen_language, chosen_language_display = list_choose['iso'], list_choose['name']
	set_setting('meta_language', chosen_language)
	set_setting('meta_language_display', chosen_language_display)
	clear_cache('meta', silent=True)

def favorites_choice(params):
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
#		(debrid_scrapers_base, enable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'true'}),
#		(debrid_scrapers_base, disable_string_base % hosters_string, {'mode': 'toggle_all', 'folder': 'hosters', 'setting': 'false'}),
#		(debrid_scrapers_base, enable_disable_string_base % hosters_string, {'mode': 'enable_disable', 'folder': 'hosters'}),
#		(torrent_scrapers_base, enable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'true'}),
#		(torrent_scrapers_base, disable_string_base % torrent_string, {'mode': 'toggle_all', 'folder': 'torrents', 'setting': 'false'}),
#		(torrent_scrapers_base, enable_disable_string_base % torrent_string, {'mode': 'enable_disable', 'folder': 'torrents'})
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
			line1, line2 = item[0], item[1]
			if line2 == '': line2 = line1
			if len(item) == 4: kwargs = {'line1': line1, 'line2': line2, 'icon': item[3]}
			else: kwargs = {'line1': line1, 'line2': line2}
			yield kwargs
	content = params.get('content', None)
	if not content: content = container_content()[:-1]
	season, episode = params.get('season', None), params.get('episode', None)
	if not meta:
		function = metadata.movie_meta if content == 'movie' else metadata.tvshow_meta
		meta = function('tmdb_id', params['tmdb_id'], settings.metadata_user_info(), get_datetime())
	watched_indicators = settings.watched_indicators()
	on_str, off_str, currently_str, open_str, settings_str = ls(32090), ls(32027), ls(32598), ls(32641), ls(32247)
	if settings.auto_play(content): autoplay_status, autoplay_toggle, quality_setting = on_str, 'false', 'autoplay_quality_%s' % content
	else: autoplay_status, autoplay_toggle, quality_setting = off_str, 'true', 'results_quality_%s' % content
	quality_filter_setting = 'autoplay_quality_%s' % content if autoplay_status == on_str else 'results_quality_%s' % content
	autoplay_next_status, autoplay_next_toggle = (on_str, 'false') if settings.autoplay_next_episode() else (off_str, 'true')
	results_xml_style_status = get_setting('results.xml_style', 'Default')
	results_filter_ignore_status, results_filter_ignore_toggle = (on_str, 'false') if settings.ignore_results_filter() else (off_str, 'true')
	results_sorting_status = get_setting('results.sort_order_display').replace('$ADDON[plugin.video.pov 32582]', ls(32582))
	current_results_highlights_action = get_setting('highlight.type')
	results_highlights_status = ls(32240) if current_results_highlights_action == '0' else ls(32583) if current_results_highlights_action == '1' else ls(32241)
	current_subs_action = get_setting('subtitles.subs_action')
	current_subs_action_status = 'Auto' if current_subs_action == '0' else ls(32193) if current_subs_action == '1' else off_str
	active_internal_scrapers = [i.replace('_', '') for i in settings.active_internal_scrapers()]
	current_scrapers_status = ', '.join([i for i in active_internal_scrapers]) if len(active_internal_scrapers) > 0 else 'N/A'
	current_quality_status =  ', '.join(settings.quality_filter(quality_setting))
	uncached_torrents_status, uncached_torrents_toggle = (on_str, 'false') if settings.display_uncached_torrents() else (off_str, 'true')
	listing = []
	base_str1 = '%s%s'
	base_str2 = '%s: [B]%s[/B]' % (currently_str, '%s')
	if content in ('movie', 'episode'):
		multi_line = 'true'
		listing += [(ls(32014), '%s %s' % (ls(32533), ls(32841)), 'clear_and_rescrape', meta['poster'])]
		listing += [(ls(32006), '%s %s' % (ls(32533), ls(32841)), 'rescrape_with_disabled', meta['poster'])]
		listing += [(ls(32807), '%s %s' % (ls(32533), ls(32841)), 'scrape_with_filters_ignored', meta['poster'])]
		listing += [(ls(32135), '%s %s' % (ls(32533), ls(32841)), 'scrape_with_custom_values', meta['poster'])]
#		listing += [(base_str1 % (ls(32175), ' (%s)' % content), base_str2 % autoplay_status, 'toggle_autoplay')]
#		if autoplay_status == on_str and content == 'episode':
#			listing += [(base_str1 % (ls(32178), ''), base_str2 % autoplay_next_status, 'toggle_autoplay_next')]
#		listing += [(base_str1 % (ls(32105), ' (%s)' % content), base_str2 % current_quality_status, 'set_quality')]
#		listing += [(base_str1 % ('', '%s %s' % (ls(32055), ls(32533))), base_str2 % current_scrapers_status, 'enable_scrapers')]
#		if autoplay_status == off_str:
#			listing += [(base_str1 % ('', ls(32140)), base_str2 % results_xml_style_status, 'set_results_xml_display')]
#			listing += [(base_str1 % ('', ls(32151)), base_str2 % results_sorting_status, 'set_results_sorting')]
#			listing += [(base_str1 % ('', ls(32138)), base_str2 % results_highlights_status, 'set_results_highlights')]
#		listing += [(base_str1 % ('', ls(32686)), base_str2 % results_filter_ignore_status, 'set_results_filter_ignore')]
#		listing += [(base_str1 % ('', ls(32183)), base_str2 % current_subs_action_status, 'set_subs_action')]
#		if 'external' in active_internal_scrapers:
#			listing += [(base_str1 % ('', ls(32160)), base_str2 % uncached_torrents_status, 'toggle_torrents_display_uncached')]
	else: multi_line = 'false'
	if content in ('tvshow') and meta: listing += [(ls(32541), '', 'play_random', meta['poster']), (ls(32542), '', 'play_random_continual', meta['poster'])]
	if content in ('movie', 'tvshow') and meta: listing += [(ls(32604) % (ls(32028) if meta['mediatype'] == 'movie' else ls(32029)), '', 'clear_media_cache', meta['poster'])]
	if watched_indicators == 1: listing += [(ls(32497) % ls(32037), '', 'clear_trakt_cache')]
	if content in ('movie', 'episode'): listing += [(ls(32637), '', 'clear_scrapers_cache')]
	listing += [('%s %s' % (ls(32118), ls(32513)), '', 'open_external_scrapers_choice')]
#	listing += [('%s %s %s' % (open_str, ls(32522), settings_str), '', 'open_scraper_settings')]
	listing += [(ls(32046), '', 'extras_lists_choice')]
	listing += [('%s %s %s' % (open_str, ls(32036), settings_str), '', 'open_pov_settings')]
#	listing += [(ls(32640), '', 'save_and_exit')]
	list_items = list(_builder())
	heading = ls(32646).replace('[B]', '').replace('[/B]', '')
	kwargs = {'items': json.dumps(list_items), 'heading': heading, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': multi_line}
	choice = select_dialog([i[2] for i in listing], **kwargs)
	if choice in (None, 'save_and_exit'): return
	elif choice == 'clear_and_rescrape': return source_utils.clear_and_rescrape(content, meta, season, episode)
	elif choice == 'rescrape_with_disabled': return source_utils.rescrape_with_disabled(content, meta, season, episode)
	elif choice == 'scrape_with_filters_ignored': return source_utils.scrape_with_filters_ignored(content, meta, season, episode)
	elif choice == 'scrape_with_custom_values': return source_utils.scrape_with_custom_values(content, meta, season, episode)
	elif choice == 'toggle_autoplay': set_setting('auto_play_%s' % content, autoplay_toggle)
	elif choice == 'toggle_autoplay_next': set_setting('autoplay_next_episode', autoplay_next_toggle)
	elif choice == 'enable_scrapers': enable_scrapers_choice()
	elif choice == 'set_results_xml_display': results_layout_choice()
	elif choice == 'set_results_sorting': results_sorting_choice()
	elif choice == 'set_results_filter_ignore': set_setting('ignore_results_filter', results_filter_ignore_toggle)
	elif choice == 'set_results_highlights': results_highlights_choice()
	elif choice == 'set_quality': set_quality_choice(quality_filter_setting)
	elif choice == 'set_subs_action': set_subtitle_choice()
	elif choice == 'extras_lists_choice': extras_lists_choice()
	elif choice == 'play_random': return random_choice(choice, meta)
	elif choice == 'play_random_continual': return random_choice(choice, meta)
	elif choice == 'clear_media_cache': return refresh_cached_meta(meta)
	elif choice == 'toggle_torrents_display_uncached': set_setting('torrent.display.uncached', uncached_torrents_toggle)
	elif choice == 'clear_trakt_cache': return clear_cache('trakt')
	elif choice == 'clear_scrapers_cache': return source_utils.clear_scrapers_cache()
	elif choice == 'open_external_scrapers_choice': return external_scrapers_choice()
#	elif choice == 'open_scraper_settings': return execute_builtin('Addon.OpenSettings(script.module.fenomscrapers)')
	elif choice == 'open_pov_settings': return kodi_utils.open_settings('0.0')
	if choice == 'clear_trakt_cache' and content in ('movie', 'tvshow', 'season', 'episode'): container_refresh()
	show_busy_dialog()
	sleep(200)
	hide_busy_dialog()
	options_menu(params, meta=meta)

def extras_menu(params):
	function = metadata.movie_meta if params['media_type'] == 'movie' else metadata.tvshow_meta
	meta = function('tmdb_id', params['tmdb_id'], settings.metadata_user_info(), get_datetime())
	open_window(['windows.extras', 'Extras'], 'extras.xml', meta=meta, is_widget=params.get('is_widget', 'false'), is_home=params.get('is_home', 'false'))

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
		kodi_utils.notification(32576, 2000)
		kodi_utils.container_refresh()
	except: kodi_utils.notification(32574)

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
				'user': params.get('user', ''), 'slug': params.get('slug', ''), 'list_id': params.get('list_id', '')}
	execute_builtin('Container.Update(%s)' % build_url(url_params))

