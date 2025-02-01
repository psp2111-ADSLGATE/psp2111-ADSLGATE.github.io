import json
from datetime import datetime
from threading import Thread
from indexers import metadata
from apis.trakt_api import trakt_watched_unwatched, trakt_official_status, trakt_progress
from caches.trakt_cache import clear_trakt_collection_watchlist_data
from modules import kodi_utils, settings, utils
# logger = kodi_utils.logger

timeout = 40
database = kodi_utils.database
WATCHED_DB = kodi_utils.watched_db
TRAKT_DB = kodi_utils.trakt_db
indicators_dict = {0: WATCHED_DB, 1: TRAKT_DB}
ls, sleep = kodi_utils.local_string, kodi_utils.sleep
progressDialogBG, execute_JSON = kodi_utils.progressDialogBG, kodi_utils.execute_JSON
metadata_user_info = settings.metadata_user_info
get_datetime, adjust_premiered_date = utils.get_datetime, utils.adjust_premiered_date
sort_for_article, make_thread_list = utils.sort_for_article, utils.make_thread_list
clean_file_name, paginate_list = utils.clean_file_name, utils.paginate_list

def get_database(watched_indicators):
	return indicators_dict[watched_indicators]

def make_database_connection(database_file):
	return database.connect(database_file, timeout=timeout, isolation_level=None)

def set_PRAGMAS(dbcon):
	dbcur = dbcon.cursor()
	dbcur.execute("""PRAGMA synchronous = OFF""")
	dbcur.execute("""PRAGMA journal_mode = OFF""")
	return dbcur

def get_next_episodes(watched_info):
	seen = set()
	watched_info = [i for i in watched_info if not i[0] is None]
	watched_info.sort(key=lambda x: (x[0], x[1], x[2]), reverse=True)
	return [
		{'media_ids': {'tmdb': int(i[0])}, 'season': int(i[1]), 'episode': int(i[2]), 'last_played': i[4]}
		for i in watched_info
		if not (i[0] in seen or seen.add(i[0]))
	]

def get_resumetime(bookmarks, tmdb_id, season='', episode=''):
	try: resume_point, curr_time, resume_id = detect_bookmark(bookmarks, tmdb_id, season, episode)
	except: resume_point, curr_time, resume_id = 0, 0, 0
	try: progress = str(int(round(float(resume_point))))
	except: progress = '0'
	try: resumetime = str(int(round(float(curr_time))))
	except: resumetime = '0'
	return resumetime, progress

def get_progress_percent(resumetime, duration):
	try: percent = str(int(round(float(resumetime)/duration*100)))
	except: percent = '0'
	return percent

def detect_bookmark(bookmarks, tmdb_id, season='', episode=''):
	return [(i[1], i[2], i[5]) for i in bookmarks if i[0] == str(tmdb_id) and i[3] == season and i[4] == episode][0]

def get_bookmarks(watched_indicators, media_type):
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		result = dbcur.execute("""SELECT media_id, resume_point, curr_time, season, episode, resume_id FROM progress WHERE db_type = ?""", (media_type,))
		return result.fetchall()
	except: pass

