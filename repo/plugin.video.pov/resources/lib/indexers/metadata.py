from apis import tmdb_api as tmdb, fanarttv_api as fanarttv
from caches.meta_cache import MetaCache
from modules.utils import jsondate_to_datetime, subtract_dates, make_thread_list
# from modules.kodi_utils import logger

movie_data, tvshow_data, english_translation = tmdb.movie_details, tmdb.tvshow_details, tmdb.english_translation
movie_external, tvshow_external, season_episodes_details = tmdb.movie_external_id, tmdb.tvshow_external_id, tmdb.season_episodes_details
default_fanarttv_data, fanarttv_get, fanarttv_add = fanarttv.default_fanart_nometa, fanarttv.get, fanarttv.add
subtract_dates_function, jsondate_to_datetime_function = subtract_dates, jsondate_to_datetime
backup_resolutions, writer_credits = {'poster': 'w780', 'fanart': 'w1280', 'still': 'original', 'profile': 'h632'}, ('Author', 'Writer', 'Screenplay', 'Characters')
alt_titles_test, trailers_test, finished_show_check, empty_value_check = ('US', 'GB', 'UK', ''), ('Trailer', 'Teaser'), ('Ended', 'Canceled'), ('', 'None', None)
tmdb_image_base, youtube_url, date_format = 'https://image.tmdb.org/t/p/%s%s', 'plugin://plugin.video.youtube/play/?video_id=%s', '%Y-%m-%d'
EXPIRES_2_DAYS, EXPIRES_4_DAYS, EXPIRES_7_DAYS, EXPIRES_14_DAYS, EXPIRES_182_DAYS = 2, 4, 7, 14, 182

def movie_meta(id_type, media_id, user_info, current_date):
	if id_type == 'trakt_dict':
		if media_id.get('tmdb', None): id_type, media_id = 'tmdb_id', media_id['tmdb']
		elif media_id.get('imdb', None): id_type, media_id = 'imdb_id', media_id['imdb']
		else: id_type, media_id = None, None
	if media_id is None: return {}
	metacache = MetaCache()
	metacache_get, metacache_set = metacache.get, metacache.set
	fanarttv_data, language, extra_fanart_enabled, fanart_client_key = None, user_info['language'], user_info['extra_fanart_enabled'], user_info['fanart_client_key']
	meta = metacache_get('movie', id_type, media_id)
	if meta:
		if 'tmdb_id' in meta:
			if not meta.get('fanart_added', False) and extra_fanart_enabled:
				meta = fanarttv_add('movies', language, meta['tmdb_id'], fanart_client_key, meta)
				metacache_set('movie', id_type, meta, movie_expiry(current_date, meta))
			return meta
		else: fanarttv_data = dict(meta)
	try:
		tmdb_api = user_info['tmdb_api']
		if id_type == 'tmdb_id' or id_type == 'imdb_id': data = movie_data(media_id, language, tmdb_api)
		else:
			external_result = movie_external(id_type, media_id, tmdb_api)
			if not external_result: data = None
			else: data = movie_data(external_result['id'], language, tmdb_api)
		if not data or data.get('success', True) is False:
			if id_type == 'tmdb_id': meta = {'tmdb_id': media_id, 'imdb_id': 'tt0000000', 'tvdb_id': '0000000', 'fanart_added': True, 'blank_entry': True}
			else: meta = {'tmdb_id': '0000000', 'imdb_id': media_id, 'tvdb_id': '0000000', 'fanart_added': True, 'blank_entry': True}
			metacache_set('movie', id_type, meta, EXPIRES_2_DAYS)
			return meta
		if language != 'en':
			if data['overview'] in empty_value_check:
				media_id, id_type = data['id'], 'tmdb_id'
				eng_data = movie_data(media_id, 'en', tmdb_api)
				eng_overview = eng_data['overview']
				data['overview'] = eng_overview
				if 'videos' in data:
					all_trailers = data['videos']['results']
					if all_trailers:
						try: trailer_test = [i for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test]
						except: trailer_test = False
					else: trailer_test = False
				else: trailer_test = False
				if not trailer_test:
					if 'videos' in eng_data:
						eng_all_trailers = eng_data['videos']['results']
						if eng_all_trailers:
							data['videos']['results'] = eng_all_trailers
		if not fanarttv_data and extra_fanart_enabled: fanarttv_data = fanarttv_get('movies', language, data['id'], fanart_client_key)
		meta = build_movie_meta(data, user_info, fanarttv_data)
		metacache_set('movie', id_type, meta, movie_expiry(current_date, meta))
	except: pass
	return meta

