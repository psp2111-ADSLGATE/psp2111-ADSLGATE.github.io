import json, re, requests
from fenom.control import dialog, multiselectDialog, selectDialog, yesnoDialog, setSetting, setting as getSetting


timeout = 3.05


class MFDebrid:
	amble = 'Use custom manifest?[CR][CR]Select No to use Direct Torrent configuration. The cached status of direct torrents is unchecked.'
#	https://mediafusion.elfhosted.com/docs#/user_data/encrypt_user_data_encrypt_user_data_post
	base_url = 'https://mediafusion.elfhosted.com'
	encr_url = 'https://mediafusion.elfhosted.com/encrypt-user-data'
#	pattern = {"enable_catalogs":False,"max_streams_per_resolution":99,"torrent_sorting_priority":[],"certification_filter":["Disable"],"nudity_filter":["Disable"]}
	pattern = 'eJwBYACf_4hAkZJe85krAoD5hN50-2M0YuyGmgswr-cis3uap4FNnLMvSfOc4e1IcejWJmykujTnWAlQKRi9cct5k3IRqhu-wFBnDoe_QmwMjJI3FnQtFNp2u3jDo23THEEgKXHYqTMrLos='
	params = {"streaming_provider":{"token":"","service":"","only_show_cached_streams":False},"enable_catalogs":False,"max_streams_per_resolution":99,"torrent_sorting_priority":[],"certification_filter":["Disable"],"nudity_filter":["Disable"]}
	services = {
		0: ('Real Debrid', 'realdebrid', 'rd.token'),
		1: ('All Debrid', 'alldebrid', 'ad.token'),
		2: ('Direct', '', '')
	}

	def __init__(self, name=''):
		self.name = name or self.__class__.__name__

	def configure(self):
		try:
			if yesnoDialog(self.amble):
				url = dialog.input(f"Enter manifest url:", defaultt=self.base_url)
				u = requests.utils.urlparse(url)
				scheme, netloc, path = u.scheme, u.netloc, u.path
				url = '%s://%s' % (scheme, netloc) if scheme and netloc else ''
				path = path if path else ''
				provider = 'Custom' if url and path else ''
			else: url, path, provider = '', '', ''
			if url and not path:
				select = selectDialog([i[0] for i in self.services.values()])
				if select < 0: return
				provider, debrid, token = self.services[select]
				if debrid and token:
					token = getSetting(token)
					self.params['streaming_provider'] = {
						'token': token, 'service': debrid, 'only_show_cached_streams': True
					}
					path = requests.post(self.encr_url, json=self.params, timeout=timeout)
					path = path.json()['encrypted_str']
				else: path = ''
			params = path.replace(url, '').replace('manifest.json', '').strip('/')
			setSetting(f"{self.name.lower()}.token", str(params))
			setSetting(f"{self.name.lower()}.url", str(url))
			setSetting(f"{self.name.lower()}.debrid", provider)
		except:
			from fenom import log_utils
			log_utils.error()

