# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcvfs
# from xbmcaddon import Addon
import xbmcaddon
import sys
import json
import requests
import _strptime
import sqlite3 as database
from threading import Thread, activeCount
from urllib.parse import unquote, unquote_plus, urlencode, quote, parse_qsl, urlparse
from modules import icons

try: xbmc_actor = xbmc.Actor
except: xbmc_actor = None
fen_addon_object = xbmcaddon.Addon()
getLocalizedString = fen_addon_object.getLocalizedString
player, xbmc_player, numeric_input, xbmc_monitor, translatePath = xbmc.Player(), xbmc.Player, 1, xbmc.Monitor, xbmcvfs.translatePath
ListItem, getSkinDir, log, getCurrentWindowId, Window = xbmcgui.ListItem, xbmc.getSkinDir, xbmc.log, xbmcgui.getCurrentWindowId, xbmcgui.Window
File, exists, copy, delete, rmdir, rename = xbmcvfs.File, xbmcvfs.exists, xbmcvfs.copy, xbmcvfs.delete, xbmcvfs.rmdir, xbmcvfs.rename
get_infolabel, get_visibility, execute_JSON, window_xml_dialog = xbmc.getInfoLabel, xbmc.getCondVisibility, xbmc.executeJSONRPC, xbmcgui.WindowXMLDialog
executebuiltin, xbmc_sleep, convertLanguage, getSupportedMedia, PlayList = xbmc.executebuiltin, xbmc.sleep, xbmc.convertLanguage, xbmc.getSupportedMedia, xbmc.PlayList
monitor, window, dialog, progressDialog, progressDialogBG = xbmc_monitor(), Window(10000), xbmcgui.Dialog(), xbmcgui.DialogProgress(), xbmcgui.DialogProgressBG()
endOfDirectory, addSortMethod, listdir, mkdir, mkdirs = xbmcplugin.endOfDirectory, xbmcplugin.addSortMethod, xbmcvfs.listdir, xbmcvfs.mkdir, xbmcvfs.mkdirs
addDirectoryItem, addDirectoryItems, setContent, setCategory = xbmcplugin.addDirectoryItem, xbmcplugin.addDirectoryItems, xbmcplugin.setContent, xbmcplugin.setPluginCategory
window_xml_left_action, window_xml_right_action, window_xml_up_action, window_xml_down_action, window_xml_info_action = 1, 2, 3, 4, 11
window_xml_selection_actions, window_xml_closing_actions, window_xml_context_actions = (7, 100), (9, 10, 13, 92), (101, 108, 117)
img_url = 'https://i.imgur.com/%s.png'
empty_poster, item_jump, item_next = img_url % icons.box_office, img_url % icons.item_jump, img_url % icons.item_next
tmdb_default_api, fanarttv_default_api = 'b370b60447737762ca38457bd77579b3', 'fa836e1c874ba95ab08a14ee88e05565'
custom_skins_version_path = 'https://github.com/Tikipeter/custom_skins/raw/main/version.txt'
custom_xml_path = 'special://profile/addon_data/plugin.video.fen/custom_skins/%s/resources/skins/Default/1080i/%s'
custom_skin_path = 'special://profile/addon_data/plugin.video.fen/custom_skins/'
default_skin_path = 'special://home/addons/plugin.video.fen'
database_path_raw = 'special://profile/addon_data/plugin.video.fen/databases/%s'
current_dbs = ('navigator.db', 'watched.db', 'favourites.db', 'traktcache4.db', 'maincache.db', 'metacache2.db', 'debridcache.db', 'providerscache2.db')
single_ep_title_prop, single_ep_format_prop, include_year_prop, fanart_key_prop = 'fen.single_ep_display', 'fen.single_ep_format', 'fen.include_year_in_title', 'fen.fanart_client_key'
datetime_offset_prop, limit_concurrent_prop, max_threads_prop, ignore_articles_prop = 'fen.datetime.offset', 'fen.limit_concurrent_threads', 'fen.max_threads', 'fen.ignore_articles'
view_type_prop, current_langinvoker_prop, refr_settings_prop, rem_props_prop = 'fen.%s', 'fen.reuse_language_invoker', 'fen.refresh_settings', 'fen.remake_properties'
season_title_prop, show_specials_prop, calendar_sort_prop, trakt_user_prop = 'fen.use_season_title', 'fen.show_specials', 'fen.trakt.calendar_sort_order', 'fen.trakt.user'
extras_open_prop, image_resos_prop, fanart_data_prop, meta_language_prop = 'fen.extras.open_action', 'fen.image_resolutions', 'fen.get_fanart_data', 'fen.meta_language'
wid_hidenext_prop, all_episodes_prop, show_unaired_prop, tmdb_api_prop = 'fen.widget_hide_next_page', 'fen.default_all_episodes', 'fen.show_unaired', 'fen.tmdb_api'
custom_context_main_menu_prop, custom_context_prop, custom_info_prop = 'fen.custom_context_main_menu', 'fen.custom_context_menu', 'fen.custom_info_dialog'
meta_mpaa_region_prop, meta_mpaa_prefix_prop, wid_hide_watched_prop = 'fen.meta_mpaa_region', 'fen.meta_mpaa_prefix', 'fen.widget_hide_watched'
int_window_prop, pause_services_prop, suppress_sett_dict_prop = 'fen.internal_results.%s', 'fen.pause_services', 'fen.suppress_settings_dict'
nextep_sort_prop, nextep_order_prop, nextep_inc_unaired_prop = 'fen.nextep.sort_type', 'fen.nextep.sort_order', 'fen.nextep.include_unaired'
watched_indic_prop, fanarttv_def_prop, nextep_inc_date_prop = 'fen.watched_indicators', 'fen.fanarttv.default', 'fen.nextep.include_airdate'
nextep_inc_unwatched_prop, nextep_airing_top_prop = 'fen.nextep.include_unwatched', 'fen.nextep.sort_airing_today_to_top'
menu_cache_prop, highlight_prop, meta_filter_prop, pause_settings_prop = 'fen.kodi_menu_cache', 'fen.highlight', 'fen.meta_filter', 'fen.pause_settings_prop'
current_skin_prop, use_skin_fonts_prop = 'fen.current_skin', 'fen.use_skin_fonts'
settings_props = (current_langinvoker_prop, custom_context_main_menu_prop, custom_context_prop, custom_info_prop, menu_cache_prop, menu_cache_prop, limit_concurrent_prop,
				max_threads_prop, wid_hidenext_prop, all_episodes_prop, show_unaired_prop, season_title_prop, show_specials_prop, calendar_sort_prop, ignore_articles_prop,
				datetime_offset_prop, single_ep_title_prop, single_ep_format_prop, include_year_prop, extras_open_prop, tmdb_api_prop, image_resos_prop, fanart_data_prop,
				meta_language_prop, meta_mpaa_region_prop, meta_mpaa_prefix_prop, wid_hide_watched_prop, fanart_key_prop, trakt_user_prop, watched_indic_prop, fanarttv_def_prop,
				nextep_inc_date_prop, nextep_sort_prop, nextep_order_prop, nextep_inc_unaired_prop, nextep_inc_unwatched_prop, nextep_airing_top_prop, highlight_prop)
