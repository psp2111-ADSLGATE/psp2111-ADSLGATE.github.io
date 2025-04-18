import sys
from caches.navigator_cache import navigator_cache as nc
from modules import kodi_utils as k, settings as s
# logger = k.logger

tp, ls, build_url, notification, list_dirs = k.translate_path, k.local_string, k.build_url, k.notification, k.list_dirs
make_listitem, add_item, end_directory, add_items = k.make_listitem, k.add_item, k.end_directory, k.add_items
set_content, set_view_mode, set_sort_method, set_category = k.set_content, k.set_view_mode, k.set_sort_method, k.set_category
easynews_active, download_directory, source_folders_directory = s.easynews_active, s.download_directory, s.source_folders_directory
get_shortcut_folders, get_shortcut_folder_contents, = nc.get_shortcut_folders, nc.get_shortcut_folder_contents
icon_directory = 'special://home/addons/plugin.video.pov/resources/media/%s'
_in_str, mov_str, tv_str, edit_str = ls(32484), ls(32028), ls(32029), ls(32705)
browse_str, add_menu_str, s_folder_str = ls(32706), ls(32730), ls(32731)

class Navigator:
	def __init__(self, params):
		self.params = params
		self.params_get = self.params.get
		self.list_name = self.params_get('action', 'RootList')

	def main(self):
		def build_main_lists():
			for item_position, item in enumerate(nc.currently_used_list(self.list_name)):
				try:
					cm = []
					cm_append = cm.append
					item_get = item.get
					icon = item_get('iconImage') if item_get('network_id', '') != '' else tp(icon_directory % item_get('iconImage'))
					isFolder = False if item_get('isFolder') == 'false' else True
					cm_append((edit_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.edit_menu', 'active_list': self.list_name, 'position': item_position})))
					cm_append((browse_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.browse', 'active_list': self.list_name})))
					listitem = make_listitem()
					listitem.setLabel(ls(item_get('name', '')))
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					listitem.addContextMenuItems(cm)
					yield (build_url(item), listitem, isFolder)
				except: pass
		__handle__, fanart = int(sys.argv[1]), k.addon_fanart()
		add_items(__handle__, list(build_main_lists()))
		self._end_directory()

	def downloads(self):
		dl_str, pr_str, im_str = ls(32107), ls(32485), ls(32798)
		mov_path, ep_path = download_directory('movie'), download_directory('episode')
		prem_path, im_path = download_directory('premium'), download_directory('image')
		n_ins = _in_str % (dl_str.upper(), '')
		self._add_item({'mode': 'navigator.folder_navigator', 'folder_path': mov_path , 'name': mov_str}, 'movies.png' , n_ins)
		self._add_item({'mode': 'navigator.folder_navigator', 'folder_path': ep_path  , 'name': tv_str }, 'tv.png'     , n_ins)
		self._add_item({'mode': 'navigator.folder_navigator', 'folder_path': prem_path, 'name': pr_str }, 'premium.png', n_ins)
		self._add_item({'mode': 'browser_image', 'folder_path': im_path,                'name': im_str }, 'people.png' , n_ins, False)
		self._end_directory()

	def discover_main(self):
		discover_str, his_str, help_str = ls(32451), ls(32486), ls(32487)
		movh_str, tvh_str = '%s %s' % (mov_str, his_str), '%s %s' % (tv_str, his_str)
		n_ins = _in_str % (discover_str.upper(), '')
		self._add_item({'mode': 'discover.movie', 'media_type': 'movie',    'name': mov_str }, 'discover.png', n_ins)
		self._add_item({'mode': 'discover.tvshow', 'media_type': 'tvshow',  'name': tv_str  }, 'discover.png', n_ins)
		self._add_item({'mode': 'discover.history', 'media_type': 'movie',  'name': movh_str}, 'discover.png', n_ins)
		self._add_item({'mode': 'discover.history', 'media_type': 'tvshow', 'name': tvh_str }, 'discover.png', n_ins)
		self._add_item({'mode': 'discover.help',                            'name': help_str}, 'discover.png', n_ins, False)
		self._end_directory()

	def premium(self):
		from modules.debrid import debrid_enabled
		easynews, debrids = easynews_active(), debrid_enabled()
		if easynews: self.easynews()
		if 'Real-Debrid' in debrids: self.real_debrid()
		if 'Premiumize.me' in debrids: self.premiumize()
		if 'AllDebrid' in debrids: self.alldebrid()
		if 'TorBox' in debrids: self.torbox()
		if 'Offcloud' in debrids: self.offcloud()
		if 'EasyDebrid' in debrids: self.easydebrid()
		self._end_directory()

	def easynews(self):
		easy_str, se_str, acc_str = ls(32070), ls(32450), ls(32494)
		n_ins = _in_str % (easy_str.upper(), '')
		self._add_item({'mode': 'search_history', 'action': 'easynews_video', 'name': se_str }, 'search.png'  , n_ins)
		self._add_item({'mode': 'easynews.account_info',                      'name': acc_str}, 'easynews.png', n_ins, False)

	def real_debrid(self):
		rd_str, acc_str, his_str, cloud_str = ls(32054), ls(32494), ls(32486), ls(32496)
		clca_str, n_ins = ls(32497) % rd_str, _in_str % (rd_str.upper(), '')
		self._add_item({'mode': 'real_debrid.rd_torrent_cloud',     'name': cloud_str}, 'realdebrid.png', n_ins)
		self._add_item({'mode': 'real_debrid.rd_downloads',         'name': his_str  }, 'realdebrid.png', n_ins)
		self._add_item({'mode': 'real_debrid.rd_account_info',      'name': acc_str  }, 'realdebrid.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'rd_cloud', 'name': clca_str }, 'realdebrid.png', n_ins, False)

	def premiumize(self):
		pm_str, acc_str, his_str, cloud_str = ls(32061), ls(32494), ls(32486), ls(32496)
		clca_str, n_ins = ls(32497) % pm_str, _in_str % (pm_str.upper(), '')
		self._add_item({'mode': 'premiumize.pm_torrent_cloud',      'name': cloud_str}, 'premiumize.png', n_ins)
		self._add_item({'mode': 'premiumize.pm_transfers',          'name': his_str  }, 'premiumize.png', n_ins)
		self._add_item({'mode': 'premiumize.pm_account_info',       'name': acc_str  }, 'premiumize.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'pm_cloud', 'name': clca_str }, 'premiumize.png', n_ins, False)

	def alldebrid(self):
		ad_str, acc_str, cloud_str = ls(32063), ls(32494), ls(32496)
		clca_str, n_ins = ls(32497) % ad_str, _in_str % (ad_str.upper(), '')
		self._add_item({'mode': 'alldebrid.ad_torrent_cloud',       'name': cloud_str}, 'alldebrid.png', n_ins)
		self._add_item({'mode': 'alldebrid.ad_account_info',        'name': acc_str  }, 'alldebrid.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'ad_cloud', 'name': clca_str }, 'alldebrid.png', n_ins, False)

	def offcloud(self):
		oc_str, clc_str = 'Offcloud', 'Clear Cloud Storage',
		cloud_str, ai_str = ls(32496), ls(32494)
		clca_str, n_ins = ls(32497) % oc_str, _in_str % (oc_str.upper(), '')
		self._add_item({'mode': 'offcloud.oc_torrent_cloud',        'name': cloud_str}, 'offcloud.png', n_ins)
		self._add_item({'mode': 'offcloud.oc_account_info',         'name': ai_str   }, 'offcloud.png', n_ins, False)
		self._add_item({'mode': 'offcloud.user_cloud_clear',        'name': clc_str  }, 'offcloud.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'oc_cloud', 'name': clca_str }, 'offcloud.png', n_ins, False)

	def torbox(self):
		tor_str, usenet_str, web_str, query_str = 'Torrent', 'Usenet', 'Web Download', 'Usenet Search'
		tb_str, cloud_str, ai_str = 'TorBox', ls(32496), ls(32494)
		clca_str, n_ins = ls(32497) % tb_str, _in_str % (tb_str.upper(), '')
		self._add_item({'mode': 'torbox.tb_torrent_cloud', 'media_type': 'torent', 'name': tor_str   }, 'torbox.png', n_ins)
		self._add_item({'mode': 'torbox.tb_torrent_cloud', 'media_type': 'usenet', 'name': usenet_str}, 'torbox.png', n_ins)
		self._add_item({'mode': 'torbox.tb_torrent_cloud', 'media_type': 'webdl',  'name': web_str   }, 'torbox.png', n_ins)
		self._add_item({'mode': 'search_history', 'action': 'tb_usenet',           'name': query_str }, 'torbox.png', n_ins)
		self._add_item({'mode': 'torbox.tb_account_info',                          'name': ai_str    }, 'torbox.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'tb_cloud',                'name': clca_str  }, 'torbox.png', n_ins, False)

	def easydebrid(self):
		ed_str, cloud_str, ai_str = 'EasyDebrid', ls(32496), ls(32494)
		n_ins = _in_str % (ed_str.upper(), '')
		self._add_item({'mode': 'easydebrid.ed_account_info',                      'name': ai_str    }, 'easydebrid.png', n_ins, False)

	def favourites(self):
		fav_str = ls(32453)
		clear_fav_str = ls(32497) % fav_str
		n_ins, c_n_ins = _in_str % (fav_str.upper(), ''), _in_str % (ls(32524).upper(), '')
		self._add_item({'mode': 'build_movie_list', 'action': 'favourites_movies',   'name': mov_str      }, 'movies.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'favourites_tvshows', 'name': tv_str       }, 'tv.png'    , n_ins)
		self._add_item({'mode': 'favourites_choice', 'cache': 'clear_favourites',     'name': clear_fav_str}, 'tools.png' , c_n_ins, False)
		self._end_directory()

	def my_content(self):
		trakt_str, imdb_str, coll_str, wlist_str, ls_str = ls(32037), ls(32064), ls(32499), ls(32500), ls(32501)
		t_n_ins, i_n_ins, m_n_ins = _in_str % (trakt_str.upper(), ''), _in_str % (imdb_str.upper(), ''), _in_str % ('MDBList'.upper(), '')
		t_str, user_str, l_str, ai_str, ml_str = ls(32037), ls(32065), ls(32501), ls(32494), ls(32454)
		tu_str, pu_str = '%s %s %s' % (ls(32458), user_str, l_str), '%s %s %s' % (ls(32459), user_str, l_str)
		sea_str, n_ins = '%s %s' % (ls(32477), l_str), _in_str % (t_str.upper(), '')
		mdb_m_str, mdb_t_str = 'My %s %s' % (wlist_str, mov_str), 'My %s %s' % (wlist_str, tv_str)
		trakt_status = k.get_setting('trakt_user') not in ('', None)
		tmdb_status = k.get_setting('tmdb.account_id') not in ('', None)
		mdblist_status = k.get_setting('mdblist.token') not in ('', None)
		imdb_status = k.get_setting('imdb_user') not in ('', None)
		if trakt_status:
			self._add_item({'mode': 'navigator.trakt_collections'                                           , 'name': coll_str }, 'trakt.png', t_n_ins)
			self._add_item({'mode': 'navigator.trakt_watchlists'                                            , 'name': wlist_str}, 'trakt.png', t_n_ins)
			self._add_item({'mode': 'navigator.trakt_lists'                                                 , 'name': ls_str   }, 'trakt.png', t_n_ins)
			self._add_item({'mode': 'trakt.trakt_account_info'                                              , 'name': ai_str   }, 'trakt.png', t_n_ins, False)
		self._add_item({'mode': 'build_trakt_list.get_trakt_trending_popular_lists', 'list_type': 'trending', 'name': tu_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_trakt_list.get_trakt_trending_popular_lists', 'list_type': 'popular' , 'name': pu_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_trakt_list.search_trakt_lists'                                       , 'name': sea_str}, 'trakt.png', n_ins)
		if tmdb_status:
			self._add_item({'mode': 'build_movie_list', 'action': 'tmdb_watchlist'          , 'name': 'Movie Watchlist'        }, 'tmdb.png', '[B]TMDB:[/B] ')
			self._add_item({'mode': 'build_tvshow_list', 'action': 'tmdb_watchlist'         , 'name': 'TV Show Watchlist'      }, 'tmdb.png', '[B]TMDB:[/B] ')
			self._add_item({'mode': 'build_movie_list', 'action': 'tmdb_favorite'           , 'name': 'Movie Favorite'         }, 'tmdb.png', '[B]TMDB:[/B] ')
			self._add_item({'mode': 'build_tvshow_list', 'action': 'tmdb_favorite'          , 'name': 'TV Show Favorite'       }, 'tmdb.png', '[B]TMDB:[/B] ')
			self._add_item({'mode': 'build_movie_list', 'action': 'tmdb_recommendations'    , 'name': 'Movie Recommendations'  }, 'tmdb.png', '[B]TMDB:[/B] ')
			self._add_item({'mode': 'build_tvshow_list', 'action': 'tmdb_recommendations'   , 'name': 'TV Show Recommendations'}, 'tmdb.png', '[B]TMDB:[/B] ')
			self._add_item({'mode': 'build_tmdb_list.get_tmdb_lists'                        , 'name': 'My Lists'               }, 'tmdb.png', '[B]TMDB:[/B] ')
		if mdblist_status:
			self._add_item({'mode': 'build_movie_list', 'action': 'mdblist_watchlist'       , 'name': mdb_m_str }, 'mdblist.png', m_n_ins)
			self._add_item({'mode': 'build_tvshow_list', 'action': 'mdblist_watchlist'      , 'name': mdb_t_str }, 'mdblist.png', m_n_ins)
			self._add_item({'mode': 'build_mdb_list.get_mdb_lists', 'list_type': 'my_lists' , 'name': ml_str    }, 'mdblist.png', m_n_ins)
			self._add_item({'mode': 'build_mdb_list.get_mdb_toplists'                       , 'name': pu_str    }, 'mdblist.png', m_n_ins)
			self._add_item({'mode': 'build_mdb_list.search_mdb_lists'                       , 'name': sea_str   }, 'mdblist.png', m_n_ins)
		if imdb_status:
			self._add_item({'mode': 'navigator.imdb_watchlists', 'name': wlist_str}, 'imdb.png', i_n_ins)
			self._add_item({'mode': 'navigator.imdb_lists',      'name': ls_str   }, 'imdb.png', i_n_ins)
		self._end_directory()

	def trakt_collections(self):
		# use 'new_page' to pass the type of list to be processed when using 'trakt_collection_lists'...
		t_str, col_str = ls(32037), ls(32499)
		tcol_str = '%s %s' % (t_str, col_str)
		n_ins = _in_str % (tcol_str.upper(), '')
		mrec_str, mran_str = '%s %s' % (ls(32498), mov_str), '%s %s' % (ls(32504), mov_str)
		tvrec_str, tvran_str, ra_str = '%s %s' % (ls(32498), tv_str), '%s %s' % (ls(32504), tv_str), '%s %s' % (ls(32505), ls(32506))
		n_ins = _in_str % (col_str.upper(), '')
		self._add_item({'mode': 'build_movie_list', 'action': 'trakt_collection'                             , 'name': mov_str  }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'trakt_collection'                            , 'name': tv_str   }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_movie_list', 'action': 'trakt_collection_lists', 'new_page': 'recent' , 'name': mrec_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_movie_list', 'action': 'trakt_collection_lists', 'new_page': 'random' , 'name': mran_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'trakt_collection_lists', 'new_page': 'recent', 'name': tvrec_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'trakt_collection_lists', 'new_page': 'random', 'name': tvran_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_my_calendar', 'recently_aired': 'true'                                , 'name': ra_str   }, 'trakt.png', n_ins)
		self._end_directory()

	def trakt_watchlists(self):
		t_str, watchlist_str = ls(32037), ls(32500)
		trakt_watchlist_str = '%s %s' % (t_str, watchlist_str)
		n_ins = _in_str % (trakt_watchlist_str.upper(), '')
		tmdb_status = k.get_setting('tmdb.account_id') not in ('', None)
		self._add_item({'mode': 'build_movie_list', 'action': 'trakt_watchlist',  'name': mov_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'trakt_watchlist', 'name': tv_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'tmdb.import_trakt_watchlist',                    'name': 'Export to TMDB'}, 'trakt.png', n_ins, False) if tmdb_status else None
		self._end_directory()

	def trakt_lists(self):
		t_str, ml_str, ll_str, rec_str = ls(32037), ls(32454), ls(32502), ls(32503)
		cal_str, ani_str, drp_str = ls(32081), 'Anime Calendar', 'Dropped TV Shows'
		n_ins = _in_str % (t_str.upper(), '')
		self._add_item({'mode': 'build_trakt_list.get_trakt_lists', 'list_type': 'my_lists'   , 'name': ml_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_trakt_list.get_trakt_lists', 'list_type': 'liked_lists', 'name': ll_str }, 'trakt.png', n_ins)
		self._add_item({'mode': 'navigator.trakt_recommendations'                             , 'name': rec_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'trakt_droplist'               , 'name': drp_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_my_calendar'                                           , 'name': cal_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_my_anime_calendar'                                     , 'name': ani_str}, 'trakt.png', n_ins)
		self._end_directory()

	def trakt_recommendations(self):
		rec_str = ls(32503)
		n_ins = _in_str % (rec_str.upper(), '')
		self._add_item({'mode': 'build_movie_list', 'action': 'trakt_recommendations',  'name': mov_str}, 'trakt.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'trakt_recommendations', 'name': tv_str }, 'trakt.png', n_ins)
		self._end_directory()

	def imdb_watchlists(self):
		imdb_str, watchlist_str = ls(32064), ls(32500)
		imdb_watchlist_str = '%s %s' % (imdb_str, watchlist_str)
		n_ins = _in_str % (imdb_watchlist_str.upper(), '')
		self._add_item({'mode': 'build_movie_list', 'action': 'imdb_watchlist',  'name': mov_str}, 'imdb.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'imdb_watchlist', 'name': tv_str }, 'imdb.png', n_ins)
		self._end_directory()

	def imdb_lists(self):
		imdb_str, lists_str = ls(32064), ls(32501)
		imdb_lists_str = '%s %s' % (imdb_str, lists_str)
		n_ins = _in_str % (imdb_lists_str.upper(), '')
		self._add_item({'mode': 'imdb_build_user_lists', 'media_type': 'movie',  'name': mov_str}, 'imdb.png', n_ins)
		self._add_item({'mode': 'imdb_build_user_lists', 'media_type': 'tvshow', 'name': tv_str }, 'imdb.png', n_ins)
		self._end_directory()

	def search(self):
		search_str, people_str, clca_str = ls(32450), ls(32507), ls(32497)
		coll_str, clear_search_str = '%s %s (%s)' % (mov_str, ls(32499), ls(32068)), clca_str % search_str
		kw_mov, kw_tv = '%s %s (%s)' % (ls(32064), ls(32092), mov_str), '%s %s (%s)' % (ls(32064), ls(32092), tv_str)
		n_ins, s_n_ins = _in_str % (ls(32524).upper(), ''), _in_str % (search_str.upper(), '')
		self._add_item({'mode': 'search_history', 'action': 'movie',               'name': mov_str         }, 'search_movie.png' , s_n_ins)
		self._add_item({'mode': 'search_history', 'action': 'tvshow',              'name': tv_str          }, 'search_tv.png'    , s_n_ins)
		self._add_item({'mode': 'search_history', 'action': 'people',              'name': people_str      }, 'search_people.png', s_n_ins)
		self._add_item({'mode': 'search_history', 'action': 'tmdb_collections',    'name': coll_str        }, 'search_tmdb.png'  , s_n_ins)
		self._add_item({'mode': 'search_history', 'action': 'imdb_keyword_movie',  'name': kw_mov          }, 'search_imdb.png'  , s_n_ins)
		self._add_item({'mode': 'search_history', 'action': 'imdb_keyword_tvshow', 'name': kw_tv           }, 'search_imdb.png'  , s_n_ins)
		self._add_item({'mode': 'clear_search_history',                            'name': clear_search_str}, 'tools.png'        , n_ins, False)
		self._end_directory()

	def settings(self):
		pov_str, manager_str, changelog_str, short_str, source_str = ls(32036), ls(32513), ls(32508), ls(32514), ls(32515)
		log_utils, views_str, clean_str, lang_inv_str, ms_str = ls(32777), ls(32510), ls(32512), ls(33017), ls(32455)
		settings_str, changelog_log_viewer_str = ls(32247), '%s & %s' % (changelog_str, log_utils)
		shortcut_manager_str, source_manager_str = '%s %s' % (short_str, manager_str), '%s %s' % (source_str, manager_str)
		n_ins = _in_str % (settings_str.upper(), '')
		self._add_item({'mode': 'open_settings',                 'name': pov_str                 }, 'pov.png', n_ins, False)
		self._add_item({'mode': 'open_settings', 'query': '6.0', 'name': ms_str                  }, 'settings.png', n_ins, False)
		self._add_item({'mode': 'navigator.clear_info',          'name': clean_str               }, 'settings.png', n_ins)
		self._add_item({'mode': 'navigator.log_utils',           'name': changelog_log_viewer_str}, 'settings.png', n_ins)
		self._add_item({'mode': 'navigator.set_view_modes',      'name': views_str               }, 'settings.png', n_ins)
		self._add_item({'mode': 'navigator.shortcut_folders',    'name': shortcut_manager_str    }, 'settings.png', n_ins)
		self._add_item({'mode': 'navigator.sources_folders',     'name': source_manager_str      }, 'settings.png', n_ins)
		self._add_item({'mode': 'toggle_language_invoker',       'name': lang_inv_str            }, 'settings.png', n_ins, False)
		self._end_directory()

	def clear_info(self):
		cache_str, clca_str, clean_str, all_str, settings_str = ls(32524), ls(32497), ls(32526), ls(32525), ls(32247)
		clean_set_cache_str = '%s %s %s' % (clean_str, ls(32247), ls(32524))
		clean_databases_str = '%s %s' % (clean_str, ls(32003))
		clean_all_str = '%s %s %s' % (clean_str, all_str, settings_str)
		clear_all_str, clear_meta_str = clca_str % all_str, clca_str % ls(32527)
		clear_list_str, clear_trakt_str = clca_str % ls(32501), clca_str % ls(32037)
		clear_imdb_str, clint_str, clext_str = clca_str % ls(32064), clca_str % ls(32096), clca_str % ls(32118)
		clear_rd_str, clear_pm_str, clear_ad_str = clca_str % ls(32054), clca_str % ls(32061), clca_str % ls(32063)
		clear_oc_str, clear_tb_str, clear_ed_str = clca_str % 'Offcloud', clca_str % 'TorBox', clca_str % 'EasyDebrid'
		clear_all_upper = '[B]%s[/B]' % clear_all_str.upper()
		n_ins, clean_ins = _in_str % (cache_str.upper(), ''), _in_str % (clean_str.upper(), '')
		self._add_item({'mode': 'clean_settings',                            'name': clean_all_str      }, 'tools.png', clean_ins, False)
		self._add_item({'mode': 'clean_settings_window_properties',          'name': clean_set_cache_str}, 'tools.png', clean_ins, False)
		self._add_item({'mode': 'clean_databases',                           'name': clean_databases_str}, 'tools.png', clean_ins, False)
		self._add_item({'mode': 'clear_all_cache',                           'name': clear_all_upper    }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'meta',              'name': clear_meta_str     }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'list',              'name': clear_list_str     }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'trakt',             'name': clear_trakt_str    }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'imdb',              'name': clear_imdb_str     }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'internal_scrapers', 'name': clint_str          }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'external_scrapers', 'name': clext_str          }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'rd_cloud',          'name': clear_rd_str       }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'pm_cloud',          'name': clear_pm_str       }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'ad_cloud',          'name': clear_ad_str       }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'oc_cloud',          'name': clear_oc_str       }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'tb_cloud',          'name': clear_tb_str       }, 'tools.png', n_ins, False)
		self._add_item({'mode': 'clear_cache', 'cache': 'ed_cloud',          'name': clear_ed_str       }, 'tools.png', n_ins, False)
		self._end_directory()

	def set_view_modes(self):
		set_views_str, lists_str, root_str, movies_str = ls(32510), ls(32501), ls(32457), ls(32028)
		tvshows_str, season_str, episode_str = ls(32029), ls(32537), ls(32506)
		premium_files_str, ep_lists_str = ls(32485), '%s %s' % (episode_str, lists_str)
		n_ins, reset_str = _in_str % (set_views_str.upper(), ''), 'Reset All Views'
		self._add_item({'mode': 'choose_view', 'view_type': 'view.main', 'content': '', 'exclude_external': 'true'                , 'name': root_str         }, 'settings.png', n_ins)
		self._add_item({'mode': 'choose_view', 'view_type': 'view.movies', 'content': 'movies', 'exclude_external': 'true'        , 'name': movies_str       }, 'settings.png', n_ins)
		self._add_item({'mode': 'choose_view', 'view_type': 'view.tvshows', 'content': 'tvshows', 'exclude_external': 'true'      , 'name': tvshows_str      }, 'settings.png', n_ins)
		self._add_item({'mode': 'choose_view', 'view_type': 'view.seasons', 'content': 'seasons', 'exclude_external': 'true'      , 'name': season_str       }, 'settings.png', n_ins)
		self._add_item({'mode': 'choose_view', 'view_type': 'view.episodes', 'content': 'episodes', 'exclude_external': 'true'    , 'name': episode_str      }, 'settings.png', n_ins)
		self._add_item({'mode': 'choose_view', 'view_type': 'view.episode_lists', 'content': 'episodes','exclude_external': 'true', 'name': ep_lists_str     }, 'settings.png', n_ins)
		self._add_item({'mode': 'choose_view', 'view_type': 'view.premium', 'content': 'files', 'exclude_external': 'true'        , 'name': premium_files_str}, 'settings.png', n_ins)
		self._add_item({'mode': 'clear_view', 'view_type': 'all'                                                                  , 'name': reset_str        }, 'settings.png', n_ins, False)
		self._end_directory()

	def log_utils(self):
		pov_vstr, log_path = k.addon().getAddonInfo('version'), 'special://home/addons/%s/changelog.txt'
		kl_loc, mt_str = tp('special://logpath/kodi.log'), tp(log_path % 'plugin.video.pov')
		pov_str, cl_str, lut_str, k_str, lv_str = ls(32036), ls(32508), ls(32777), ls(32538), ls(32509)
		mh_str, klv_h, klu_h = '%s  [I](v.%s)[/I]' % (pov_str, pov_vstr), '%s %s' % (k_str, lv_str), ls(32853)
		cl_n_ins, lu_n_ins = _in_str % (cl_str.upper(), ''), _in_str % (lut_str.upper(), '')
		self._add_item({'mode': 'show_text', 'heading': mh_str, 'file': mt_str, 'exclude_external': 'true',                    'name': mh_str}, 'lists.png', cl_n_ins, False)
		self._add_item({'mode': 'show_text', 'heading': klv_h, 'file': kl_loc, 'kodi_log': 'true', 'exclude_external': 'true', 'name': klv_h }, 'lists.png', lu_n_ins, False)
		self._add_item({'mode': 'upload_logfile', 'exclude_external': 'true',                                                  'name': klu_h }, 'lists.png', lu_n_ins, False)
		self._end_directory()

	def anime(self):
		n_ins, t_ins = _in_str % ('SIMKL', ''), _in_str % ('TRAKT', '')
		self._add_item({'mode': 'build_anime_calendar'                                     , 'name': 'Series Calendar'         }, 'trakt.png',    t_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'simkl_tv_popular',           'name': 'Series Popular This Week'}, 'tv.png',       n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'simkl_tv_most_watched',      'name': 'Series Most Watched'     }, 'tv.png',       n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'simkl_tv_recent_release',    'name': 'Series Recent Released'  }, 'tv.png',       n_ins)
		self._add_item({'mode': 'navigator.anime_genres', 'menu_type': 'tvshow',             'name': 'Series Genres'           }, 'genres.png',   n_ins)
		self._add_item({'mode': 'navigator.anime_years', 'menu_type': 'tvshow',              'name': 'Series Years'            }, 'calender.png', n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'simkl_onas_popular',         'name': 'ONAs Popular This Week'  }, 'tv.png',       n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'simkl_onas_most_watched',    'name': 'ONAs Most Watched'       }, 'tv.png',       n_ins)
		self._add_item({'mode': 'build_tvshow_list', 'action': 'simkl_onas_recent_release',  'name': 'ONAs Recent Released'    }, 'tv.png',       n_ins)
		self._add_item({'mode': 'build_movie_list', 'action': 'simkl_movies_popular',        'name': 'Movies Popular This Week'}, 'movies.png',   n_ins)
		self._add_item({'mode': 'build_movie_list', 'action': 'simkl_movies_most_watched',   'name': 'Movies Most Watched'     }, 'movies.png',   n_ins)
		self._add_item({'mode': 'build_movie_list', 'action': 'simkl_movies_recent_release', 'name': 'Movies Recent Released'  }, 'movies.png',   n_ins)
		self._add_item({'mode': 'navigator.anime_genres', 'menu_type': 'movie',              'name': 'Movies Genres'           }, 'genres.png',   n_ins)
		self._add_item({'mode': 'navigator.anime_years', 'menu_type': 'movie',               'name': 'Movies Years'            }, 'calender.png', n_ins)
		self._end_directory()

	def certifications(self):
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie': from modules.meta_lists import movie_certifications as certifications
		else: from modules.meta_lists import tvshow_certifications as certifications
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_certifications' if menu_type == 'movie' else 'trakt_tv_certifications'
		lst_ins = self.make_list_name(menu_type)
		for cert in certifications:
			list_name = '%s: %s %s' % (lst_ins.upper(), cert.upper(), ls(32473))
			self._add_item({'mode': mode, 'action': action, 'certification': cert, 'name': cert.upper()}, 'certifications.png', list_name=list_name)
		self._end_directory()

	def languages(self):
		from modules.meta_lists import languages
		menu_type = self.params_get('menu_type')
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_languages' if menu_type == 'movie' else 'tmdb_tv_languages'
		lst_ins = self.make_list_name(menu_type)
		for lang in languages:
			list_name = '%s: %s %s' % (lst_ins.upper(), lang[0], ls(32471))
			self._add_item({'mode': mode, 'action': action, 'language': lang[1], 'name': lang[0]}, 'languages.png', list_name=list_name)
		self._end_directory()

	def years(self):
		from modules.meta_lists import years
		menu_type = self.params_get('menu_type')
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_year' if menu_type == 'movie' else 'tmdb_tv_year'
		lst_ins = self.make_list_name(menu_type)
		for i in years():
			list_name = '%s: %s %s' % (lst_ins.upper(), str(i), ls(32460))
			self._add_item({'mode': mode, 'action': action, 'year': str(i), 'name': str(i)}, 'calender.png', list_name=list_name)
		self._end_directory()

	def anime_years(self):
		from modules.meta_lists import years
		menu_type = self.params_get('menu_type')
		mode = 'build_movie_list' if menu_type == 'movie' else 'build_tvshow_list'
		action = 'simkl_movies_year' if menu_type == 'movie' else 'simkl_tv_year'
		lst_ins = self.make_list_name(menu_type)
		for i in years():
			list_name = 'ANIME %s: %s %s' % (lst_ins.upper(), str(i), ls(32460))
			self._add_item({'mode': mode, 'action': action, 'year': str(i), 'name': str(i)}, 'calender.png', list_name=list_name)
		self._end_directory()

	def genres(self):
		import json
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie':
			from modules.meta_lists import movie_genres as genre_list
			mode, action = 'build_movie_list', 'tmdb_movies_genres'
		else:
			from modules.meta_lists import tvshow_genres as genre_list
			mode, action = 'build_tvshow_list', 'tmdb_tv_genres'
		lst_ins = self.make_list_name(menu_type)
		self._add_item({'mode': 'navigator.multiselect_genres', 'genre_list': json.dumps(genre_list), 'menu_type': menu_type, 'exclude_external': 'true', 'name': ls(32789)}, 'genres.png', isFolder=False)
		for genre, value in sorted(genre_list.items()):
			list_name = '%s: %s %s' % (lst_ins.upper(), genre, ls(32470))
			self._add_item({'mode': mode, 'action': action, 'genre_id': value[0], 'name': genre}, 'genres.png', list_name=list_name)
		self._end_directory()

	def anime_genres(self):
		menu_type = self.params_get('menu_type')
		if menu_type == 'movie':
			from modules.meta_lists import anime_genres as genre_list
			mode, action = 'build_movie_list', 'simkl_movies_genres'
		else:
			from modules.meta_lists import anime_genres as genre_list
			mode, action = 'build_tvshow_list', 'simkl_tv_genres'
		lst_ins = self.make_list_name(menu_type)
		for genre, slug in sorted(genre_list):
			list_name = 'ANIME %s: %s %s' % (lst_ins.upper(), genre, ls(32470))
			self._add_item({'mode': mode, 'action': action, 'genre_id': slug, 'name': genre}, 'genres.png', list_name=list_name)
		self._end_directory()

	def multiselect_genres(self):
		import json
		def _builder():
			for genre, value in sorted(genre_list.items()):
				function_list_append(value[0])
