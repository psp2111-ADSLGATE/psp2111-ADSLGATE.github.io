from apis.easydebrid_api import EasyDebridAPI
from modules import kodi_utils
# from modules.kodi_utils import logger

ls = kodi_utils.local_string
EasyDebrid = EasyDebridAPI()

def ed_account_info():
	from datetime import datetime
	try:
		kodi_utils.show_busy_dialog()
		account_info = EasyDebrid.account_info()
		expires = datetime.fromtimestamp(account_info['paid_until'])
		days_remaining = (expires - datetime.today()).days
		body = []
		append = body.append
		append(ls(32755) % account_info['id'])
		append(ls(32750) % expires.strftime('%Y-%m-%d'))
		append(ls(32751) % days_remaining)
		kodi_utils.hide_busy_dialog()
		return kodi_utils.show_text('EasyDebrid'.upper(), '\n\n'.join(body), font_size='large')
	except: kodi_utils.hide_busy_dialog()

