import requests
from caches.main_cache import cache_object
from caches.meta_cache import cache_function
from modules import kodi_utils, settings, utils

EXPIRES_1_HOURS = 1
base_url = 'https://api.mdblist.com'
list_json = 'https://mdblist.com/lists/%s/%s/json'
review_provider_id = {1: 'Trakt', 2: 'TMDb', 3: 'RT', 4: 'Metacritics'}
timeout = 3.05
session = requests.Session()
retry = requests.adapters.Retry(total=None, status=1, status_forcelist=(429, 502, 503, 504))
session.mount(base_url, requests.adapters.HTTPAdapter(pool_maxsize=100, max_retries=retry))

def call_mdblist(path, params=None, json=None, method=None):
	params = params or {}
	if 'api' in path: params['apikey'] = kodi_utils.get_setting('mdblist.token')
	try:
		response = session.request(
			method or 'get',
			path,
			params=params,
			json=json,
			timeout=timeout
		)
		response.raise_for_status()
	except requests.exceptions.RequestException as e: kodi_utils.logger('mdblist error',
		f"{e}\n{e.response.text if response else e.request.url}")
	try: result = response.json()
	except: result = []
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

def mdb_list_items(list_id, slug, user, list_type):
	index = settings.lists_sort_order('mdblist')
	if list_type: params = (
		{'sort': 'title', 'order': 'asc'},
		{'sort': 'added', 'order': 'desc'},
		{'sort': 'released', 'order': 'desc'}
	)[index]
	else: params = None
	url = list_json % (user, slug) # /json endpoint only way to get combined movies/shows list sort correct
	results = call_mdblist(url, params=params)
	if list_type and not index: # /json endpoint always returns desc order
		ignore_articles = settings.ignore_articles()
		results.sort(key=lambda k: utils.title_key(k['title'], ignore_articles), reverse=False)
	return results

def mdb_modify_list(list_id, params, action='add'):
	key = 'shows' if params['media_type'] == 'tvshow' else 'movies'
	val = [{'tmdb': params.get('tmdb_id'), 'imdb': params.get('imdb_id')}]
	url = '%s/lists/%s/items/%s' % (base_url, list_id, action)
	results = call_mdblist(url, json={key: val}, method='post')
	if 'detail' in results: kodi_utils.notification(results['detail'])
	if 'added' in results and results['added'][key]: return True
	else: return False

def mdb_media_info(imdb_id, media_type):
	if not kodi_utils.get_setting('mdblist.token'): return
	media_type = 'show' if media_type == 'tvshow' else 'movie'
	string = 'mdb_%s_id_%s' % (media_type, imdb_id)
	url = '%s/%s/%s/%s?append_to_response=review' % (base_url, 'imdb', media_type, imdb_id)
	return cache_function(call_mdblist, string, url, json=False)

