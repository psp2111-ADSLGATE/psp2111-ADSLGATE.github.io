import sys
from queue import SimpleQueue
from threading import Thread
from apis import trakt_api
from indexers.episodes import Episodes
from indexers.movies import Movies
from indexers.tvshows import TVShows
from indexers.seasons import Seasons
from modules import kodi_utils
from modules.utils import paginate_list, jsondate_to_datetime
from modules.settings import paginate, page_limit, nav_jump_use_alphabet
# logger = kodi_utils.logger

KODI_VERSION, ls = kodi_utils.get_kodi_version(), kodi_utils.local_string
build_url, make_listitem = kodi_utils.build_url, kodi_utils.make_listitem
default_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/trakt.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
item_jump = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/item_jump.png')
add2menu_str, add2folder_str, likelist_str, unlikelist_str = ls(32730), ls(32731), ls(32776), ls(32783)
newlist_str, deletelist_str, nextpage_str, jump2_str = ls(32780), ls(32781), ls(32799), ls(32964)

def search_trakt_lists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				list_key = item['type']
				list_info = item[list_key]
				item_count = list_info['item_count']
				if list_info['privacy'] == 'private' or item_count == 0: continue
				name, slug, list_id = list_info['name'], list_info['ids']['slug'], list_info['ids']['trakt']
				user, username = list_info['user']['ids']['slug'], list_info['user']['username']
				display = '[B]%s[/B] | [I](x%s) - %s[/I]' % (name.upper(), str(item_count), username)
				plot = '[B]Link[/B]: [I]%s[/I][CR][CR][B]Likes[/B]: %s' % (list_info['share_link'], list_info['likes'])
				url = build_url({'mode': 'build_trakt_list', 'user': user, 'slug': slug, 'list_id': list_id})
				cm_append((add2menu_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': 'trakt.png'})))
				cm_append((add2folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': 'trakt.png'})))
				cm_append((likelist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug})))
				cm_append((unlikelist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon})
				listitem.setInfo('video', {'plot': plot}) if KODI_VERSION < 20 else listitem.getVideoInfoTag().setPlot(plot)
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	page = params.get('new_page', '1')
	search_title = params.get('search_title', None) or kodi_utils.dialog.input('POV')
	if search_title: lists, pages = trakt_api.trakt_search_lists(search_title, page)
	else: lists, pages = [], page
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_process()))
	if int(pages) > int(page):
		url = {'mode': 'build_trakt_list.search_trakt_lists', 'search_title': search_title, 'new_page': int(page) + 1}
		kodi_utils.add_dir(__handle__, url, nextpage_str)
	kodi_utils.set_category(__handle__, search_title)
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def get_trakt_lists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				if list_type == 'liked_lists': item = item['list']
				name, user, slug, list_id = item['name'], item['user']['ids']['slug'], item['ids']['slug'], item['ids']['trakt']
				item_count, privacy = item.get('item_count', None), item['privacy'] == 'private'
				url = build_url({'mode': 'build_trakt_list', 'user': user, 'slug': slug, 'list_id': list_id, 'list_type': list_type})
				if list_type == 'liked_lists':
					display = '%s (x%s) - [I]%s[/I]' % (name, item_count, user) if item_count else '%s - [I]%s[/I]' % (name, user)
					cm_append((unlikelist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug})))
				else:
					display = '%s (x%s)' % (name, item_count) if item_count else name
					if privacy: display = '[COLOR cyan][I]%s[/I][/COLOR]' % display
					cm_append((newlist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.make_new_trakt_list'})))
					cm_append((deletelist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.delete_trakt_list', 'user': user, 'list_slug': slug})))
				cm_append((add2menu_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': display, 'iconImage': 'trakt.png'})))
				cm_append((add2folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': display, 'iconImage': 'trakt.png'})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon})
				listitem.addContextMenuItems(cm, replaceItems=False)
				yield (url, listitem, True)
			except: pass
	list_type = params['list_type']
	lists = trakt_api.trakt_get_lists(list_type)
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_category(__handle__, params.get('name'))
	kodi_utils.set_sort_method(__handle__, 'label')
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def get_trakt_trending_popular_lists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				item = item['list']
				name, user, slug, list_id = item['name'], item['user']['ids']['slug'], item['ids']['slug'], item['ids']['trakt']
				likes, share_link, item_count = item['likes'], item['share_link'], item.get('item_count', '?')
				display = '[B]%s[/B] | [I](x%s) - %s[/I]' % (name, item_count, user)
				plot = '[B]Link[/B]: [I]%s[/I][CR][CR][B]Likes[/B]: %s' % (share_link, likes)
				url = build_url({'mode': 'build_trakt_list', 'user': user, 'slug': slug, 'list_id': list_id, 'list_type': 'user_lists', 'name': name})
				cm_append((add2menu_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': 'trakt.png'})))
				cm_append((add2folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': 'trakt.png'})))
				cm_append((likelist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_like_a_list', 'user': user, 'list_slug': slug})))
				cm_append((unlikelist_str, 'RunPlugin(%s)' % build_url({'mode': 'trakt.trakt_unlike_a_list', 'user': user, 'list_slug': slug})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon})
				listitem.setInfo('video', {'plot': plot}) if KODI_VERSION < 20 else listitem.getVideoInfoTag().setPlot(plot)
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	list_type = params['list_type']
	lists = trakt_api.trakt_trending_popular_lists(list_type)
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_category(__handle__, params.get('name'))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def build_trakt_list(params):
	def _thread_target(q):
		while not q.empty():
			target, *args = q.get()
			target(*args)
	__handle__, _queue, is_widget = int(sys.argv[1]), SimpleQueue(), kodi_utils.external_browse()
	user, slug, name = params.get('user'), params.get('slug'), params.get('name')
	list_type, list_id = params.get('list_type'), params.get('list_id')
	letter, page = params.get('new_letter', 'None'), int(params.get('new_page', '1'))
	results = trakt_api.get_trakt_list_contents(list_type, list_id, user, slug)
	if paginate(): process_list, total_pages = paginate_list(results, page, letter, page_limit())
	else: process_list, total_pages = results, 1
	process_dict = {'movies': 0, 'tvshows': 0, 'seasons': 0, 'episodes': 0}
	movies, tvshows = Movies({'id_type': 'trakt_dict'}), TVShows({'id_type': 'trakt_dict'})
	episodes, seasons = Episodes({'id_type': 'trakt_dict'}), Seasons({'id_type': 'trakt_dict'})
	maxsize = min(len(process_list), int(kodi_utils.get_setting('pov.max_threads', '100')))
	for p, tag in enumerate(process_list, 1):
		mtype = tag['type']
		if   mtype == 'movie':
			process_dict['movies'] += 1
			_queue.put((movies.build_movie_content, p, tag[mtype]['ids']))
		elif mtype == 'show':
			process_dict['tvshows'] += 1
			_queue.put((tvshows.build_tvshow_content, p, tag[mtype]['ids']))
		elif mtype == 'episode':
			process_dict['episodes'] += 1
			params = {'media_ids': {'tmdb': tag['show']['ids']['tmdb']}, 'season': tag['episode']['season'], 'episode': tag['episode']['number']}
			_queue.put((episodes.build_episode_content, p, params))
		elif mtype == 'season':
			process_dict['seasons'] += 1
			params = {'tmdb_id': tag['show']['ids']['tmdb'], 'season': tag['season']['number'], 'sort': p}
			_queue.put((seasons.build_season_list, params))
	threads = [Thread(target=_thread_target, args=(_queue,)) for i in range(maxsize)]
	[i.start() for i in threads]
	[i.join() for i in threads]
	items = movies.items + tvshows.items + episodes.items + seasons.items
	items.sort(key=lambda k: int(k[1].getProperty('pov_sort_order')))
	content, total = max(process_dict.items(), key=lambda k: k[1])
	if total_pages > 2 and not is_widget and nav_jump_use_alphabet():
		url = {'mode': 'build_navigate_to_page', 'transfer_mode': 'build_trakt_list', 'media_type': 'Media', 'name': name,
				'user': user, 'slug': slug, 'list_id': list_id, 'current_page': page, 'total_pages': total_pages, 'list_type': list_type}
		kodi_utils.add_dir(__handle__, url, jump2_str, iconImage=item_jump, isFolder=False)
	kodi_utils.add_items(__handle__, items)
	if total_pages > page:
		url = {'mode': 'build_trakt_list', 'user': user, 'slug': slug, 'name': name, 'list_id': list_id,
				'new_page': page + 1, 'new_letter': letter, 'list_type': list_type}
		kodi_utils.add_dir(__handle__, url, nextpage_str)
	kodi_utils.set_category(__handle__, name)
	kodi_utils.set_content(__handle__, content)
	kodi_utils.end_directory(__handle__, False if is_widget else None)
	kodi_utils.set_view_mode('view.%s' % content, content)

def trakt_account_info():
	from datetime import timedelta
	try:
		kodi_utils.show_busy_dialog()
		account_info = trakt_api.call_trakt('users/settings', with_auth=True)
		stats = trakt_api.call_trakt('users/%s/stats' % account_info['user']['ids']['slug'], with_auth=True)
		username = account_info['user']['username']
		timezone = account_info['account']['timezone']
		joined = jsondate_to_datetime(account_info['user']['joined_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
		private = account_info['user']['private']
		vip = account_info['user']['vip']
		if vip: vip = '%s Years' % str(account_info['user']['vip_years'])
		total_given_ratings = stats['ratings']['total']
		movies_collected = stats['movies']['collected']
		movies_watched = stats['movies']['watched']
		movie_minutes = stats['movies']['minutes']
		if movie_minutes == 0: movies_watched_minutes = ['0 days', '0:00:00']
		elif movie_minutes < 1440: movies_watched_minutes = ['0 days', '{:0>8}'.format(str(timedelta(minutes=movie_minutes)))]
		else: movies_watched_minutes = ('{:0>8}'.format(str(timedelta(minutes=movie_minutes)))).split(', ')
		movies_watched_minutes = ('%s %s hours %s minutes' % (movies_watched_minutes[0], movies_watched_minutes[1].split(':')[0], movies_watched_minutes[1].split(':')[1]))
		shows_collected = stats['shows']['collected']
		shows_watched = stats['shows']['watched']
		episodes_watched = stats['episodes']['watched']
		episode_minutes = stats['episodes']['minutes']
		if episode_minutes == 0: episodes_watched_minutes = ['0 days', '0:00:00']
		elif episode_minutes < 1440: episodes_watched_minutes = ['0 days', '{:0>8}'.format(str(timedelta(minutes=episode_minutes)))]
		else: episodes_watched_minutes = ('{:0>8}'.format(str(timedelta(minutes=episode_minutes)))).split(', ')
		episodes_watched_minutes = ('%s %s hours %s minutes' % (episodes_watched_minutes[0], episodes_watched_minutes[1].split(':')[0], episodes_watched_minutes[1].split(':')[1]))
		body = []
		append = body.append
		append('[B]Username:[/B] %s' % username)
		append('[B]Timezone:[/B] %s' % timezone)
		append('[B]Joined:[/B] %s' % joined)
		append('[B]Private:[/B] %s' % private)
		append('[B]VIP Status:[/B] %s' % vip)
		append('[B]Ratings Given:[/B] %s' % str(total_given_ratings))
		append('[B]Movies:[/B] [B]%s[/B] Collected, [B]%s[/B] Watched for [B]%s[/B]' % (movies_collected, movies_watched, movies_watched_minutes))
		append('[B]Shows:[/B] [B]%s[/B] Collected, [B]%s[/B] Watched' % (shows_collected, shows_watched))
		append('[B]Episodes:[/B] [B]%s[/B] Watched for [B]%s[/B]' % (episodes_watched, episodes_watched_minutes))
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text(ls(32037).upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

