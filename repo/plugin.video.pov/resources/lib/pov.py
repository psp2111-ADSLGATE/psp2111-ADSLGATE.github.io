import sys
from modules.router import Router

if __name__ == '__main__':
	with Router() as r: r.routing(sys)