def tvshow_meta(id_type, media_id, user_info, current_date):
	if id_type == 'trakt_dict':
		if media_id.get('tmdb', None): id_type, media_id = 'tmdb_id', media_id['tmdb']
		elif media_id.get('imdb', None): id_type, media_id = 'imdb_id', media_id['imdb']
		elif media_id.get('tvdb', None): id_type, media_id = 'tvdb_id', media_id['tvdb']
		else: id_type, media_id = None, None
	if media_id is None: return {}
	metacache = MetaCache()
	metacache_get, metacache_set = metacache.get, metacache.set
	fanarttv_data, language, extra_fanart_enabled, fanart_client_key = None, user_info['language'], user_info['extra_fanart_enabled'], user_info['fanart_client_key']
	meta = metacache_get('tvshow', id_type, media_id)
	if meta:
		if 'tmdb_id' in meta:
			if not meta.get('fanart_added', False) and extra_fanart_enabled:
				meta = fanarttv_add('tv', language, meta['tvdb_id'], fanart_client_key, meta)
				metacache_set('tvshow', id_type, meta, tvshow_expiry(current_date, meta))
			return meta
		else: fanarttv_data = dict(meta)
	try:
		tmdb_api = user_info['tmdb_api']
		if id_type == 'tmdb_id':
			data = tvshow_data(media_id, language, tmdb_api)
		else:
			external_result = tvshow_external(id_type, media_id, tmdb_api)
			if not external_result: data = None
			else: data = tvshow_data(external_result['id'], language, tmdb_api)
		if not data or data.get('success', True) is False:
			if id_type == 'tmdb_id': meta = {'tmdb_id': media_id, 'imdb_id': 'tt0000000', 'tvdb_id': '0000000', 'fanart_added': True, 'blank_entry': True}
			elif id_type == 'imdb_id': meta = {'tmdb_id': '0000000', 'imdb_id': media_id, 'tvdb_id': '0000000', 'fanart_added': True, 'blank_entry': True}
			else: meta = {'tmdb_id': '0000000', 'imdb_id': 'tt0000000', 'tvdb_id': media_id, 'fanart_added': True, 'blank_entry': True}
			metacache_set('tvshow', id_type, meta, EXPIRES_2_DAYS)
			return meta
		if language != 'en':
			if data['overview'] in empty_value_check:
				media_id, id_type = data['id'], 'tmdb_id'
				eng_data = tvshow_data(media_id, 'en', tmdb_api)
				eng_overview = eng_data['overview']
				data['overview'] = eng_overview
				if 'videos' in data:
					all_trailers = data['videos']['results']
					if all_trailers:
						try: trailer_test = [i for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test]
						except: trailer_test = False
					else: trailer_test = False
				else: trailer_test = False
				if not trailer_test:
					if 'videos' in eng_data:
						eng_all_trailers = eng_data['videos']['results']
						if eng_all_trailers:
							data['videos']['results'] = eng_all_trailers
		if not fanarttv_data and extra_fanart_enabled: fanarttv_data = fanarttv_get('tv', language, data['external_ids']['tvdb_id'], fanart_client_key)
		meta = build_tvshow_meta(data, user_info, fanarttv_data)
		metacache_set('tvshow', id_type, meta, tvshow_expiry(current_date, meta))
	except: pass
	return meta

