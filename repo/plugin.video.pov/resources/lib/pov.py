import sys
from urllib.parse import parse_qsl
#from xbmc import getInfoLabel
from modules.router import routing

if __name__ == '__main__':
	params = dict(parse_qsl(sys.argv[2][1:]))
	routing(params)
#	if 'pov' not in getInfoLabel('Container.PluginName'): sys.exit(1)

