import re
import requests
from caches.main_cache import cache_object
from caches.meta_cache import cache_function
from modules import kodi_utils, settings, utils
# logger = kodi_utils.logger

EXPIRES_1_HOURS = 1
base_url = 'https://api.mdblist.com'
review_provider_id = {1: 'Trakt', 2: 'TMDb', 3: 'RT', 4: 'Metacritics'}
rank_map = {'0': 'mild', '1': 'mild', '2': 'moderate', '3': 'moderate', '4': 'severe', '5': 'severe'}
guide_map = {'Nudity': 'Sex & Nudity', 'Violence': 'Violence & Gore', 'Profanity': 'Profanity', 'Alcohol': 'Alcohol, Drugs & Smoking'}
watchlist_obj = {'name': 'Watchlist', 'slug': 'watchlist', 'id': '', 'user_name': '', 'likes': None, 'items': None}
timeout = 3.05
session = requests.Session()
retry = requests.adapters.Retry(total=None, status=1, status_forcelist=(429, 502, 503, 504))
session.mount(base_url, requests.adapters.HTTPAdapter(pool_maxsize=100, max_retries=retry))

def call_mdblist(path, params=None, json=None, method=None):
	params = params or {}
	params['apikey'] = kodi_utils.get_setting('mdblist.token')
	try:
		response = session.request(
			method or 'get',
			path,
			params=params,
			json=json,
			timeout=timeout
		)
		if not response.ok: response.raise_for_status()
		result = response.json()
	except requests.exceptions.RequestException as e:
		kodi_utils.logger('mdblist error', str(e))
		result = []
	return result

def mdb_searchlists(query):
	query = requests.utils.quote(query)
	string = 'mdb_searchlists_%s' % query
	url = '%s/lists/search?query=%s' % (base_url, query)
	return cache_object(call_mdblist, string, url, False, EXPIRES_1_HOURS)

def mdb_userlists():
	string = 'mdb_userlists'
	url = '%s/lists/user' % base_url
	return cache_object(call_mdblist, string, url, False, EXPIRES_1_HOURS)

def mdb_toplists():
	string = 'mdb_toplists'
	url = '%s/lists/top' % base_url
	return cache_object(call_mdblist, string, url, False)

def mdb_media_info(imdb_id, media_type):
	if not kodi_utils.get_setting('mdblist.token'): return
	media_type = 'show' if media_type == 'tvshow' else 'movie'
	string = 'mdb_%s_mediainfo_%s' % (media_type, imdb_id)
	url = '%s/%s/%s/%s?append_to_response=review' % (base_url, 'imdb', media_type, imdb_id)
	return cache_function(call_mdblist, string, url, json=False)

def mdb_media_info_batch(items, provider, media_type):
	url = '%s/%s/%s' % (base_url, provider, media_type)
	return call_mdblist(url, json=items, method='post')

def mdb_parentsguide(imdb_id, media_type):
	media_type = 'show' if media_type == 'tvshow' else 'movie'
	url = 'https://www.mdblist.com/%s/%s' % (media_type, imdb_id)
	string = 'mdb_%s_parentsguide_%s' % (media_type, imdb_id)
	params = {'url': url, 'action': 'mdb_parentsguide'}
	return cache_function(get_mdb, string, params, json=False)

def mdb_modify_list(list_id, data, action='add'):
	if list_id: url = '%s/lists/%s/items/%s' % (base_url, list_id, action)
	else: url = '%s/watchlist/items/%s' % (base_url, action)
	results = call_mdblist(url, json=data, method='post')
	if 'detail' in results: kodi_utils.notification(results['detail'])
	success = 'added' in results and any(results['added'][i] for i in ('movies', 'shows'))
	return True if success else False

def mdb_list_items(list_id, list_type):
	sort_index = settings.lists_sort_order('mdblist')
	ignore_articles = settings.ignore_articles()
	if list_type: params = (
			{'sort': 'title', 'order': 'asc'},
			{'sort': 'added', 'order': 'desc'},
			{'sort': 'released', 'order': 'desc'},
			{'sort': 'random'}, {'sort': 'usort'}
		)[sort_index]
	else: params = None
	if list_id: url = '%s/lists/%s/items?unified=true' % (base_url, list_id)
	else: url = '%s/watchlist/items?unified=true' % base_url
	results = call_mdblist(url, params=params)
	if list_type and ignore_articles and not sort_index:
		results.sort(key=lambda k: utils.title_key(k['title'], ignore_articles), reverse=False)
	return results

def mdblist_watchlist(media_type, page_no, letter):
	url = '%s/watchlist/items' % base_url
	original_list = call_mdblist(url)
	original_list = original_list[media_type]
	sort_key = settings.lists_sort_order('watchlist')
	if   sort_key == 2: original_list.sort(key=lambda k: k['release_year'], reverse=True)
	elif sort_key == 1: original_list.sort(key=lambda k: k['watchlist_at'], reverse=True)
	else: original_list = utils.sort_for_article(original_list, 'title', settings.ignore_articles())
	if settings.paginate():
		limit = settings.page_limit()
		final_list, total_pages = utils.paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def mdb_clean_watchlist(list_id=None, silent=False):
	if not kodi_utils.get_setting('mdblist.token'): return
	if not silent and not kodi_utils.confirm_dialog(): return
	try:
		from caches.watched_cache import get_watched_items, get_in_progress_tvshows
		m = get_watched_items('movie', 1, 'None', False)
		t = get_watched_items('tvshow', 1, 'None', False)
		p = get_in_progress_tvshows('tvshow', 1, 'None', False)
		data = {
			'movies': [{'tmdb': int(i['media_id'])} for i in m[0]],
			'shows': [{'tmdb': int(i['media_id'])} for i in t[0] + p[0]]
		}
		if not data['movies'] and not data['shows']: return
		if list_id: url = '%s/lists/%s/items/%s' % (base_url, list_id, 'remove')
		else: url = '%s/watchlist/items/%s' % (base_url, 'remove')
		call_mdblist(url, json=data, method='post')
		clear_mdbl_cache()
	except: pass

def get_mdb(params):
	results = []
	action = params['action']
	url = params['url']
	response = requests.get(url, timeout=timeout)
	if action == 'mdb_parentsguide':
		def _process():
			for key, val in guide_map.items():
				try:
					if not (match := re.search(f"{key}\:\ \d", html)): continue
					rank = rank_map[match.group().split(': ')[-1]]
					yield {'title': val, 'ranking': rank, 'listings': []}
				except: pass
		html = response.text.replace('\n', ' ')
		results = list(_process())
	return results

def clear_mdbl_cache(silent=False):
	maincache_db = kodi_utils.maincache_db
	try:
		if not kodi_utils.path_exists(maincache_db): return True
		dbcon = kodi_utils.database.connect(maincache_db, timeout=40.0, isolation_level=None)
		dbcur = dbcon.cursor()
		dbcur.execute("""PRAGMA synchronous = OFF""")
		dbcur.execute("""PRAGMA journal_mode = OFF""")
		dbcur.execute("""SELECT id FROM maincache WHERE id LIKE ?""", ('mdb_%',))
		mdb_results = [str(i[0]) for i in dbcur.fetchall()]
		if not mdb_results: return True
		dbcur.execute("""DELETE FROM maincache WHERE id LIKE ?""", ('mdb_%',))
		for i in mdb_results: kodi_utils.clear_property(i)
		return True
	except: return False

