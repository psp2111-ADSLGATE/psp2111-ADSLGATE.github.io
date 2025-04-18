import json
import requests
from threading import Thread
from caches.main_cache import cache_object
from caches.meta_cache import cache_function
from modules import kodi_utils
from modules.settings import tmdb_api_key, get_language, show_unaired_watchlist, ignore_articles, lists_sort_order, paginate, page_limit
from modules.utils import paginate_list, sort_for_article, jsondate_to_datetime, get_datetime, chunks, TaskPool

EXPIRES_4_HOURS, EXPIRES_2_DAYS, EXPIRES_1_WEEK, EXPIRES_1_MONTH = 4, 48, 168, 672
ls, logger, js2date = kodi_utils.local_string, kodi_utils.logger, jsondate_to_datetime
get_setting, set_setting = kodi_utils.get_setting, kodi_utils.set_setting
movies_append = 'external_ids,videos,credits,release_dates,alternative_titles,translations,images'
tvshows_append = 'external_ids,videos,credits,content_ratings,alternative_titles,translations,images'
eps_map = {1: 'Original air date', 2: 'Absolute', 3: 'DVD', 4: 'Digital', 5: 'Story arc', 6: 'Production', 7: 'TV'}
tmdb_image_base = 'https://image.tmdb.org/t/p/%s%s'
base_url = 'https://api.themoviedb.org/3'
timeout = 3.05
session = requests.Session()
retry = requests.adapters.Retry(total=None, status=1, status_forcelist=(429, 502, 503, 504))
session.mount('https://api.themoviedb.org', requests.adapters.HTTPAdapter(pool_maxsize=100, max_retries=retry))

def get_tmdb(url, errors=True):
	try:
		response = session.get(url, timeout=timeout)
		if not response.ok: response.raise_for_status()
	except requests.exceptions.RequestException as e:
		if errors: logger('tmdb error', str(e))
	return response

