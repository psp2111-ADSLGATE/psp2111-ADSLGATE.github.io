import json, re, requests
from urllib.parse import urlparse
from fenom.control import dialog, multiselectDialog, yesnoDialog, setSetting


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
	base_url = 'https://mediafusion.elfhosted.com'
	pattern = 'eJwB4AEf_lnXQtODtVEQPYTzN5RH5ekzdON8j6UfgBIzKmwW1uMrQleG82Nq_AC3GmUVA0XDSiL2WzX3HgB6X6dyaNXQNui09IcpCE6JVfVcio7wjtL6a4dB64mBGFk4NCKxpZgr6J5D2tdURTyVdv15lJV0RUXp6OT-ojBKt13ldML-KPFFRe7KuHRwUhN7LF3bY7mdunCw88dpH7Il5HTZkZqVrrb4bu7RlsvgtSFs8bW-JP3emhHG37wen3PFG2OsK0kO1BYN0INshwF8nXnHX6dLnZO-lL7Ec7NsMpvsvnTJYRka6tPEZRQx3bFyMXXA8j2RgVUYxPbC6YSoamWp1Gd9MVPdY_kO8oftLC3jh1o3PdcTmuigdAtH0O6nkmBc3q8vye5Xp72GNnBgLXfGAhBqUv1bd9PvIu61_w-PL6Ch2JWRu9WuGVoY4ctbFJmqnwGXf-4x-0m50J-CaWxVE-c1ekOW7TTRGnpb1voDYWzVzqhcQBt7H9Fx9-DtXuFAxUi8Trxef3JKcSC3AoHXBEkkNAcOWoe7zXPEERcmFhriI4QRZBGjIih_o0lNRiyuoZFO9qmU28eKVbadfcKoIuqQmiFb5oNTPDsM3QXE0g0Hr8HM43URPStEh1B2TkfnuiKQ_rO2850='
	amble = 'Use custom manifest?[CR][CR]Select No to use Direct Torrent configuration. The cached status of direct torrents is unchecked.'

	def configure(self):
		try:
			if yesnoDialog(self.amble):
				url = dialog.input(f"Enter manifest url:")
				u = urlparse(url)
				scheme, netloc, path = u.scheme, u.netloc, u.path
				url = '%s://%s' % (scheme, netloc) if scheme and netloc else ''
				path = path if path else ''
			else: url, path = self.base_url, self.pattern
			params = path.replace(self.base_url, '').replace('manifest.json', '').strip('/')
			setSetting(f"{self.name.lower()}.url", str(url))
			setSetting(f"{self.name.lower()}.token", str(params))
		except:
			from fenom import log_utils
			log_utils.error()

class MFDebrid(Mediafusion):
	base_url = ''
	pattern = ''

