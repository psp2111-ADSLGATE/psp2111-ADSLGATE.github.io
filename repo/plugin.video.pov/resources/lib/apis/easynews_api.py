import re
import json
import base64
import requests
from urllib.parse import urlencode, quote
from caches.main_cache import cache_object
from modules.kodi_utils import get_setting
# from modules.kodi_utils import logger

video_extensions = (
	'm4v,3g2,3gp,nsv,tp,ts,ty,pls,rm,rmvb,mpd,ifo,mov,qt,divx,xvid,bivx,vob,nrg,img,iso,udf,pva,wmv,asf,asx,ogm,m2v,avi,bin,dat,mpg,mpeg,mp4,mkv,'
	'mk3d,avc,vp3,svq3,nuv,viv,dv,fli,flv,wpl,xspf,vdr,dvr-ms,xsp,mts,m2t,m2ts,evo,ogv,sdp,avs,rec,url,pxml,vc1,h264,rcv,rss,mpls,mpl,webm,bdmv,bdm,wtv,trp,f4v,pvr,disc'
)
SEARCH_PARAMS = {'st': 'adv', 'sb': 1, 'fex': video_extensions, 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3,
				's1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-', 'pby': 350}
timeout = 10.0
session = requests.Session()
session.mount('https://', requests.adapters.HTTPAdapter(max_retries=1))

def import_easynews():
	''' API version setting currently disabled '''
	# if get_setting('easynews.api_version') == '0': return EasyNewsAPI()
	# else: return EasyNewsAPIv3()
	return EasyNewsAPI()

