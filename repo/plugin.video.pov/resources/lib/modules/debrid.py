import time
from threading import Thread
from caches.debrid_cache import DebridCache
from apis import real_debrid_api, premiumize_api, alldebrid_api, offcloud_api, torbox_api, easydebrid_api
from modules.utils import make_thread_list, chunks
from modules.settings import display_sleep_time, enabled_debrids_check
from modules import kodi_utils
# from modules.kodi_utils import logger

get_setting, sleep, monitor, ls = kodi_utils.get_setting, kodi_utils.sleep, kodi_utils.monitor, kodi_utils.local_string
show_busy_dialog, hide_busy_dialog, notification = kodi_utils.show_busy_dialog, kodi_utils.hide_busy_dialog, kodi_utils.notification
ok_dialog, progressDialogBG = kodi_utils.ok_dialog, kodi_utils.progressDialogBG
plswait_str, checking_debrid_str, remaining_debrid_str = ls(32577), ls(32578), ls(32579)
main_line = '%s[CR]%s[CR]%s'

debrid_list = (
	('Real-Debrid', 'rd','realdebrid.png'), ('Premiumize.me', 'pm', 'premiumize.png'),
	('AllDebrid', 'ad', 'alldebrid.png'), ('EasyDebrid', 'ed', 'easydebrid.png'),
	('TorBox', 'tb','torbox.png'), ('Offcloud', 'oc', 'offcloud.png')
)

def import_debrid(debrid_provider):
	return {
		'Real-Debrid': real_debrid_api.RealDebridAPI, 'Premiumize.me': premiumize_api.PremiumizeAPI,
		'AllDebrid': alldebrid_api.AllDebridAPI, 'EasyDebrid': easydebrid_api.EasyDebridAPI,
		'TorBox': torbox_api.TorBoxAPI, 'Offcloud': offcloud_api.OffcloudAPI
	}.get(debrid_provider)

def debrid_enabled():
	return [i[0] for i in debrid_list if enabled_debrids_check(i[1])]

def debrid_type_enabled(debrid_type, enabled_debrids):
	return [i[0] for i in debrid_list if i[0] in enabled_debrids and get_setting('%s.%s.enabled' % (i[1], debrid_type)) == 'true']

def debrid_valid_hosts(enabled_debrids):
	def _get_hosts(function):
		debrid_hosts_append(function().get_hosts())
	if not enabled_debrids: return []
	debrid_hosts = []
	debrid_hosts_append = debrid_hosts.append
	threads = list(make_thread_list(_get_hosts, [import_debrid(i[0]) for i in debrid_list if i[0] in enabled_debrids], Thread))
	[i.join() for i in threads]
	return debrid_hosts

def manual_add_magnet_to_cloud(params):
	show_busy_dialog()
	function = import_debrid(params['provider'])
	result = function().create_transfer(params['magnet_url'])
	function().clear_cache()
	hide_busy_dialog()
	if result: notification(32576)
	else: notification(32575)

def manual_add_nzb_to_cloud(params):
	show_busy_dialog()
	function = import_debrid(params['provider'])
	result = function().create_transfer(params['url'], params['name'])
	function().clear_cache()
	hide_busy_dialog()
	text = '%s...[CR][CR]%s' % (params['name'][:40], ls(32576) if result else ls(32575))
	ok_dialog(heading=32733, text=text, top_space=True)

class DebridCheck:
	def __init__(self, hash_list, background, debrid_enabled, meta, progress_dialog):
		self.hash_list = hash_list
		self.background = background
		self.debrid_enabled = debrid_enabled
