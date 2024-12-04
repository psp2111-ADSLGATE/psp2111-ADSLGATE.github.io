import json
from windows import BaseDialog
from modules.kodi_utils import translate_path, hide_busy_dialog, dialog, select_dialog, close_all_dialog, ok_dialog, local_string as ls
from modules.settings import get_art_provider, provider_sort_ranks, get_fanart_data
# from modules.kodi_utils import logger

media_folder = 'special://home/addons/plugin.video.pov/resources/skins/Default/media/%s'
info_icons_dict = {
					'easynews': translate_path(media_folder % 'providers/easynews.png'),
					'alldebrid': translate_path(media_folder % 'providers/alldebrid.png'),
					'real-debrid': translate_path(media_folder % 'providers/realdebrid.png'),
					'premiumize': translate_path(media_folder % 'providers/premiumize.png'),
					'offcloud': translate_path(media_folder % 'providers/offcloud.png'),
					'torbox': translate_path(media_folder % 'providers/torbox.png'),
					'easydebrid': translate_path(media_folder % 'providers/easydebrid.png'),
					'ad_cloud': translate_path(media_folder % 'providers/alldebrid.png'),
					'rd_cloud': translate_path(media_folder % 'providers/realdebrid.png'),
					'pm_cloud': translate_path(media_folder % 'providers/premiumize.png'),
					'oc_cloud': translate_path(media_folder % 'providers/offcloud.png'),
					'tb_cloud': translate_path(media_folder % 'providers/torbox.png')}
info_quality_dict = {'4k': translate_path(media_folder % 'flags/4k.png'),
					'1080p': translate_path(media_folder % 'flags/1080p.png'),
					'720p': translate_path(media_folder % 'flags/720p.png'),
					'sd': translate_path(media_folder % 'flags/sd.png'),
					'cam': translate_path(media_folder % 'flags/sd.png'),
					'tele': translate_path(media_folder % 'flags/sd.png'),
					'scr': translate_path(media_folder % 'flags/sd.png')}
extra_info_choices = (('PACK', '[B]PACK[/B]'), ('DOLBY VISION', '[B]D/VISION[/B]'), ('HIGH DYNAMIC RANGE (HDR)', '[B]HDR[/B]'), ('HYBRID', '[B]HYBRID[/B]'), ('AV1', '[B]AV1[/B]'),
					('HEVC (X265)', '[B]HEVC[/B]'), ('REMUX', 'REMUX'), ('BLURAY', 'BLURAY'), ('SDR', 'SDR'), ('3D', '3D'), ('DOLBY ATMOS', 'ATMOS'), ('DOLBY TRUEHD', 'TRUEHD'),
					('DOLBY DIGITAL EX', 'DD-EX'), ('DOLBY DIGITAL PLUS', 'DD+'), ('DOLBY DIGITAL', 'DD'), ('DTS-HD MASTER AUDIO', 'DTS-HD MA'), ('DTS-X', 'DTS-X'),
					('DTS-HD', 'DTS-HD'), ('DTS', 'DTS'), ('ADVANCED AUDIO CODING (AAC)', 'AAC'), ('MP3', 'MP3'), ('8 CHANNEL AUDIO', '8CH'), ('7 CHANNEL AUDIO', '7CH'),
					('6 CHANNEL AUDIO', '6CH'), ('2 CHANNEL AUDIO', '2CH'), ('DVD SOURCE', 'DVD'), ('WEB SOURCE', 'WEB'), ('MULTIPLE LANGUAGES', 'MULTI-LANG'), ('SUBTITLES', 'SUBS'))
quality_choices = ('4K', '1080P', '720P', 'SD', 'TELE', 'CAM', 'SCR')
filter_str, clr_filter_str, extra_info_str, down_file_str, browse_pack_str = ls(32152), ls(32153), ls(32605), ls(32747), ls(33004)
down_pack_str, cloud_str = ls(32007), ls(32016)
filters_ignored, start_full_scrape = ls(32686), ls(33023)
filter_quality, filter_provider, filter_title, filter_extraInfo = ls(32154), ls(32157), ls(32679), ls(32169)
run_plugin_str = 'RunPlugin(%s)'
pack_check = ('true', 'show', 'season')
backup_poster = translate_path('special://home/addons/plugin.video.pov/resources/media/box_office.png')
backup_fanart = translate_path('special://home/addons/plugin.video.pov/fanart.png')
string = str
upper = string.upper
lower = string.lower