userdata_path = translatePath('special://profile/addon_data/plugin.video.fen/')
addon_settings = translatePath('special://home/addons/plugin.video.fen/resources/settings.xml')
user_settings = translatePath('special://profile/addon_data/plugin.video.fen/settings.xml')
addon_icon = translatePath('special://home/addons/plugin.video.fen/resources/media/fen_icon.png')
addon_fanart = translatePath('special://home/addons/plugin.video.fen/resources/media/fen_fanart.png')
addon_clearlogo = translatePath('special://home/addons/plugin.video.fen/resources/media/fen_clearlogo.png')
databases_path = translatePath('special://profile/addon_data/plugin.video.fen/databases/')
colorpalette_path = translatePath('special://profile/addon_data/plugin.video.fen/color_palette2/')
navigator_db = translatePath(database_path_raw % current_dbs[0])
watched_db = translatePath(database_path_raw % current_dbs[1])
favorites_db = translatePath(database_path_raw % current_dbs[2])
trakt_db = translatePath(database_path_raw % current_dbs[3])
maincache_db = translatePath(database_path_raw % current_dbs[4])
metacache_db = translatePath(database_path_raw % current_dbs[5])
debridcache_db = translatePath(database_path_raw % current_dbs[6])
external_db = translatePath(database_path_raw % current_dbs[7])
myvideos_db_paths = {19: '119', 20: '121', 21: '121'}
sort_method_dict = {'episodes': 24, 'files': 5, 'label': 2}
playlist_type_dict = {'music': 0, 'video': 1}
extras_button_label_values = {'movie': {'movies_play': 32174, 'show_trailers': 32606, 'show_keywords': 32092, 'show_images': 32798,  'show_extrainfo': 32605,
						'show_genres': 32470, 'show_director': 32627, 'show_options': 32516, 'show_recommended': 32503, 'show_trakt_manager': 33117,
						'playback_choice': 32187, 'show_favorites_manager': 32197},
						'tvshow': {'tvshow_browse': 32838, 'show_trailers': 32606, 'show_keywords': 32092, 'show_images': 32798, 'show_extrainfo': 32605,
						'show_genres': 32470, 'play_nextep': 33115, 'show_options': 32516, 'show_recommended': 32503, 'show_trakt_manager': 33117,
						'play_random_episode': 32613, 'show_favorites_manager': 32197}}