#		self.meta = meta
		self.progress_dialog = progress_dialog
		self.sleep_time = display_sleep_time()
		self.timeout = int(get_setting('scrapers.timeout.1', '10'))
		self.processing_hashes = False
		self.ad_cached_hashes, self.pm_cached_hashes, self.rd_cached_hashes = [], [], []
		self.oc_cached_hashes, self.tb_cached_hashes, self.ed_cached_hashes = [], [], []
		self.hashes_to_cache = []
		self.hashes_to_cache_append = self.hashes_to_cache.append

	def run(self):
		def _background():
			end_time = time.monotonic() + self.timeout
			while time.monotonic() < end_time:
				sleep(self.sleep_time)
				alive_threads = [x for x in threads if x.is_alive()]
				if not self.processing_hashes: continue
				if not alive_threads: break
		def _foreground():
			end_time = time.monotonic() + self.timeout
			while time.monotonic() < end_time:
				if self.progress_dialog and self.progress_dialog.iscanceled(): break
				elif monitor.abortRequested(): break
				try:
					len_threads = len(threads) if self.processing_hashes else len(self.debrid_enabled)
					processing_hashes = self.processing_hashes
					remaining_debrids = [x.name for x in threads if x.is_alive()]
					current_time = time.monotonic()
					insert_line = remaining_debrid_str % ', '.join(remaining_debrids).upper()
					line = main_line % (plswait_str, checking_debrid_str, insert_line)
					progress = int((len_threads-len(remaining_debrids))/len_threads*100)
					if self.progress_dialog: self.progress_dialog.update(line, progress)
					else: progressBG.update(progress, insert_line)
					sleep(self.sleep_time)
					if not processing_hashes: continue
					if not remaining_debrids: break
				except: pass
		debrid_cache = DebridCache()
		self.cached_hashes = debrid_cache.get_many(self.hash_list) or []
		threads = []
		threads_append = threads.append
		if not self.background:
			if not self.progress_dialog: progressBG = progressDialogBG
			dialog = Thread(target=_foreground)
		else: dialog = Thread(target=_background)
		dialog.start()
		debrid_runners = {
			'Real-Debrid': self.RD_check, 'Premiumize.me': self.PM_check,
			'AllDebrid': self.AD_check, 'EasyDebrid': self.ED_check,
			'TorBox': self.TB_check, 'Offcloud': self.OC_check
		}
		for item in self.debrid_enabled:
			thread = Thread(target=debrid_runners[item], name=item)
			threads_append(thread)
			thread.start()
		dialog.join(self.timeout)
		[debrid_cache.set_many(i[0], i[1]) for i in self.hashes_to_cache]
		return {
			'Real-Debrid': self.rd_cached_hashes, 'Premiumize.me': self.pm_cached_hashes,
			'AllDebrid': self.ad_cached_hashes, 'EasyDebrid': self.ed_cached_hashes,
			'TorBox': self.tb_cached_hashes, 'Offcloud': self.oc_cached_hashes
		}

	def cached_check(self, debrid):
		cached_list = [i[0] for i in self.cached_hashes if i[1] == debrid and i[2] == 'True']
		unchecked_list = [i for i in self.hash_list if not any([h for h in self.cached_hashes if h[0] == i and h[1] == debrid])]
		self.processing_hashes = True
		return cached_list, unchecked_list

	def RD_check(self):
		self.rd_cached_hashes, unchecked_hashes = self.cached_check('rd')
		if not unchecked_hashes: return
		# RealDebrid = import_debrid('Real-Debrid')
		rd_cache = None # RealDebrid().check_cache(unchecked_hashes)
		if not rd_cache: return
		cached_append = self.rd_cached_hashes.append
		process_list = []
		process_append = process_list.append
		try:
			for h in unchecked_hashes:
				cached = 'False'
				if h in rd_cache:
					info = rd_cache[h]
					if isinstance(info, dict) and len(info.get('rd')) > 0:
						cached_append(h)
						cached = 'True'
				process_append((h, cached))
		except:
			for i in unchecked_hashes: process_append((i, 'False'))
		self.hashes_to_cache_append((process_list, 'rd'))

	def PM_check(self):
		self.pm_cached_hashes, unchecked_hashes = self.cached_check('pm')
		if not unchecked_hashes: return
		Premiumize = import_debrid('Premiumize.me')
		pm_cache = Premiumize().check_cache(unchecked_hashes)
		if not pm_cache: return
		cached_append = self.pm_cached_hashes.append
		process_list = []
		process_append = process_list.append
		try:
			pm_cache = pm_cache['response']
			for c, h in enumerate(unchecked_hashes):
				cached = 'False'
				if pm_cache[c] is True:
					cached_append(h)
					cached = 'True'
				process_append((h, cached))
		except:
			for i in unchecked_hashes: process_append((i, 'False'))
		self.hashes_to_cache_append((process_list, 'pm'))

	def AD_check(self):
		self.ad_cached_hashes, unchecked_hashes = self.cached_check('ad')
		if not unchecked_hashes: return
		# AllDebrid = import_debrid('AllDebrid')
		ad_cache = None # AllDebrid().check_cache(unchecked_hashes)
		if not ad_cache: return
		cached_append = self.ad_cached_hashes.append
		process_list = []
		process_append = process_list.append
		try:
			ad_cache = ad_cache['magnets']
			for i in ad_cache:
				cached = 'False'
				if i['instant'] is True:
					cached_append(i['hash'])
					cached = 'True'
				process_append((i['hash'], cached))
		except:
			for i in unchecked_hashes: process_append((i, 'False'))
		self.hashes_to_cache_append((process_list, 'ad'))

	def ED_check(self):
		self.ed_cached_hashes, unchecked_hashes = self.cached_check('ed')
		if not unchecked_hashes: return
		EasyDebrid = import_debrid('EasyDebrid')
		ed_cache = EasyDebrid().check_cache(unchecked_hashes)
		if not ed_cache: return
		cached_append = self.ed_cached_hashes.append
		process_list = []
		process_append = process_list.append
		try:
			ed_cache = ed_cache['cached']
			for h, is_cached in zip(unchecked_hashes, ed_cache):
				cached = 'False'
				if is_cached:
					cached_append(h)
					cached = 'True'
				process_append((h, cached))
		except:
			for i in unchecked_hashes: process_append((i, 'False'))
		self.hashes_to_cache_append((process_list, 'ed'))

	def TB_check(self):
		self.tb_cached_hashes, unchecked_hashes = self.cached_check('tb')
		if not unchecked_hashes: return
		TorBox = import_debrid('TorBox')
		tb_cache = TorBox().check_cache(unchecked_hashes)
		if not tb_cache: return
		cached_append = self.tb_cached_hashes.append
		process_list = []
		process_append = process_list.append
		try:
			tb_cache = [i['hash'] for i in tb_cache]
			for h in unchecked_hashes:
				cached = 'False'
				if h in tb_cache:
					cached_append(h)
					cached = 'True'
				process_append((h, cached))
		except:
			for i in unchecked_hashes: process_append((i, 'False'))
		self.hashes_to_cache_append((process_list, 'tb'))

	def OC_check(self):
		self.oc_cached_hashes, unchecked_hashes = self.cached_check('oc')
		if not unchecked_hashes: return
		Offcloud = import_debrid('Offcloud')
		oc_cache = Offcloud().check_cache(unchecked_hashes)
		if not oc_cache: return
		cached_append = self.oc_cached_hashes.append
		process_list = []
		process_append = process_list.append
		try:
			oc_cache = oc_cache['cachedItems']
			for h in unchecked_hashes:
				cached = 'False'
				if h in oc_cache:
					cached_append(h)
					cached = 'True'
				process_append((h, cached))
		except:
			for i in unchecked_hashes: process_append((i, 'False'))
		self.hashes_to_cache_append((process_list, 'oc'))

