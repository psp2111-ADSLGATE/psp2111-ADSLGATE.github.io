import json
import sys
from urllib.parse import unquote
from datetime import timedelta
from caches.main_cache import main_cache
from modules import kodi_utils
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
build_url = kodi_utils.build_url
make_listitem = kodi_utils.make_listitem
search_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/search_history.png')
default_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/search.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
four_insert_string, five_insert_string = '%s %s %s %s', '%s %s %s %s %s'
delete_str, search_str, hist_str, mov_str, key_str = ls(32785), ls(32450), ls(32486), ls(32028), ls(32092)
tv_str, easy_str, peop_str, imdb_str, tmdb_str, coll_str = ls(32029), ls(32070), ls(32507), ls(32064), ls(32068), ls(32499)
history_str, remove_str = '[B]%s:[/B] [I]%s[/I]' % (ls(32486).upper(), '%s'), ls(32786)
new_search_str = '[B]%s %s...[/B]' % (ls(32857).upper(), ls(32450).upper())
mode_dict = {'movie': ('movie_queries', {'mode': 'get_search_term', 'media_type': 'movie'}),
			'tvshow': ('tvshow_queries', {'mode': 'get_search_term', 'media_type': 'tv_show'}),
			'people': ('people_queries', {'mode': 'get_search_term', 'search_type': 'people'}),
			'tmdb_collections': ('tmdb_collections_queries', {'mode': 'get_search_term', 'search_type': 'tmdb_collections', 'media_type': 'movie'}),
			'imdb_keyword_movie': ('imdb_keyword_movie_queries', {'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'media_type': 'movie'}),
			'imdb_keyword_tvshow': ('imdb_keyword_tvshow_queries', {'mode': 'get_search_term', 'search_type': 'imdb_keyword', 'media_type': 'tvshow'}),
			'easynews_video': ('easynews_video_queries', {'mode': 'get_search_term', 'search_type': 'easynews_video'}),
			'tb_usenet': ('torbox_usenet_queries', {'mode': 'get_search_term', 'search_type': 'tb_usenet'})}
clear_history_list = [(four_insert_string % (delete_str, mov_str, search_str, hist_str), 'movie_queries'),
					(four_insert_string % (delete_str, tv_str, search_str, hist_str), 'tvshow_queries'),
					(four_insert_string % (delete_str, peop_str, search_str, hist_str), 'people_queries'),
					(five_insert_string % (delete_str, tmdb_str, coll_str, search_str, hist_str), 'tmdb_collections_queries'),
					(five_insert_string % (delete_str, imdb_str, key_str, mov_str, hist_str), 'imdb_keyword_movie_queries'),
					(five_insert_string % (delete_str, imdb_str, key_str, tv_str, hist_str), 'imdb_keyword_tvshow_queries'),
					(four_insert_string % (delete_str, easy_str, search_str, hist_str), 'easynews_video_queries')]

def search_history(params):
	def _builder():
		for h in main_cache.get(setting_id):
			try:
				cm = []
				query = unquote(h)
				url_params['query'] = query
				display = history_str % query
				url = build_url(url_params)
				cm.append((remove_str, 'RunPlugin(%s)' % build_url({'mode': 'remove_from_history', 'setting_id':setting_id, 'query': query})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': search_icon, 'poster': search_icon, 'thumb': search_icon, 'fanart': fanart, 'banner': search_icon})
				listitem.addContextMenuItems(cm)
				yield (url, listitem, False)
			except: pass
	__handle__ = int(sys.argv[1])
	setting_id, action_dict = mode_dict[params['action']]
	url_params = dict(action_dict)
	kodi_utils.add_dir(__handle__, action_dict, new_search_str, iconImage=default_icon, isFolder=False)
	try: kodi_utils.add_items(__handle__, list(_builder()))
	except: pass
	kodi_utils.set_category(__handle__, params.get('name'))
	kodi_utils.set_content(__handle__, '')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main', '')

def get_search_term(params):
	kodi_utils.close_all_dialog()
	media_type = params.get('media_type', '')
	search_type = params.get('search_type', 'media_title')
	params_query = params.get('query', '')
	if search_type == 'people':
		url_params, string = {'mode': 'person_search'}, 'people_queries'
	elif search_type == 'imdb_keyword':
		url_params, string = {'mode': 'imdb_build_keyword_results', 'media_type': media_type}, 'imdb_keyword_%s_queries' % media_type
	elif search_type == 'easynews_video':
		url_params, string = {'mode': 'easynews.search_easynews'}, 'easynews_video_queries'
	elif search_type == 'tmdb_collections':
		url_params, string = {'mode': 'build_movie_list', 'action': 'tmdb_movies_search_collections'}, 'tmdb_collections_queries'
	elif search_type == 'tb_usenet':
		url_params, string = {'mode': 'torbox.tb_usenet_query'}, 'torbox_usenet_queries'
	else:
		if media_type == 'movie': url_params, string = {'mode': 'build_movie_list', 'action': 'tmdb_movies_search'}, 'movie_queries'
		else: url_params, string = {'mode': 'build_tvshow_list', 'action': 'tmdb_tv_search'}, 'tvshow_queries'
	query = params_query or kodi_utils.dialog.input('POV')
	if not query.strip(): return
	query = unquote(query)
	add_to_search_history(query, string)
	url_params['query'] = query
	if search_type == 'people':
		return kodi_utils.execute_builtin('RunPlugin(%s)' % kodi_utils.build_url(url_params))
	if kodi_utils.external_browse():
		return kodi_utils.execute_builtin('ActivateWindow(Videos,%s,return)' % kodi_utils.build_url(url_params))
	return kodi_utils.execute_builtin('Container.Update(%s)' % kodi_utils.build_url(url_params))

def add_to_search_history(search_name, search_list):
	try:
		result = []
		cache = main_cache.get(search_list)
		if cache: result = cache
		if search_name in result: result.remove(search_name)
		result.insert(0, search_name)
		result = result[:50]
		main_cache.set(search_list, result, expiration=timedelta(days=365))
	except: pass

def remove_from_search_history(params):
	try:
		result = main_cache.get(params['setting_id'])
		result.remove(params.get('query'))
		main_cache.set(params['setting_id'], result, expiration=timedelta(days=365))
		kodi_utils.notification(32576)
		kodi_utils.container_refresh()
	except: pass

def clear_search_history():
	try:
		list_items = [{'line1': item[0], 'icon': default_icon} for item in clear_history_list]
		kwargs = {'items': json.dumps(list_items), 'heading': ls(32450), 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		setting = kodi_utils.select_dialog([item[1] for item in clear_history_list], **kwargs)
		if setting is None: return
		main_cache.set(setting, '', expiration=timedelta(days=365))
		kodi_utils.notification(32576)
	except: pass