movie_extras_buttons_defaults = [('extras.movie.button10', 'movies_play'), ('extras.movie.button11', 'show_trailers'), ('extras.movie.button12', 'show_keywords'),
					('extras.movie.button13', 'show_images'), ('extras.movie.button14', 'show_extrainfo'), ('extras.movie.button15', 'show_genres'),
					('extras.movie.button16', 'show_director'), ('extras.movie.button17', 'show_options')]
tvshow_extras_buttons_defaults = [('extras.tvshow.button10', 'tvshow_browse'), ('extras.tvshow.button11', 'show_trailers'), ('extras.tvshow.button12', 'show_keywords'),
					('extras.tvshow.button13', 'show_images'), ('extras.tvshow.button14', 'show_extrainfo'), ('extras.tvshow.button15', 'show_genres'),
					('extras.tvshow.button16', 'play_nextep'), ('extras.tvshow.button17', 'show_options')]
movie_dict_removals = ('fanart_added', 'cast', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id', 'all_trailers', 'fanart', 'banner', 'clearlogo', 'clearlogo2', 'clearart',
						'landscape', 'discart', 'original_title', 'english_title', 'extra_info', 'alternative_titles', 'country_codes', 'fanarttv_fanart', 'fanarttv_poster',
						'fanart2', 'poster2', 'keyart', 'images', 'custom_poster', 'custom_fanart', 'custom_clearlogo', 'custom_banner', 'custom_clearart', 'custom_landscape',
						'custom_discart', 'custom_keyart')
tvshow_dict_removals = ('fanart_added', 'cast', 'poster', 'rootname', 'imdb_id', 'tmdb_id', 'tvdb_id', 'all_trailers', 'discart', 'total_episodes', 'total_seasons', 'fanart',
						'banner', 'clearlogo', 'clearlogo2', 'clearart', 'landscape', 'season_data', 'original_title', 'extra_info', 'alternative_titles', 'english_title',
						'season_summary', 'country_codes', 'fanarttv_fanart', 'fanarttv_poster', 'total_aired_eps', 'fanart2', 'poster2', 'keyart', 'images', 'custom_poster',
						'custom_fanart', 'custom_clearlogo', 'custom_banner', 'custom_clearart', 'custom_landscape', 'custom_discart', 'custom_keyart', 'season_art')
