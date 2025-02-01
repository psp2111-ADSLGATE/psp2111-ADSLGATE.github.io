from tmdbhelper.lib.monitor.images import ImageManipulations
from tmdbhelper.lib.monitor.poller import Poller, POLL_MIN_INCREMENT
from tmdbhelper.lib.monitor.listitemtools import ListItemInfoGetter
from tmdbhelper.lib.addon.logger import kodi_try_except
from threading import Thread


class ImagesMonitor(Thread, ListItemInfoGetter, ImageManipulations, Poller):
    _cond_on_disabled = (
        "!Skin.HasSetting(TMDbHelper.EnableCrop) + "
        "!Skin.HasSetting(TMDbHelper.EnableBlur) + "
        "!Skin.HasSetting(TMDbHelper.EnableDesaturate) + "
        "!Skin.HasSetting(TMDbHelper.EnableColors)")

    _allow_list = ('crop', 'blur', 'desaturate', 'colors', )
    idle_cycles = 10 / POLL_MIN_INCREMENT  # Reupdate idle item every ten seconds for extrafanart TODO: Allow skin to set value?

    def __init__(self, parent):
        Thread.__init__(self)
        self._cur_item = 0
        self._pre_item = 1
        self._cur_window = 0
        self._pre_window = 1
        self._idle_cycle = 0
        self.exit = False
        self.update_monitor = parent.update_monitor
        self.crop_image_cur = None
        self.blur_image_cur = None
        self.remote_artwork = {}
        self.added_artworks = {}
        self._allow_on_scroll = True  # Allow updating while scrolling
        self._parent = parent

    @kodi_try_except('lib.monitor.imgmon.on_listitem')
    def on_listitem(self):
        with self._parent.mutex_lock:
            self.setup_current_container()
            if self.is_same_window(update=True) and self.is_same_item(update=True) and self._idle_cycle < self.idle_cycles:
                self._idle_cycle += 1
                return
            self._idle_cycle = 0
            self.update_artwork()

    def get_allow_list(self, check_set=False):
        if not check_set:
            return self._allow_list
        return [k for k in self._allow_list if not self.get_property(f'ListItem.{k}Image')]

    def update_artwork(self, check_set=False):
        self.added_artworks[self._pre_item] = self.get_image_manipulations(
            use_winprops=True,
            built_artwork=self.remote_artwork.get(self._pre_item),
            allow_list=self.get_allow_list(check_set=check_set))

    def _on_listitem(self):
        self.on_listitem()
        self._on_idle(POLL_MIN_INCREMENT)

    def _on_scroll(self):
        if self._allow_on_scroll:
            return self._on_listitem()
        self._on_idle(POLL_MIN_INCREMENT)

    def run(self):
        self.poller()
