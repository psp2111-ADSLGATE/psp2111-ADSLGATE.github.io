import requests
# from modules.kodi_utils import logger

# Code snippets from nixgates. Thankyou.
API_KEY = 'a7ad21743fd710fccb738232f2fbdcfc'
base_url = 'https://webservice.fanart.tv/v3/%s/%s'
default_fanart_meta = {'poster2': '', 'fanart2': '', 'banner': '', 'clearart': '', 'clearlogo': '', 'landscape': '', 'discart': '', 'fanart_added': True}
default_fanart_nometa = {'poster2': '', 'fanart2': '', 'banner': '', 'clearart': '', 'clearlogo': '', 'landscape': '', 'discart': '', 'fanart_added': False}
timeout = 3.05
session = requests.Session()
session.mount('https://webservice.fanart.tv', requests.adapters.HTTPAdapter(pool_maxsize=100))

def get(media_type, language, media_id, client_key):
	if not media_id: return default_fanart_meta
	query = base_url % (media_type, media_id)
	headers = {'client-key': client_key, 'api-key': API_KEY}
	try: art = session.get(query, headers=headers, timeout=timeout).json()
	except: art = None
	if art is None or 'error_message' in art: return default_fanart_meta
	art_get = art.get
	if media_type == 'movies':
		fanart_data = {'poster2': parse_art(art_get('movieposter'), language),
						'fanart2': parse_art(art_get('moviebackground'), language),
						'banner': parse_art(art_get('moviebanner'), language),
						'clearart': parse_art(art_get('movieart', []) + art_get('hdmovieclearart', []), language),
						'clearlogo': parse_art(art_get('movielogo', []) + art_get('hdmovielogo', []), language),
						'landscape': parse_art(art_get('moviethumb'), language),
						'discart': parse_art(art_get('moviedisc'), language),
						'fanart_added': True}
	else:
		fanart_data = {'poster2': parse_art(art_get('tvposter'), language),
						'fanart2': parse_art(art_get('showbackground'), language),
						'banner': parse_art(art_get('tvbanner'), language),
						'clearart': parse_art(art_get('clearart', []) + art_get('hdclearart', []), language),
						'clearlogo': parse_art(art_get('hdtvlogo', []) + art_get('clearlogo', []), language),
						'landscape': parse_art(art_get('tvthumb'), language),
						'discart': '',
						'fanart_added': True}
	return fanart_data

def parse_art(art, language):
	if art is None: return ''
	try:
		result = [(x['url'], x['likes']) for x in art if x.get('lang') == language]
		if not result and language != 'en': result = [(x['url'], x['likes']) for x in art if x.get('lang') == 'en']
		if not result: result = [(x['url'], x['likes']) for x in art if any(value == x.get('lang') for value in ('00', ''))]
		if result:
			result.sort(key=lambda x: int(x[1]), reverse=True)
			result = [x[0] for x in result][0]
	except: result = ''
	if not 'http' in result: result = ''
	return result

def add(media_type, language, media_id, client_key, meta):
	if not media_id: meta.update(default_fanart_meta)
	else:
		try: meta.update(get(media_type, language, media_id, client_key))
		except: meta.update(default_fanart_meta)
	return meta