episode_dict_removals = ('thumb', 'guest_stars')
tmdb_dict_removals = ('adult', 'backdrop_path', 'genre_ids', 'original_language', 'original_title', 'overview', 'popularity', 'vote_count', 'video', 'origin_country', 'original_name')
trakt_dict_removals = ('collected_at', 'released')
view_ids = ('view.main', 'view.movies', 'view.tvshows', 'view.seasons', 'view.episodes', 'view.episodes_single', 'view.premium')
video_extensions = ('m4v', '3g2', '3gp', 'nsv', 'tp', 'ts', 'ty', 'pls', 'rm', 'rmvb', 'mpd', 'ifo', 'mov', 'qt', 'divx', 'xvid', 'bivx', 'vob', 'nrg', 'img', 'iso', 'udf', 'pva',
					'wmv', 'asf', 'asx', 'ogm', 'm2v', 'avi', 'bin', 'dat', 'mpg', 'mpeg', 'mp4', 'mkv', 'mk3d', 'avc', 'vp3', 'svq3', 'nuv', 'viv', 'dv', 'fli', 'flv', 'wpl',
					'xspf', 'vdr', 'dvr-ms', 'xsp', 'mts', 'm2t', 'm2ts', 'evo', 'ogv', 'sdp', 'avs', 'rec', 'url', 'pxml', 'vc1', 'h264', 'rcv', 'rss', 'mpls', 'mpl', 'webm',
					'bdmv', 'bdm', 'wtv', 'trp', 'f4v', 'pvr', 'disc')
image_extensions = ('jpg', 'jpeg', 'jpe', 'jif', 'jfif', 'jfi', 'bmp', 'dib', 'png', 'gif', 'webp', 'tiff', 'tif',
					'psd', 'raw', 'arw', 'cr2', 'nrw', 'k25', 'jp2', 'j2k', 'jpf', 'jpx', 'jpm', 'mj2')
default_highlights = (('hoster.identify', 'FF0166FF'), ('torrent.identify', 'FFFF00FE'), ('provider.rd_colour', 'FF3C9900'), ('provider.pm_colour', 'FFFF3300'),
					('provider.ad_colour', 'FFE6B800'), ('provider.furk_colour', 'FFE6002E'), ('provider.easynews_colour', 'FF00B3B2'),
					('provider.debrid_cloud_colour', 'FF7A01CC'), ('provider.folders_colour', 'FFB36B00'), ('scraper_4k_highlight', 'FFFF00FE'),
					('scraper_1080p_highlight', 'FFE6B800'), ('scraper_720p_highlight', 'FF3C9900'), ('scraper_SD_highlight', 'FF0166FF'), ('highlight', 'FF12A0C7'),
					('scraper_flag_identify_colour', 'FF7C7C7C'), ('scraper_result_identify_colour', 'FFFFFFFF'))

def get_icon(image_name):
	return img_url % getattr(icons, image_name, 'I1JJhji')

def local_string(string):
	if isinstance(string, str):
		try: string = int(string)
		except: return string
	return getLocalizedString(string)

def build_url(url_params):
	return 'plugin://plugin.video.fen/?%s' % urlencode(url_params)

def remove_keys(dict_item, dict_removals):
	for k in dict_removals: dict_item.pop(k, None)
	return dict_item

def add_dir(url_params, list_name, handle, iconImage='folder', fanartImage=None, isFolder=True):
	fanart = fanartImage or addon_fanart
	icon = get_icon(iconImage)
	url = build_url(url_params)
	listitem = make_listitem()
	listitem.setLabel(list_name)
	listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon, 'clearlogo': addon_clearlogo})
	info_tag = listitem.getVideoInfoTag()
	info_tag.setPlot(' ')
	add_item(handle, url, listitem, isFolder)

