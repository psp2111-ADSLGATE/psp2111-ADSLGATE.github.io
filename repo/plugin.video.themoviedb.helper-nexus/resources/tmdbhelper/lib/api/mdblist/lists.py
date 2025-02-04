from tmdbhelper.lib.items.container import Container
from tmdbhelper.lib.addon.plugin import get_plugin_category, get_localized, PLUGINPATH
from tmdbhelper.lib.addon.consts import MDBLIST_LIST_OF_LISTS


class ListLocal(Container):
    def get_items(self, paths, page=None, **kwargs):
        if not paths or not isinstance(paths, list):
            return

        import json
        import xbmcvfs
        import contextlib

        response = None
        filepath = paths[0]

        if filepath.startswith('http'):
            import requests
            response = requests.get(filepath, timeout=10.000)
            response = response.json() if response else None
        else:
            with contextlib.suppress(IOError, json.JSONDecodeError):
                with xbmcvfs.File(filepath, 'r') as file:
                    response = json.load(file)

        if not response:
            return

        response = self.mdblist_api.get_paginated(response, page=page or 1)

        self.tmdb_cache_only = False
        self.set_mixed_content(response.paginated_items_dict)

        return response.items + response.next_page


class ListLists(Container):
    def get_items(self, info, page=None, **kwargs):
        from xbmcplugin import SORT_METHOD_UNSORTED

        info_model = MDBLIST_LIST_OF_LISTS.get(info)

        items = self.mdblist_api.get_list_of_lists(
            path=info_model.get('path', '').format(**kwargs),
            page=page or 1)

        self.library = 'video'
        self.plugin_category = get_plugin_category(info_model)
        self.sort_methods = [{'sortMethod': SORT_METHOD_UNSORTED, 'label2Mask': '%U'}]  # Label2 Mask by Studio (i.e. User Name)
        return items


class ListCustom(Container):
    def get_items(self, list_id, page=None, **kwargs):
        response = self.mdblist_api.get_custom_list(list_id, page=page or 1)

        self.tmdb_cache_only = False
        self.set_mixed_content(response.paginated_items_dict)

        return response.items + response.next_page


class ListCustomSearch(Container):
    def get_items(self, query=None, **kwargs):
        if not query:
            from xbmcgui import Dialog
            kwargs['query'] = query = Dialog().input(get_localized(32044))
            if not kwargs['query']:
                return
            from tmdbhelper.lib.addon.plugin import encode_url
            self.container_update = f'{encode_url(PLUGINPATH, **kwargs)},replace'
        from xbmcplugin import SORT_METHOD_UNSORTED
        items = self.mdblist_api.get_list_of_lists_search(query)
        self.library = 'video'
        self.sort_methods = [{'sortMethod': SORT_METHOD_UNSORTED, 'label2Mask': '%U'}]  # Label2 Mask by Studio (i.e. User Name)
        return items