def tmdb_keyword_id(query):
	string = 'tmdb_keyword_id_%s' % query
	url = '%s/search/keyword?api_key=%s&query=%s' % (base_url, tmdb_api_key(), query)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_company_id(query):
	string = 'tmdb_company_id_%s' % query
	url = '%s/search/company?api_key=%s&query=%s' % (base_url, tmdb_api_key(), query)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_media_images(media_type, tmdb_id):
	if media_type == 'movies': media_type = 'movie'
	string = 'tmdb_media_images_%s_%s' % (media_type, tmdb_id)
	url = '%s/%s/%s/images?api_key=%s' % (base_url, media_type, tmdb_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_media_videos(media_type, tmdb_id):
	if media_type == 'movies': media_type = 'movie'
	if media_type in ('tvshow', 'tvshows'): media_type = 'tv'
	string = 'tmdb_media_videos_%s_%s' % (media_type, tmdb_id)
	url = '%s/%s/%s/videos?api_key=%s' % (base_url, media_type, tmdb_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_movies_discover(query, page_no):
	string = query % page_no
	url = query % page_no
	return cache_object(get_tmdb, string, url)

def tmdb_movies_collection(collection_id):
	string = 'tmdb_movies_collection_%s' % collection_id
	url = '%s/collection/%s?api_key=%s&language=en-US' % (base_url, collection_id, tmdb_api_key())
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_movies_title_year(title, year=None):
	if year:
		string = 'tmdb_movies_title_year_%s_%s' % (title, year)
		url = '%s/search/movie?api_key=%s&language=en-US&query=%s&year=%s' % (base_url, tmdb_api_key(), title, year)
	else:
		string = 'tmdb_movies_title_year_%s' % title
		url = '%s/search/movie?api_key=%s&language=en-US&query=%s' % (base_url, tmdb_api_key(), title)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_MONTH)

def tmdb_movies_popular(page_no):
	string = 'tmdb_movies_popular_%s' % page_no
	url = '%s/movie/popular?api_key=%s&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_blockbusters(page_no):
	string = 'tmdb_movies_blockbusters_%s' % page_no
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US&sort_by=revenue.desc&page=%s' % (base_url, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_in_theaters(page_no):
	string = 'tmdb_movies_in_theaters_%s' % page_no
	url = '%s/movie/now_playing?api_key=%s&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_premieres(page_no):
	current_date, previous_date = get_dates(31, reverse=True)
	string = 'tmdb_movies_premieres_%s' % page_no
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&release_date.gte=%s&release_date.lte=%s&with_release_type=1|3|2&page=%s' % (previous_date, current_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_latest_releases(page_no):
	current_date, previous_date = get_dates(31, reverse=True)
	string = 'tmdb_movies_latest_releases_%s' % page_no
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&release_date.gte=%s&release_date.lte=%s&with_release_type=4|5&page=%s' % (previous_date, current_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_upcoming(page_no):
	current_date, future_date = get_dates(31, reverse=False)
	string = 'tmdb_movies_upcoming_%s' % page_no
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&release_date.gte=%s&release_date.lte=%s&with_release_type=3|2|1&page=%s' % (current_date, future_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_genres(genre_id, page_no):
	string = 'tmdb_movies_genres_%s_%s' % (genre_id, page_no)
	url = '%s/discover/movie?api_key=%s&with_genres=%s&language=en-US&region=US&sort_by=popularity.desc&page=%s' % (base_url, tmdb_api_key(), genre_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_languages(language, page_no):
	string = 'tmdb_movies_languages_%s_%s' % (language, page_no)
	url = '%s/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&with_original_language=%s&page=%s' % (base_url, tmdb_api_key(), language, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_certifications(certification, page_no):
	string = 'tmdb_movies_certifications_%s_%s' % (certification, page_no)
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&certification_country=US&certification=%s&page=%s' % (certification, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_year(year, page_no):
	string = 'tmdb_movies_year_%s_%s' % (year, page_no)
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&certification_country=US&primary_release_year=%s&page=%s' % (year, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_networks(network_id, page_no):
	string = 'tmdb_movies_networks_%s_%s' % (network_id, page_no)
	url = '%s/discover/movie?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&certification_country=US&with_companies=%s&page=%s' % (network_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_similar(tmdb_id, page_no):
	string = 'tmdb_movies_similar_%s_%s' % (tmdb_id, page_no)
	url = '%s/movie/%s/similar?api_key=%s&language=en-US&page=%s' % (base_url, tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_recommendations(tmdb_id, page_no):
	string = 'tmdb_movies_recommendations_%s_%s' % (tmdb_id, page_no)
	url = '%s/movie/%s/recommendations?api_key=%s&language=en-US&page=%s' % (base_url, tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_movies_search(query, page_no):
	string = 'tmdb_movies_search_%s_%s' % (query, page_no)
	url = '%s/search/movie?api_key=%s&language=en-US&query=%s&page=%s' % (base_url, tmdb_api_key(), query, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_4_HOURS)

def tmdb_movies_search_collections(query, page_no):
	string = 'tmdb_movies_search_collections_%s_%s' % (query, page_no)
	url = '%s/search/collection?api_key=%s&language=en-US&query=%s&page=%s' % (base_url, tmdb_api_key(), query, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_tv_discover(query, page_no):
	string = url = query % page_no
	return cache_object(get_tmdb, string, url)

def tmdb_tv_title_year(title, year=None):
	if year:
		string = 'tmdb_tv_title_year_%s_%s' % (title, year)
		url = '%s/search/tv?api_key=%s&query=%s&first_air_date_year=%s&language=en-US' % (base_url, tmdb_api_key(), title, year)
	else:
		string = 'tmdb_tv_title_year_%s' % title
		url = '%s/search/tv?api_key=%s&query=%s&language=en-US' % (base_url, tmdb_api_key(), title)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_MONTH)

def tmdb_tv_popular(page_no):
	string = 'tmdb_tv_popular_%s' % page_no
#	url = '%s/tv/popular?api_key=%s&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
#	url = '%s/tv/popular?api_key=%s&with_original_language=en&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	url = '%s/discover/tv?api_key=%s&with_original_language=en&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	url += '&sort_by=popularity.desc&without_genres=10763,10767'
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_premieres(page_no):
	current_date, previous_date = get_dates(31, reverse=True)
	string = 'tmdb_tv_premieres_%s' % page_no
#	url = '%s/discover/tv?api_key=%s&language=en-US&region=US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (base_url, tmdb_api_key(), previous_date, current_date, page_no)
	url = '%s/discover/tv?api_key=%s&with_original_language=en&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (previous_date, current_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_airing_today(page_no):
	string = 'tmdb_tv_airing_today_%s' % page_no
#	url = '%s/tv/airing_today?api_key=%s&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	url = '%s/tv/airing_today?api_key=%s&with_original_language=en&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_4_HOURS)

def tmdb_tv_on_the_air(page_no):
	string = 'tmdb_tv_on_the_air_%s' % page_no
#	url = '%s/tv/on_the_air?api_key=%s&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	url = '%s/tv/on_the_air?api_key=%s&with_original_language=en&language=en-US&region=US&page=%s' % (base_url, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_upcoming(page_no):
	current_date, future_date = get_dates(31, reverse=False)
	string = 'tmdb_tv_upcoming_%s' % page_no
#	url = '%s/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (base_url, tmdb_api_key(), current_date, future_date, page_no)
	url = '%s/discover/tv?api_key=%s&with_original_language=en&language=en-US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (current_date, future_date, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_genres(genre_id, page_no):
	string = 'tmdb_tv_genres_%s_%s' % (genre_id, page_no)
	url = '%s/discover/tv?api_key=%s' % (base_url, tmdb_api_key())
	url += '&with_genres=%s&sort_by=popularity.desc&include_null_first_air_dates=false&page=%s' % (genre_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_languages(language, page_no):
	string = 'tmdb_tv_languages_%s_%s' % (language, page_no)
	url = '%s/discover/tv?api_key=%s&language=en-US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language=%s&page=%s' % (language, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_year(year, page_no):
	string = 'tmdb_tv_year_%s_%s' % (year, page_no)
	url = '%s/discover/tv?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&include_null_first_air_dates=false&first_air_date_year=%s&page=%s' % (year, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_networks(network_id, page_no):
	string = 'tmdb_tv_networks_%s_%s' % (network_id, page_no)
	url = '%s/discover/tv?api_key=%s&language=en-US&region=US' % (base_url, tmdb_api_key())
	url += '&sort_by=popularity.desc&include_null_first_air_dates=false&with_networks=%s&page=%s' % (network_id, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_similar(tmdb_id, page_no):
	string = 'tmdb_tv_similar_%s_%s' % (tmdb_id, page_no)
	url = '%s/tv/%s/similar?api_key=%s&language=en-US&page=%s' % (base_url, tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_recommendations(tmdb_id, page_no):
	string = 'tmdb_tv_recommendations_%s_%s' % (tmdb_id, page_no)
	url = '%s/tv/%s/recommendations?api_key=%s&language=en-US&page=%s' % (base_url, tmdb_id, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_2_DAYS)

def tmdb_tv_search(query, page_no):
	string = 'tmdb_tv_search_%s_%s' % (query, page_no)
	url = '%s/search/tv?api_key=%s&language=en-US&query=%s&page=%s' % (base_url, tmdb_api_key(), query, page_no)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_4_HOURS)

def tmdb_popular_people(page_no):
	string = 'tmdb_popular_people_%s' % page_no
	url = '%s/person/popular?api_key=%s&language=en-US&page=%s' % (base_url, tmdb_api_key(), page_no)
	return cache_object(get_tmdb, string, url)

def tmdb_people_full_info(actor_id, language=None):
	if not language: language = get_language()
	string = 'tmdb_people_full_info_%s_%s' % (actor_id, language)
	url = '%s/person/%s?api_key=%s&language=%s&append_to_response=external_ids,combined_credits,images,tagged_images' % (base_url, actor_id, tmdb_api_key(), language)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_1_WEEK)

def tmdb_people_info(query):
	string = 'tmdb_people_info_%s' % query
	url = '%s/search/person?api_key=%s&language=en-US&query=%s' % (base_url, tmdb_api_key(), query)
	return cache_object(get_tmdb, string, url, expiration=EXPIRES_4_HOURS)['results']

def get_dates(days, reverse=True):
	import datetime
	current_date = datetime.date.today()
	if reverse: new_date = (current_date - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
	else: new_date = (current_date + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
	return str(current_date), new_date

def movie_details(tmdb_id, language, tmdb_api=None):
	try:
		url = '%s/movie/%s?api_key=%s&language=%s&append_to_response=%s' % (base_url, tmdb_id, get_tmdb_api(tmdb_api), language, movies_append)
		return get_tmdb(url).json()
	except: return None

def tvshow_details(tmdb_id, language, tmdb_api=None):
	try:
		url = '%s/tv/%s?api_key=%s&language=%s&append_to_response=%s' % (base_url, tmdb_id, get_tmdb_api(tmdb_api), language, tvshows_append)
		return get_tmdb(url).json()
	except: return None

def season_episodes_details(tmdb_id, season_no, language, tmdb_api=None):
	try:
		url = '%s/tv/%s/season/%s?api_key=%s&language=%s&append_to_response=credits' % (base_url, tmdb_id, season_no, get_tmdb_api(tmdb_api), language)
		return get_tmdb(url, False).json()
	except: return None

def movie_external_id(external_source, external_id, tmdb_api=None):
	try:
		string = 'movie_external_id_%s_%s' % (external_source, external_id)
		url = '%s/find/%s?api_key=%s&external_source=%s' % (base_url, external_id, get_tmdb_api(tmdb_api), external_source)
		result = cache_function(get_tmdb, string, url, EXPIRES_1_MONTH)
		result = result['movie_results']
		if result: return result[0]
		else: return None
	except: return None

def tvshow_external_id(external_source, external_id, tmdb_api=None):
	try:
		string = 'tvshow_external_id_%s_%s' % (external_source, external_id)
		url = '%s/find/%s?api_key=%s&external_source=%s' % (base_url, external_id, get_tmdb_api(tmdb_api), external_source)
		result = cache_function(get_tmdb, string, url, EXPIRES_1_MONTH)
		result = result['tv_results']
		if result: return result[0]
		else: return None
	except: return None

def movie_title_year(title, year, tmdb_api=None):
	try:
		string = 'movie_title_year_%s_%s' % (title, year)
		url = '%s/search/movie?api_key=%s&query=%s&year=%s&page=%s' % (base_url, get_tmdb_api(tmdb_api), title, year)
		result = cache_function(get_tmdb, string, url, EXPIRES_1_MONTH)
		result = result['results']
		if result: return result[0]
		else: return None
	except: return None

def tvshow_title_year(title, year, tmdb_api=None):
	try:
		string = 'tvshow_title_year_%s_%s' % (title, year)
		url = '%s/search/tv?api_key=%s&query=%s&first_air_date_year=%s' % (base_url, get_tmdb_api(tmdb_api), title, year)
		result = cache_function(get_tmdb, string, url, EXPIRES_1_MONTH)
		result = result['results']
		if result: return result[0]
		else: return None
	except: return None

def english_translation(media_type, tmdb_id, tmdb_api=None):
	try:
		string = 'english_translation_%s_%s' % (media_type, tmdb_id)
		url = '%s/%s/%s/translations?api_key=%s' % (base_url, media_type, tmdb_id, get_tmdb_api(tmdb_api))
		result = cache_function(get_tmdb, string, url, 8760)['']
		try: result = result['translations']
		except: result = None
		return result
	except: return None

def get_tmdb_api(tmdb_api):
	return tmdb_api or tmdb_api_key()

def episode_groups(tmdb_id, tmdb_api=None):
	string = 'tmdb_episode_group_%s' % tmdb_id
	url = '%s/tv/%s/episode_groups?api_key=%s' % (base_url, tmdb_id, get_tmdb_api(tmdb_api))
	result = cache_function(get_tmdb, string, url, EXPIRES_1_WEEK)
	for i in result['results']: i['type'] = eps_map[i['type']]
	result = result['results']
	return result

def episode_group_details(group_id, tmdb_api=None):
	try:
		string = 'tmdb_episode_group_details_%s' % group_id
		url = '%s/tv/episode_group/%s?api_key=%s' % (base_url, group_id, get_tmdb_api(tmdb_api))
		result = cache_function(get_tmdb, string, url, EXPIRES_1_WEEK)
		result = sorted(result['groups'], key=lambda k: k['order'])
		return result
	except: return []

def tmdb_watchlist(media_type, page, letter):
	title, premiered = ('name', 'first_air_date') if media_type == 'tv' else ('title', 'release_date')
	original_list = all_items(watchlist, media_type)
	if not show_unaired_watchlist():
		current_date = get_datetime()
		str_format = '%Y-%m-%d'
		original_list = [i for i in original_list if i.get(premiered) and js2date(i.get(premiered), str_format, remove_time=True) <= current_date]
	sort_key = lists_sort_order('watchlist')
	if   sort_key == 2: original_list.sort(key=lambda k: k[premiered], reverse=True)
	elif sort_key == 1: pass # api call for list specifies params created_at.desc
	else: original_list = sort_for_article(original_list, title, ignore_articles())
	if paginate():
		limit = page_limit()
		final_list, total_pages = paginate_list(original_list, page, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def tmdb_favorite(media_type, page, letter):
	original_list = all_items(favorite, media_type)
	if paginate():
		limit = page_limit()
		final_list, total_pages = paginate_list(original_list, page, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def tmdb_recommendations(media_type, page, dummy):
	original_list = recommendations(media_type, page)
	final_list, total_pages = original_list['results'], original_list['total_pages']
	return final_list, total_pages

def add_to_watchlist_favorite(item, list_type):
	session_account_id = get_setting('tmdb.session_account_id')
	session_id = get_setting('tmdb.session_id')
	if not (session_account_id and session_id):
		try: session_account_id, session_id = convert_to_session_id()
		except: pass
	if not (session_account_id and session_id): return {'success': False}
	params = {'session_id': session_id}
	url = '%s/account/%s/%s' % (base_url, session_account_id, list_type)
	return list_request(url, params=params, data=item, method='post')

list_obj = {'description': '', 'name': '', 'iso_3166_1': 'US', 'iso_639_1': 'en', 'public': True}
list_url = 'https://api.themoviedb.org/4'
list_heading = 'TMDB Lists'

def list_request(url, params=None, data=None, method='get'):
	access_token = get_setting('tmdb.token')
	headers = {'Authorization': f"Bearer {access_token}"}
	try:
		response = session.request(
			method,
			url,
			params=params,
			json=data,
			headers=headers,
			timeout=timeout ** 2 if not method in ('get',) else timeout
		)
		response.raise_for_status()
		results = response.json()
		return results
	except requests.exceptions.RequestException as e:
		logger('tmdb error', str(e))

def _account_id(func):
	def wrapper(*args, **kwargs):
		kwargs['account_id'] = kwargs.get('account_id') or get_setting('tmdb.account_id')
		result = func(*args, **kwargs)
		return result
	return wrapper

def all_items(func, *args):
	def _process(f, *a):
		r = f(*a)
		results[a[-1]] = r['results']
		return r['total_pages']
	results, page, total_pages = {}, 1, 1
	total_pages = _process(func, *args, page)
	threads = TaskPool(40).tasks(_process, [(func, *args, i) for i in range(page + 1, total_pages + 1)], Thread)
	[i.join() for i in threads]
	results = [item for items in sorted(results.items()) for item in items[1]]
	return results

def user_lists_all():
	sort = int(get_setting('tmdblist.sort_name', '0'))
	results = all_items(user_lists)
	try:
		if   sort == 2: results.sort(key=lambda k: k['updated_at'], reverse=True)
		elif sort == 1: results.sort(key=lambda k: k['number_of_items'], reverse=True)
		else: results.sort(key=lambda k: k['name'].lower(), reverse=False)
	except: pass
	return results

def list_details(list_id, page=1):
	string = 'tmdblist_detail_%s_%s' % (list_id, page)
	url = '%s/list/%s?page=%s' % (list_url, list_id, page)
	return cache_object(list_request, string, url, json=False)

def list_add_items(list_id, items=None):
	url = '%s/list/%s/items' % (list_url, list_id)
	return list_request(url, data=items, method='post')

def list_remove_items(list_id, items=None):
	url = '%s/list/%s/items' % (list_url, list_id)
	return list_request(url, data=items, method='delete')

def list_update(list_id, data):
	url = '%s/list/%s' % (list_url, list_id)
	return list_request(url, data=data, method='put')

def list_status(list_id, media_type, media_id):
	params = {'media_type': media_type, 'media_id': int(media_id)}
	url = '%s/list/%s/item_status' % (list_url, list_id)
	return list_request(url, params=params)

def list_create(item):
	url = '%s/list' % list_url
	return list_request(url, data=item, method='post')

def list_clear(list_id):
	url = '%s/list/%s/clear' % (list_url, list_id)
	return list_request(url)

def list_delete(list_id):
	url = '%s/list/%s' % (list_url, list_id)
	return list_request(url, method='delete')

@_account_id
def user_lists(page=1, account_id=''):
	string = 'tmdblist_user_lists_%s' % page
	url = '%s/account/%s/lists?page=%s' % (list_url, account_id, page)
	return cache_object(list_request, string, url, json=False)

@_account_id
def watchlist(media_type, page=1, account_id=''):
	string = 'tmdblist_watchlist_%s_%s_%s' % (account_id, media_type, page)
	url = '%s/account/%s/%s/watchlist' % (list_url, account_id, media_type)
	url += '?page=%slanguage=en-US&sort_by=created_at.desc' % page
	return cache_object(list_request, string, url, json=False)

@_account_id
def favorite(media_type, page=1, account_id=''):
	string = 'tmdblist_favorite_%s_%s_%s' % (account_id, media_type, page)
	url = '%s/account/%s/%s/favorites' % (list_url, account_id, media_type)
	url += '?page=%slanguage=en-US&sort_by=created_at.desc' % page
	return cache_object(list_request, string, url, json=False)

@_account_id
def recommendations(media_type, page=1, account_id=''):
	string = 'tmdblist_recommendations_%s_%s_%s' % (account_id, media_type, page)
	url = '%s/account/%s/%s/recommendations' % (list_url, account_id, media_type)
	url += '?page=%slanguage=en-US' % page
	return cache_object(list_request, string, url, json=False)

def tmdb_clean_watchlist(silent=False):
	if not get_setting('tmdb.token'): return
	if not silent and not kodi_utils.confirm_dialog(): return
	try:
		from caches.watched_cache import get_watched_items, get_in_progress_tvshows
		watchlist_ids = []
		watchlist_ids += all_items(watchlist, 'movie')
		watchlist_ids += all_items(watchlist, 'tv')
		watchlist_ids = [str(i['id']) for i in watchlist_ids]
		m = get_watched_items('movie', 1, 'None', False)
		t = get_watched_items('tvshow', 1, 'None', False)
		p = get_in_progress_tvshows('tvshow', 1, 'None', False)
		items = []
		items += [
			{'watchlist': False, 'media_type': 'movie', 'media_id': i['media_id']}
			for i in m[0] if i['media_id'] in watchlist_ids
		]
		items += [
			{'watchlist': False, 'media_type': 'tv', 'media_id': i['media_id']}
			for i in t[0] + p[0] if i['media_id'] in watchlist_ids
		]
		if not items: return '0 items to remove.'
		threads = TaskPool(40).tasks(add_to_watchlist_favorite, [(i, 'watchlist') for i in items], Thread)
		[i.join() for i in threads]
		clear_tmdbl_cache()
		if not silent: kodi_utils.notification(32576)
		return '%d items removed.' % len(items)
	except: pass

def convert_to_session_id(token=None):
	if not get_setting('tmdb.token') and not token: return
	read_token, access_token = get_setting('tmdb_read_token'), token or get_setting('tmdb.token')
	headers = {'Authorization': f"Bearer {read_token}"}
	data = {'access_token': access_token}
	url = 'https://api.themoviedb.org/3/authentication/session/convert/4'
	response = requests.post(url, data=data, headers=headers, timeout=timeout)
	result = response.json()
	if not result['success']: return
	session_id = result['session_id']
	params = {'session_id': session_id}
	url = 'https://api.themoviedb.org/3/account'
	response = requests.get(url, params=params, headers=headers, timeout=timeout)
	result = response.json()
	if not 'id' in result: return
	username, session_account_id = str(result['username']), str(result['id'])
	set_setting('tmdb.username', username)
	set_setting('tmdb.session_id', session_id)
	set_setting('tmdb.session_account_id', session_account_id)
	return session_account_id, session_id

def authorize():
	read_token = get_setting('tmdb_read_token')
	headers = {'Authorization': f"Bearer {read_token}"}
	url = 'https://api.themoviedb.org/4/auth/request_token'
	response = requests.post(url, headers=headers, timeout=timeout)
	result = response.json()
	if not result['success']: return
	url = 'https://www.themoviedb.org/auth/access?request_token=%s' % result['request_token']
	qr_url = '&data=%s' % requests.utils.quote(url)
	qr_icon = 'https://api.qrserver.com/v1/create-qr-code/?size=256x256&qzone=1%s' % qr_url
	tiny_url = 'http://tinyurl.com/api-create.php'
	try: tiny_url = requests.get(tiny_url, params={'url': url}, timeout=timeout).text
	except: pass
	logger('tmdblist', '%s\n%s' % (tiny_url, url))
	line2 = ls(32700) % tiny_url
	choices = [
		('none', 'Use the QR Code to approve access at TMDB', 'Step 1: %s' % line2),
		('approve', 'Access approved at TMDB', 'Step 2'),
		('cancel', 'Cancel', 'Cancel')
	]
	list_items = [{'line1': item[1], 'line2': item[2], 'icon': qr_icon} for item in choices]
	kwargs = {'items': json.dumps(list_items), 'heading': list_heading, 'multi_line': 'true'}
	choice = kodi_utils.select_dialog([i[0] for i in choices], **kwargs)
	if choice != 'approve': return
	data = {'request_token': result['request_token']}
	url = 'https://api.themoviedb.org/4/auth/access_token'
	response = requests.post(url, json=data, headers=headers, timeout=timeout)
	result = response.json()
	if not result['success']: return kodi_utils.notification(32574)
	account_id, access_token = str(result['account_id']), str(result['access_token'])
	set_setting('tmdb.account_id', account_id)
	set_setting('tmdb.token', access_token)
	kodi_utils.notification('%s %s' % (ls(32576), list_heading))
	convert_to_session_id(access_token)

def deauthorize():
	read_token, access_token = get_setting('tmdb_read_token'), get_setting('tmdb.token')
	headers = {'Authorization': f"Bearer {read_token}"}
	data = {'access_token': access_token}
	url = 'https://api.themoviedb.org/4/auth/access_token'
	response = requests.delete(url, json=data, headers=headers, timeout=timeout)
	result = response.json()
	if not result['success']: return kodi_utils.notification(32574)
	set_setting('tmdb.account_id', '')
	set_setting('tmdb.token', '')
	kodi_utils.notification('%s %s' % (ls(32576), list_heading))
	clear_tmdbl_cache()
	session_id = get_setting('tmdb.session_id')
	data = {'session_id': session_id}
	url = 'https://api.themoviedb.org/3/authentication/session'
	response = requests.delete(url, json=data, headers=headers, timeout=timeout)
	result = response.json()
	if not result['success']: return
	set_setting('tmdb.session_account_id', '')
	set_setting('tmdb.session_id', '')
	set_setting('tmdb.username', '')

def clear_tmdbl_cache(silent=False):
	maincache_db = kodi_utils.maincache_db
	try:
		if not kodi_utils.path_exists(maincache_db): return True
		dbcon = kodi_utils.database.connect(maincache_db, timeout=40.0, isolation_level=None)
		dbcur = dbcon.cursor()
		dbcur.execute("""PRAGMA synchronous = OFF""")
		dbcur.execute("""PRAGMA journal_mode = OFF""")
		dbcur.execute("""SELECT id FROM maincache WHERE id LIKE ?""", ('tmdblist_%',))
		tmdb_results = [str(i[0]) for i in dbcur.fetchall()]
		if not tmdb_results: return True
		dbcur.execute("""DELETE FROM maincache WHERE id LIKE ?""", ('tmdblist_%',))
		for i in tmdb_results: kodi_utils.clear_property(i)
		return True
	except: return False

def import_trakt_watchlist(dummy):
	if not kodi_utils.confirm_dialog(): return
	def _process(group, count):
		add_to_watchlist_favorite(group, 'watchlist')
		progressBG.update(int(count / len_items * 100), send_str)
	from apis.trakt_api import trakt_fetch_collection_watchlist
	send_str = 'Sending items to TMDB Watchlist...'
	try:
		progressBG = kodi_utils.progressDialogBG
		progressBG.create(send_str, list_heading)
		items = []
		for i in (('movie', 'movie'), ('show', 'tv')):
			try: items += [
					{'collected_at': item['collected_at'], 'watchlist': True, 'media_type': i[1], 'media_id': item['media_ids']['tmdb']}
					for item in trakt_fetch_collection_watchlist('watchlist', i[0]) if 'tmdb' in item['media_ids']
				]
			except: pass
		if not items: return kodi_utils.notification(32760)
		try: items.sort(key=lambda k: k['collected_at'], reverse=False)
		except: pass
		len_items = len(items)
		threads = TaskPool(40).tasks(_process, [(i[1], i[0]) for i in enumerate(items, 1)], Thread)
		[i.join(3/4) for i in threads]
		clear_tmdbl_cache()
		kodi_utils.notification('List sent to TMDB')
	except: kodi_utils.notification(32574)
	finally: progressBG.close()

def import_trakt_list(params):
	from apis.trakt_api import get_trakt_list_contents
	send_str = 'Sending items to TMDB Watchlist...'
	try:
		progressBG = kodi_utils.progressDialogBG
		progressBG.create(send_str, list_heading)
		list_id, user, slug = params['trakt_list_id'], params['user'], params['list_slug']
		items = get_trakt_list_contents(params.get('list_type'), list_id, user, slug)
		len_items, wait = len(items), sum(1000 for i in chunks(items, 500))
		for count, item in enumerate(items, 1):
			kodi_utils.sleep(int(wait / len_items))
			if (mtype := item['type']) in ('movie', 'show') and 'tmdb' in item[mtype]['ids']:
				if not item[mtype]['ids']['tmdb']: continue
				item['export'] = {'media_type': 'tv' if mtype == 'show' else mtype, 'media_id': item[mtype]['ids']['tmdb']}
			else: item['export'] = None
			progressBG.update(int(count / len_items * 100), send_str)
		items = {'items': [i['export'] for i in items if i['export']]}
		Thread(target=list_add_items, args=(params['list_id'], items)).start()
		clear_tmdbl_cache()
		kodi_utils.notification('List sent to TMDB')
	except: kodi_utils.notification(32574)
	finally: progressBG.close()

def import_mdbl_list(params):
	from apis.mdblist_api import mdb_list_items
	send_str = 'Sending list to TMDB...'
	try:
		progressBG = kodi_utils.progressDialogBG
		progressBG.create(send_str, list_heading)
		items = mdb_list_items(params['mdbl_list_id'], None)
		len_items, wait = len(items), sum(1000 for i in chunks(items, 500))
		for count, item in enumerate(items, 1):
			kodi_utils.sleep(int(wait / len_items))
			if (mtype := item['mediatype']) in ('movie', 'show') and item['id']:
				item['export'] = {'media_type': 'tv' if mtype == 'show' else mtype, 'media_id': item['id']}
			else: item['export'] = None
			progressBG.update(int(count / len_items * 100), send_str)
		items = {'items': [i['export'] for i in items if i['export']]}
		Thread(target=list_add_items, args=(params['list_id'], items)).start()
		clear_tmdbl_cache()
		kodi_utils.notification('List sent to TMDB')
	except: kodi_utils.notification(32574)
	finally: progressBG.close()

