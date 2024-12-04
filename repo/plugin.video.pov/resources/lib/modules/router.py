# from modules.kodi_utils import logger

def routing(params):
	params_get = params.get
	mode = params_get('mode', 'navigator.main')
	if 'navigator.' in mode:
		from indexers.navigator import Navigator
		exec('Navigator(params).%s()' % mode.split('.')[1])
	elif 'menu_editor.' in mode:
		from modules.menu_editor import MenuEditor
		exec('MenuEditor(params).%s()' % mode.split('.')[1])
	elif 'discover.' in mode:
		from indexers.discover import Discover
		exec('Discover(params).%s()' % mode.split('.')[1])
	elif '_play' in mode or 'play_' in mode:
		if mode == 'play_media':
			import json
			from modules.sources import Sources
			if 'params' in params: params = json.loads(params['params'])
			Sources().playback_prep(params)
		elif mode == 'media_play':
			from modules.player import POVPlayer
			POVPlayer().run(params_get('url'), params_get('media_type'))
	elif 'choice' in mode:
		from modules import dialogs
		if mode == 'scraper_color_choice':
			dialogs.scraper_color_choice(params['setting'])
		elif mode == 'scraper_dialog_color_choice':
			dialogs.scraper_dialog_color_choice(params['setting'])
		elif mode == 'scraper_quality_color_choice':
			dialogs.scraper_quality_color_choice(params['setting'])
		elif mode == 'imdb_images_choice':
			dialogs.imdb_images_choice(params['imdb_id'], params['rootname'])
		elif mode == 'set_quality_choice':
			dialogs.set_quality_choice(params['quality_setting'])
		elif mode == 'results_sorting_choice':
			dialogs.results_sorting_choice()
		elif mode == 'results_layout_choice':
			dialogs.results_layout_choice()
		elif mode == 'options_menu_choice':
			dialogs.options_menu(params)
		elif mode == 'meta_language_choice':
			dialogs.meta_language_choice()
		elif mode == 'extras_menu_choice':
			dialogs.extras_menu(params)
		elif mode == 'enable_scrapers_choice':
			dialogs.enable_scrapers_choice()
		elif mode == 'favorites_choice':
			dialogs.favorites_choice(params)
		elif mode == 'trakt_manager_choice':
			dialogs.trakt_manager_choice(params)
		elif mode == 'folder_scraper_manager_choice':
			dialogs.folder_scraper_manager_choice()
		elif mode == 'set_language_filter_choice':
			dialogs.set_language_filter_choice(params['filter_setting'])
		elif mode == 'media_extra_info_choice':
			dialogs.media_extra_info(params['media_type'], params['meta'])
		elif mode == 'extras_lists_choice':
			dialogs.extras_lists_choice()
		elif mode == 'random_choice':
			dialogs.random_choice(params['tmdb_id'], params['poster'])
	elif 'trakt.' in mode:
		if 'trakt_account_info' in mode:
			from indexers.trakt import trakt_account_info
			trakt_account_info()
		elif 'trakt_auth' in mode:
			from apis.trakt_api import trakt_auth
			trakt_auth()
		elif 'trakt_revoke' in mode:
			from apis.trakt_api import trakt_revoke
			trakt_revoke()
		elif 'hide_unhide_trakt_items' in mode:
			from apis.trakt_api import hide_unhide_trakt_items
			hide_unhide_trakt_items(params['action'], params['media_type'], params['media_id'], params['section'])
		else:
			from modules.utils import manual_function_import
			function = manual_function_import('apis.trakt_api', mode.split('.')[-1])
			function(params)
	elif 'build' in mode:
		if 'build_trakt_list' in mode:
			from modules.utils import manual_function_import
			function = manual_function_import('indexers.trakt', mode.split('.')[-1])
			function(params)
		elif mode == 'build_movie_list':
			from indexers.movies import Movies
			Movies(params).run()
		elif mode == 'build_tvshow_list':
			from indexers.tvshows import TVShows
			TVShows(params).run()
		elif mode == 'build_season_list':
			from indexers.seasons import Seasons
			Seasons(params).run()
		elif mode == 'build_episode_list':
			from indexers.seasons import Seasons
			Seasons(params).run()
		elif mode == 'build_in_progress_episode':
			from indexers.episodes import Episodes
			Episodes(params).run()
		elif mode == 'build_next_episode':
			from indexers.episodes import Episodes
			Episodes(params).run()
		elif mode == 'build_my_calendar':
			from indexers.episodes import Episodes
			Episodes(params).run()
		elif mode == 'build_my_anime_calendar':
			from indexers.episodes import Episodes
			Episodes(params).run()
		elif mode == 'build_anime_calendar':
			from indexers.episodes import Episodes
			Episodes(params).run()
		elif mode == 'build_navigate_to_page':
			from modules.dialogs import build_navigate_to_page
			build_navigate_to_page(params)
		elif mode == 'build_next_episode_manager':
			from modules.episode_tools import build_next_episode_manager
			build_next_episode_manager()
		elif mode == 'imdb_build_user_lists':
			from apis.imdb_api import imdb_build_user_lists
			imdb_build_user_lists(params_get('media_type'))
		elif mode == 'build_popular_people':
			from indexers.people import popular_people
			popular_people()
		elif mode == 'imdb_build_keyword_results':
			from apis.imdb_api import imdb_build_keyword_results
			imdb_build_keyword_results(params['media_type'], params['query'])
	elif 'watched_unwatched' in mode:
		if mode == 'mark_as_watched_unwatched_episode':
			from caches.watched_cache import mark_as_watched_unwatched_episode
			mark_as_watched_unwatched_episode(params)
		elif mode == 'mark_as_watched_unwatched_season':
			from caches.watched_cache import mark_as_watched_unwatched_season
			mark_as_watched_unwatched_season(params)
		elif mode == 'mark_as_watched_unwatched_tvshow':
			from caches.watched_cache import mark_as_watched_unwatched_tvshow
			mark_as_watched_unwatched_tvshow(params)
		elif mode == 'mark_as_watched_unwatched_movie':
			from caches.watched_cache import mark_as_watched_unwatched_movie
			mark_as_watched_unwatched_movie(params)
		elif mode == 'watched_unwatched_erase_bookmark':
			from caches.watched_cache import erase_bookmark
			erase_bookmark(params_get('media_type'), params_get('tmdb_id'), params_get('season', ''), params_get('episode', ''), params_get('refresh', 'false'))
	elif 'toggle' in mode:
		if mode == 'toggle_jump_to':
			from modules.kodi_utils import toggle_jump_to
			toggle_jump_to()
		elif mode == 'toggle_provider':
			from modules.utils import toggle_provider
			toggle_provider()
		elif mode == 'toggle_language_invoker':
			from modules.kodi_utils import toggle_language_invoker
			toggle_language_invoker()
	elif 'history' in mode:
		if mode == 'search_history':
			from indexers.history import search_history
			search_history(params)
		elif mode == 'clear_search_history':
			from indexers.history import clear_search_history
			clear_search_history()
		elif mode == 'remove_from_history':
			from indexers.history import remove_from_search_history
			remove_from_search_history(params)
		elif mode == 'discover_remove_from_history':
			from indexers.discover import remove_from_history
			remove_from_history(params)
		elif mode == 'discover_remove_all_history':
			from indexers.discover import remove_all_history
			remove_all_history(params)
	elif 'easynews.' in mode:
		from modules.utils import manual_function_import
		function = manual_function_import('indexers.easynews', mode.split('.')[-1])
		function(params)
	elif 'real_debrid' in mode:
		if mode == 'real_debrid.rd_torrent_cloud':
			from indexers.real_debrid import rd_torrent_cloud
			rd_torrent_cloud()
		if mode == 'real_debrid.rd_downloads':
			from indexers.real_debrid import rd_downloads
			rd_downloads()
		elif mode == 'real_debrid.browse_rd_cloud':
			from indexers.real_debrid import browse_rd_cloud
			browse_rd_cloud(params['id'])
		elif mode == 'real_debrid.resolve_rd':
			from indexers.real_debrid import resolve_rd
			resolve_rd(params)
		elif mode == 'real_debrid.rd_account_info':
			from indexers.real_debrid import rd_account_info
			rd_account_info()
		elif mode == 'real_debrid.delete':
			from indexers.real_debrid import rd_delete
			rd_delete(params_get('id'), params_get('cache_type'))
		elif mode == 'real_debrid.delete_download_link':
			from indexers.real_debrid import delete_download_link
			delete_download_link(params['download_id'])
		elif mode == 'real_debrid.rd_auth':
			from apis.real_debrid_api import RealDebridAPI
			RealDebridAPI().auth()
		elif mode == 'real_debrid.rd_revoke':
			from apis.real_debrid_api import RealDebridAPI
			RealDebridAPI().revoke_auth()
	elif 'premiumize' in mode:
		if mode == 'premiumize.pm_torrent_cloud':
			from indexers.premiumize import pm_torrent_cloud
			pm_torrent_cloud(params_get('id'), params_get('folder_name'))
		elif mode == 'premiumize.pm_transfers':
			from indexers.premiumize import pm_transfers
			pm_transfers()
		elif mode == 'premiumize.pm_account_info':
			from indexers.premiumize import pm_account_info
			pm_account_info()
		elif mode == 'premiumize.rename':
			from indexers.premiumize import pm_rename
			pm_rename(params_get('file_type'), params_get('id'), params_get('name'))
		elif mode == 'premiumize.delete':
			from indexers.premiumize import pm_delete
			pm_delete(params_get('file_type'), params_get('id'))
		elif mode == 'premiumize.pm_auth':
			from apis.premiumize_api import PremiumizeAPI
			PremiumizeAPI().auth()
		elif mode == 'premiumize.pm_revoke':
			from apis.premiumize_api import PremiumizeAPI
			PremiumizeAPI().revoke_auth()
	elif 'alldebrid' in mode:
		if mode == 'alldebrid.ad_torrent_cloud':
			from indexers.alldebrid import ad_torrent_cloud
			ad_torrent_cloud(params_get('id'))
		elif mode == 'alldebrid.browse_ad_cloud':
			from indexers.alldebrid import browse_ad_cloud
			browse_ad_cloud(params['folder'])
		elif mode == 'alldebrid.resolve_ad':
			from indexers.alldebrid import resolve_ad
			resolve_ad(params)
		elif mode == 'alldebrid.ad_account_info':
			from indexers.alldebrid import ad_account_info
			ad_account_info()
		elif mode == 'alldebrid.ad_auth':
			from apis.alldebrid_api import AllDebridAPI
			AllDebridAPI().auth()
		elif mode == 'alldebrid.ad_revoke':
			from apis.alldebrid_api import AllDebridAPI
			AllDebridAPI().revoke_auth()
	elif 'offcloud' in mode:
		if mode == 'offcloud.oc_torrent_cloud':
			from indexers.offcloud import oc_torrent_cloud
			oc_torrent_cloud()
		elif mode == 'offcloud.browse_oc_cloud':
			from indexers.offcloud import browse_oc_cloud
			browse_oc_cloud(params_get('folder_id'))
		elif mode == 'offcloud.resolve_oc':
			from indexers.offcloud import resolve_oc
			resolve_oc(params)
		elif mode == 'offcloud.oc_account_info':
			from indexers.offcloud import oc_account_info
			oc_account_info()
		elif mode == 'offcloud.delete':
			from indexers.offcloud import oc_delete
			oc_delete(params_get('folder_id'))
		elif mode == 'offcloud.user_cloud_clear':
			from apis.offcloud_api import OffcloudAPI
			OffcloudAPI().user_cloud_clear()
		elif mode == 'offcloud.oc_auth':
			from apis.offcloud_api import OffcloudAPI
			OffcloudAPI().auth()
		elif mode == 'offcloud.oc_revoke':
			from apis.offcloud_api import OffcloudAPI
			OffcloudAPI().revoke_auth()
	elif 'torbox' in mode:
		if mode == 'torbox.tb_torrent_cloud':
			from indexers.torbox import tb_torrent_cloud
			tb_torrent_cloud()
		elif mode == 'torbox.browse_tb_cloud':
			from indexers.torbox import browse_tb_cloud
			browse_tb_cloud(params_get('folder_id'))
		elif mode == 'torbox.resolve_tb':
			from indexers.torbox import resolve_tb
			resolve_tb(params)
		elif mode == 'torbox.tb_account_info':
			from indexers.torbox import tb_account_info
			tb_account_info()
		elif mode == 'torbox.delete':
			from indexers.torbox import tb_delete
			tb_delete(params_get('folder_id'))
		elif mode == 'torbox.tb_auth':
			from apis.torbox_api import TorBoxAPI
			TorBoxAPI().auth()
		elif mode == 'torbox.tb_revoke':
			from apis.torbox_api import TorBoxAPI
			TorBoxAPI().revoke_auth()
	elif 'easydebrid' in mode:
		if mode == 'easydebrid.ed_account_info':
			pass
		elif mode == 'easydebrid.ed_auth':
			from apis.easydebrid_api import EasyDebridAPI
			EasyDebridAPI().auth()
		elif mode == 'easydebrid.ed_revoke':
			from apis.easydebrid_api import EasyDebridAPI
			EasyDebridAPI().revoke_auth()
	elif '_settings' in mode:
		if mode == 'open_settings':
			from modules.kodi_utils import open_settings
			open_settings(params_get('query'))
		elif mode == 'clean_settings':
			from modules.kodi_utils import clean_settings
			clean_settings()
		elif mode == 'erase_all_settings':
			from modules.nav_utils import erase_all_settings
			erase_all_settings()
		elif mode == 'external_settings':
			from modules.kodi_utils import open_settings
			open_settings(params_get('query', '0.0'), params_get('ext_addon'))
		elif mode == 'clean_settings_window_properties':
			from modules.kodi_utils import clean_settings_window_properties
			clean_settings_window_properties()
	elif '_cache' in mode:
		if mode == 'clear_all_cache':
			from modules.cache_utils import clear_all_cache
			clear_all_cache()
		else:
			from modules.cache_utils import clear_cache
			clear_cache(params_get('cache'))
	elif '_image' in mode:
		from indexers.images import Images
		Images().run(params)
	elif '_text' in mode:
		from modules.kodi_utils import show_text
		show_text(params_get('heading'), params_get('text'), params_get('file'),
							params_get('font_size', 'small'), params_get('kodi_log', 'false') == 'true')
	elif '_view' in mode:
		from modules import kodi_utils
		if mode == 'choose_view':
			kodi_utils.choose_view(params['view_type'], params_get('content', ''))
		elif mode == 'set_view':
			kodi_utils.set_view(params['view_type'])
	##EXTRA modes##
	elif mode == 'get_search_term':
		from indexers.history import get_search_term
		get_search_term(params)
	elif 'person_data_dialog' in mode:
		from indexers.people import person_data_dialog
		person_data_dialog(params)
	elif mode == 'downloader':
		from modules.downloader import runner
		runner(params)
	elif mode == 'clean_databases':
		from modules.cache_utils import clean_databases
		clean_databases()
	elif mode == 'manual_add_magnet_to_cloud':
		from modules.debrid import manual_add_magnet_to_cloud
		manual_add_magnet_to_cloud(params)
	elif mode == 'debrid.browse_packs':
		from modules.sources import Sources
		Sources().debridPacks(params['provider'], params['name'], params['magnet_url'], params['info_hash'], params['highlight'])
	elif mode == 'upload_logfile':
		from modules.kodi_utils import upload_logfile
		upload_logfile()
	##FENOM modes###
	elif mode == 'undesirablesInput':
		from caches.undesirables_cache import undesirablesInput
		undesirablesInput()
	elif mode == 'undesirablesUserRemove':
		from caches.undesirables_cache import undesirablesUserRemove
		undesirablesUserRemove()
	elif mode == 'comet_configure':
		from fenom.hosted import Comet
		Comet().configure()
	elif mode == 'mfdebrid_configure':
		from fenom.hosted import MFDebrid
		MFDebrid().configure()