def season_episodes_meta(season, meta, user_info):
	metacache = MetaCache()
	metacache_get, metacache_set = metacache.get, metacache.set
	media_id, data = meta['tmdb_id'], None
	string = '%s_%s' % (media_id, season)
	data = metacache_get('season', 'tmdb_id', string)
	if data: return data
	try:
		if meta['status'] in finished_show_check or meta['total_seasons'] > int(season): expiration = EXPIRES_182_DAYS
		else: expiration = EXPIRES_4_DAYS
		image_resolution = user_info.get('image_resolution', backup_resolutions)
		data = season_episodes_details(media_id, season, user_info['language'], user_info['tmdb_api'])['episodes']
		data = build_episodes_meta(data, image_resolution)
		metacache_set('season', 'tmdb_id', data, expiration, string)
	except: pass
	return data

def all_episodes_meta(meta, user_info, Thread):
	def _get_tmdb_episodes(season):
		try: data.extend(season_episodes_meta(season, meta, user_info))
		except: pass
	try:
		data = []
#		threads = [Thread(target=_get_tmdb_episodes, args=(i['season_number'],)) for i in meta['season_data']]
#		[i.start() for i in threads]
		threads = list(make_thread_list(_get_tmdb_episodes, (i['season_number'] for i in meta['season_data']), Thread))
		[i.join() for i in threads]
	except: pass
	return data

def build_episodes_meta(data, image_resolution):
	def _process():
		for ep_data in data:
			writer, director, guest_stars = '', '', []
			ep_data_get = ep_data.get
			title, plot, premiered = ep_data_get('name'), ep_data_get('overview'), ep_data_get('air_date')
			season, episode = ep_data_get('season_number'), ep_data_get('episode_number')
			rating, votes, still_path = ep_data_get('vote_average'), ep_data_get('vote_count'), ep_data_get('still_path', None)
			if still_path: thumb = tmdb_image_base % (still_resolution, still_path)
			else: thumb = None
			guest_stars_list = ep_data_get('guest_stars', None)
			if guest_stars_list:
				try: guest_stars = [
					{'name': i['name'], 'role': i['character'], 'thumbnail': tmdb_image_base % (profile_resolution, i['profile_path']) if i['profile_path'] else ''}
					for i in guest_stars_list
				]
				except: pass
			crew = ep_data_get('crew', None)
			if crew:
				try: writer = ', '.join([i['name'] for i in crew if i['job'] in writer_credits])
				except: pass
				try: director = [i['name'] for i in crew if i['job'] == 'Director'][0]
				except: pass
			yield {'writer': writer, 'director': director, 'guest_stars': guest_stars, 'mediatype': 'episode', 'title': title, 'plot': plot,
					'premiered': premiered, 'season': season, 'episode': episode, 'rating': rating, 'votes': votes, 'thumb': thumb}
	still_resolution, profile_resolution = image_resolution['still'], image_resolution['profile']
	return list(_process())

def movie_meta_external_id(external_source, external_id):
	return movie_external(external_source, external_id)

def tvshow_meta_external_id(external_source, external_id):
	return tvshow_external(external_source, external_id)

def english_translation(media_type, media_id, user_info):
	key = 'title' if media_type == 'movie' else 'name'
	translations = english_translation(media_type, media_id, user_info['tmdb_api'])
	try: english = [i['data'][key] for i in translations if i['iso_639_1'] == 'en'][0]
	except: english = ''
	return english

def movie_expiry(current_date, meta):
	try:
		difference = subtract_dates_function(current_date, jsondate_to_datetime_function(meta['premiered'], date_format, remove_time=True))
		if difference < 0: expiration = abs(difference) + 1
		elif difference <= 14: expiration = EXPIRES_7_DAYS
		elif difference <= 30: expiration = EXPIRES_14_DAYS
		else: expiration = EXPIRES_182_DAYS
	except: return EXPIRES_7_DAYS
	return max(expiration, EXPIRES_7_DAYS)

