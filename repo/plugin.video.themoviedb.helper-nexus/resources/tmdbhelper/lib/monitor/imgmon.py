from tmdbhelper.lib.monitor.images import ImageManipulations
from tmdbhelper.lib.monitor.poller import Poller, POLL_MIN_INCREMENT
from tmdbhelper.lib.monitor.listitemtools import ListItemInfoGetter
from tmdbhelper.lib.addon.logger import kodi_try_except
from threading import Thread


class ImagesMonitor(Thread, ListItemInfoGetter, ImageManipulations, Poller):
    def __init__(self, parent):
        Thread.__init__(self)
        self.exit = False
        self.update_monitor = parent.update_monitor
        self.crop_image_cur = None
        self.blur_image_cur = None
        self.pre_item = None
        self._readahead_li = True  # get_setting('service_listitem_readahead')  # Allows readahead queue of next ListItems when idle
        self._parent = parent

    def setup_current_container(self):
        self._container_item = self.container_item

    @kodi_try_except('lib.monitor.imgmon.on_listitem')
    def on_listitem(self):
        with self._parent.mutex_lock:
            self.setup_current_container()
            if self.pre_item != self.cur_item:
                self.get_image_manipulations(use_winprops=True)
                self.pre_item = self.cur_item

    def _on_listitem(self):
        self.on_listitem()
        self._on_idle(POLL_MIN_INCREMENT)

    def _on_scroll(self):
        if self._readahead_li:
            return self._on_listitem()
        self._on_idle(POLL_MIN_INCREMENT)

    def run(self):
        self.poller()
