import json, re, requests
from fenom.control import dialog, multiselectDialog, selectDialog, yesnoDialog, setSetting, setting as getSetting


timeout = 3.05


class Hosted:
	base_url: str = ''
	pattern: str = r''
	indexers: list = []
	languages: list = []

	def __init__(self, name=''):
		self.name = name or self.__class__.__name__

	def parse_html(self, html):
		return {}

	def configure(self):
		try:
			url = dialog.input(f"{self.name} base url:", defaultt=self.base_url)
			if not url: return
			response = requests.get(url + '/configure', timeout=timeout)
			config_dict = self.parse_html(response.text)
			indexers = config_dict['indexers'] if 'indexers' in config_dict else self.indexers
			if indexers:
				preselect = []
				ret = multiselectDialog(indexers, preselect=preselect, heading='Select indexers:')
				if ret is None: return
				user_indexers = [indexers[i] for i in ret]
			else: user_indexers = []
			languages = config_dict['languages'] if 'languages' in config_dict else []
			languages = sorted(i for i in languages if i not in ['All', 'Multi', 'English'])
			languages = ['All', 'Multi', 'English'] + languages
			ret = multiselectDialog(languages, preselect=[0], heading='Select languages:')
			if ret is None: return
			if 0 in ret: user_langs = ['All']
			else: user_langs = [languages[i] for i in ret]
			setSetting(f"{self.name.lower()}.url", url)
			setSetting(f"{self.name.lower()}.indexers", ','.join(user_indexers))
			setSetting(f"{self.name.lower()}.langs", ','.join(user_langs))
		except:
			from fenom import log_utils
			log_utils.error()


class Comet(Hosted):
	base_url = 'https://comet.elfhosted.com'
	pattern = r'const webConfig = \s*(.*?);'
	indexers = ['bitsearch', 'eztv', 'thepiratebay', 'therarbg', 'yts']
	languages = ['All']

	def parse_html(self, html):
		values = re.findall(self.pattern, html, re.DOTALL | re.MULTILINE)
		values = iter(values)
		config_dict = json.loads(next(values, []))
		return config_dict


class Mediafusion(Hosted):
	amble = 'Use custom manifest?[CR][CR]Select No to use Direct Torrent configuration. The cached status of direct torrents is unchecked.'
#	https://mediafusion.elfhosted.com/docs#/user_data/encrypt_user_data_encrypt_user_data_post
	base_url = 'https://mediafusion.elfhosted.com'
	encr_url = 'https://mediafusion.elfhosted.com/encrypt-user-data'
#	pattern = {"enable_catalogs":False,"max_streams_per_resolution":99,"torrent_sorting_priority":[],"certification_filter":["Disable"],"nudity_filter":["Disable"]}
	pattern = 'eJwBYACf_4hAkZJe85krAoD5hN50-2M0YuyGmgswr-cis3uap4FNnLMvSfOc4e1IcejWJmykujTnWAlQKRi9cct5k3IRqhu-wFBnDoe_QmwMjJI3FnQtFNp2u3jDo23THEEgKXHYqTMrLos='
	params = {"streaming_provider":{"token":"","service":"","only_show_cached_streams":True},"enable_catalogs":False,"max_streams_per_resolution":99,"torrent_sorting_priority":[],"certification_filter":["Disable"],"nudity_filter":["Disable"]}
	services_list = ['Real Debrid', 'Premiumize', 'All Debrid', 'TorBox', 'Direct']
	services_dict = {
		0: ('realdebrid', 'rd.token'),
		1: ('premiumize', 'pm.token'),
		2: ('alldebrid', 'ad.token'),
		3: ('torbox', 'tb.token'),
		4: ('', '')
	}

	def configure(self):
		try:
			if yesnoDialog(self.amble):
				url = dialog.input(f"Enter manifest url:", defaultt=self.base_url)
				u = requests.utils.urlparse(url)
				scheme, netloc, path = u.scheme, u.netloc, u.path
				url = '%s://%s' % (scheme, netloc) if scheme and netloc else ''
				path = path if path else ''
			else: url, path = '', ''
			if url and not path:
				debrid = selectDialog(self.services_list)
				if debrid < 0: return
				debrid, token = self.services_dict[debrid]
				if not (debrid and token): return
				token = getSetting(token)
				self.params['streaming_provider'] = {
					'token': token, 'service': debrid, 'only_show_cached_streams': True
				}
				path = requests.post(self.encr_url, json=self.params, timeout=timeout)
				path = path.json()['encrypted_str']
			params = path.replace(url, '').replace('manifest.json', '').strip('/')
			setSetting(f"{self.name.lower()}.url", str(url))
			setSetting(f"{self.name.lower()}.token", str(params))
		except:
			from fenom import log_utils
			log_utils.error()


class MFDebrid(Mediafusion):
	services_list = ['Real Debrid', 'All Debrid', 'Direct']
	services_dict = {
		0: ('realdebrid', 'rd.token'),
		1: ('alldebrid', 'ad.token'),
		2: ('', '')
	}