def tvshow_expiry(current_date, meta):
	try:
		if meta['status'] in finished_show_check: return EXPIRES_182_DAYS
		next_episode_to_air = meta['extra_info'].get('next_episode_to_air', None)
		if not next_episode_to_air: return EXPIRES_7_DAYS
		expiration = subtract_dates_function(jsondate_to_datetime_function(next_episode_to_air['air_date'], date_format, remove_time=True), current_date)
	except: return EXPIRES_4_DAYS
	return max(expiration, EXPIRES_4_DAYS)

def build_movie_meta(data, user_info, fanarttv_data=None):
	image_resolution = user_info.get('image_resolution', backup_resolutions)
	data_get = data.get
	cast, all_trailers, country, country_codes = [], [], [], []
	writer, mpaa, director, trailer, studio = '', '', '', '', ''
	tmdb_id, imdb_id = data_get('id', ''), data_get('imdb_id', '')
	rating, votes = data_get('vote_average', ''), data_get('vote_count', '')
	plot, tagline, premiered = data_get('overview', ''), data_get('tagline', ''), data_get('release_date', '')
	poster_path, backdrop_path = data_get('poster_path', None), data_get('backdrop_path', None)
	if poster_path: poster = tmdb_image_base % (image_resolution['poster'], poster_path)
	else: poster = ''
	if backdrop_path: fanart = tmdb_image_base % (image_resolution['fanart'], backdrop_path)
	else: fanart = ''
	try: tmdblogo_path = [i['file_path'] for i in data_get('images')['logos'] if 'file_path' in i if i['file_path'].endswith('png')][0]
	except: tmdblogo_path = None
	if tmdblogo_path: tmdblogo = tmdb_image_base % (image_resolution['fanart'], tmdblogo_path)
	else: tmdblogo = ''
	title, original_title = data_get('title'), data_get('original_title')
	try: english_title = [i['data']['title'] for i in data_get('translations')['translations'] if i['iso_639_1'] == 'en'][0]
	except: english_title = None
	try: year = str(data_get('release_date').split('-')[0])
	except: year = ''
	try: duration = int(data_get('runtime', '90') * 60)
	except: duration = 0
	try: genre = ', '.join([i['name'] for i in data_get('genres')])
	except: genre == []
	rootname = '%s (%s)' % (title, year)
	companies = data_get('production_companies')
	if companies:
		if len(companies) == 1: studio = [i['name'] for i in companies][0]
		else:
			try: studio = [i['name'] for i in companies if i['logo_path'] not in empty_value_check][0] or [i['name'] for i in companies][0]
			except: pass
	production_countries = data_get('production_countries', None)
	if production_countries:
		country = [i['name'] for i in production_countries]
		country_codes = [i['iso_3166_1'] for i in production_countries]
	release_dates = data_get('release_dates')
	if release_dates:
		try: mpaa = [
			x['certification']
			for i in release_dates['results']
			for x in i['release_dates']
			if i['iso_3166_1'] == 'US' and x['certification'] != '' and x['note'] == ''
		][0]
		except: pass
	credits = data_get('credits')
	if credits:
		all_cast = credits.get('cast', None)
		if all_cast:
			try: cast = [
				{'name': i['name'], 'role': i['character'], 'thumbnail': tmdb_image_base % (image_resolution['profile'], i['profile_path'])if i['profile_path'] else ''}
				for i in all_cast
			]
			except: pass
		crew = credits.get('crew', None)
		if crew:
			try: writer = ', '.join([i['name'] for i in crew if i['job'] in writer_credits])
			except: pass
			try: director = [i['name'] for i in crew if i['job'] == 'Director'][0]
			except: pass
	alternative_titles = data_get('alternative_titles', None)
	if alternative_titles:
		alternatives = alternative_titles['titles']
		alternative_titles = [i['title'] for i in alternatives if i['iso_3166_1'] in alt_titles_test]
	videos = data_get('videos', None)
	if videos:
		all_trailers = videos['results']
		try: trailer = [youtube_url % i['key'] for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test][0]
		except: pass
	status, homepage = data_get('status', 'N/A'), data_get('homepage', 'N/A')
	belongs_to_collection = data_get('belongs_to_collection')
	if belongs_to_collection: ei_collection_name, ei_collection_id = belongs_to_collection['name'], belongs_to_collection['id']
	else: ei_collection_name, ei_collection_id = None, None
	try: ei_budget = '${:,}'.format(data_get('budget'))
	except: ei_budget = '$0'
	try: ei_revenue = '${:,}'.format(data_get('revenue'))
	except: ei_revenue = '$0'
	extra_info = {'status': status, 'collection_name': ei_collection_name, 'collection_id': ei_collection_id, 'budget': ei_budget, 'revenue': ei_revenue, 'homepage': homepage}
	meta_dict = {'tmdb_id': tmdb_id, 'imdb_id': imdb_id, 'rating': rating, 'tagline': tagline, 'votes': votes, 'premiered': premiered, 'imdbnumber': imdb_id, 'trailer': trailer,
				'poster': poster, 'fanart': fanart, 'genre': genre, 'title': title, 'original_title': original_title, 'english_title': english_title, 'year': year, 'cast': cast,
				'duration': duration, 'rootname': rootname, 'country': country, 'country_codes': country_codes, 'mpaa': mpaa,'writer': writer, 'all_trailers': all_trailers,
				'director': director, 'alternative_titles': alternative_titles, 'plot': plot, 'studio': studio, 'extra_info': extra_info, 'mediatype': 'movie', 'tvdb_id': 'None',
				'tmdblogo': tmdblogo}
	if fanarttv_data: meta_dict.update(fanarttv_data)
	else: meta_dict.update(default_fanarttv_data)
	return meta_dict