#				yield {'line1': genre, 'icon': tp(''.join([icon_directory, 'genres.png']))}
				yield {'line1': genre, 'icon': tp(icon_directory % 'genres.png')}
		menu_type, genre_list = self.params['menu_type'], self.params['genre_list']
		function_list = []
		function_list_append = function_list.append
#		icon_directory = 'special://home/addons/plugin.video.pov/resources/media/'
		genre_list = json.loads(genre_list)
		list_items = list(_builder())
		kwargs = {'items': json.dumps(list_items), 'heading': ls(32847), 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false'}
		genre_ids = k.select_dialog(function_list, **kwargs)
		if genre_ids is None: return
		genre_id = ','.join(genre_ids)
		if menu_type == 'movie': url = {'mode': 'build_movie_list', 'action': 'tmdb_movies_genres', 'genre_id': genre_id}
		else: url = {'mode': 'build_tvshow_list', 'action': 'tmdb_tv_genres', 'genre_id': genre_id}
		return k.execute_builtin('Container.Update(%s)' % build_url(url))

	def networks(self):
		from modules.meta_lists import networks
		lst_ins = self.make_list_name(self.params_get('menu_type'))
		for item in sorted(networks, key=lambda k: k['name']):
			list_name = '%s: %s %s' % (lst_ins.upper(), item['name'], ls(32480))
			self._add_item({'mode': 'build_tvshow_list', 'action': 'tmdb_tv_networks', 'network_id': item['id'], 'name': item['name']}, item['logo'], list_name=list_name)
		self._end_directory()

	def folder_navigator(self):
		import os
		from modules.utils import clean_file_name, normalize
		def _process():
			for tup in items:
				try:
					item = tup[0]
					url = os.path.join(folder_path, item)
					listitem = make_listitem()
					listitem.setLabel(clean_file_name(normalize(item)))
					listitem.setArt({'fanart': fanart})
					yield (url, listitem, tup[1])
				except: pass
		__handle__, fanart = int(sys.argv[1]), k.addon_fanart()
		folder_path = self.params_get('folder_path')
		sources_folders = self.params_get('sources_folders', None)
		dirs, files = list_dirs(folder_path)
		items = [(i, True) for i in dirs] + [(i, False) for i in files]
		item_list = list(_process())
		add_items(__handle__, item_list)
		set_sort_method(__handle__, 'files')
		self._end_directory()

	def sources_folders(self):
		name_str = '[B]%s (%s): %s[/B]\n     [I]%s[/I]'
		for source in ('folder1', 'folder2', 'folder3', 'folder4', 'folder5'):
			for media_type in ('movie', 'tvshow'):
				folder_path = source_folders_directory(media_type, source)
				if not folder_path: continue
				name = name_str % (source.upper(), self.make_list_name(media_type).upper(), k.get_setting('%s.display_name' % source).upper(), folder_path)
				self._add_item({'mode': 'navigator.folder_navigator','sources_folders': 'True', 'folder_path': folder_path, 'name': name}, 'most_collected.png')
		self._end_directory()

	def because_you_watched(self):
		from caches.watched_cache import get_watched_info_movie, get_watched_info_tv
		def _convert_pov_watched_episodes_info(watched_indicators):
			seen = set()
			_watched = get_watched_info_tv(watched_indicators)
			_watched.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
			return [(i[0], i[3], i[4], [(i[1], i[2])]) for i in _watched if not (i[0] in seen or seen.add(i[0]))]
		watched_indicators = s.watched_indicators()
		media_type = self.params_get('menu_type')
		function = get_watched_info_movie if media_type == 'movie' else _convert_pov_watched_episodes_info
		mode = 'build_movie_list' if media_type == 'movie' else 'build_tvshow_list'
		action = 'tmdb_movies_recommendations' if media_type == 'movie' else 'tmdb_tv_recommendations'
		recently_watched = function(watched_indicators)
		recently_watched = sorted(recently_watched, key=lambda k: k[2], reverse=True)
		because_ins = '[I]%s[/I]  [B]%s[/B]' % (ls(32474), '%s')
		for item in recently_watched:
			tmdb_id = item[0]
			if media_type == 'movie': name = because_ins % item[1]
			else:
				season, episode = item[3][-1]
				name = because_ins % '%s - %sx%s' % (item[1], season, episode)
			self._add_item({'mode': mode, 'action': action, 'tmdb_id': tmdb_id, 'exclude_external': 'true', 'name': name}, 'because_you_watched.png')
		self._end_directory()

	def make_list_name(self, menu_type):
		return menu_type.replace('tvshow', tv_str).replace('movie', mov_str)

	def shortcut_folders(self):
		def _make_new_item():
			icon, art = tp(icon_directory % 'new.png'), tp(k.fanart_default)
			display_name = '[I]%s...[/I]' % ls(32702)
			url_params = {'mode': 'menu_editor.shortcut_folder_make'}
			url = build_url(url_params)
			listitem = make_listitem()
			listitem.setLabel(display_name)
			listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': art, 'banner': icon})
			add_item(__handle__, url, listitem, False)
		def _builder():
			short_str, delete_str = ls(32514), ls(32703)
			icon = tp(icon_directory % 'folder.png')
			for i in folders:
				try:
					cm = []
					cm_append = cm.append
					name = i[0]
					display_name = '[B]%s : [/B] %s ' % (short_str.upper(), i[0])
					contents = eval(i[1])
					url_params = {'mode': 'navigator.build_shortcut_folder_list', 'name': name, 'iconImage': 'folder.png',
								'shortcut_folder': 'True', 'external_list_item': 'True'}
					url = build_url(url_params)
					listitem = make_listitem()
					listitem.setLabel(display_name)
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					cm_append((delete_str, 'RunPlugin(%s)'% build_url({'mode': 'menu_editor.shortcut_folder_delete', 'list_name': name})))
					listitem.addContextMenuItems(cm)
					yield (url, listitem, True)
				except: pass
		__handle__, fanart = int(sys.argv[1]), k.addon_fanart()
		_make_new_item()
		folders = get_shortcut_folders()
		if folders: add_items(__handle__, list(_builder()))
		self._end_directory()

	def build_shortcut_folder_list(self):
		def _process():
			for item_position, item in enumerate(contents):
				try:
					cm = []
					item_get = item.get
					name = item_get('name', 'Error: No Name')
					icon = item_get('iconImage') if item_get('network_id', '') != '' else tp(icon_directory % item_get('iconImage'))
					isFolder = False if item_get('isFolder', '') == 'false' else True
					url = build_url(item)
					cm.append((ls(32705),'RunPlugin(%s)' % build_url(
						{'mode': 'menu_editor.edit_menu_shortcut_folder', 'active_list': list_name, 'position': item_position})))
					listitem = make_listitem()
					listitem.setLabel(name)
					listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon})
					listitem.addContextMenuItems(cm)
					yield (url, listitem, isFolder)
				except: pass
		__handle__, fanart = int(sys.argv[1]), k.addon_fanart()
		list_name = self.params_get('name')
		contents = get_shortcut_folder_contents(list_name)
		add_items(__handle__, list(_process()))
		self._end_directory()

	def _add_item(self, url_params, iconImage='DefaultFolder.png', prefix='', isFolder=True, list_name=''):
		__handle__, fanart = int(sys.argv[1]), k.addon_fanart()
		cm = []
		cm_append = cm.append
		icon = iconImage if 'network_id' in url_params else tp(icon_directory % iconImage)
		url_params['iconImage'] = icon
		if not isFolder: url_params['isFolder'] = 'false'
		url = build_url(url_params)
		listitem = make_listitem()
		listitem.setLabel(f"{prefix}{url_params['name']}")
		listitem.setArt({'icon': icon, 'poster': icon, 'thumb': icon, 'fanart': fanart, 'banner': icon, 'landscape': icon})
		if not 'exclude_external' in url_params:
			list_name = list_name or f"{prefix}{url_params['name']}"
			cm_append((add_menu_str, 'RunPlugin(%s)'% build_url({'mode': 'menu_editor.add_external', 'name': list_name, 'iconImage': iconImage})))
			cm_append((s_folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': list_name, 'iconImage': iconImage})))
			listitem.addContextMenuItems(cm)
		add_item(__handle__, url, listitem, isFolder)

	def _end_directory(self):
		__handle__ = int(sys.argv[1])
		set_category(__handle__, ls(self.params_get('name')))
		set_content(__handle__, '')
		end_directory(__handle__)
		set_view_mode('view.main', '')

