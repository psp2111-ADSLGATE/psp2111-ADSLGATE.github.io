import xbmcaddon

import os

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
PATH = xbmcaddon.Addon().getAddonInfo('path')
ART = os.path.join(PATH, 'resources', 'media')
BACKUPLOCATION = 'plugin.program.709wiz'

ADDONTITLE = 'Trakt & Debrid Account Manager'
ICON709 = os.path.join(ART, '709.png')
ICONSAVE = os.path.join(ART, 'savedata.png')
ICONTRAKT = os.path.join(ART, 'keeptrakt.png')
ICONREAL = os.path.join(ART, 'keepdebrid.png')
HIDESPACERS = 'No'
SPACER = '<>'
COLOR1 = 'gray'
COLOR2 = 'white'
THEME2 = u'[COLOR {color1}]{{}}[/COLOR]'.format(color1=COLOR1)
THEME3 = u'[COLOR {color1}]{{}}[/COLOR]'.format(color1=COLOR2)






