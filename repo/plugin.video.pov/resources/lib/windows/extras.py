import json
from threading import Thread
from datetime import datetime, timedelta
from windows import BaseDialog
from apis import tmdb_api, imdb_api, mdblist_api
from caches import watched_cache as ws
from indexers import people, metadata
from indexers.images import Images
from modules import settings, dialogs
from modules.sources import Sources
from modules.downloader import runner
from modules.meta_lists import networks
from modules.utils import get_datetime
from modules.kodi_utils import translate_path, close_all_dialog, hide_busy_dialog, ok_dialog, fetch_kodi_imagecache, local_string as ls
# from modules.kodi_utils import logger

backup_poster = translate_path('special://home/addons/plugin.video.pov/resources/media/box_office.png')
backup_fanart = translate_path('special://home/addons/plugin.video.pov/fanart.png')
backup_thumbnail = translate_path('special://home/addons/plugin.video.pov/resources/media/box_office.png')
backup_cast_thumbnail = translate_path('special://home/addons/plugin.video.pov/resources/media/people.png')
tmdb_image_base = 'https://image.tmdb.org/t/p/%s%s'
button_ids = (10, 11, 12, 13, 14, 15, 16, 17, 50)
cast_id, recommended_id, reviews_id, trivia_id, blunders_id, parentsguide_id = 2050, 2051, 2052, 2053, 2054, 2055
videos_id, posters_id, backdrops_id, year_id, genres_id, networks_id, collection_id = 2056, 2057, 2058, 2059, 2060, 2061, 2062
playbrowse_id, trailer_id, keywords_id, images_id, extrainfo_id, genre_id, directorrandom_id, trakt_id, plot_id = button_ids
tmdb_list_ids = (recommended_id, year_id, genres_id, networks_id, collection_id)
imdb_list_ids = (reviews_id, trivia_id, blunders_id, parentsguide_id)
art_ids = (posters_id, backdrops_id)
parentsguide_levels = {'mild': ls(32996), 'moderate': ls(32997), 'severe': ls(32998)}
parentsguide_inputs = {'Sex & Nudity': (ls(32990), 'porn.png'), 'Violence & Gore': (ls(32991), 'war.png'), 'Profanity': (ls(32992), 'bad_language.png'),
						'Alcohol, Drugs & Smoking': (ls(32993), 'drugs_alcohol.png'), 'Frightening & Intense Scenes': (ls(32994), 'horror.png')}