class SourceResults(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_style = kwargs.get('window_style', 'list contrast details')
		self.window_id = kwargs.get('window_id')
		self.results = kwargs.get('results')
		self.meta = kwargs.get('meta')
		self.info_highlights_dict = kwargs.get('scraper_settings')
		self.prescrape = kwargs.get('prescrape')
		if kwargs.get('filters_ignored'):
			self.filters_ignored = '[B][COLOR dodgerblue](%s)[/COLOR][/B]' % filters_ignored
		else: self.filters_ignored = ''
		self.make_items()
		self.set_properties()

	def onInit(self):
		self.filter_applied = False
		self.win = self.getControl(self.window_id)
		self.win.addItems(self.item_list)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		self.clearProperties()
		hide_busy_dialog()
		return self.selected

	def get_provider_and_path(self, provider):
		if provider in info_icons_dict: provider_path = info_icons_dict[provider]
		else: provider, provider_path = 'folders', translate_path('special://home/addons/plugin.video.pov/resources/skins/Default/media/providers/folders.png')
		return provider, provider_path

	def get_quality_and_path(self, quality):
		quality_path = info_quality_dict[quality]
		return quality, quality_path

	def onAction(self, action):
		chosen_listitem = self.get_listitem(self.window_id)
		if action == self.info_actions:
			self.open_window(('windows.sources', 'ResultsInfo'), 'sources_info.xml', item=chosen_listitem, fanart=self.original_fanart())
		elif action in self.selection_actions:
			if self.prescrape:
				if chosen_listitem.getProperty('tikiskins.perform_full_search') == 'true':
					self.selected = ('perform_full_search', '')
					return self.close()
			self.selected = ('play', json.loads(chosen_listitem.getProperty('source')))
			return self.close()
		elif action in self.context_actions:
			highlight = chosen_listitem.getProperty('tikiskins.highlight')
			source = json.loads(chosen_listitem.getProperty('source'))
			choice = self.open_window(('windows.sources', 'ResultsContextMenu'), 'contextmenu.xml',
									item=source, highlight=highlight, meta=self.meta, filter_applied=self.filter_applied)
			if choice:
				if 'results_info' in choice: self.open_window(('windows.sources', 'ResultsInfo'), 'sources_info.xml', item=chosen_listitem)
				elif 'clear_results_filter' in choice: return self.clear_filter()
				elif 'results_filter' in choice: return self.filter_results()
				else: self.execute_code(choice)
		elif action in self.closing_actions:
			if self.filter_applied: return self.clear_filter()
			self.selected = (None, '')
			return self.close()

	def make_items(self):
		def builder():
			for count, item in enumerate(self.results, 1):
				try:
					get = item.get
					listitem = self.make_listitem()
					set_property = listitem.setProperty
					scrape_provider = item['scrape_provider']
					source = get('source')
					quality = get('quality', 'SD')
					basic_quality, quality_icon = self.get_quality_and_path(lower(quality))
					try: name = upper(get('URLName', 'N/A'))
					except: name = 'N/A'
					pack = get('package', 'false') in pack_check
					if pack: extra_info = '[B]%s[/B] | %s' % (upper(get('package')), get('extraInfo', ''))
					else: extra_info = get('extraInfo', 'N/A')
					if not extra_info: extra_info = 'N/A'
					extra_info = extra_info.rstrip('| ')
					if scrape_provider == 'external':
						source_site = upper(get('cache') if 'cache' in item else get('provider'))
						provider = upper(get('debrid', source_site).replace('.me', ''))
						provider_lower = lower(provider)
						provider_icon = self.get_provider_and_path(provider_lower)[1]
						if 'cache_provider' in item:
							if 'Uncached' in item['cache_provider']:
								key = 'uncached'
								set_property('tikiskins.source_type',
									'UNCACHED (%d SEEDERS)' % get('seeders', 0)
									if 'seeders' in item else
									'UNCACHED')
								set_property('tikiskins.highlight', self.info_highlights_dict[key])
							else:
								if highlight_type == 0: key = 'torrent_highlight'
								elif highlight_type == 1: key = provider_lower
								else: key = basic_quality
								set_property('tikiskins.source_type',
									'CACHED [B]PACK[/B]'
									if pack else
									'CACHED')
								set_property('tikiskins.highlight', self.info_highlights_dict[key])
						else:
							if highlight_type == 0: key = 'hoster_highlight'
							elif highlight_type == 1: key = provider_lower
							else: key = basic_quality
							set_property('tikiskins.source_type', source)
							set_property('tikiskins.highlight', self.info_highlights_dict[key])
						set_property('tikiskins.name', name)
						set_property('tikiskins.provider', provider)
					else:
						source_site = upper(source)
						provider, provider_icon = self.get_provider_and_path(lower(source))
						if highlight_type in (0, 1): key = provider
						else: key = basic_quality
						set_property('tikiskins.highlight', self.info_highlights_dict[key])
						set_property('tikiskins.name', name)
						set_property('tikiskins.source_type', 'DIRECT')
						set_property('tikiskins.provider', upper(provider))
					set_property('tikiskins.source_site', source_site)
					set_property('tikiskins.provider_icon', provider_icon)
					set_property('tikiskins.quality_icon', quality_icon)
					set_property('tikiskins.size_label', get('size_label', 'N/A'))
					set_property('tikiskins.extra_info', extra_info)
					set_property('tikiskins.quality', upper(quality))
					set_property('tikiskins.count', '%02d.' % count)
					set_property('tikiskins.hash', get('hash', 'N/A'))
					set_property('source', json.dumps(item))
					yield listitem
				except: pass
		try:
			highlight_type = self.info_highlights_dict['highlight_type']
			self.item_list = list(builder())
			if self.prescrape:
				prescrape_listitem = self.make_listitem()
				prescrape_listitem.setProperty('tikiskins.perform_full_search', 'true')
				prescrape_listitem.setProperty('tikiskins.start_full_scrape', '[B]***%s***[/B]' % upper(start_full_scrape))
			self.total_results = string(len(self.item_list))
			self.scrape_time = ls(32675) % '[B]%.2f[/B]' % self.meta.get('scrape_time', '0')
			if self.prescrape: self.item_list.append(prescrape_listitem)
		except: pass

	def set_properties(self):
		self.poster_main, self.poster_backup, self.fanart_main, self.fanart_backup = get_art_provider()
		self.setProperty('tikiskins.window_style', self.window_style)
		self.setProperty('tikiskins.fanart', self.original_fanart())
		self.setProperty('tikiskins.poster', self.original_poster())
		self.setProperty('tikiskins.title', self.meta['title'])
		self.setProperty('tikiskins.clearlogo', self.meta['clearlogo'] if get_fanart_data() else self.meta['tmdblogo'] or '')
		self.setProperty('tikiskins.plot', self.meta['plot'])
		self.setProperty('tikiskins.total_results', self.total_results)
		self.setProperty('tikiskins.filters_ignored', self.filters_ignored)
		self.setProperty('tikiskins.scrape_time', self.scrape_time)

	def original_poster(self):
		poster = self.meta.get(self.poster_main) or self.meta.get(self.poster_backup) or backup_poster
		return poster

	def original_fanart(self):
		fanart = self.meta.get(self.fanart_main) or self.meta.get(self.fanart_backup) or backup_fanart
		return fanart

	def filter_results(self):
		choices = [(filter_quality, 'quality'), (filter_provider, 'provider'), (filter_title, 'keyword_title'), (filter_extraInfo, 'extra_info')]
		list_items = [{'line1': item[0]} for item in choices]
		kwargs = {'items': json.dumps(list_items), 'heading': filter_str, 'enumerate': 'false', 'multi_choice': 'false', 'multi_line': 'false'}
		main_choice = select_dialog([i[1] for i in choices], **kwargs)
		if main_choice is None: return
		if main_choice in ('quality', 'provider'):
			if main_choice == 'quality': choice_sorter = quality_choices
			else:
				sort_ranks = provider_sort_ranks()
				sort_ranks['premiumize'] = sort_ranks.pop('premiumize.me')
				choice_sorter = sorted(sort_ranks.keys(), key=sort_ranks.get)
				choice_sorter = [upper(i) for i in choice_sorter]
			filter_property = 'tikiskins.%s' % main_choice
			duplicates = set()
			provider_choices = [
				i.getProperty(filter_property)
				for i in self.item_list
				if not (i.getProperty(filter_property) in duplicates or duplicates.add(i.getProperty(filter_property)))
				and not i.getProperty(filter_property) == ''
			]
			provider_choices.sort(key=choice_sorter.index)
			list_items = [{'line1': item} for item in provider_choices]
			kwargs = {'items': json.dumps(list_items), 'heading': filter_str, 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false'}
			choice = select_dialog(provider_choices, **kwargs)
			if choice is None: return
			filtered_list = [i for i in self.item_list if any(x in i.getProperty(filter_property) for x in choice)]
		elif main_choice == 'keyword_title':
			keywords = dialog.input('Enter Keyword (Comma Separated for Multiple)')
			if not keywords: return
			keywords.replace(' ', '')
			keywords = keywords.split(',')
			choice = [upper(i) for i in keywords]
			filtered_list = [i for i in self.item_list if all(x in i.getProperty('tikiskins.name') for x in choice)]
		else:# extra_info
			list_items = [{'line1': item[0]} for item in extra_info_choices]
			kwargs = {'items': json.dumps(list_items), 'heading': filter_str, 'enumerate': 'false', 'multi_choice': 'true', 'multi_line': 'false'}
			choice = select_dialog(extra_info_choices, **kwargs)
			if choice is None: return
			choice = [i[1] for i in choice]
			filtered_list = [i for i in self.item_list if all(x in i.getProperty('tikiskins.extra_info') for x in choice)]
		if not filtered_list: return ok_dialog(text=32760, top_space=True)
		self.filter_applied = True
		self.win.reset()
		self.win.addItems(filtered_list)
		self.setFocusId(self.window_id)
		self.setProperty('tikiskins.total_results', string(len(filtered_list)))

	def clear_filter(self):
		self.win.reset()
		self.setProperty('tikiskins.total_results', self.total_results)
		self.onInit()

class ResultsInfo(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.item = kwargs['item']
		self.fanart = kwargs.get('fanart') or ''
		self.set_properties()

	def run(self):
		self.doModal()

	def onAction(self, action):
		self.close()

	def get_provider_and_path(self):
		provider = lower(self.item.getProperty('tikiskins.provider'))
		if provider in info_icons_dict: provider_path = info_icons_dict[provider]
		else: provider_path = translate_path('special://home/addons/plugin.video.pov/resources/skins/Default/media/providers/folders.png')
		return provider, provider_path

	def get_quality_and_path(self):
		quality = lower(self.item.getProperty('tikiskins.quality'))
		quality_path = info_quality_dict[quality]
		return quality, quality_path

	def set_properties(self):
		provider, provider_path = self.get_provider_and_path()
		quality, quality_path = self.get_quality_and_path()
		self.setProperty('tikiskins.results.info.fanart', self.fanart)
		self.setProperty('tikiskins.results.info.name', self.item.getProperty('tikiskins.name'))
		self.setProperty('tikiskins.results.info.source_type', self.item.getProperty('tikiskins.source_type'))
		self.setProperty('tikiskins.results.info.source_site', self.item.getProperty('tikiskins.source_site'))
		self.setProperty('tikiskins.results.info.size_label', self.item.getProperty('tikiskins.size_label'))
		self.setProperty('tikiskins.results.info.extra_info', self.item.getProperty('tikiskins.extra_info'))
		self.setProperty('tikiskins.results.info.highlight', self.item.getProperty('tikiskins.highlight'))
		self.setProperty('tikiskins.results.info.hash', self.item.getProperty('tikiskins.hash'))
		self.setProperty('tikiskins.results.info.provider', provider)
		self.setProperty('tikiskins.results.info.quality', quality)
		self.setProperty('tikiskins.results.info.provider_icon', provider_path)
		self.setProperty('tikiskins.results.info.quality_icon', quality_path)

class ResultsContextMenu(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 2020
		self.item = kwargs['item']
		self.highlight = kwargs['highlight']
		self.meta = kwargs['meta']
		self.filter_applied = kwargs['filter_applied']
		self.item_list = []
		self.selected = None
		self.make_menu()
		self.set_properties()

	def onInit(self):
		win = self.getControl(self.window_id)
		win.addItems(self.item_list)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		return self.selected

	def onAction(self, action):
		if action in self.selection_actions:
			chosen_listitem = self.get_listitem(self.window_id)
			self.selected = chosen_listitem.getProperty('tikiskins.context.action')
			return self.close()
		elif action in self.context_actions: return self.close()
		elif action in self.closing_actions: return self.close()

	def make_menu(self):
		meta_json = json.dumps(self.meta)
		item_id = self.item.get('id', None)
		name = self.item.get('name')
		down_pack_params, browse_pack_params, add_magnet_to_cloud_params = None, None, None
		provider_source = self.item.get('source')
		scrape_provider = self.item.get('scrape_provider')
		cache_provider = self.item.get('cache_provider', 'None')
		magnet_url = self.item.get('url', 'None')
		info_hash = self.item.get('hash', 'None')
		uncached_torrent = 'Uncached' in cache_provider
		source = json.dumps(self.item)
		if self.filter_applied: self.item_list.append(self.make_contextmenu_item('[B]%s[/B]' % clr_filter_str, run_plugin_str, {'mode': 'clear_results_filter'}))
		else: self.item_list.append(self.make_contextmenu_item('[B]%s[/B]' % filter_str, run_plugin_str, {'mode': 'results_filter'}))
		self.item_list.append(self.make_contextmenu_item('[B]%s[/B]' % extra_info_str, run_plugin_str, {'mode': 'results_info'}))
		if not uncached_torrent and scrape_provider != 'folders':
			down_file_params = {'mode': 'downloader', 'action': 'meta.single', 'name': self.meta.get('rootname', ''), 'source': source,
								'url': None, 'provider': scrape_provider, 'meta': meta_json}
			self.item_list.append(self.make_contextmenu_item(down_file_str, run_plugin_str, down_file_params))
		if 'package' in self.item:
			if not uncached_torrent:
				browse_pack_params = {'mode': 'debrid.browse_packs', 'provider': cache_provider, 'highlight': self.highlight, 'name': name,
									'magnet_url': magnet_url, 'info_hash': info_hash}
				down_pack_params = {'mode': 'downloader', 'action': 'meta.pack', 'highlight': self.highlight, 'name': self.meta.get('rootname', ''), 'source': source, 'url': None,
									'provider': cache_provider, 'meta': meta_json, 'magnet_url': magnet_url, 'info_hash': info_hash}
		if provider_source == 'torrent' and not uncached_torrent:
			add_magnet_to_cloud_params = {'mode': 'manual_add_magnet_to_cloud', 'provider': cache_provider, 'magnet_url': magnet_url}
		if down_pack_params: self.item_list.append(self.make_contextmenu_item(down_pack_str, run_plugin_str, down_pack_params))
		if browse_pack_params: self.item_list.append(self.make_contextmenu_item(browse_pack_str, run_plugin_str, browse_pack_params))
		if add_magnet_to_cloud_params: self.item_list.append(self.make_contextmenu_item(cloud_str, run_plugin_str, add_magnet_to_cloud_params))

	def set_properties(self):
		self.setProperty('tikiskins.context.highlight', self.highlight)

class SourceResultsChooser(BaseDialog):
	def __init__(self, *args, **kwargs):
		BaseDialog.__init__(self, args)
		self.window_id = 5001
		self.xml_choices = kwargs.get('xml_choices')
		self.xml_items = []
		self.make_items()

	def onInit(self):
		self.win = self.getControl(self.window_id)
		self.win.addItems(self.xml_items)
		self.setFocusId(self.window_id)

	def run(self):
		self.doModal()
		return self.choice

	def onAction(self, action):
		if action in self.closing_actions:
			self.choice = None
			self.close()
		if action in self.selection_actions:
			chosen_listitem = self.get_listitem(self.window_id)
			self.choice = chosen_listitem.getProperty('tikiskins.window.name')
			self.close()

	def make_items(self):
		append = self.xml_items.append
		for item in self.xml_choices:
			listitem = self.make_listitem()
			listitem.setProperty('tikiskins.window.name', item[0])
			listitem.setProperty('tikiskins.window.image', item[1])
			append(listitem)

