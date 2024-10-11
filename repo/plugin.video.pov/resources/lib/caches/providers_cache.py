from datetime import datetime, timedelta
from caches.base_cache import BaseCache
from modules.kodi_utils import external_db
# from modules.kodi_utils import logger

SELECT_RESULTS = 'SELECT results, expires FROM results_data WHERE provider = ? AND db_type = ? AND tmdb_id = ? AND title = ? AND year = ? AND season = ? AND episode = ?'
DELETE_RESULTS = 'DELETE FROM results_data WHERE provider = ? AND db_type = ? AND tmdb_id = ? AND title = ? AND year = ? AND season = ? AND episode = ?'
INSERT_RESULTS = 'INSERT OR REPLACE INTO results_data VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
SINGLE_DELETE = 'DELETE FROM results_data WHERE db_type=? AND tmdb_id=?'
FULL_DELETE = 'DELETE FROM results_data'

class ExternalProvidersCache(BaseCache):
	db_file = external_db

	def get(self, source, media_type, tmdb_id, title, year, season, episode):
		result = None
		try:
			self.dbcur.execute(SELECT_RESULTS, (source, media_type, tmdb_id, title, year, season, episode))
			cache_data = self.dbcur.fetchone()
			if cache_data:
				if cache_data[1] > self._get_timestamp(datetime.now()): result = eval(cache_data[0])
				else: self.delete(source, media_type, tmdb_id, title, season, episode)
		except: pass
		return result

	def set(self, source, media_type, tmdb_id, title, year, season, episode, results, expire_time):
		try:
			expiration = timedelta(hours=expire_time)
			expires = self._get_timestamp(datetime.now() + expiration)
			self.dbcur.execute(INSERT_RESULTS, (source, media_type, tmdb_id, title, year, season, episode, repr(results), int(expires)))
		except: pass

	def delete(self, source, media_type, tmdb_id, title, season, episode):
		try: self.dbcur.execute(DELETE_RESULTS, (source, media_type, tmdb_id, title, season, episode))
		except: pass

	def delete_cache(self):
		try:
			self.dbcur.execute(FULL_DELETE, ())
			self.dbcur.execute('VACUUM')
			return 'success'
		except: return 'failure'

	def delete_cache_single(self, media_type, tmdb_id):
		try:
			self.dbcur.execute(SINGLE_DELETE, (media_type, tmdb_id))
			self.dbcur.execute('VACUUM')
			return True
		except: return False