class EasyNewsAPI:
	def __init__(self):
		self.base_url = 'https://members.easynews.com'
		self.search_link = '/2.0/search/solr-search/advanced'
		self.account_link = 'https://account.easynews.com/editinfo.php'
		self.usage_link = 'https://account.easynews.com/usageview.php'
		self.username = get_setting('easynews_user')
		self.password = get_setting('easynews_password')
		self.moderation = 1 if get_setting('easynews_moderation') == 'true' else 0
		self.auth = self._get_auth()
		self.base_get = self._get
		self.base_process = self._process_files
		self.base_resolver = self.resolver

	def _get_auth(self):
		user_info = '%s:%s' % (self.username, self.password)
		user_info = user_info.encode('utf-8')
		auth = 'Basic ' + base64.b64encode(user_info).decode('utf-8')
		return auth

	def search(self, query, expiration=48):
		url, self.params = self._translate_search(query)
		string = 'pov_EASYNEWS_SEARCH_' + urlencode(self.params)
		return cache_object(self._process_search, string, url, json=False, expiration=expiration)

	def account(self):
		from modules.dom_parser import parseDOM
		account_info, usage_info = None, None
		try:
			account_html = self._get(self.account_link)
			account_info = parseDOM(account_html, 'form', attrs={'id': 'accountForm'})
			account_info = parseDOM(account_info, 'td')[0:11][1::3]
		except: pass
		try:
			usage_html = self._get(self.usage_link)
			usage_info = parseDOM(usage_html, 'div', attrs={'class': 'table-responsive'})
			usage_info = parseDOM(usage_info, 'td')[0:11][1::3]
			usage_info[1] = re.sub(r'[</].+?>', '', usage_info[1])
		except: pass
		return account_info, usage_info

	def _process_files(self, files):
		def _process():
			for item in files:
				try:
					post_hash, size, post_title, ext, duration = item['0'], item['4'], item['10'], item['11'], item['14']
					if 'alangs' in item and item['alangs']: language = item['alangs']
					else: language = ''
					if 'type' in item and item['type'].upper() != 'VIDEO': continue
					elif 'virus' in item and item['virus']: continue
					elif re.match(r'^\d+s', duration) or re.match(r'^[0-5]m', duration): continue
					stream_url = down_url + quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
					file_dl = stream_url + '|Authorization=%s' % (quote(self.auth))
					thumbnail = 'https://th.easynews.com/thumbnails-%s/pr-%s.jpg' % (post_hash[0:3], post_hash)
					result = {'name': post_title,
							  'size': size,
							  'rawSize': item['rawSize'],
							  'url_dl': file_dl,
							  'version': 'version2',
							  'full_item': item,
							  'language': language,
							  'thumbnail': thumbnail}
					yield result
				except Exception as e:
					from modules.kodi_utils import logger
					logger('POV easynews API Exception', str(e))
		down_url = files.get('downURL')
		dl_farm = files.get('dlFarm')
		dl_port = files.get('dlPort')
		files = files.get('data', [])
		results = list(_process())
		return results

	def _process_files_v3(self, results):
		def _process():
			for item in files:
				try:
					post_hash, size, post_title, ext, duration, sig = item['hash'], item['bytes'], item['filename'], item['extension'], item['runtime'], item['sig']
					if 'alangs' in item and item['alangs']: language = item['alangs']
					else: language = ''
					if 'type' in item and item['type'].upper() != 'VIDEO': continue
					elif 'virus' in item and item['virus']: continue
					elif re.match(r'^\d+s', duration) or re.match(r'^[0-5]m', duration): continue
					url_dl = self.stream_url % (post_hash, ext, post_title, sid, sig)
					thumbnail = 'https://th.easynews.com/thumbnails-%s/pr-%s.jpg' % (post_hash[0:3], post_hash)
					result = {'name': post_title,
							  'size': size,
							  'rawSize': size,
							  'url_dl': url_dl,
							  'version': 'version3',
							  'full_item': item,
							  'language': language,
							  'thumbnail': thumbnail}
					yield result
				except Exception as e:
					from modules.kodi_utils import logger
					logger('POV easynews API Exception', str(e))
		files = results.get('data', [])
		sid = results.get('sid')
		results = list(_process())
		return results

	def _translate_search(self, query):
		params = SEARCH_PARAMS
		params['safeO'] = self.moderation
		params['gps'] = query
		url = self.base_url + self.search_link
		return url, params

	def _process_search(self, url):
		results = self.base_get(url, self.params)
		files = self.base_process(results)
		return files

	def _get(self, url, params={}):
		headers = {'Authorization': self.auth}
		response = session.get(url, params=params, headers=headers, timeout=timeout).text
		try: return json.loads(response)
		except: return response

	def _get_v3(self, url, params={}):
		headers = {'Authorization': self.auth}
		response = session.get(url, params=params, headers=headers, timeout=timeout).content
		response = re.compile(self.regex,re.DOTALL).findall(response)[0]
		response = response + '}'
		try: return json.loads(response)
		except: return response

	def resolve_easynews(self, url_dl):
		return self.base_resolver(url_dl)

	def resolver(self, url_dl):
		return url_dl

	def resolver_v3(self, url_dl):
		headers = {'Authorization': self.auth}
		response = session.get(url_dl, headers=headers, stream=True, timeout=timeout)
		stream_url = response.url
		resolved_link = stream_url + '|Authorization=%s' % (quote(self.auth))
		return resolved_link

class EasyNewsAPIv3(EasyNewsAPI):
	def __init__(self):
		EasyNewsAPI.__init__(self)
		self.base_url = 'https://members-beta.easynews.com/3.0/index/basic'
		self.stream_url = 'https://members-beta.easynews.com/os/3.0/auto/443/%s%s/%s?sid=%s&sig=%s'
		self.search_link = ''
		self.regex = 'var INIT_RES = (.+?)};'
		self.base_get = self._get_v3
		self.base_process = self._process_files_v3
		self.base_resolver = self.resolver_v3

def clear_media_results_database():
	from modules.kodi_utils import clear_property, database, maincache_db
	dbcon = database.connect(maincache_db, timeout=40.0, isolation_level=None)
	dbcur = dbcon.cursor()
	dbcur.execute("""PRAGMA synchronous = OFF""")
	dbcur.execute("""PRAGMA journal_mode = OFF""")
	dbcur.execute("""SELECT id FROM maincache WHERE id LIKE 'pov_EASYNEWS_SEARCH_%'""")
	easynews_results = [str(i[0]) for i in dbcur.fetchall()]
	if not easynews_results: return 'success'
	try:
		dbcur.execute("""DELETE FROM maincache WHERE id LIKE 'pov_EASYNEWS_SEARCH_%'""")
		for i in easynews_results: clear_property(i)
		return 'success'
	except: return 'failed'