def make_listitem():
	return ListItem(offscreen=True)

def add_item(handle, url, listitem, isFolder):
	addDirectoryItem(handle, url, listitem, isFolder)

def add_items(handle, item_list):
	addDirectoryItems(handle, item_list)

def set_content(handle, content):
	setContent(handle, content)

def set_category(handle, label):
	setCategory(handle, label)

def end_directory(handle, cacheToDisc=None):
	if cacheToDisc == None: cacheToDisc = get_property(menu_cache_prop) == 'true'
	endOfDirectory(handle, cacheToDisc=cacheToDisc)

def set_view_mode(view_type, content='files', is_external=None):
	if is_external == None: is_external = external()
	if is_external: return
	view_id = get_property(view_type_prop % view_type)
	if not view_id: view_id = get_setting(view_type) or None
	try:
		hold = 0
		sleep(100)
		while not container_content() == content:
			hold += 1
			if hold < 5000: sleep(1)
			else: return
		if view_id: execute_builtin('Container.SetViewMode(%s)' % view_id)
	except: return

def append_path(_path):
	sys.path.append(translatePath(_path))

def logger(heading, function):
	log('###%s###: %s' % (heading, function), 1)

def get_property(prop):
	return window.getProperty(prop)

def set_property(prop, value):
	return window.setProperty(prop, value)

def clear_property(prop):
	return window.clearProperty(prop)

def addon(addon_id='plugin.video.fen'):
	return xbmcaddon.Addon(id=addon_id)

def addon_installed(addon_id):
	return get_visibility('System.HasAddon(%s)' % addon_id)

def addon_enabled(addon_id):
	return get_visibility('System.AddonIsEnabled(%s)' % addon_id)

def container_content():
	return get_infolabel('Container.Content')

def set_sort_method(handle, method):
	addSortMethod(handle, sort_method_dict[method])

def make_session(url='https://'):
	session = requests.Session()
	session.mount(url, requests.adapters.HTTPAdapter(pool_maxsize=100))
	return session	

def make_playlist(playlist_type='video'):
	return PlayList(playlist_type_dict[playlist_type])

def convert_language(lang):
	return convertLanguage(lang, 1)

def supported_media():
	return getSupportedMedia('video')

def path_exists(path):
	return exists(path)

def open_file(_file, mode='r'):
	return File(_file, mode)

def copy_file(source, destination):
	return copy(source, destination)

def delete_file(_file):
	delete(_file)

def delete_folder(_folder, force=False):
	rmdir(_folder, force)

def rename_file(old, new):
	rename(old, new)

def list_dirs(location):
	return listdir(location)

def make_directory(path):
	mkdir(path)

def make_directories(path):
	mkdirs(path)

def translate_path(path):
	return translatePath(path)

def sleep(time):
	return xbmc_sleep(time)

def execute_builtin(command, block=False):
	return executebuiltin(command, block)

def current_skin():
	return getSkinDir()

def get_window_id():
	return getCurrentWindowId()

def current_window_object():
	return Window(get_window_id())

def kodi_version():
	return int(get_infolabel('System.BuildVersion')[0:2])

def get_video_database_path():
	return translate_path('special://profile/Database/MyVideos%s.db' % myvideos_db_paths[kodi_version()])

def show_busy_dialog():
	return execute_builtin('ActivateWindow(busydialognocancel)')

def hide_busy_dialog():
	execute_builtin('Dialog.Close(busydialognocancel)')
	execute_builtin('Dialog.Close(busydialog)')

def close_dialog(dialog, block=False):
	execute_builtin('Dialog.Close(%s,true)' % dialog, block)

def close_all_dialog():
	execute_builtin('Dialog.Close(all,true)')

