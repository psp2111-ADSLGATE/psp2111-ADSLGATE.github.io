# -*- coding: utf-8 -*-
"""
	My Accounts
"""

import requests
from accountmgr.modules import control
from accountmgr.modules import log_utils

API_key = control.setting('tmdb.api.key')
if API_key == '' or API_key is None:
	API_key = '05a454b451f2f9003fbca293744e4a85'

tmdb_icon = control.joinPath(control.artPath(), 'tmdb.png')

class Auth:
	def __init__(self):
		self.auth_base_link = 'https://api.themoviedb.org/3/authentication'

	def create_session_id(self):
		try:
			if control.setting('tmdb.username') == '' or control.setting('tmdb.password') == '':
				return control.notification(title='default', message=32683, icon=tmdb_icon)
			url = self.auth_base_link + '/token/new?api_key=%s' % API_key
			result = requests.get(url).json()
			token = result.get('request_token')
			url2 = self.auth_base_link + '/token/validate_with_login?api_key=%s' % API_key
			username = control.setting('tmdb.username')
			password = control.setting('tmdb.password')
			post2 = {"username": "%s" % username,
							"password": "%s" % password,
							"request_token": "%s" % token}
			result2 = requests.post(url2, data=post2).json()
			url3 = self.auth_base_link + '/session/new?api_key=%s' % API_key
			post3 = {"request_token": "%s" % token}
			result3 = requests.post(url3, data=post3).json()
			if result3.get('success') is True:
				session_id = result3.get('session_id')
				msg = '%s' % ('username =' + username + '[CR]password =' + password + '[CR]token = ' + token + '[CR]confirm?')
				if control.yesnoDialog(msg):
					control.setSetting('tmdb.session_id', session_id)
					control.notification_tmdb(title='default', message=32679, icon=tmdb_icon)
				else: control.notification(title='default', message=32680, icon=tmdb_icon)
		except:
			log_utils.error()

	def revoke_session_id(self):
		try:
			if control.setting('tmdb.session_id') == '': return
			url = self.auth_base_link + '/session?api_key=%s' % API_key
			post = {"session_id": "%s" % control.setting('tmdb.session_id')}
			result = requests.delete(url, data=post).json()
			if result.get('success') is True:
				control.setSetting('tmdb.session_id', '')
				control.notification(title='default', message=32681, icon=tmdb_icon)
			else: control.notification(title='default', message=32682, icon=tmdb_icon)
		except:
			log_utils.error()
