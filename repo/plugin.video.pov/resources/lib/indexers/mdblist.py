import sys
from queue import SimpleQueue
from threading import Thread
from apis import mdblist_api
from indexers.movies import Movies
from indexers.tvshows import TVShows
from modules import kodi_utils
from modules.utils import paginate_list, TaskPool
from modules.settings import paginate, page_limit, nav_jump_use_alphabet
# logger = kodi_utils.logger

KODI_VERSION, ls = kodi_utils.get_kodi_version(), kodi_utils.local_string
build_url, make_listitem = kodi_utils.build_url, kodi_utils.make_listitem
default_icon = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/mdblist.png')
fanart = kodi_utils.translate_path('special://home/addons/plugin.video.pov/fanart.png')
item_jump = kodi_utils.translate_path('special://home/addons/plugin.video.pov/resources/media/item_jump.png')
add2menu_str, add2folder_str, copy2str = ls(32730), ls(32731), '[B]Export to TMDB[/B]'
nextpage_str, jump2_str = ls(32799), ls(32964)

def search_mdb_lists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				name, user, slug, list_id = item['name'], item['user_name'], item['slug'], item['id']
				likes, item_count = item['likes'] or 0, item.get('items', '?')
				display = '[B]%s[/B] | [I](x%s) - %s[/I]' % (name.upper(), str(item_count), user)
				plot = '[B]Likes[/B]: %s' % likes
				url = build_url({'mode': 'build_mdb_list', 'user': user, 'slug': slug, 'list_id': list_id, 'name': name})
				cm_append((add2menu_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': 'mdblist.png'})))
				cm_append((add2folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': 'mdblist.png'})))
				cm_append((copy2str, 'RunPlugin(%s)' % build_url({'mode': 'tmdb_manager_choice', 'mdbl_list_id': list_id, 'mdbl_list_name': name, 'user': user, 'list_slug': slug})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon})
				listitem.setInfo('video', {'plot': plot}) if KODI_VERSION < 20 else listitem.getVideoInfoTag().setPlot(plot)
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	page = params.get('new_page', '1')
	search_title = params.get('search_title', None) or kodi_utils.dialog.input('POV')
	if search_title: lists, pages = mdblist_api.mdb_searchlists(search_title), '1'
	else: lists, pages = [], page
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_process()))
	if int(pages) > int(page):
		url = {'mode': 'build_mdb_list.search_mdb_lists', 'search_title': search_title, 'new_page': int(page) + 1}
		kodi_utils.add_dir(__handle__, url, nextpage_str)
	kodi_utils.set_category(__handle__, search_title)
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def get_mdb_lists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				name, user, slug, list_id = item['name'], item['user_name'], item['slug'], item['id']
				likes, item_count = item['likes'] or 0, item.get('items', '?')
				display = '%s (x%s)' % (name, item_count) if item_count else name
				plot, cln_str = '[B]Likes[/B]: %s' % likes, '[B]Clean List[/B]'
				if item.get('private'): display = '[COLOR cyan][I]%s[/I][/COLOR]' % display
				elif item.get('dynamic'): display = '[COLOR magenta][I]%s[/I][/COLOR]' % display
				url = build_url({'mode': 'build_mdb_list', 'user': user, 'slug': slug, 'list_id': list_id, 'list_type': 'user_lists', 'name': name})
				cm_append((add2menu_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': display, 'iconImage': 'mdblist.png'})))
				cm_append((add2folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': display, 'iconImage': 'mdblist.png'})))
				cm_append((copy2str, 'RunPlugin(%s)' % build_url({'mode': 'tmdb_manager_choice', 'mdbl_list_id': list_id, 'mdbl_list_name': name, 'user': user, 'list_slug': slug})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon})
				listitem.setInfo('video', {'plot': plot}) if KODI_VERSION < 20 else listitem.getVideoInfoTag().setPlot(plot)
				listitem.addContextMenuItems(cm, replaceItems=False)
				yield (url, listitem, True)
			except: pass
	lists = mdblist_api.mdb_userlists()
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_category(__handle__, params.get('name'))
	kodi_utils.set_sort_method(__handle__, 'label')
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def get_mdb_toplists(params):
	def _process():
		for item in lists:
			try:
				cm = []
				cm_append = cm.append
				name, user, slug, list_id = item['name'], item['user_name'], item['slug'], item['id']
				likes, item_count = item['likes'], item.get('items', '?')
				display = '[B]%s[/B] | [I](x%s) - %s[/I]' % (name, item_count, user)
				plot = '[B]Likes[/B]: %s' % likes
				url = build_url({'mode': 'build_mdb_list', 'user': user, 'slug': slug, 'list_id': list_id, 'name': name})
				cm_append((add2menu_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.add_external', 'name': name, 'iconImage': 'mdblist.png'})))
				cm_append((add2folder_str, 'RunPlugin(%s)' % build_url({'mode': 'menu_editor.shortcut_folder_add_item', 'name': name, 'iconImage': 'mdblist.png'})))
				cm_append((copy2str, 'RunPlugin(%s)' % build_url({'mode': 'tmdb_manager_choice', 'mdbl_list_id': list_id, 'mdbl_list_name': name, 'user': user, 'list_slug': slug})))
				listitem = make_listitem()
				listitem.setLabel(display)
				listitem.setArt({'icon': default_icon, 'poster': default_icon, 'thumb': default_icon, 'fanart': fanart, 'banner': default_icon})
				listitem.setInfo('video', {'plot': plot}) if KODI_VERSION < 20 else listitem.getVideoInfoTag().setPlot(plot)
				listitem.addContextMenuItems(cm)
				yield (url, listitem, True)
			except: pass
	lists = mdblist_api.mdb_toplists()
	__handle__ = int(sys.argv[1])
	kodi_utils.add_items(__handle__, list(_process()))
	kodi_utils.set_category(__handle__, params.get('name'))
	kodi_utils.set_content(__handle__, 'files')
	kodi_utils.end_directory(__handle__)
	kodi_utils.set_view_mode('view.main')

def build_mdb_list(params):
	def _thread_target(q):
		while not q.empty():
			try: target, *args = q.get() ; target(*args)
			except: pass
	__handle__, _queue, is_widget = int(sys.argv[1]), SimpleQueue(), kodi_utils.external_browse()
	max_threads = int(kodi_utils.get_setting('pov.max_threads', '100'))
	user, slug, name = params.get('user'), params.get('slug'), params.get('name')
	list_type, list_id = params.get('list_type'), params.get('list_id')
	letter, page = params.get('new_letter', 'None'), int(params.get('new_page', '1'))
	results = mdblist_api.mdb_list_items(list_id, list_type)
	if paginate() and results: process_list, total_pages = paginate_list(results, page, letter, page_limit())
	else: process_list, total_pages = results, 1
	movies, tvshows = Movies({'id_type': 'trakt_dict'}), TVShows({'id_type': 'trakt_dict'})
	for idx, tag in enumerate(process_list, 1):
		mtype = tag['mediatype']
		if   mtype == 'movie':
			_queue.put((movies.build_movie_content, idx, {'imdb': tag['imdb_id'], 'tmdb': tag['id']}))
		elif mtype == 'show':
			_queue.put((tvshows.build_tvshow_content, idx, {'imdb': tag['imdb_id'], 'tmdb': tag['id']}))
	max_threads = min(_queue.qsize(), max_threads)
	threads = (Thread(target=_thread_target, args=(_queue,)) for i in range(max_threads))
	threads = list(TaskPool.process(threads))
	[i.join() for i in threads]
	items = movies.items + tvshows.items
	items.sort(key=lambda k: int(k[1].getProperty('pov_sort_order')))
	content, total = max(
		('movies', movies), ('tvshows', tvshows), key=lambda k: len(k[1].items)
	)
	if total_pages > 2 and not is_widget and nav_jump_use_alphabet():
		url = {'mode': 'build_navigate_to_page', 'transfer_mode': 'build_mdb_list', 'media_type': 'Media', 'name': name,
				'user': user, 'slug': slug, 'list_id': list_id, 'current_page': page, 'total_pages': total_pages, 'list_type': list_type}
		kodi_utils.add_dir(__handle__, url, jump2_str, iconImage=item_jump, isFolder=False)
	kodi_utils.add_items(__handle__, items)
	if total_pages > page:
		url = {'mode': 'build_mdb_list', 'user': user, 'slug': slug, 'name': name, 'list_id': list_id,
				'new_page': page + 1, 'new_letter': letter, 'list_type': list_type}
		kodi_utils.add_dir(__handle__, url, nextpage_str)
	kodi_utils.set_category(__handle__, name)
	kodi_utils.set_content(__handle__, content)
	kodi_utils.end_directory(__handle__, False if is_widget else None)
	kodi_utils.set_view_mode('view.%s' % content, content)