def run_addon(addon='plugin.video.fen', block=False):
	return execute_builtin('RunAddon(%s)' % addon, block)

def external():
	return 'fen' not in get_infolabel('Container.PluginName')

def home():
	return getCurrentWindowId() == 10000

def folder_path():
	return get_infolabel('Container.FolderPath')

def reload_skin():
	execute_builtin('ReloadSkin()')

def kodi_refresh():
	execute_builtin('UpdateLibrary(video,special://skin/foo)')

def run_plugin(params, block=False):
	if isinstance(params, dict): params = build_url(params)
	return execute_builtin('RunPlugin(%s)' % params, block)

def container_update(params, block=False):
	if isinstance(params, dict): params = build_url(params)
	return execute_builtin('Container.Update(%s)' % params, block)

def activate_window(params, block=False):
	if isinstance(params, dict): params = build_url(params)
	return execute_builtin('ActivateWindow(Videos,%s,return)' % params, block)

def container_refresh():
	return execute_builtin('Container.Refresh')

def container_refresh_input(params, block=False):
	if isinstance(params, dict): params = build_url(params)
	return execute_builtin('Container.Refresh(%s)' % params, block)

def replace_window(params, block=False):
	if isinstance(params, dict): params = build_url(params)
	return execute_builtin('ReplaceWindow(Videos,%s)' % params, block)

def disable_enable_addon(addon_name='plugin.video.fen'):
	try:
		execute_JSON(json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'Addons.SetAddonEnabled', 'params': {'addonid': addon_name, 'enabled': False}}))
		execute_JSON(json.dumps({'jsonrpc': '2.0', 'id': 1, 'method': 'Addons.SetAddonEnabled', 'params': {'addonid': addon_name, 'enabled': True}}))
	except: pass

def update_local_addons():
	execute_builtin('UpdateLocalAddons', True)
	sleep(2500)

def get_jsonrpc(request):
	response = execute_JSON(json.dumps(request))
	result = json.loads(response)
	return result.get('result', None)

def jsonrpc_get_directory(directory, properties=['title', 'file', 'thumbnail']):
	command = {'jsonrpc': '2.0', 'id': 1, 'method': 'Files.GetDirectory', 'params': {'directory': directory, 'media': 'files', 'properties': properties}}
	try: results = [i for i in get_jsonrpc(command).get('files') if i['file'].startswith('plugin://') and i['filetype'] == 'directory']
	except: results = None
	return results

def make_global_list():
	global global_list
	global_list = []

def progress_dialog(heading='', icon=addon_icon):
	from windows import create_window
	if isinstance(heading, int): heading = local_string(heading)
	progress_dialog = create_window(('windows.progress', 'Progress'), 'progress.xml', heading=heading, icon=icon)
	Thread(target=progress_dialog.run).start()
	return progress_dialog

def select_dialog(function_list, **kwargs):
	from windows import open_window
	selection = open_window(('windows.default_dialogs', 'Select'), 'select.xml', **kwargs)
	if selection in (None, []): return selection
	if kwargs.get('multi_choice', 'false') == 'true': return [function_list[i] for i in selection]
	return function_list[selection]

def confirm_dialog(heading='', text=32580, ok_label=32839, cancel_label=32840, default_control=11):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	if isinstance(ok_label, int): ok_label = local_string(ok_label)
	if isinstance(cancel_label, int): cancel_label = local_string(cancel_label)
	kwargs = {'heading': heading, 'text': text, 'ok_label': ok_label, 'cancel_label': cancel_label, 'default_control': default_control}
	return open_window(('windows.default_dialogs', 'Confirm'), 'confirm.xml', **kwargs)

def ok_dialog(heading='', text=32760, ok_label=32839):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	if isinstance(ok_label, int): ok_label = local_string(ok_label)
	kwargs = {'heading': heading, 'text': text, 'ok_label': ok_label}
	return open_window(('windows.default_dialogs', 'OK'), 'ok.xml', **kwargs)

