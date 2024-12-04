import json, re, requests
from fenom.control import dialog, multiselectDialog, setSetting


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

class MFDebrid(Hosted):
	base_url = 'https://mediafusion.elfhosted.com'

	def configure(self):
		try:
			url = dialog.input(f"{self.base_url} manifest url")
			params = url.replace(self.base_url, '').replace('manifest.json', '').strip('/')
			if not params: return
			setSetting(f"{self.name.lower()}.token", str(params))
		except:
			from fenom import log_utils
			log_utils.error()
