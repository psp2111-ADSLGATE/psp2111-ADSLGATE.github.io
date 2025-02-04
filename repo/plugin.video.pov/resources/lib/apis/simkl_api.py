import requests
from threading import Thread
from caches.main_cache import cache_object
from caches.meta_cache import cache_function
from modules import kodi_utils

EXPIRES_2_DAYS = 48
API_KEY = kodi_utils.get_setting('simkl_api')
base_url = 'https://api.simkl.com'
timeout = 3.05
session = requests.Session()
retry = requests.adapters.Retry(total=None, status=1, status_forcelist=(429, 502, 503, 504))
session.mount(base_url, requests.adapters.HTTPAdapter(pool_maxsize=100, max_retries=retry))

def call_simkl(url):
	params = {'client_id': API_KEY} if API_KEY else None
	try:
		response = session.get(url, params=params, timeout=timeout)
		response.raise_for_status()
	except requests.exceptions.RequestException as e: kodi_utils.logger('simkl error',
		f"{e}\n{e.response.text if response else e.request.url}")
	try: result = response.json()
	except: result = []
	return result

def simkl_list(url):
	try:
		result = call_simkl(url)
		if result is None: return
	except: return
	items = []
	threads = []
	for item_position, item in enumerate(result):
		i = Thread(target=summary, args=(item_position, item['ids']['simkl_id'], items))
		threads.append(i)
		i.start()
	[i.join() for i in threads]
	items.sort(key=lambda k: k['sort'])
	return items

def summary(position, sid, collector, media='anime'):
	try:
		string = 'simkl_%s_id_%s' % (media, sid)
		url = '%s/%s/%s?extended=full' % (base_url, media, sid)
		result = cache_function(call_simkl, string, url, json=False)
		if result is None: return
		imdb = result.get('ids').get('imdb') if result.get('ids').get('imdb') else ''
		tmdb = result.get('ids').get('tmdb') if result.get('ids').get('tmdb') else ''
		title = result.get('en_title') if result.get('en_title') else result.get('title')
		if tmdb or imdb: collector.append({'imdb': str(imdb), 'tmdb': str(tmdb), 'title': title, 'sort': position})
	except: pass

def simkl_movies_most_watched(page_no, media='anime'):
	string = 'simkl_movies_most_watched'
	url = '%s/%s/best/watched?type=movies' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_movies_most_voted(page_no, media='anime'):
	string = 'simkl_movies_most_voted'
	url = '%s/%s/best/voted?type=movies' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_movies_popular(page_no, media='anime'):
	string = 'simkl_movies_popular'
	url = '%s/%s/genres/all/movies/all-years/popular-this-week' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_movies_ranked(page_no, media='anime'):
	string = 'simkl_movies_ranked'
	url = '%s/%s/genres/all/movies/all-years/rank' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_movies_recent_release(page_no, media='anime'):
	string = 'simkl_movies_recent_release'
	url = '%s/%s/genres/all/movies/all-years/release-date' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_movies_genres(genre_id, media='anime'):
	string = 'simkl_movies_genres_%s' % genre_id
	url = '%s/%s/genres/%s/movies/all-years' % (base_url, media, genre_id)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_movies_year(year, media='anime'):
	string = 'simkl_movies_year_%s' % year
	url = '%s/%s/genres/all/movies/%s' % (base_url, media, year)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_most_watched(page_no, media='anime'):
	string = 'simkl_tv_most_watched'
	url = '%s/%s/best/watched?type=tv' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_most_voted(page_no, media='anime'):
	string = 'simkl_tv_most_voted'
	url = '%s/%s/best/voted?type=tv' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_popular(page_no, media='anime'):
	string = 'simkl_tv_popular'
	url = '%s/%s/genres/all/series/all-years/popular-this-week' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_ranked(page_no, media='anime'):
	string = 'simkl_tv_ranked'
	url = '%s/%s/genres/all/series/all-years/rank' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_recent_release(page_no, media='anime'):
	string = 'simkl_tv_recent_release'
	url = '%s/%s/genres/all/series/all-years/release-date' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_genres(genre_id, media='anime'):
	string = 'simkl_tv_genres_%s' % genre_id
	url = '%s/%s/genres/%s/series/all-years' % (base_url, media, genre_id)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_tv_year(year, media='anime'):
	string = 'simkl_tv_year_%s' % year
	url = '%s/%s/genres/all/series/%s' % (base_url, media, year)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_onas_most_watched(page_no, media='anime'):
	string = 'simkl_onas_most_watched'
	url = '%s/%s/best/watched?type=onas' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_onas_most_voted(page_no, media='anime'):
	string = 'simkl_onas_most_voted'
	url = '%s/%s/best/voted?type=onas' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_onas_popular(page_no, media='anime'):
	string = 'simkl_onas_popular'
	url = '%s/%s/genres/all/onas/all-years/popular-this-week' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_onas_ranked(page_no, media='anime'):
	string = 'simkl_onas_ranked'
	url = '%s/%s/genres/all/onas/all-years/rank' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

def simkl_onas_recent_release(page_no, media='anime'):
	string = 'simkl_onas_recent_release'
	url = '%s/%s/genres/all/onas/all-years/release-date' % (base_url, media)
	return cache_object(simkl_list, string, url, json=False, expiration=EXPIRES_2_DAYS)

