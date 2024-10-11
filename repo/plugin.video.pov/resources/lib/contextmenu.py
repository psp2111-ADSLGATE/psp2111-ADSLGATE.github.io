import sys
from xbmc import executebuiltin, sleep

mode = sys.argv[1]
if   mode == 'refresh_widgets':
	executebuiltin('UpdateLibrary(video,special://skin/foo)')
elif mode == 'pov_watched_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_watched_params'))
	sleep(1000)
	executebuiltin('UpdateLibrary(video,special://skin/foo)')
elif mode == 'pov_unwatched_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_unwatched_params'))
	sleep(1000)
	executebuiltin('UpdateLibrary(video,special://skin/foo)')
elif mode == 'pov_clearprog_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_clearprog_params'))
	sleep(1000)
	executebuiltin('UpdateLibrary(video,special://skin/foo)')
elif mode == 'pov_browse_params':
	executebuiltin('ActivateWindow(Videos,%s)' % sys.listitem.getProperty('pov_browse_params'))
elif mode == 'pov_browse_seas_params':
	executebuiltin('ActivateWindow(Videos,%s)' % sys.listitem.getProperty('pov_browse_seas_params'))
elif mode == 'pov_trakt_manager_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_trakt_manager_params'))
elif mode == 'pov_fav_manager_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_fav_manager_params'))
elif mode == 'pov_random_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_random_params'))
elif mode == 'pov_options_menu_params':
	executebuiltin('RunPlugin(%s)' % sys.listitem.getProperty('pov_options_menu_params'))
elif mode == 'pov_extras_menu_params':
	params = sys.listitem.getProperty('pov_extras_menu_params')
	params += '&is_widget=false&is_home=true'
	executebuiltin('RunPlugin(%s)' % params)