class Extras(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.control_id = None
		self.set_starting_constants(kwargs)
		self.set_properties()

	def onInit(self):
		tasks = (self.set_poster, self.make_cast, self.make_recommended, self.make_reviews, self.make_trivia, self.make_blunders,
				self.make_parentsguide, self.make_videos, self.make_year, self.make_genres, self.make_network)
		[Thread(target=i).start() for i in tasks]
		for i in ('posters', 'backdrops'): Thread(target=self.make_artwork, args=(i,)).start()
		if self.media_type == 'movie': Thread(target=self.make_collection).start()
		else: self.setProperty('tikiskins.extras.make.collection', 'false')

	def run(self):
		self.doModal()
		self.clearProperties()
		hide_busy_dialog()
		if self.selected: self.execute_code(self.selected)

	def onClick(self, controlID):
		self.control_id = None
		if controlID in button_ids:
			if controlID == playbrowse_id:
				if self.media_type == 'movie':
					url_params = {'mode': 'play_media', 'media_type': 'movie', 'query': self.rootname, 'tmdb_id': self.tmdb_id}
					Sources().playback_prep(url_params)
				else:
					close_all_dialog()
					url_params = self.make_tvshow_browse_params()
					self.selected = self.folder_runner % self.build_url(url_params)
					self.close()
			elif controlID == trailer_id:
				chosen = dialogs.trailer_choice(self.media_type, self.poster, self.tmdb_id, self.meta['trailer'], self.meta['all_trailers'])
				if not chosen: return ok_dialog()
				elif chosen == 'canceled': return
				if self.is_widget == 'true':
					close_all_dialog()
					self.selected = self.plugin_runner % chosen
					self.close()
				else:
					params = {'import_info': json.dumps(['windows.videoplayer', 'VideoPlayer']), 'skin_xml': 'videoplayer.xml', 'kwargs': json.dumps({'video': chosen})}
					return self.open_window(('windows.videoplayer', 'VideoPlayer'), 'videoplayer.xml', video=chosen)
			elif controlID == keywords_id:
				base_media = 'movies' if self.media_type == 'movie' else 'tv'
				keyword_params = dialogs.imdb_keywords_choice(base_media, self.imdb_id, self.poster)
				if not keyword_params: return
				close_all_dialog()
				self.selected = self.folder_runner % self.build_url(keyword_params)
				self.close()
			elif controlID == images_id:
				params = {'mode': 'imdb_image_results', 'imdb_id': self.imdb_id, 'media_title': self.rootname, 'page_no': 1, 'rolling_count': 0}
				return Images().run(params)
			elif controlID == extrainfo_id:
				text = dialogs.media_extra_info(self.media_type, self.meta)
				self.open_window(('windows.extras', 'ShowTextMedia'), 'textviewer_media.xml', text=text, poster=self.poster)
			elif controlID == genre_id:
				if not self.genre: return
				base_media = 'movies' if self.media_type == 'movie' else 'tv'
				genre_params = dialogs.genres_choice(base_media, self.genre, self.poster)
				if not genre_params: return
				close_all_dialog()
				self.selected = self.folder_runner % self.build_url(genre_params)
				self.close()
			elif controlID == directorrandom_id:
				if self.media_type == 'movie':
					director = self.meta.get('director', None)
					if not director: return
					return people.person_data_dialog({'query': director})
				else:
					close_all_dialog()
					self.selected = self.plugin_runner % self.build_url({'mode': 'random_choice', 'tmdb_id': self.tmdb_id, 'poster': self.poster})
					self.close()
			elif controlID == trakt_id:
				params = {'tmdb_id': self.tmdb_id, 'imdb_id': self.imdb_id, 'tvdb_id': self.meta['tvdb_id'], 'media_type': self.media_type,
						'icon': self.poster}
				return dialogs.trakt_manager_choice(params)
			elif controlID == plot_id:
				self.open_window(('windows.extras', 'ShowTextMedia'), 'textviewer_media.xml', text=self.plot, poster=self.poster)
		else: self.control_id = controlID

	def onAction(self, action):
		if action in self.closing_actions: self.close()
		if action in self.context_actions:
			focus_id = self.getFocusId()
			if focus_id == playbrowse_id and self.media_type == 'movie':
				dialogs.playback_choice('movie', self.poster, self.meta)
			elif focus_id in (posters_id, backdrops_id):
				chosen_listitem = self.get_listitem(focus_id)
				image = chosen_listitem.getProperty('tikiskins.extras.thumbnail')
				params = {'action': 'image', 'name': '%s %s' % (self.rootname, chosen_listitem.getProperty('tikiskins.extras.name')),
						'thumb_url': image.replace('w780', {posters_id: 'w185', backdrops_id: 'w300'}[focus_id]), 'image_url': image.replace('w780', 'original'),
						'media_type': 'image', 'image': translate_path('special://home/addons/plugin.video.pov/icon.png')}
				return runner(params)
		if not self.control_id: return
		if action in self.selection_actions:
			try: chosen_var = self.get_listitem(self.control_id).getProperty(self.item_action_dict[self.control_id])
			except: return
			if self.control_id == cast_id:
				return people.person_data_dialog({'query': chosen_var})
			elif self.control_id == videos_id:
				chosen = dialogs.imdb_videos_choice(chosen_var, self.poster)
				if not chosen: return
				self.open_window(('windows.videoplayer', 'VideoPlayer'), 'videoplayer.xml', meta=self.meta, video=chosen)
			elif self.control_id in tmdb_list_ids:
				function = metadata.movie_meta if self.media_type == 'movie' else metadata.tvshow_meta
				meta = function('tmdb_id', chosen_var, settings.metadata_user_info(), get_datetime())
				if not meta: return
				params = {'mode': 'extras_menu_choice', 'tmdb_id': chosen_var, 'media_type': self.media_type, 'is_widget': self.is_widget, 'is_home': self.is_home}
				return dialogs.extras_menu(params)
			elif self.control_id in imdb_list_ids:
				if self.control_id == parentsguide_id:
					listings = json.loads(chosen_var)
					if not listings: return
					chosen_var = '\n\n'.join(['%02d. %s' % (count, i) for count, i in enumerate(listings, 1)])
				self.open_window(('windows.extras', 'ShowTextMedia'), 'textviewer_media.xml', text=chosen_var, poster=self.poster)
			elif self.control_id in art_ids:
				slideshow_params = {'mode': 'slideshow_image', 'all_images': chosen_var, 'current_index': self.get_position(self.control_id)}
				ending_position = Images().run(slideshow_params)
				self.getControl(self.control_id).selectItem(ending_position)

	def make_cast(self):
		if not cast_id in self.enabled_lists: return
		def builder():
			for item in self.meta['cast']:
				try:
					listitem = self.make_listitem()
					thumbnail = item['thumbnail']
					if not thumbnail: thumbnail = backup_cast_thumbnail
					listitem.setProperty('tikiskins.extras.name', item['name'])
					listitem.setProperty('tikiskins.extras.role', item['role'])
					listitem.setProperty('tikiskins.extras.thumbnail', thumbnail)
					yield listitem
				except: pass
		try:
			item_list = list(builder())
			self.setProperty('tikiskins.extras.cast.number', '(x%02d)' % len(item_list))
			self.item_action_dict[cast_id] = 'tikiskins.extras.name'
			self.add_items(cast_id, item_list)
		except: pass

	def make_recommended(self):
		if not recommended_id in self.enabled_lists: return
		try:
			function = tmdb_api.tmdb_movies_recommendations if self.media_type == 'movie' else tmdb_api.tmdb_tv_recommendations
			data = function(self.tmdb_id, 1)['results']
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('tikiskins.extras.recommended.number', '(x%02d)' % len(item_list))
			self.item_action_dict[recommended_id] = 'tikiskins.extras.tmdb_id'
			self.add_items(recommended_id, item_list)
		except: pass

	def make_reviews(self):
		if not reviews_id in self.enabled_lists: return
		def builder():
			for count, item in enumerate(reviews, 1):
				try:
					listitem = self.make_listitem()
					provider = mdblist_api.review_provider_id[item['provider_id']].upper()
					updated_at = item['updated_at'] or 'NA'
					rating = item['rating'] or 'NA'
					if 'spoiler' in item and item['spoiler']: content = (
						'[B][COLOR red][%s][/COLOR][CR]%02d. [I]%s - %s - %s[/I][/B]\n\n%s'
						% (spoiler, count, provider, rating, updated_at, item['content'])
					)
					else: content = (
						'[B]%02d. [I]%s - %s - %s[/I][/B]\n\n%s'
						% (count, provider, rating, updated_at, item['content'])
					)
					listitem.setProperty('tikiskins.extras.text', content)
					yield listitem
				except: pass
		try:
			spoiler = ls(32985).upper()
			data = mdblist_api.mdb_media_info(self.imdb_id, self.media_type)
			ratings, reviews = data['ratings'], data['reviews']
			sources = ('imdb', 'metacritic', 'tomatoes', 'trakt', 'tmdb')
			ratings = {i['source']: str(i['value']) for i in ratings if i['value'] and i['source'] in sources}
			ratings['mdblist'] = str(data['score'] or '')
			for k, v in ratings.items(): self.setProperty('tikiskins.extras.rating.%s' % k, v)
			reviews.sort(key=lambda k: k['updated_at'] or '', reverse=True)
			item_list = list(builder())
			self.setProperty('tikiskins.extras.imdb_reviews.number', '(x%02d)' % len(item_list))
			self.item_action_dict[reviews_id] = 'tikiskins.extras.text'
			self.add_items(reviews_id, item_list)
		except: pass

	def make_trivia(self):
		if not trivia_id in self.enabled_lists: return
		def builder():
			for count, item in enumerate(data, 1):
				try:
					listitem = self.make_listitem()
					listitem.setProperty('tikiskins.extras.text', '[B]%s %02d.[/B][CR][CR]%s' % (trivia, count, item))
					yield listitem
				except: pass
		try:
			trivia = ls(32984).upper()
			data = imdb_api.imdb_trivia(self.imdb_id)
			item_list = list(builder())
			self.setProperty('tikiskins.extras.imdb_trivia.number', '(x%02d)' % len(item_list))
			self.item_action_dict[trivia_id] = 'tikiskins.extras.text'
			self.add_items(trivia_id, item_list)
		except: pass

	def make_blunders(self):
		if not blunders_id in self.enabled_lists: return
		def builder():
			for count, item in enumerate(data, 1):
				try:
					listitem = self.make_listitem()
					listitem.setProperty('tikiskins.extras.text', '[B]%s %02d.[/B][CR][CR]%s' % (blunders, count, item))
					yield listitem
				except: pass
		try:
			blunders = ls(32986).upper()
			data = imdb_api.imdb_blunders(self.imdb_id)
			item_list = list(builder())
			self.setProperty('tikiskins.extras.imdb_blunders.number', '(x%02d)' % len(item_list))
			self.item_action_dict[blunders_id] = 'tikiskins.extras.text'
			self.add_items(blunders_id, item_list)
		except: pass

	def make_parentsguide(self):
		if not parentsguide_id in self.enabled_lists: return
		def builder():
			for item in data:
				try:
					listitem = self.make_listitem()
					name = parentsguide_inputs[item['title']][0]
					ranking = parentsguide_levels[item['ranking'].lower()].upper()
					if item['listings']:
						ranking += ' (x%02d)' % len(item['listings'])
					icon = translate_path('special://home/addons/plugin.video.pov/resources/media/%s' % parentsguide_inputs[item['title']][1])
					listitem.setProperty('tikiskins.extras.name', name)
					listitem.setProperty('tikiskins.extras.ranking', ranking)
					listitem.setProperty('tikiskins.extras.thumbnail', icon)
					listitem.setProperty('tikiskins.extras.listings', json.dumps(item['listings']))
					yield listitem
				except: pass
		try:
			data = imdb_api.imdb_parentsguide(self.imdb_id)
			item_list = list(builder())
			self.setProperty('tikiskins.extras.imdb_parentsguide.number', '(x%02d)' % len(item_list))
			self.item_action_dict[parentsguide_id] = 'tikiskins.extras.listings'
			self.add_items(parentsguide_id, item_list)
		except: pass

	def make_videos(self):
		if not videos_id in self.enabled_lists: return
		def builder():
			for count, item in enumerate(data, 1):
				try:
					listitem = self.make_listitem()
					listitem.setProperty('tikiskins.extras.name', '%01d. %s' % (count, item['title']))
					listitem.setProperty('tikiskins.extras.thumbnail', item['poster'])
					listitem.setProperty('tikiskins.extras.qualities', json.dumps(item['videos']))
					yield listitem
				except: pass
		try:
			data = imdb_api.imdb_videos(self.imdb_id)
			item_list = list(builder())
			self.setProperty('tikiskins.extras.imdb_videos.number', '(x%02d)' % len(item_list))
			self.item_action_dict[videos_id] = 'tikiskins.extras.qualities'
			self.add_items(videos_id, item_list)
		except: pass

	def make_artwork(self, image_type):
		if image_type == 'posters':
			if not posters_id in self.enabled_lists: return
			_id = posters_id
		else:
			if not backdrops_id in self.enabled_lists: return
			_id = backdrops_id
		def builder():
			for count, item in enumerate(data, 1):
				try:
					listitem = self.make_listitem()
					thumb_url = tmdb_image_base % ('w780', item['file_path'])
					name = '%sx%s' % (item['height'], item['width'])
					listitem.setProperty('tikiskins.extras.name', '%01d. %s' % (count, name))
					listitem.setProperty('tikiskins.extras.thumbnail', thumb_url)
					listitem.setProperty('tikiskins.extras.all_images', json_all_images)
					yield listitem
				except: pass
		try:
			dbtype = 'movie' if self.media_type == 'movie' else 'tv'
			data = tmdb_api.tmdb_media_images(dbtype, self.tmdb_id)[image_type]
			data.sort(key=lambda x: x['file_path'])
			json_all_images = json.dumps([(tmdb_image_base % ('original', i['file_path']), '%sx%s' % (i['height'], i['width'])) for i in data])
			item_list = list(builder())
			self.setProperty('tikiskins.extras.tmdb_artwork.%s.number' % image_type, '(x%02d)' % len(item_list))
			self.item_action_dict[_id] = 'tikiskins.extras.all_images'
			self.add_items(_id, item_list)
		except: pass

	def make_year(self):
		if not year_id in self.enabled_lists: return
		try:
			function = tmdb_api.tmdb_movies_year if self.media_type == 'movie' else tmdb_api.tmdb_tv_year
			data = self.remove_current_tmdb_mediaitem(function(self.year, 1)['results'])
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('tikiskins.extras.more_from_year.number', '(x%02d)' % len(item_list))
			self.item_action_dict[year_id] = 'tikiskins.extras.tmdb_id'
			self.add_items(year_id, item_list)
		except: pass

	def make_genres(self):
		if not genres_id in self.enabled_lists: return
		try:
			function = tmdb_api.tmdb_movies_genres if self.media_type == 'movie' else tmdb_api.tmdb_tv_genres
			genre_dict = dialogs.genres_choice(self.media_type, self.genre, '', return_genres=True)
			genre_list = ','.join([i['value'][0] for i in genre_dict])
			data = self.remove_current_tmdb_mediaitem(function(genre_list, 1)['results'])
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('tikiskins.extras.more_from_genres.number', '(x%02d)' % len(item_list))
			self.item_action_dict[genres_id] = 'tikiskins.extras.tmdb_id'
			self.add_items(genres_id, item_list)
		except: pass

	def make_network(self):
		if not networks_id in self.enabled_lists: return
		try:
			network = self.meta['studio']
			if self.media_type == 'movie': network_id = [i['id'] for i in tmdb_api.tmdb_company_id(network)['results'] if i['name'] == network][0]
			else: network_id = [item['id'] for item in networks if 'name' in item and item['name'] == network][0]
			function = tmdb_api.tmdb_movies_networks if self.media_type == 'movie' else tmdb_api.tmdb_tv_networks
			data = self.remove_current_tmdb_mediaitem(function(network_id, 1)['results'])
			item_list = list(self.make_tmdb_listitems(data))
			self.setProperty('tikiskins.extras.more_from_networks.number', '(x%02d)' % len(item_list))
			self.item_action_dict[networks_id] = 'tikiskins.extras.tmdb_id'
			self.add_items(networks_id, item_list)
		except: pass

	def make_collection(self):
		if not collection_id in self.enabled_lists: return
		try: coll_id = self.meta['extra_info']['collection_id']
		except: coll_id = self.meta['extra_info']['ei_collection_id']
		if not coll_id: return
		try:
			data = tmdb_api.tmdb_movies_collection(coll_id)
			poster_path = data['poster_path']
			if poster_path: poster = tmdb_image_base % (self.poster_resolution, poster_path)
			else: poster = backup_poster
			self.setProperty('tikiskins.extras.more_from_collection.name', data['name'])
			self.setProperty('tikiskins.extras.more_from_collection.overview', data['overview'])
			self.setProperty('tikiskins.extras.more_from_collection.poster', poster)
			item_list = list(self.make_tmdb_listitems(sorted(data['parts'], key=lambda k: k['release_date'] or '2050')))
			self.setProperty('tikiskins.extras.more_from_collection.number', '(x%02d)' % len(item_list))
			self.item_action_dict[collection_id] = 'tikiskins.extras.tmdb_id'
			self.add_items(collection_id, item_list)
		except: pass

	def get_release_year(self, release_data):
		try:
			if release_data in ('', None): release_data = 'N/A'
			else: release_data = release_data.split('-')[0]
		except: pass
		return release_data

	def get_finish(self):
		if self.percent_watched in ('0', '100') and self.listitem_check():
			finished = self.get_infolabel('ListItem.EndTime')
		else:
			kodi_clock = self.get_infolabel('System.Time')
			if any(i in kodi_clock for i in ['AM', 'PM']): _format = '%I:%M %p'
			else: _format = '%H:%M'
			current_time = datetime.now()
			remaining_time = ((100 - int(self.percent_watched))/100) * self.duration_data
			finish_time = current_time + timedelta(minutes=remaining_time)
			finished = finish_time.strftime(_format)
		return '%s: %s' % (ls(33062), finished)

	def get_duration(self):
		return ls(33058) % self.duration_data

	def get_progress(self):
		try: resume_point, curr_time, resume_id = ws.detect_bookmark(ws.get_bookmarks(self.watched_indicators, 'movie'), self.tmdb_id)
		except: resume_point = 0
		if resume_point in (0, '0', 0.0, '0.0'):
			watched_info = ws.get_watched_info_movie(self.watched_indicators)
			playcount, overlay = ws.get_watched_status_movie(watched_info, str(self.tmdb_id))
			self.meta.update({'playcount': playcount, 'overlay': overlay})
			if playcount == 1: self.percent_watched = '100'
			else: self.percent_watched = '0'
		else: self.percent_watched = str(int(float(resume_point)))
		progress_status = '%s%% %s' % (self.percent_watched, ls(32475))
		return progress_status

	def get_last_aired(self):
		extra_info = self.meta['extra_info']
		if extra_info.get('last_episode_to_air', False):
			last_ep = extra_info['last_episode_to_air']
			last_aired = 'S%.2dE%.2d' % (last_ep['season_number'], last_ep['episode_number'])
		else: return ''
		return '%s: %s' % (ls(32634), last_aired)

	def get_next_aired(self):
		extra_info = self.meta['extra_info']
		if extra_info.get('next_episode_to_air', False):
			next_ep = extra_info['next_episode_to_air']
			next_aired = 'S%.2dE%.2d' % (next_ep['season_number'], next_ep['episode_number'])
		else: return ''
		return '%s: %s' % (ls(32635), next_aired)

	def get_next_episode(self):
		watched_info = ws.get_watched_info_tv(self.watched_indicators)
		ep_list = ws.get_next_episodes(watched_info)
		try: info = [i for i in ep_list if i['media_ids']['tmdb'] == self.tmdb_id][0]
		except: return ''
		current_season = info['season']
		current_episode = info['episode']
		season_data = self.meta['season_data']
		curr_season_data = [i for i in season_data if i['season_number'] == current_season][0]
		season = current_season if current_episode < curr_season_data['episode_count'] else current_season + 1
		episode = current_episode + 1 if current_episode < curr_season_data['episode_count'] else 1
		try: info = [i for i in season_data if i['season_number'] == season][0]
		except: return ''
		if info['episode_count'] >= episode:
			next_episode = 'S%.2dE%.2d' % (season, episode)
			return '%s: %s' % (ls(33041), next_episode)
		else: return ''

	def make_tvshow_browse_params(self):
		total_seasons = self.meta['total_seasons']
		all_episodes = settings.default_all_episodes()
		show_all_episodes = True if all_episodes in (1, 2) else False
		if show_all_episodes:
			if all_episodes == 1 and total_seasons > 1: url_params = {'mode': 'build_season_list', 'tmdb_id': self.tmdb_id}
			else: url_params = {'mode': 'build_episode_list', 'tmdb_id': self.tmdb_id, 'season': 'all'}
		else: url_params = {'mode': 'build_season_list', 'tmdb_id': self.tmdb_id}
		return url_params

	def original_poster(self):
		poster = self.meta.get(self.poster_main) or self.meta.get(self.poster_backup) or backup_thumbnail
		self.current_poster = poster
		if 'image.tmdb' in self.current_poster:
			try: poster = self.current_poster.replace('w185', 'original').replace('w342', 'original').replace('w780', 'original')
			except: pass
		elif 'fanart.tv' in self.current_poster:
			if not self.check_poster_cached(self.current_poster): self.current_poster = self.meta.get(self.poster_backup) or backup_thumbnail
		return poster

	def original_fanart(self):
		fanart = self.meta.get(self.fanart_main) or self.meta.get(self.fanart_backup) or backup_fanart
		return fanart

	def remove_current_tmdb_mediaitem(self, data):
		return [i for i in data if int(i['id']) != self.tmdb_id]

	def make_tmdb_listitems(self, data):
		name_key = 'title' if self.media_type == 'movie' else 'name'
		release_key = 'release_date' if self.media_type == 'movie' else 'first_air_date'
		for item in data:
			try:
				listitem = self.make_listitem()
				poster_path = item['poster_path']
				if poster_path: thumbnail = tmdb_image_base % (self.poster_resolution, poster_path)
				else: thumbnail = backup_poster
				year = self.get_release_year(item[release_key])
				listitem.setProperty('tikiskins.extras.name', item[name_key])
				listitem.setProperty('tikiskins.extras.release_date', year)
				listitem.setProperty('tikiskins.extras.vote_average', '%.1f' % item['vote_average'])
				listitem.setProperty('tikiskins.extras.thumbnail', thumbnail)
				listitem.setProperty('tikiskins.extras.tmdb_id', str(item['id']))
				yield listitem
			except: pass

	def listitem_check(self):
		return self.get_infolabel('ListItem.Title') == self.meta['title']

	def add_items(self,_id, items):
		self.getControl(_id).addItems(items)

	def set_poster(self):
		if self.current_poster:
			self.getControl(200).setImage(self.current_poster)
			self.getControl(201).setImage(self.poster)
			total_time = 0
			while not self.check_poster_cached(self.poster):
				if total_time >= 200: break
				total_time += 1
				self.sleep(50)
			self.getControl(200).setImage(self.poster)
		else: self.setProperty('tikiskins.extras.active_poster', 'false')

	def check_poster_cached(self, poster):
		try:
			if poster == backup_thumbnail: return True
			if fetch_kodi_imagecache(poster): return True
			return False
		except: return True

	def set_starting_constants(self, kwargs):
		self.item_action_dict = {}
		self.selected = None
		self.is_widget = kwargs['is_widget'].lower()
		self.is_home = kwargs['is_home'].lower()
		self.meta = kwargs['meta']
		self.media_type = self.meta['mediatype']#movie, tvshow
		self.tmdb_id = self.meta['tmdb_id']
		self.imdb_id = self.meta['imdb_id']
		if self.is_widget == 'true' or self.is_home == 'true': self.folder_runner = 'ActivateWindow(Videos,%s,return)'
		else: self.folder_runner = 'Container.Update(%s)'
		self.plugin_runner = 'RunPlugin(%s)'
		self.enabled_lists = settings.extras_enabled_menus()
		self.enable_scrollbars = settings.extras_enable_scrollbars()
		self.poster_resolution = settings.get_resolution()['poster']
		self.watched_indicators = settings.watched_indicators()
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = settings.get_art_provider()
		self.title = self.meta['title']
		self.year = str(self.meta['year'])
		self.rootname = self.meta['rootname']
		self.poster = self.original_poster()
		self.fanart = self.original_fanart()
		self.clearlogo = self.meta['clearlogo'] if settings.get_fanart_data() else self.meta['tmdblogo'] or ''
		self.plot = self.meta['tvshow_plot'] if 'tvshow_plot' in self.meta else self.meta['plot']
		if not self.plot: self.plot = ''
		self.rating = str(self.meta['rating'])
		self.mpaa = self.meta['mpaa']
		self.status = self.meta['extra_info'].get('status', '').replace('Series', '')
		self.genre = self.meta['genre']
		self.network = self.meta['studio'] or 'N/A'
		if not self.network: self.network = ''
		self.duration_data = int(float(self.meta['duration'])/60)
		self.duration = self.get_duration()
		if self.media_type == 'movie':
			self.progress = self.get_progress()
			self.finish_watching = self.get_finish()
			self.last_aired_episode, self.next_aired_episode, self.next_episode = '', '', ''
		else:
			self.progress, self.finish_watching = '', ''
			self.last_aired_episode = self.get_last_aired()
			if self.status not in ('', 'Ended', 'Canceled'): self.next_aired_episode = self.get_next_aired()
			else: self.next_aired_episode = ''
			self.next_episode = self.get_next_episode()

	def set_properties(self):
		self.setProperty('tikiskins.extras.media_type', self.media_type)
		self.setProperty('tikiskins.extras.fanart', self.fanart)
		self.setProperty('tikiskins.extras.clearlogo', self.clearlogo)
		self.setProperty('tikiskins.extras.title', self.title)
		self.setProperty('tikiskins.extras.plot', self.plot)
		self.setProperty('tikiskins.extras.year', self.year)
		self.setProperty('tikiskins.extras.rating', self.rating)
		self.setProperty('tikiskins.extras.mpaa', self.mpaa)
		self.setProperty('tikiskins.extras.status', self.status)
		self.setProperty('tikiskins.extras.genre', self.genre)
		self.setProperty('tikiskins.extras.network', self.network)
		self.setProperty('tikiskins.extras.duration', self.duration)
		self.setProperty('tikiskins.extras.progress', self.progress)
		self.setProperty('tikiskins.extras.finish_watching', self.finish_watching)
		self.setProperty('tikiskins.extras.last_aired_episode', self.last_aired_episode)
		self.setProperty('tikiskins.extras.next_aired_episode', self.next_aired_episode)
		self.setProperty('tikiskins.extras.next_episode', self.next_episode)
		self.setProperty('tikiskins.extras.enable_scrollbars', self.enable_scrollbars)

class ShowTextMedia(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.text = kwargs.get('text')
		self.poster = kwargs.get('poster')
		self.focus_id = 2060
		self.set_properties()

	def onInit(self):
		self.setFocusId(self.focus_id)

	def run(self):
		self.doModal()

	def onAction(self, action):
		if action in self.closing_actions: self.close()

	def set_properties(self):
		self.setProperty('tikiskins.text_media.text', self.text)
		self.setProperty('tikiskins.text_media.poster', self.poster)

class ExtrasChooser(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 5001
		self.kwargs = kwargs
		self.preselect = self.kwargs['preselect']
		self.items = json.loads(self.kwargs['items'])
		self.item_list = []
		self.chosen_indexes = []
		self.append = self.chosen_indexes.append
		self.selected = None
		self.make_menu()

	def onInit(self):
		self.win = self.getControl(self.window_id)
		self.win.addItems(self.item_list)
		if self.preselect:
			for index in self.preselect:
				self.item_list[index].setProperty('tikiskins.check_status', 'checked')
				self.append(index)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		return self.selected

	def onClick(self, controlID):
		if controlID == 10:
			self.selected = sorted(self.chosen_indexes)
			self.close()
		elif controlID == 11:
			self.close()

	def onAction(self, action):
		if action in self.selection_actions:
			position = self.get_position(self.window_id)
			chosen_listitem = self.get_listitem(self.window_id)
			if chosen_listitem.getProperty('tikiskins.check_status') == 'checked':
				chosen_listitem.setProperty('tikiskins.check_status', '')
				self.chosen_indexes.remove(position)
			else:
				chosen_listitem.setProperty('tikiskins.check_status', 'checked')
				self.append(position)
		elif action in self.closing_actions:
			return self.close()

	def make_menu(self):
		def builder():
			for item in self.items:
				listitem = self.make_listitem()
				listitem.setProperty('tikiskins.extras_chooser.name', item['name'])
				listitem.setProperty('tikiskins.extras_chooser.image', item['image'])
				listitem.setProperty('tikiskins.extras_chooser.item', json.dumps(item))
				yield listitem
		self.item_list = list(builder())

