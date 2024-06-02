# -*- coding: utf-8 -*-
# Module: default
# Author: jurialmunkey
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import sys
import xbmcaddon
from jurialmunkey.parser import parse_paramstring
from jurialmunkey.litems import Container

ADDON = xbmcaddon.Addon('script.texturemaker')
ADDONPATH = ADDON.getAddonInfo('path')
ADDONDATA = 'special://profile/addon_data/script.texturemaker/'
COLORDEFS = '{}/resources/colors/colors.json'.format(ADDONPATH)


class ListGetColorSwatches(Container):
    def get_directory(self, **kwargs):
        import os
        import json
        import xbmcvfs
        from PIL import Image

        def load_colors(filename=None, meta=None):
            filename = 'special://skin/{}'.format(filename) if filename else COLORDEFS
            filename = xbmcvfs.translatePath(filename)
            if os.path.exists(filename):
                with open(filename, 'r') as file:
                    meta = json.load(file) or meta
            return meta if meta else load_colors(meta={"ffffffff": "ffffffff"})

        colors = load_colors(self.paramstring)
        save_dir = '{}/colors'.format(ADDONDATA)

        if not os.path.exists(xbmcvfs.translatePath(save_dir)):
            os.makedirs(xbmcvfs.translatePath(save_dir))

        items = []
        for k, v in colors.items():
            rrggbb = '#{}'.format(k[2:])
            swatch = xbmcvfs.translatePath('{}/{}.png'.format(save_dir, k))

            if not os.path.exists(swatch):
                img = Image.new('RGB', (16, 16), rrggbb)
                img.save(swatch)

            items.append(self.get_list_item(k, v, swatch, is_folder=False))

        self.add_items(items)


class ListGetPixelValue(Container):
    def get_directory(self, x, y, res_w=1920, res_h=1080, window_prop=None, window_id=None, **kwargs):
        import xbmcgui
        from jurialmunkey.window import set_to_windowprop

        try:
            x = (int(x) / int(res_w)) * xbmcgui.getScreenWidth()
            y = (int(y) / int(res_h)) * xbmcgui.getScreenHeight()
        except (TypeError, ValueError):
            return

        from PIL import ImageGrab
        rgb = ImageGrab.grab().getpixel((x, y,))

        label = f'FF{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
        items = [self.get_list_item(label)]
        set_to_windowprop(label, 0, window_prop, window_id)

        self.add_items(items)


class Plugin(object):
    def __init__(self):
        self.handle = int(sys.argv[1])
        self.paramstring = sys.argv[2][1:]
        self.params = parse_paramstring(self.paramstring)  # paramstring dictionary

    def run(self):
        routes = {
            'get_pixel_value': ListGetPixelValue
        }

        try:
            container = routes[self.params['info']]
        except KeyError:
            container = ListGetColorSwatches

        container(self.handle, self.paramstring, **self.params).get_directory(**self.params)
