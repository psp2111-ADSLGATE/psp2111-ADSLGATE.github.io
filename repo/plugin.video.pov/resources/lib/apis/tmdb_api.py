import requests
from caches.main_cache import cache_object
from caches.meta_cache import cache_function
from modules.settings import tmdb_api_key, get_language
# from modules.kodi_utils import logger

EXPIRES_4_HOURS, EXPIRES_2_DAYS, EXPIRES_1_WEEK, EXPIRES_1_MONTH = 4, 48, 168, 672
movies_append = 'external_ids,videos,credits,release_dates,alternative_titles,translations,images'
tvshows_append = 'external_ids,videos,credits,content_ratings,alternative_titles,translations,images'
base_url = 'https://api.themoviedb.org/3'
timeout = 3.05
session = requests.Session()
retry = requests.adapters.Retry(total=None, status=1, status_forcelist=(429, 502, 503, 504), raise_on_status=False)
session.mount(base_url, requests.adapters.HTTPAdapter(pool_maxsize=100, max_retries=retry))

def get_tmdb(url):
	try:
		response = session.get(url, timeout=timeout)
		response.raise_for_status()
	except requests.exceptions.RequestException as e:
		from modules.kodi_utils import logger
		logger('tmdb error', f"{e}\n{e.request.url}\n{e.response.text}")
	response.encoding = 'utf-8'
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
		return get_tmdb(url).json()
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