def show_text(heading, text=None, file=None, font_size='small', kodi_log=False):
	from windows import open_window
	if isinstance(heading, int): heading = local_string(heading)
	if isinstance(text, int): text = local_string(text)
	heading = heading.replace('[B]', '').replace('[/B]', '')
	if file:
		with open(file, encoding='utf-8') as r: text = r.readlines()
	if kodi_log:
		confirm = confirm_dialog(text=32855, ok_label=32824, cancel_label=32828)
		if confirm == None: return
		if confirm: text = [i for i in text if any(x in i.lower() for x in ('exception', 'error', '[test]'))]
	text = ''.join(text)
	return open_window(('windows.textviewer', 'TextViewer'), 'textviewer.xml', heading=heading, text=text, font_size=font_size)

def notification(line1, time=5000, icon=None, sound=False):
	if isinstance(line1, int): line1 = local_string(line1)
	icon = icon or addon_icon
	dialog.notification(local_string(32036), line1, icon, time, sound)

def choose_view(view_type, content):
	handle = int(sys.argv[1])
	set_view_str = local_string(32547)
	settings_icon = get_icon('settings')
	listitem = make_listitem()
	listitem.setLabel(set_view_str)
	params_url = build_url({'mode': 'set_view', 'view_type': view_type})
	listitem.setArt({'icon': settings_icon, 'poster': settings_icon, 'thumb': settings_icon, 'fanart': addon_fanart, 'banner': settings_icon, 'clearlogo': addon_clearlogo})
	info_tag = listitem.getVideoInfoTag()
	info_tag.setPlot(' ')
	add_item(handle, params_url, listitem, False)
	set_content(handle, content)
	end_directory(handle)
	set_view_mode(view_type, content, False)

def set_view(view_type):
	view_id = str(current_window_object().getFocusId())
	set_setting(view_type, view_id)
	set_property(view_type_prop % view_type, view_id)
	notification(get_infolabel('Container.Viewmode').upper(), time=500)

def set_temp_highlight(temp_highlight):
	current_highlight = get_property(highlight_prop)
	set_property(highlight_prop, temp_highlight)
	return current_highlight

def restore_highlight(current_highlight):
	set_property(highlight_prop, current_highlight)

def timeIt(func):
	# Thanks to 123Venom
	import time
	fnc_name = func.__name__
	def wrap(*args, **kwargs):
		started_at = time.time()
		result = func(*args, **kwargs)
		logger('%s.%s' % (__name__ , fnc_name), (time.time() - started_at))
		return result
	return wrap

def volume_checker():
	# 0% == -60db, 100% == 0db
	try:
		if get_setting('playback.volumecheck_enabled', 'false') == 'false' or get_visibility('Player.Muted'): return
		from modules.utils import string_alphanum_to_num
		max_volume = min(int(get_setting('playback.volumecheck_percent', '50')), 100)
		if int(100 - (float(string_alphanum_to_num(get_infolabel('Player.Volume').split('.')[0]))/60)*100) > max_volume: execute_builtin('SetVolume(%d)' % max_volume)
	except: pass

def focus_index(index, sleep_time=1000):
	show_busy_dialog()
	sleep(sleep_time)
	current_window = current_window_object()
	focus_id = current_window.getFocusId()
	try: current_window.getControl(focus_id).selectItem(index)
	except: pass
	hide_busy_dialog()

def fetch_kodi_imagecache(image):
	result = None
	try:
		dbcon = database.connect(translate_path('special://database/Textures13.db'), timeout=40.0)
		dbcur = dbcon.cursor()
		dbcur.execute("SELECT cachedurl FROM texture WHERE url = ?", (image,))
		result = dbcur.fetchone()[0]
	except: pass
	return result