def build_tvshow_meta(data, user_info, fanarttv_data=None):
	image_resolution = user_info.get('image_resolution', backup_resolutions)
	data_get = data.get
	cast, all_trailers, country, country_codes = [], [], [], []
	writer, mpaa, director, trailer, studio = '', '', '', '', ''
	external_ids = data_get('external_ids')
	tmdb_id, imdb_id, tvdb_id = data_get('id', ''), external_ids.get('imdb_id', ''), external_ids.get('tvdb_id', 'None')
	rating, votes = data_get('vote_average', ''), data_get('vote_count', '')
	plot, tagline, premiered = data_get('overview', ''), data_get('tagline', ''), data_get('first_air_date', '')
	season_data, total_seasons, total_aired_eps = data_get('seasons'), data_get('number_of_seasons'), data_get('number_of_episodes')
	poster_path, backdrop_path = data_get('poster_path', None), data_get('backdrop_path', None)
	if poster_path: poster = tmdb_image_base % (image_resolution['poster'], poster_path)
	else: poster = ''
	if backdrop_path: fanart = tmdb_image_base % (image_resolution['fanart'], backdrop_path)
	else: fanart = ''
	try: tmdblogo_path = [i['file_path'] for i in data_get('images')['logos'] if 'file_path' in i if i['file_path'].endswith('png')][0]
	except: tmdblogo_path = None
	if tmdblogo_path: tmdblogo = tmdb_image_base % (image_resolution['fanart'], tmdblogo_path)
	else: tmdblogo = ''
	title, original_title = data_get('name'), data_get('original_name')
	try: english_title = [i['data']['name'] for i in data_get('translations')['translations'] if i['iso_639_1'] == 'en'][0]
	except: english_title = None
	try: year = str(data_get('first_air_date').split('-')[0]) or ''
	except: year = ''
	try: duration = min(data_get('episode_run_time')) * 60
	except: duration = 0
	try: genre = ', '.join([i['name'] for i in data_get('genres')])
	except: genre = []
	rootname = '%s (%s)' % (title, year)
	networks = data_get('networks', None)
	if networks:
		if len(networks) == 1: studio = [i['name'] for i in networks][0]
		else:
			try: studio = [i['name'] for i in networks if i['logo_path'] not in empty_value_check][0] or [i['name'] for i in networks][0]
			except: pass
	production_countries = data_get('production_countries', None)
	if production_countries:
		country = [i['name'] for i in production_countries]
		country_codes = [i['iso_3166_1'] for i in production_countries]
	content_ratings = data_get('content_ratings', None)
	release_dates = data_get('release_dates', None)
	if content_ratings:
		try: mpaa = [i['rating'] for i in content_ratings['results'] if i['iso_3166_1'] == 'US'][0]
		except: pass
	elif release_dates:
		try: mpaa = [i['release_dates'][0]['certification'] for i in release_dates['results'] if i['iso_3166_1'] == 'US'][0]
		except: pass
	credits = data_get('credits')
	if credits:
		all_cast = credits.get('cast', None)
		if all_cast:
			try: cast = [
				{'name': i['name'], 'role': i['character'], 'thumbnail': tmdb_image_base % (image_resolution['profile'], i['profile_path']) if i['profile_path'] else ''}
				for i in all_cast
			]
			except: pass
		crew = credits.get('crew', None)
		if crew:
			try: writer = ', '.join([i['name'] for i in crew if i['job'] in writer_credits])
			except: pass
			try: director = [i['name'] for i in crew if i['job'] == 'Director'][0]
			except: pass
	alternative_titles = data_get('alternative_titles', None)
	if alternative_titles:
		alternatives = alternative_titles['results']
		alternative_titles = [i['title'] for i in alternatives if i['iso_3166_1'] in alt_titles_test]
	videos = data_get('videos', None)
	if videos:
		all_trailers = videos['results']
		try: trailer = [youtube_url % i['key'] for i in all_trailers if i['site'] == 'YouTube' and i['type'] in trailers_test][0]
		except: pass
	status, _type, homepage = data_get('status', 'N/A'), data_get('type', 'N/A'), data_get('homepage', 'N/A')
	created_by = data_get('created_by', None)
	if created_by:
		try: ei_created_by = ', '.join([i['name'] for i in created_by])
		except: ei_created_by = 'N/A'
	else: ei_created_by = 'N/A'
	ei_next_ep = data_get('next_episode_to_air', None)
	ei_last_ep = data_get('last_episode_to_air', None)
	if ei_last_ep and not status in finished_show_check:
		total_aired_eps = sum([
			i['episode_count']
			for i in season_data
			if i['season_number'] < ei_last_ep['season_number'] and i['season_number'] != 0
		]) + ei_last_ep['episode_number']
	extra_info = {'status': status, 'type': _type, 'homepage': homepage, 'created_by': ei_created_by, 'next_episode_to_air': ei_next_ep, 'last_episode_to_air': ei_last_ep}
	meta_dict = {'tmdb_id': tmdb_id, 'tvdb_id': tvdb_id, 'imdb_id': imdb_id, 'rating': rating, 'plot': plot, 'tagline': tagline, 'votes': votes, 'premiered': premiered, 'year': year,
				'poster': poster, 'fanart': fanart, 'genre': genre, 'title': title, 'original_title': original_title, 'english_title': english_title, 'season_data': season_data,
				'alternative_titles': alternative_titles, 'duration': duration, 'rootname': rootname, 'imdbnumber': imdb_id, 'country': country, 'mpaa': mpaa, 'trailer': trailer,
				'country_codes': country_codes, 'writer': writer, 'director': director, 'all_trailers': all_trailers, 'cast': cast, 'studio': studio, 'extra_info': extra_info,
				'total_aired_eps': total_aired_eps, 'mediatype': 'tvshow', 'total_seasons': total_seasons, 'tvshowtitle': title, 'status': status,
				'tmdblogo': tmdblogo}
	if fanarttv_data: meta_dict.update(fanarttv_data)
	else: meta_dict.update(default_fanarttv_data)
	return meta_dict