def set_bookmark(media_type, tmdb_id, curr_time, total_time, title, season='', episode=''):
	try:
		adjusted_current_time = float(curr_time) - 5
		resume_point = round(adjusted_current_time/float(total_time)*100,1)
		watched_indicators = settings.watched_indicators()
		if watched_indicators == 1: trakt_progress('set_progress', media_type, tmdb_id, resume_point, season, episode, refresh_trakt=True)
		else:
			erase_bookmark(media_type, tmdb_id, season, episode)
			data_base = get_database(watched_indicators)
			last_played = get_last_played_value(data_base)
			dbcon = make_database_connection(data_base)
			dbcur = set_PRAGMAS(dbcon)
			dbcur.execute("""INSERT OR REPLACE INTO progress VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
						(media_type, tmdb_id, season, episode, str(resume_point), str(curr_time), last_played, 0, title))
		if settings.sync_kodi_library_watchstatus():
#			from modules.kodi_library import set_bookmark_kodi_library
			set_bookmark_kodi_library(media_type, tmdb_id, curr_time, total_time, season, episode)
		refresh_container()
	except: pass

def erase_bookmark(media_type, tmdb_id, season='', episode='', refresh='false'):
	try:
		watched_indicators = settings.watched_indicators()
		bookmarks = get_bookmarks(watched_indicators, media_type)
		if media_type == 'episode': season, episode = int(season), int(episode)
		try: resume_id = detect_bookmark(bookmarks, tmdb_id, season, episode)[2]
		except: return
		if watched_indicators == 1: trakt_progress('clear_progress', media_type, tmdb_id, 0, season, episode, resume_id)
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.execute("""DELETE FROM progress where db_type = ? and media_id = ? and season = ? and episode = ?""", (media_type, tmdb_id, season, episode))
		refresh_container(refresh == 'true')
	except: pass

def batch_erase_bookmark(watched_indicators, insert_list, action):
	try:
		if action == 'mark_as_watched': modified_list = [(i[0], i[1], i[2], i[3]) for i in insert_list]
		else: modified_list = insert_list
		if watched_indicators == 1:
			def _process(arg):
				try: trakt_progress(*arg)
				except: pass
			process_list = []
			process_list_append = process_list.append
			media_type = insert_list[0][0]
			tmdb_id = insert_list[0][1]
			bookmarks = get_bookmarks(watched_indicators, media_type)
			for i in insert_list:
				try: resume_point, curr_time, resume_id = detect_bookmark(bookmarks, tmdb_id, i[2], i[3])
				except: continue
				process_list_append(('clear_progress', i[0], i[1], 0, i[2], i[3], resume_id))
			if process_list: threads = list(make_thread_list(_process, process_list, Thread))
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.executemany("""DELETE FROM progress where db_type = ? and media_id = ? and season = ? and episode = ?""", modified_list)
	except: pass

def get_watched_info_movie(watched_indicators):
	info = []
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.execute("""SELECT media_id, title, last_played FROM watched_status WHERE db_type = ?""", ('movie',))
		info = dbcur.fetchall()
	except: pass
	return info

def get_watched_info_tv(watched_indicators):
	info = []
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		dbcur.execute("""SELECT media_id, season, episode, title, last_played FROM watched_status WHERE db_type = ?""", ('episode',))
		info = dbcur.fetchall()
	except: pass
	return info

def get_in_progress_movies(dummy_arg, page_no, letter):
	watched_indicators = settings.watched_indicators()
	paginate = settings.paginate()
	limit = settings.page_limit()
	dbcon = make_database_connection(get_database(watched_indicators))
	dbcur = set_PRAGMAS(dbcon)
	dbcur.execute("""SELECT media_id, last_played, title FROM progress WHERE db_type = ?""", ('movie',))
	data = dbcur.fetchall()
	data = [{'media_id': i[0], 'title': i[2], 'last_played': i[1]} for i in data if not i[0] == '']
	if settings.lists_sort_order('progress') == 0: original_list = sort_for_article(data, 'title', settings.ignore_articles())
	else: original_list = sorted(data, key=lambda x: x['last_played'], reverse=True)
	if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def get_in_progress_tvshows(dummy_arg, page_no, letter):
	def _process(item):
		tmdb_id = item['media_id']
		meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
		watched_status = get_watched_status_tvshow(watched_info, tmdb_id, meta.get('total_aired_eps'))
		if watched_status[0] == 0: data_append(item)
	duplicates = set()
	duplicates_add = duplicates.add
	data = []
	data_append = data.append
	watched_indicators = settings.watched_indicators()
	paginate = settings.paginate()
	limit = settings.page_limit()
	meta_user_info = settings.metadata_user_info()
	watched_info = get_watched_info_tv(watched_indicators)
	watched_info.sort(key=lambda x: (x[0], x[4]), reverse=True)
	prelim_data = [{'media_id': i[0], 'title': i[3], 'last_played': i[4]} for i in watched_info if not (i[0] in duplicates or duplicates_add(i[0]))]
	threads = list(make_thread_list(_process, prelim_data, Thread))
	[i.join() for i in threads]
	if settings.lists_sort_order('progress') == 0: original_list = sort_for_article(data, 'title', settings.ignore_articles())
	else: original_list = sorted(data, key=lambda x: x['last_played'], reverse=True)
	if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def get_in_progress_episodes():
	watched_indicators = settings.watched_indicators()
	dbcon = make_database_connection(get_database(watched_indicators))
	dbcur = set_PRAGMAS(dbcon)
	dbcur.execute("""SELECT media_id, season, episode, resume_point, last_played, title FROM progress WHERE db_type = ?""", ('episode',))
	data = dbcur.fetchall()
	if settings.lists_sort_order('progress') == 0: data = sort_for_article(data, 5, settings.ignore_articles())
	else: data.sort(key=lambda k: k[4], reverse=True)
	episode_list = [{'media_ids': {'tmdb': i[0]}, 'season': int(i[1]), 'episode': int(i[2]), 'resume_point': float(i[3])} for i in data]
	return episode_list

def get_watched_items(media_type, page_no, letter):
	paginate = settings.paginate()
	limit = settings.page_limit()
	watched_indicators = settings.watched_indicators()
	if media_type == 'tvshow':
		def _process(item):
			tmdb_id = item['media_id']
			meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
			watched_status = get_watched_status_tvshow(watched_info, tmdb_id, meta.get('total_aired_eps'))
			if watched_status[0] == 1: data_append(item)
		watched_info = get_watched_info_tv(watched_indicators)
		meta_user_info = settings.metadata_user_info()
		duplicates = set()
		duplicates_add = duplicates.add
		data = []
		data_append = data.append
		prelim_data = [{'media_id': i[0], 'title': i[3], 'last_played': i[4]} for i in watched_info if not (i[0] in duplicates or duplicates_add(i[0]))]
		threads = list(make_thread_list(_process, prelim_data, Thread))
		[i.join() for i in threads]
	else:
		watched_info = get_watched_info_movie(watched_indicators)
		data = [{'media_id': i[0], 'title': i[1], 'last_played': i[2]} for i in watched_info]
	if settings.lists_sort_order('watched') == 0: original_list = sort_for_article(data, 'title', settings.ignore_articles())
	else: original_list = sorted(data, key=lambda x: x['last_played'], reverse=True)
	if paginate: final_list, total_pages = paginate_list(original_list, page_no, letter, limit)
	else: final_list, total_pages = original_list, 1
	return final_list, total_pages

def get_watched_status_movie(watched_info, tmdb_id):
	try:
		watched = [i for i in watched_info if i[0] == tmdb_id]
		if watched: return 1, 5
		return 0, 4
	except: return 0, 4

def get_watched_status_tvshow(watched_info, tmdb_id, aired_eps):
	playcount, overlay, watched, unwatched = 0, 4, 0, aired_eps
	try:
		watched = len([i for i in watched_info if i[0] == tmdb_id])
		unwatched = aired_eps - watched
		if watched >= aired_eps and not aired_eps == 0: playcount, overlay = 1, 5
	except: pass
	return playcount, overlay, watched, unwatched

def get_watched_status_season(watched_info, tmdb_id, season, aired_eps):
	playcount, overlay, watched, unwatched = 0, 4, 0, aired_eps
	try:
		watched = len([i for i in watched_info if i[0] == tmdb_id and i[1] == season])
		unwatched = aired_eps - watched
		if watched >= aired_eps and not aired_eps == 0: playcount, overlay = 1, 5
	except: pass
	return playcount, overlay, watched, unwatched

def get_watched_status_episode(watched_info, tmdb_id, season='', episode=''):
	try:
		watched = [i for i in watched_info if i[0] == tmdb_id and (i[1],i[2]) == (season,episode)]
		if watched: return 1, 5
		else: return 0, 4
	except: return 0, 4

def mark_as_watched_unwatched_movie(params):
	action, media_type = params.get('action'), 'movie'
	refresh, from_playback = params.get('refresh', 'true') == 'true', params.get('from_playback', 'false') == 'true'
	tmdb_id, title, year = params.get('tmdb_id'), params.get('title'), params.get('year')
	watched_indicators = settings.watched_indicators()
	if watched_indicators == 1:
		if from_playback == 'true' and trakt_official_status(media_type) is False: skip_trakt_mark = True
		else: skip_trakt_mark = False
		if skip_trakt_mark: kodi_utils.sleep(3000)
		elif not trakt_watched_unwatched(action, 'movies', tmdb_id): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', media_type)
	mark_as_watched_unwatched(watched_indicators, media_type, tmdb_id, action, title=title)
	if settings.sync_kodi_library_watchstatus():
#		from modules.kodi_library import mark_as_watched_unwatched_kodi_library
		mark_as_watched_unwatched_kodi_library(media_type, action, title, year)
	refresh_container(refresh)

def mark_as_watched_unwatched_tvshow(params):
	action, tmdb_id = params.get('action'), params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	watched_indicators = settings.watched_indicators()
	kodi_utils.progressDialogBG.create(ls(32577), '')
	if watched_indicators == 1:
		if not trakt_watched_unwatched(action, 'shows', tmdb_id, tvdb_id): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	data_base = get_database(watched_indicators)
	title, year = params.get('title', ''), params.get('year', '')
	meta_user_info = settings.metadata_user_info()
	adjust_hours = settings.date_offset()
	current_date = get_datetime()
	insert_list = []
	insert_append = insert_list.append
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
	season_data = meta['season_data']
	season_data = [i for i in season_data if i['season_number'] > 0]
	total = len(season_data)
	last_played = get_last_played_value(data_base)
	for count, item in enumerate(season_data, 1):
		season_number = item['season_number']
		ep_data = metadata.season_episodes_meta(season_number, meta, meta_user_info)
		for ep in ep_data:
			season_number = ep['season']
			ep_number = ep['episode']
			display = 'S%.2dE%.2d' % (int(season_number), int(ep_number))
			kodi_utils.progressDialogBG.update(int(float(count)/float(total)*100), ls(32577), '%s' % display)
			episode_date, premiered = adjust_premiered_date(ep['premiered'], adjust_hours)
			if not episode_date or current_date < episode_date: continue
			insert_append(make_batch_insert(action, 'episode', tmdb_id, season_number, ep_number, last_played, title))
	batch_mark_as_watched_unwatched(watched_indicators, insert_list, action)
	kodi_utils.progressDialogBG.close()
	if settings.sync_kodi_library_watchstatus(): batch_mark_kodi_library(action, insert_list, title, year)
	refresh_container()

def mark_as_watched_unwatched_season(params):
	season = int(params.get('season'))
	if season == 0: return kodi_utils.notification(32575)
	action, title, year, tmdb_id = params.get('action'), params.get('title'), params.get('year'), params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	watched_indicators = settings.watched_indicators()
	insert_list = []
	insert_append = insert_list.append
	kodi_utils.progressDialogBG.create(ls(32577), '')
	if watched_indicators == 1:
		if not trakt_watched_unwatched(action, 'season', tmdb_id, tvdb_id, season): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	data_base = get_database(watched_indicators)
	meta_user_info = settings.metadata_user_info()
	adjust_hours = settings.date_offset()
	current_date = get_datetime()
	meta = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
	ep_data = metadata.season_episodes_meta(season, meta, meta_user_info)
	last_played = get_last_played_value(data_base)
	for count, item in enumerate(ep_data, 1):
		season_number = item['season']
		ep_number = item['episode']
		display = 'S%.2dE%.2d' % (season_number, ep_number)
		episode_date, premiered = adjust_premiered_date(item['premiered'], adjust_hours)
		if not episode_date or current_date < episode_date: continue
		kodi_utils.progressDialogBG.update(int(float(count) / float(len(ep_data)) * 100), ls(32577), '%s' % display)
		insert_append(make_batch_insert(action, 'episode', tmdb_id, season_number, ep_number, last_played, title))
	batch_mark_as_watched_unwatched(watched_indicators, insert_list, action)
	kodi_utils.progressDialogBG.close()
	if settings.sync_kodi_library_watchstatus(): batch_mark_kodi_library(action, insert_list, title, year)
	refresh_container()

def mark_as_watched_unwatched_episode(params):
	action, media_type = params.get('action'), 'episode'
	refresh, from_playback = params.get('refresh', 'true') == 'true', params.get('from_playback', 'false') == 'true'
	tmdb_id = params.get('tmdb_id')
	try: tvdb_id = int(params.get('tvdb_id', '0'))
	except: tvdb_id = 0
	season, episode, title, year = int(params.get('season')), int(params.get('episode')), params.get('title'), params.get('year')
	watched_indicators = settings.watched_indicators()
	if season == 0: kodi_utils.notification(32575); return
	if watched_indicators == 1:
		if from_playback == 'true' and trakt_official_status(media_type) is False: skip_trakt_mark = True
		else: skip_trakt_mark = False
		if skip_trakt_mark: kodi_utils.sleep(3000)
		elif not trakt_watched_unwatched(action, media_type, tmdb_id, tvdb_id, season, episode): return kodi_utils.notification(32574)
		clear_trakt_collection_watchlist_data('watchlist', 'tvshow')
	mark_as_watched_unwatched(watched_indicators, media_type, tmdb_id, action, season, episode, title)
	if settings.sync_kodi_library_watchstatus():
#		from modules.kodi_library import mark_as_watched_unwatched_kodi_library
		mark_as_watched_unwatched_kodi_library(media_type, action, title, year, season, episode)
	refresh_container(refresh)

def mark_as_watched_unwatched(watched_indicators, media_type='', tmdb_id='', action='', season='', episode='', title=''):
	try:
		data_base = get_database(watched_indicators)
		last_played = get_last_played_value(data_base)
		dbcon = make_database_connection(data_base)
		dbcur = set_PRAGMAS(dbcon)
		if action == 'mark_as_watched':
			dbcur.execute("""INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)""", (media_type, tmdb_id, season, episode, last_played, title))
		elif action == 'mark_as_unwatched':
			dbcur.execute("""DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)""", (media_type, tmdb_id, season, episode))
		erase_bookmark(media_type, tmdb_id, season, episode)
	except: kodi_utils.notification(32574)

def batch_mark_as_watched_unwatched(watched_indicators, insert_list, action):
	try:
		dbcon = make_database_connection(get_database(watched_indicators))
		dbcur = set_PRAGMAS(dbcon)
		if action == 'mark_as_watched':
			dbcur.executemany("""INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)""", insert_list)
		elif action == 'mark_as_unwatched':
			dbcur.executemany("""DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)""", insert_list)
		batch_erase_bookmark(watched_indicators, insert_list, action)
	except: kodi_utils.notification(32574)

def get_last_played_value(database_type):
	if database_type == WATCHED_DB: return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	else: return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.000Z')

def make_batch_insert(action, media_type, tmdb_id, season, episode, last_played, title):
	if action == 'mark_as_watched': return (media_type, tmdb_id, season, episode, last_played, title)
	else: return (media_type, tmdb_id, season, episode)

def batch_mark_kodi_library(action, insert_list, title, year):
#	from modules.kodi_library import get_library_video, batch_mark_episodes_as_watched_unwatched_kodi_library
	in_library = get_library_video('tvshow', title, year)
	if not in_library: return
	if batch_mark_episodes_as_watched_unwatched_kodi_library(action, in_library, insert_list): kodi_utils.notification(32787)

def refresh_container(refresh=True):
	if refresh: kodi_utils.container_refresh()

def clear_local_bookmarks():
	try:
		dbcon = make_database_connection(kodi_utils.get_video_database_path())
		dbcur = set_PRAGMAS(dbcon)
		file_ids = dbcur.execute("""SELECT idFile FROM files WHERE strFilename LIKE 'plugin.video.pov%'""").fetchall()
		for i in ('bookmark', 'streamdetails', 'files'):
			dbcur.executemany("""DELETE FROM %s WHERE idFile = ?""" % i, file_ids)
	except: pass

def get_library_video(media_type, title, year, season=None, episode=None):
	try:
		years = range(int(year)-1, int(year)+2)
		filters = [{"field": "year", "operator": "is", "value": str(i)} for i in years]
		properties = ["imdbnumber", "title", "originaltitle", "file"] if media_type == 'movie' else ["title", "year"]
		params = {"filter": {"or": filters}, "properties": properties}
		if media_type == 'movie':
			r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": params, "id": 1}))
			r = json.loads(r)['result']['movies']
			try:
				r = [i for i in r if clean_file_name(title).lower() in clean_file_name(i['title']).lower()][0]
				return r
			except:
				return None
		elif media_type  == 'tvshow':
			r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": params, "id": 1}))
			r = json.loads(r)['result']['tvshows']
			try:
				r = [
					i for i in r
					if clean_file_name(title).lower()
					in (clean_file_name(i['title']).lower() if not ' (' in i['title'] else clean_file_name(i['title']).lower().split(' (')[0])
				][0]
				return r
			except:
				return None
	except: pass

def set_bookmark_kodi_library(media_type, tmdb_id, curr_time, total_time, season='', episode=''):
	meta_user_info = metadata_user_info()
	try:
		if media_type == 'movie': info = metadata.movie_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
		else: info = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
		title, year = info['title'], info['year']
		years = range(int(year)-1, int(year)+2)
		filters = [{"field": "year", "operator": "is", "value": str(i)} for i in years]
		params = {"filter": {"or": filters}, "properties": ["title"]}
		method = 'VideoLibrary.GetMovies' if media_type == 'movie' else 'VideoLibrary.GetTVShows'
		r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}))
		r = json.loads(r)['result']['movies'] if media_type == 'movie' else json.loads(r)['result']['tvshows']
		if media_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(i['title']).lower()][0]
		else:
			r = [
				i for i in r
				if clean_file_name(title).lower()
				in (clean_file_name(i['title']).lower() if not ' (' in i['title'] else clean_file_name(i['title']).lower().split(' (')[0])
			][0]
		if media_type == 'episode':
			filters = [{"field": "season", "operator": "is", "value": str(season)}, {"field": "episode", "operator": "is", "value": str(episode)}]
			params = {"filter": {"and": filters}, "properties": ["file"], "tvshowid": r['tvshowid']}
			r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": params, "id": 1}))
			r = json.loads(r)['result']['episodes'][0]
		if media_type == 'movie': method, id_name, library_id = 'VideoLibrary.SetMovieDetails', 'movieid', r['movieid']
		else: method, id_name, library_id = 'VideoLibrary.SetEpisodeDetails', 'episodeid', r['episodeid']
		query = {"jsonrpc": "2.0", "id": "setResumePoint", "method": method, "params": {id_name: library_id, "resume": {"position": curr_time, "total": total_time}}}
		execute_JSON(json.dumps(query))
	except: pass

def get_bookmark_kodi_library(media_type, tmdb_id, season='', episode=''):
	resume = '0'
	meta_user_info = metadata_user_info()
	try:
		if media_type == 'movie': info = metadata.movie_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
		else: info = metadata.tvshow_meta('tmdb_id', tmdb_id, meta_user_info, get_datetime())
		title, year = info['title'], info['year']
		years = range(int(year)-1, int(year)+2)
		filters = [{"field": "year", "operator": "is", "value": str(i)} for i in years]
		properties = ["title", "resume"] if media_type == 'movie' else ["title"]
		params = {"filter": {"or": filters}, "properties": properties}
		method = 'VideoLibrary.GetMovies' if media_type == 'movie' else 'VideoLibrary.GetTVShows'
		r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}))
		r = json.loads(r)['result']['movies'] if media_type == 'movie' else json.loads(r)['result']['tvshows']
		if media_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(i['title']).lower()][0]
		else:
			r = [
				i for i in r
				if clean_file_name(title).lower()
				in (clean_file_name(i['title']).lower() if not ' (' in i['title'] else clean_file_name(i['title']).lower().split(' (')[0])
			][0]
		if media_type == 'episode':
			filters = [{"field": "season", "operator": "is", "value": str(season)}, {"field": "episode", "operator": "is", "value": str(episode)}]
			params = {"filter": {"and": filters}, "properties": ["file"], "tvshowid": r['tvshowid']}
			r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": params, "id": 1}))
			r = json.loads(r)['result']['episodes'][0]
		if media_type == 'movie': method, id_name, library_id, results_key = 'VideoLibrary.GetMovieDetails', 'movieid', r['movieid'], 'moviedetails'
		else: method, id_name, library_id, results_key = 'VideoLibrary.GetEpisodeDetails', 'episodeid', r['episodeid'], 'episodedetails'
		query = {"jsonrpc": "2.0", "id": "getResumePoint", "method": method, "params": {id_name: library_id, "properties": ["title", "resume"]}}
		r = json.loads(execute_JSON(json.dumps(query)))
		resume = r["result"][results_key]["resume"]["position"]
		return resume
	except: pass

def mark_as_watched_unwatched_kodi_library(media_type, action, title, year, season=None, episode=None):
	try:
		playcount = 1 if action == 'mark_as_watched' else 0
		years = range(int(year)-1, int(year)+2)
		filters = [{"field": "year", "operator": "is", "value": str(i)} for i in years]
		params = {"filter": {"or": filters}, "properties": ["title"]}
		method = 'VideoLibrary.GetMovies' if media_type == 'movie' else 'VideoLibrary.GetTVShows'
		r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}))
		r = json.loads(r)['result']['movies'] if media_type == 'movie' else json.loads(r)['result']['tvshows']
		if media_type == 'movie': r = [i for i in r if clean_file_name(title).lower() in clean_file_name(i['title']).lower()][0]
		else:
			r = [
				i for i in r
				if clean_file_name(title).lower()
				in (clean_file_name(i['title']).lower() if not ' (' in i['title'] else clean_file_name(i['title']).lower().split(' (')[0])
			][0]
		if media_type == 'episode':
			filters = [{"field": "season", "operator": "is", "value": str(season)}, {"field": "episode", "operator": "is", "value": str(episode)}]
			params = {"filter": {"and": filters}, "properties": ["file"], "tvshowid": r['tvshowid']}
			r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": params, "id": 1}))
			r = json.loads(r)['result']['episodes'][0]
		if media_type == 'movie': method, id_name, library_id = 'VideoLibrary.SetMovieDetails', 'movieid', r['movieid']
		else: method, id_name, library_id = 'VideoLibrary.SetEpisodeDetails', 'episodeid', r['episodeid']
		query = {"jsonrpc": "2.0", "method": method, "params": {id_name: library_id, "playcount": playcount}, "id": 1}
		execute_JSON(json.dumps(query))
		query = {"jsonrpc": "2.0", "id": "setResumePoint", "method": method, "params": {id_name: library_id, "resume": {"position": 0,}}}
		execute_JSON(json.dumps(query))
	except: pass

def batch_mark_episodes_as_watched_unwatched_kodi_library(action, show_info, episode_list):
	playcount = 1 if action == 'mark_as_watched' else 0
	tvshowid = str(show_info['tvshowid'])
	ep_ids, action_list = [], []
	ep_ids_append, action_append = ep_ids.append, action_list.append
	progressDialogBG.create(ls(32577), '')
	try:
		for item in episode_list:
			try:
				season = item[2]
				episode = item[3]
				filters = [{"field": "season", "operator": "is", "value": str(season)}, {"field": "episode", "operator": "is", "value": str(episode)}]
				params = {"filter": {"and": filters}, "properties": ["file", "playcount"], "tvshowid": tvshowid}
				r = execute_JSON(json.dumps({"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": params, "id": 1}))
				r = json.loads(r)['result']['episodes'][0]
				ep_ids_append((r['episodeid'], r['playcount']))
			except: pass
		for count, item in enumerate(ep_ids, 1):
			try:
				ep_id = item[0]
				current_playcount = item[1]
				if int(current_playcount) != playcount:
					sleep(50)
					display = ls(32856)
					progressDialogBG.update(int(float(count) / float(len(ep_ids)) * 100), ls(32577), display)
					query = {"jsonrpc": "2.0", "method": "VideoLibrary.SetEpisodeDetails", "params": {"episodeid": ep_id, "playcount": playcount}, "id": 1}
					action_append(query)
				else: pass
			except: pass
		progressDialogBG.update(100, ls(32577), ls(32788))
		r = execute_JSON(json.dumps(action_list))
		progressDialogBG.close()
		return r
	except: pass