def get_all_icon_vars(include_values=False):
	if include_values: return [(k, v) for k, v in vars(icons).items() if not k.startswith('__')]
	else: return [k for k, v in vars(icons).items() if not k.startswith('__')]

def toggle_language_invoker():
	from xml.dom.minidom import parse as mdParse
	close_all_dialog()
	sleep(100)
	addon_xml = translate_path('special://home/addons/plugin.video.fen/addon.xml')
	current_addon_setting = get_setting('reuse_language_invoker', 'true')
	new_value = 'false' if current_addon_setting == 'true' else 'true'
	if not confirm_dialog(text=local_string(33018) % (current_addon_setting.upper(), new_value.upper())): return
	if new_value == 'true' and not confirm_dialog(text=33019): return
	root = mdParse(addon_xml)
	root.getElementsByTagName("reuselanguageinvoker")[0].firstChild.data = new_value
	new_xml = str(root.toxml()).replace('<?xml version="1.0" ?>', '')
	with open(addon_xml, 'w') as f: f.write(new_xml)
	set_setting('reuse_language_invoker', new_value)
	set_property(current_langinvoker_prop, new_value)
	ok_dialog(text=32576)
	execute_builtin('ActivateWindow(Home)', True)
	update_local_addons()
	disable_enable_addon()

def upload_logfile(params):
	log_files = [(33145, 'kodi.log'), (33146, 'kodi.old.log')]
	list_items = [{'line1': local_string(i[0])} for i in log_files]
	kwargs = {'items': json.dumps(list_items), 'heading': local_string(33147), 'narrow_window': 'true'}
	log_file = select_dialog(log_files, **kwargs)
	if log_file == None: return
	log_name, log_file = log_file
	if not confirm_dialog(heading=log_name, text=32580): return
	show_busy_dialog()
	url = 'https://paste.kodi.tv/'
	log_file = translate_path('special://logpath/%s' % log_file)
	if not path_exists(log_file): return ok_dialog(text=33039)
	try:
		with open_file(log_file) as f: text = f.read()
		UserAgent = 'Fen %s' % fen_addon_object.getAddonInfo('version')
		response = requests.post('%s%s' % (url, 'documents'), data=text.encode('utf-8', errors='ignore'), headers={'User-Agent': UserAgent}).json()
		user_code = response['key']
		if 'key' in response:
			try:
				from modules.utils import copy2clip
				copy2clip('%s%s' % (url, user_code))
			except: pass
			ok_dialog(text='%s%s' % (url, user_code))
		else: ok_dialog(text=33039)
	except: ok_dialog(text=33039)
	hide_busy_dialog()

def open_settings(query, addon='plugin.video.fen'):
	hide_busy_dialog()
	if query:
		try:
			button, control = 100, 80
			menu, function = query.split('.')
			execute_builtin('Addon.OpenSettings(%s)' % addon)
			execute_builtin('SetFocus(%i)' % (int(menu) - button))
			execute_builtin('SetFocus(%i)' % (int(function) - control))
		except: execute_builtin('Addon.OpenSettings(%s)' % addon)
	else: execute_builtin('Addon.OpenSettings(%s)' % addon)

def set_setting(setting_id, value):
	fen_addon_object.setSetting(setting_id, value)

def get_setting(setting_id, fallback=''):
	return fen_addon_object.getSetting(setting_id) or fallback

def make_window_properties():
	for item in view_ids: set_property(view_type_prop % item, fen_addon_object.getSetting(item))
	for item in settings_props: set_property(item, fen_addon_object.getSetting(item.replace('fen.', '')))

def manage_settings_reset(cancel=False):
	if cancel: trigger_settings_refresh()
	else: set_property(pause_settings_prop, 'true'); sleep(500)

def trigger_settings_refresh():
	set_property(refr_settings_prop, 'true')
	set_property(rem_props_prop, 'true')
	set_property(pause_settings_prop, 'false')
	run_plugin({'mode': 'dummy_run'}, block=True)
